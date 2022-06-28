from Model.Camera import Basler
from Model.HSI import HSImage
from Model.Servomotor import Servomotor
from tqdm import tqdm
import configparser

def do_step(camera: Basler,
            hsi: HSImage,
            servomotor: Servomotor,
            **kwargs):
    """
    Does one step of system concluded shot, adding to hypercube this shot and step of servomotor

    Parameters
    ----------
    camera : Basler
        instance of Basler camera
    hsi : HSImage
        hyperspectral image
    servomotor : Servomotor
        instance of servomotor
    **kwargs concludes
        ind : int
            number of channel of HSI
        num : int
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
        raise "Saving error: please check file format"

def start_record(number_of_steps: int,
                 exposure: int,
                 mode: int,
                 direction: int,
                 path_to_save: str,
                 path_to_coef=None,
                 key_coef=None):
    """
    Starts recording of hyperspectral image

    Parameters
    ----------
    number_of_steps : int
        count of layers (images) of hyperspectral image which will shouted
    exposure : int
        time of exposure in milliseconds
    mode: int
        mode for servomotor
    velocity: int
        velocity of servomotor
    direction : int
        get 1 or 0 values
    path_to_save : str
        path to mat file in which hyperspepctral image will be saved
    path_to_coef : str
        path to file with matrix of normalized coefficients
    key_coef : str
        key for mat file of matrix of normalized coefficients
    """
    print('Start recording...')

    try:
        camera = Basler()
        camera.set_camera_configures(exposure=exposure)
        print('Camera initializing successfully')
    except:
        raise "Error camera initializing"

    hsi = HSImage()
    if path_to_coef:
        hsi.set_coef(path_to_coef, key_coef)
        print('Normalize HSI enabled')
    else:
        print('Normalize HSI disabled')

    try:
        servomotor = Servomotor(direction, mode=mode)
        servomotor.initialize_pins()
        print('Servomotor connects successfully')
    except:
        raise "Error with servomotor connections"

    for i in tqdm(range(number_of_steps)):
       do_step(camera, hsi, servomotor, ind=i, num=number_of_steps)

    try:
        save_hsi(hsi, path_to_save=path_to_save)
        print(f'Hyperspectral image was saved in {path_to_save}')
    except:
        raise "Error with  saving HSI"

if __name__ == '__main__':

    conf = configparser.ConfigParser()
    conf.read("configuration.ini")
    start_record(number_of_steps=int(conf['Basler']['NUMBER_OF_STEPS']),
                 exposure=int(conf['Basler']['EXPOSURE']),
                 mode=int(conf['Servomotor']['MODE']),
                 direction=int(conf['Basler']['DIRECTION']),
                 path_to_save=conf['Paths']['PATH_TO_SAVE'],
                 path_to_coef=conf['Paths']['PATH_TO_COEF'])



