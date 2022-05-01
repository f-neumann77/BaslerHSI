from Model.Camera import Basler
from Model.HSI import HSImage
from Model.Servomotor import Servomotor


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

def start_record(count_of_steps: int, exposure: int, direction: int, path_to_mat: str, path_coef=None, key=None):
    """
    Starts recording of hyperspectral image

    Parameters
    ----------
    count_of_steps : int
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
    hsi.set_coef(path_coef, key)
    servomotor = Servomotor(direction, mode=mode, velocity=velocity)
    servomotor.initialize_pins()

    for i in range(count_of_steps):
       do_step(camera, hsi, servomotor, ind=i, num=count_of_steps)

    hsi.save_to_mat(path_to_file=path_to_mat, key='image')

if __name__ == '__main__':

    NUMBER_OF_STEPS: int = 100
    EXPOSURE: int = 1_000_000
    DIRECTION: int = 0
    PATH_TO_MAT: str = './cube.mat'
    PATH_TO_COEF: str = './lampa.tiff'

    start_record(number_of_steps=NUMBER_OF_STEPS,
                 exposure=EXPOSURE,
                 direction=DIRECTION,
                 path_to_mat=PATH_TO_MAT)

