from Model.Camera import Basler
from Model.HSI import HSImage
from Model.Servomotor import Servomotor
from tqdm import trange
import configparser

def do_step(camera: Basler,
            hsi: HSImage,
            servomotor: Servomotor,
            **kwargs):
    """
    Does one step of system concluded shot, adding to hypercube this shot and step of servomotor

    Parameters
    ----------
    camera: Basler
        instance of Basler camera
    hsi: HSImage
        hyperspectral image
    servomotor : Servomotor
        instance of servomotor
    **kwargs concludes
        ind: int
            number of channel of HSI
        num: int
            count of layers (in X-coordinate) in HSI
    """
    ind = kwargs['ind']
    num = kwargs['num']
    layer = camera.make_shot()
    hsi.add_layer_yz_fast(layer.astype('uint16'), ind, num)
    servomotor.next_step()

def save_hsi(hsi: HSImage,
             path_to_save: str):
    """
    Saves hypespectral image in different formats

    Parameters
    ----------
    hsi: HSImage
        hyperspectral image
    path_to_save: str
        path to saving HSI in format ends with .tiff, .mat, .npy
    """

    if path_to_save.endswith('.mat'):
        hsi.save_to_mat(path_to_file=path_to_save, key='image')
    elif path_to_save.endswith('.tiff'):
        hsi.save_to_tiff(path_to_file=path_to_save)
    elif path_to_save.endswith('.npy'):
        hsi.save_to_npy(path_to_file=path_to_save)
    else:
        print("Saving error: please check file format.\nHSI was not saved")

def start_record(conf: dict):
    """
    Starts recording of hyperspectral image

    Parameters
    ----------
    number_of_steps: int
        count of layers (images) of hyperspectral image which will shouted
    exposure: int
        time of exposure in milliseconds
    mode: int
        mode for servomotor
    velocity: int
        velocity of servomotor
    direction: int
        get 1 or 0 values
    path_to_save: str
        path to mat file in which hyperspepctral image will be saved
    path_to_coef: str
        path to file with raw spectrum obtained from slit
    key_coef: str
        key for mat file of matrix of normalized coefficients
    """

    print('Start recording...')

    number_of_steps = int(conf['Basler']['NUMBER_OF_STEPS'])
    exposure = int(conf['Basler']['EXPOSURE'])
    gain_value = int(conf['Basler']['GAIN'])
    mode = int(conf['Servomotor']['MODE'])
    direction = int(conf['Basler']['DIRECTION'])
    path_to_save = conf['Paths']['PATH_TO_SAVE']
    path_to_coef = conf['Paths']['PATH_TO_COEF']
    key_coef = conf['HSI']['KEY_NORM']

    try:
        camera = Basler()
        camera.set_camera_configures(exposure=exposure, gain_value=gain_value)
        print('Camera initializing successfully')
    except Exception:
        raise "Error camera initializing"

    hsi = HSImage(conf=conf)
    if path_to_coef:
        hsi.set_coef(path_to_norm=path_to_coef, key=key_coef)
        print('Normalize HSI enabled')
    else:
        print('Normalize HSI disabled')

    try:
        servomotor = Servomotor(direction, mode=mode)
        servomotor.initialize_pins()
        print('Servomotor connects successfully')
    except Exception:
        raise "Error with servomotor connections"

    for i in trange(number_of_steps):
        do_step(camera, hsi, servomotor, ind=i, num=number_of_steps)

    try:
        save_hsi(hsi, path_to_save=path_to_save)
        print(f'Hyperspectral image was saved in {path_to_save}')
    except Exception:
        raise "Error with  saving HSI"

    path_to_log = path_to_save.split('.')[0] + '_log.txt'
    log = f'{number_of_steps}\n' \
          f'{exposure}\n' \
          f'{gain_value}\n' \
          f'{mode}\n' \
          f'{direction}\n' \
          f'{path_to_save}\n' \
          f'{path_to_coef}\n' \
          f'{key_coef}\n'
    try:
        with open(path_to_log) as f:
            f.write(log)
    except Exception:
        raise "Error with creating log-file"


if __name__ == '__main__':

    conf = configparser.ConfigParser()
    conf.read("configuration.ini")
    start_record(conf)



