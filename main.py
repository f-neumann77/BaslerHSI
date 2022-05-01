from Model.Camera import Basler
from Model.HSI import HSImage
from Model.Servomotor import Servomotor


def do_step(camera: Basler, hsi: HSImage, servomotor: Servomotor, **kwargs):
    ind = kwargs['ind']
    num = kwargs['num']
    layer = camera.make_shot()
    hsi.add_layer_yz_fast(layer.astype('uint16'), ind, num)
    servomotor.next_step()

def start_record(number_of_steps: int, exposure: int, direction: str, path_to_mat: str, path_coef=None, key=None):

    camera = Basler()
    camera.set_camera_configures(exposure=exposure)
    hsi = HSImage()
    hsi.set_coef(path_coef, key)
    servomotor = Servomotor(direction)

    for i in range(number_of_steps):
       do_step(camera, hsi, servomotor, ind=i, num=number_of_steps)

    hsi.save_to_mat(path_to_file=path_to_mat, key='image')

if __name__ == '__main__':

    NUMBER_OF_STEPS: int = 100
    EXPOSURE: int = 1_000_000
    DIRECTION: str = 'left'
    PATH_TO_MAT: str = './cube.mat'
    PATH_TO_COEF: str = './lampa.tiff'

    start_record(number_of_steps=NUMBER_OF_STEPS,
                 exposure=EXPOSURE,
                 direction=DIRECTION,
                 path_to_mat=PATH_TO_MAT)

