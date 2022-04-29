import numpy as np
import tifffile as tiff
from scipy.io import loadmat, savemat


class HSImage:
    """
    Hyperspectral Image has dimension X - Y - Z where Z - count of channels
    """

    def __init__(self, hsi=None, coef=None):
        self.hsi = hsi
        self.coef = coef

    def coef_norm(self, hs_layer: np.array, thresh=100) -> np.array:
        coef = []
        for i in range(250):
            coef.append([x / thresh for x in hs_layer[:, i]])
        return np.array(coef).T

    def set_coef(self, path_to_norm: str, key: str):
        """
        This method set coefficients for normalize HSI from file with .mat or .tiff extension

        path_to_norm - path to file with raw spectrum obtained from slit
        key - key from .mat file
        """
        if path_to_norm:
            if path_to_norm.endswith('.mat'):
                if key:
                    temp = loadmat(path_to_norm)[key]
                    self.coef = self.coef_norm(temp[:, 5, :])
            if path_to_norm.endswith('.tiff'):
                temp = tiff.imread(path_to_norm)
                self.coef = self.coef_norm(temp[:, 5, :])


    def _crop_layer(self, layer: np.array,
                    gap_coord=620,
                    range_to_spectrum=185,
                    range_to_end_spectrum=250,
                    left_bound_spectrum=490,
                    right_bound_spectrum=1390
                    ) -> np.array:
        """
        This method crops layer to target area which contain spectrum
        gap_coord - int, it means coordinate of line from difraction slit
        range_to_spec - int, range from difraction slit line to area of spectrum
        range_to_end_spectrum - int, width of spectrum line
        left_bound_spectrum and right_bound spectrum - bounderies of where is spectrum
        """
        x1 = gap_coord + range_to_spectrum
        x2 = x1 + range_to_end_spectrum
        return layer[x1: x2, left_bound_spectrum: right_bound_spectrum].T

    def _normalize_spectrum_layer(self, layer: np.array,
                                  coef=None,
                                  ) -> np.array:
        """
        This method normalizes layer with not uniform light
        layer - np.array, layer of HSI
        coef - np.array, array of coefficients for uniform light
        """
        return layer / coef if coef else layer

    def add_layer_yz_fast(self, layer: np.array, i: int, count_images: int):
        # TODO replace to separate function?
        layer = self._crop_layer(layer)
        layer = self._normalize_spectrum_layer(layer, self.coef)

        x, y, z = count_images, *(layer.shape)

        if (self.hsi is None):
            self.hsi = np.zeros((x, y, z))
        # TODO squeeze
        self.hsi[i, :, :] = layer[None, :, :]

    def add_layer_yz(self, layer: np.array):
        # TODO replace to separate function?
        layer = self._crop_layer(layer)
        layer = self._normalize_spectrum_layer(layer, self.coef)

        if (self.hsi is None):
            self.hsi = layer
        elif (len(np.shape(self.hsi)) < 3):
            self.hsi = np.stack((self.hsi, layer), axis=0)
        else:
            self.hsi = np.append(self.hsi, layer[None, :, :], axis=0)

    def add_layer_xy(self, layer: np.array):
        if (self.hsi is None):
            self.hsi = layer
        elif (len(np.shape(self.hsi)) < 3):
            self.hsi = np.stack((self.hsi, layer), axis=2)
        else:
            self.hsi = np.append(self.hsi, layer[:, :, None], axis=2)

    # TODO make
    def rgb(self, channels=(80, 70, 20)) -> np.array:
        r, g, b = channels
        return np.stack((self.hsi[:, :, r], self.hsi[:, :, g], self.hsi[:, :, b]), axis=2)

    def hyp_to_mult(self, number_of_channels: int) -> np.array:
        """
        Convert hyperspectral image to multispectral
        HSI - np.array of hyperspectral image with shape X - Y - Number of channel
        number_of_channels - number of channels of multyspectral image
        """

        if (number_of_channels > np.shape(self.hsi)[2]):
            raise ValueError('Number of MSI is over then HSI')

        MSI = np.zeros((np.shape(self.hsi)[0], np.shape(self.hsi)[1], number_of_channels))
        l = [int(x * (250 / number_of_channels)) for x in range(0, number_of_channels)]
        for k, i in enumerate(l):
            MSI[:, :, k] = self.hsi[:, :, i]

        return MSI

    def get_hsi(self) -> np.array:
        return self.hsi

    def get_channel(self, number_of_channel: int) -> np.array:
        return self.hsi[:, :, number_of_channel]

    def load_from_array(self, hsi: np.array):
        self.hsi = hsi

    def load_from_mat(self, path_to_file: str, key: str):
        self.hsi = loadmat(path_to_file)[key]

    def save_to_mat(self, path_to_file: str, key: str):
        # TODO Check values in raw images
        savemat(path_to_file, {key: self.hsi.astype('int16')})

    def load_from_tiff(self, path_to_file: str):
        self.hsi = tiff.imread(path_to_file)

    def save_to_tiff(self, path_to_file):
        pass

    def load_from_npy(self, path_to_file: str):
        pass

    def save_to_npy(self):
        pass

    def yxz_to_xyz(self):
        pass

    def zxy_to_xyz(self):
        pass

    def xzy_to_xyz(self):
        pass
