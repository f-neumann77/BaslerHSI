from pypylon import pylon
import numpy as np

class Basler:
    """
    Class to work with Basler camera

    After calling StartGrabbing all settings of camera will be frozen!

    Attributes
    ----------
    camera : pylon.InstantCamera
        instance of Basler camera from pylon, must be set exposure time for it
    """
    def __init__(self, exposure: int):
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()
        self.camera.ExposureTime.SetValue(exposure)
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    def make_shot(self) -> np.array:
        """
        Makes shot from camera and return it as array
        """
        grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        while not grabResult.GrabSucceeded():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        return grabResult.Array

    def camera_close(self):
        self.camera.Close()
