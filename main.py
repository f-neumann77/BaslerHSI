from Model.Camera import Basler
from Model.HSI import HSImage
from Model.Servomotor import Servomotor
from tqdm import tqdm
import configparser

def do_step(camera: Basler, hsi: HSImage, servomotor: Servomotor, **kwargs):
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

def start_record(number_of_steps: int, exposure: int, direction: int, path_to_mat: str, path_to_coef=None, key_coef=None):
    """
    Starts recording of hyperspectral image

    Parameters
    ----------
    number_of_steps : int
        count of layers (images) of hyperspectral image which will shouted
    exposure : int
        time of exposure in milliseconds
    direction : int
        get 1 or 0 values
    path_to_mat : str
        path to mat file in which hyperspepctral image will be saved
    path_coef : str
        path to file with matrix of normalized coefficients
    key : str
        key for mat file of matrix of normalized coefficients
    """
    mode = 0
    velocity = 100

    camera = Basler()
    camera.set_camera_configures(exposure=exposure)
    hsi = HSImage()
    hsi.set_coef(path_to_coef, key_coef)
    servomotor = Servomotor(direction, mode=mode, velocity=velocity)
    servomotor.initialize_pins()

    for i in tqdm(range(number_of_steps)):
       do_step(camera, hsi, servomotor, ind=i, num=number_of_steps)

    hsi.save_to_mat(path_to_file=path_to_mat, key='image')

if __name__ == '__main__':

    conf = configparser.ConfigParser()
    conf.read("configuration.ini")
    start_record(number_of_steps=int(conf['Basler']['NUMBER_OF_STEPS']),
                 exposure=int(conf['Basler']['EXPOSURE']),
                 direction=int(conf['Basler']['DIRECTION']),
                 path_to_mat=conf['Paths']['PATH_TO_MAT'],
                 path_to_coef=conf['Paths']['PATH_TO_COEF'])

