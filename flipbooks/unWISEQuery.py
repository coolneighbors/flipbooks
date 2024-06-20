import os
import time
from copy import copy

import astropy.io.fits as fits
from astropy.visualization import AsinhStretch, LinearStretch
import numpy
import numpy as np
from flipbooks import WiseViewQuery
import matplotlib.pyplot as plt
from PIL import Image
import tarfile
import requests

unWISE_pixel_scale = 2.75

class unWISEQuery:

    def __init__(self, **kwargs):
        self.unWISE_parameters = self.customParams(**kwargs)
        self.filenames = self.request_unWISE_FITS()
        self.w1_image_data, self.w2_image_data = self.getImageData(self.filenames)

    def defaultParams(self):
        """
        Get a default dictionary of unWISE API parameters.

        Returns
        -------
            params : dict
                Default dictionary of unWISE API parameters.

        Notes
        -----
            Default (RA, Dec) are those of WISE 0855.

            Size refers to the pixel side-length of the image, which relates to FOV.
            unWise has a pixel-ratio of ~2.75 arc-seconds per pixel (Dan Caselden)
        """

        params = {
            "version": "neo1",
            "ra": 133.786245,
            "dec": -7.244372,
            "bands": 12,
            "size": 128,
            "file_img_m" : 1,
            "file_invvar_m" : 0,
            "file_n_m" : 0,
            "file_std_m" : 0
        }

        return params

    def customParams(self, **kwargs):
        """
        Get a custom dictionary of unWISE API parameters.

        Parameters
        ----------
            **kwargs : dict
                Keyword arguments which are keys located in the dict of default parameters, otherwise it will raise an error. Even if the keyword
                argument is given in uppercase, it will still work.

        Returns
        -------
            params : dict
                Custom dictionary of unWISE API parameters.

        Notes
        -----
            Default (RA, Dec) are those of WISE 0855.

            Size refers to the pixel side-length of the image, which relates to FOV.
            unWise has a pixel-ratio of ~2.75 arc-seconds per pixel (Dan Caselden)
        """

        params = self.defaultParams()

        for key in kwargs:
            if (key.lower() in params):
                params[key.lower()] = kwargs[key]
            else:
                raise KeyError(f"The following key is not a valid parameter: {key}. The available parameters are: {list(params.keys())}.")

        return params

    def generateRequestURL(self):
        unWISE_template_query_url = "http://unwise.me/cutout_fits?version={}&ra={}&dec={}&size={}&bands={}"
        unWISE_query_url = unWISE_template_query_url.format(self.unWISE_parameters["version"], self.unWISE_parameters["ra"], self.unWISE_parameters["dec"], self.unWISE_parameters["size"], self.unWISE_parameters["bands"])

        if (self.unWISE_parameters["file_img_m"] == 1):
            unWISE_query_url += "&file_img_m=on"
        if (self.unWISE_parameters["file_invvar_m"] == 1):
            unWISE_query_url += "&file_invvar_m=on"
        if (self.unWISE_parameters["file_n_m"] == 1):
            unWISE_query_url += "&file_n_m=on"
        if (self.unWISE_parameters["file_std_m"] == 1):
            unWISE_query_url += "&file_std_m=on"

        return unWISE_query_url

    def request_unWISE_FITS(self, delay=0):
        unWISE_query_url = self.generateRequestURL()
        filenames = []
        time.sleep(delay)
        id = hash((self.unWISE_parameters["version"], self.unWISE_parameters["ra"], self.unWISE_parameters["dec"], self.unWISE_parameters["size"], self.unWISE_parameters["bands"]))
        try:
            unWISE_response = requests.get(unWISE_query_url)
            with open(f"unWISE_zipped_folder_{id}.tar.gz", 'wb') as f:
                f.write(unWISE_response.content)
            with tarfile.open(f"unWISE_zipped_folder_{id}.tar.gz", "r:gz") as tar:
                # change the filenames to include the id in the tar file
                for member in tar.getmembers():
                    split_name =  member.name.split(".")
                    name_without_extension = split_name[0]
                    extension = split_name[1]
                    new_name = f"{name_without_extension}_{id}.{extension}"
                    member.name = new_name

                filenames = tar.getnames()
                tar.extractall()

            os.remove(f"unWISE_zipped_folder_{id}.tar.gz")
        except tarfile.ReadError:
            delay *= 2
            if delay == 0:
                delay = 5
            elif delay >= 300:
                delay = 300
            print(f"unWISE Provided an Incomplete FITS Response. Retrying in {delay} seconds...")
            filenames = self.request_unWISE_FITS(delay=delay)
            print('Success')
        except ConnectionError:
            delay *= 2
            if delay == 0:
                delay = 5
            elif delay >= 300:
                delay = 300
            print(f"unWISE Connection was Unsuccessful. Retrying in {delay} seconds...")
            filenames = self.request_unWISE_FITS(delay=delay)
            print('Success')
        except ConnectionResetError:
            delay *= 2
            if delay == 0:
                delay = 5
            elif delay >= 300:
                delay = 300
            print(f"unWISE Connection was Reset. Retrying in {delay} seconds...")
            filenames = self.request_unWISE_FITS(delay=delay)
            print('Success')
        except ConnectionRefusedError:
            raise ConnectionRefusedError(f"unWISE Connection was Refused.")

        return filenames

    def getImageData(self, flist):
        w1_image_data = None
        w2_image_data = None
        for filename in flist:
            if ("w1" in filename):
                with fits.open(filename, memmap=False) as w1_fits:
                    if(w1_fits[0].data.shape[0] == w1_fits[0].data.shape[1]):
                        w1_image_data = w1_fits[0].data

            elif ("w2" in filename):
                with fits.open(filename, memmap=False) as w2_fits:
                    if (w2_fits[0].data.shape[0] == w2_fits[0].data.shape[1]):
                        w2_image_data = w2_fits[0].data

        if(w1_image_data is None):
            for filename in flist:
                if ("w1" in filename):
                    with fits.open(filename, memmap=False) as w1_fits:
                        w1_image_data = w1_fits[0].data
                        break
        if(w2_image_data is None):
            for filename in flist:
                if ("w2" in filename):
                    with fits.open(filename, memmap=False) as w2_fits:
                        w2_image_data = w2_fits[0].data
                        break

        for filename in flist:
            os.remove(filename)

        return w1_image_data, w2_image_data

    def calculateBrightnessClip(self, mode = "percentile", **kwargs):
        """
        Calculate the brightness clip for the unWISE image.

        Parameters
        ----------
            mode : str
                The method to be used for calculating the brightness clip.

        Returns
        -------
            brightness_clip : list
                Two element list of the minimum and maximum brightness threshold for the unWISE image.
        """

        if(self.unWISE_parameters["bands"] == 1):
            image_data = self.w1_image_data
        elif(self.unWISE_parameters["bands"] == 2):
            image_data = self.w2_image_data
        elif(self.unWISE_parameters["bands"] == 12):
            image_data = (self.w1_image_data + (self.w2_image_data/2)) / 2
        else:
            raise TypeError("The bands are not 1, 2, or 12.")

        if(mode == "full"):
            brightness_clip = [np.min(image_data), np.max(image_data)]
        elif(mode == "percentile"):
            upper_percentile = kwargs["percentile"]
            if(upper_percentile > 100):
                raise ValueError("The upper percentile must be less than 100.")
            elif(upper_percentile < 50):
                raise ValueError("The upper percentile must be greater than or equal to 50.")
            lower_percentile = 100-upper_percentile
            min_bright = np.percentile(image_data, lower_percentile)
            max_bright = np.percentile(image_data, upper_percentile)

            if(upper_percentile == 50):
                return [min_bright, max_bright]

            default_min_bright = -50
            default_max_bright = 50

            if(min_bright == max_bright):
                current_version = copy(self.unWISE_parameters["version"])
                if ("neo" in current_version):
                    neo_version_number = int(current_version.split("neo")[1])
                    if (neo_version_number == 7):
                        min_bright = default_min_bright
                        max_bright = default_max_bright
                    else:
                        print(f"The current version of the unWISE data has a blank frame. Incrementing from {current_version} to neo{neo_version_number + 1}.")
                        self.unWISE_parameters["version"] = f"neo{neo_version_number + 1}"
                        self.filenames = self.request_unWISE_FITS()
                        self.w1_image_data, self.w2_image_data = self.getImageData(self.filenames)
                        brightness_clip = self.calculateBrightnessClip(mode="percentile", percentile=percentile)
                        min_bright = brightness_clip[0]
                        max_bright = brightness_clip[1]
                else:
                    min_bright = default_min_bright
                    max_bright = default_max_bright

            if(max_bright < min_bright):
                raise ValueError("The maximum brightness is less than the minimum brightness.")

            brightness_clip = [min_bright, max_bright]
        else:
            raise TypeError("The mode must be either 'full' or 'percentile'.")

        return brightness_clip

    def showBrightnessHistogram(self, image_data, title = "", brightness_clip = None, bins = 500, color = "blue", show_lines = False, immediately_show = False):
        if(brightness_clip is None):
            brightness_clip = [np.min(image_data), np.max(image_data)]
        plt.hist(image_data.flatten(), bins = bins, color= color, label=title, alpha=0.5)
        plt.title(title)

        if(show_lines):
            plt.axvline(x=brightness_clip[0], color='r', label= title + ' minbright')
            plt.axvline(x=np.mean(image_data), color='black', label= title + ' average')
            plt.axvline(x=brightness_clip[1], color='b', label=title + ' maxbright')
            plt.legend(loc='best')
        if(immediately_show):
            plt.show()
        else:
            plt.legend(loc='best')
            plt.title("Combined Brightness Histogram")

    def generateWiseViewImage(self, brightness_clip = [-50, 500], invert=True):
        stretched_w1_image_data = self.asinhStretchImage(self.normalizeImage(self.w1_image_data, brightness_clip[0], brightness_clip[1]))
        stretched_w2_image_data = self.asinhStretchImage(self.normalizeImage(self.w2_image_data, brightness_clip[0], brightness_clip[1]))
        rgb_image_data = numpy.empty((stretched_w1_image_data.shape[0], stretched_w1_image_data.shape[1], 3))
        for i in range(rgb_image_data.shape[0]):
            for j in range(rgb_image_data.shape[1]):
                rgb_image_data[i, j, 0] = stretched_w1_image_data[i, j]
                rgb_image_data[i, j, 1] = (stretched_w1_image_data[i, j] + stretched_w2_image_data[i, j]) / 2
                rgb_image_data[i, j, 2] = stretched_w2_image_data[i, j]
        if (invert):
            return self.invertRGBImage(rgb_image_data)
        else:
            return rgb_image_data


    def displayWiseViewImage(self, brightness_clip = [-50, 500], invert=True):
        self.displayImage(self.generateWiseViewImage(brightness_clip, invert))

    def saveWiseViewImage(self, filename, brightness_clip = [-50, 500], invert=True):
        self.saveImage(self.generateWiseViewImage(brightness_clip, invert), filename)

    @classmethod
    def normalizeImage(cls, image_data, min_value=None, max_value=None):
        normalized_image_data = copy(image_data)
        if (min_value is None):
            min_value = image_data.min()

        if (max_value is None):
            max_value = image_data.max()

        # go through each pixel and normalize it
        for i in range(normalized_image_data.shape[0]):
            for j in range(normalized_image_data.shape[1]):
                normalized_image_data[i, j] = (normalized_image_data[i, j] - min_value) / (max_value - min_value)
        return normalized_image_data

    @classmethod
    def convertToRGBImage(self, image_data, color = (1,0,0)):
        R, G, B = color
        normalized_image_data = self.normalizeImage(image_data)
        rgb_image_data = numpy.empty((normalized_image_data.shape[0], normalized_image_data.shape[1], 3))
        for i in range(rgb_image_data.shape[0]):
            for j in range(rgb_image_data.shape[1]):
                rgb_image_data[i, j, 0] = R * normalized_image_data[i, j]
                rgb_image_data[i, j, 1] = G * normalized_image_data[i, j]
                rgb_image_data[i, j, 2] = B * normalized_image_data[i, j]
        return rgb_image_data

    @classmethod
    def asinhStretchImage(cls, image_data, linear = 1):
        stretched_image_data = copy(image_data)
        stretch = AsinhStretch(linear)
        stretched_image_data = stretch(stretched_image_data)
        return stretched_image_data

    #TODO: VERIFY THIS IS CORRECT
    @classmethod
    def linearlyStretchImage(cls, image_data, slope = 1, intercept = 0):
        stretched_image_data = copy(image_data)
        stretch = LinearStretch(slope, intercept)
        stretched_image_data = stretch(stretched_image_data)
        return stretched_image_data

    @classmethod
    def invertRGBImage(cls, image_data):
        inverted_image_data = copy(image_data)
        for i in range(inverted_image_data.shape[0]):
            for j in range(inverted_image_data.shape[1]):
                inverted_image_data[i, j, 0] = 1 - inverted_image_data[i, j, 0]
                inverted_image_data[i, j, 1] = 1 - inverted_image_data[i, j, 1]
                inverted_image_data[i, j, 2] = 1 - inverted_image_data[i, j, 2]
        return inverted_image_data

    @classmethod
    # display an RGB image array
    def displayImage(cls, image_data):
        # display the image_data
        plt.imshow(numpy.flipud(image_data), interpolation="none")
        plt.show()

    @classmethod
    # save an RGB image array to a file
    def saveImage(cls, image_data, filename):
        Image.fromarray(np.array(255 * numpy.flipud(image_data), dtype=np.uint8)).save(filename)

    @classmethod
    def FOVToPixelSize(cls, FOV):
        """
        Calculate the corresponding pixel size of a given FOV (in arcseconds).

        Parameters
        ----------
            FOV : float
                Field of view in arcseconds.

        Returns
        -------
            pixel_size : int
                Side length in pixels

        Notes
        -----
            Since WiseView uses the unWISE Catalog, it has a pixel ratio of ~2.75 arcseconds per pixel.
            Notice, since pixel size must be an integer, this conversion can not be exact for all FOVs.
            In general, for some pixel_size, it can correspond to an FOV of FOV±2.75 arcseconds (depending on how you
            round to an integer). Since the int casting truncates the value of FOV / unWISE_pixel_scale, this means our
            pixel_size can correspond to an FOV between FOV-2.75 arcseconds and FOV arcseconds.
        """

        pixel_size = int(FOV / unWISE_pixel_scale)
        return pixel_size

    @classmethod
    def PixelSizeToFOV(cls, pixel_size):
        """
        Calculate the corresponding Field of View from a provided pixel_size.

        Parameters
        ----------
            pixel_size : int
                Side length in pixels

        Returns
        -------
            FOV : float
                Field of view in arcseconds.

        Notes
        -----
            Since WiseView uses the unWISE Catalog, it has a pixel ratio of ~2.75 arcseconds per pixel.
        """

        FOV = unWISE_pixel_scale * pixel_size
        return FOV

if (__name__ == "__main__"):
    version = "neo4"
    ra = 243.9804845454199
    dec = 79.0040665827614
    size = unWISEQuery.FOVToPixelSize(120)
    bands = 12

    if (bands == 1):
        band = 1
    elif (bands == 2):
        band = 2
    else:
        band = 3

    unWISE_Query = unWISEQuery(version=version, ra=ra, dec=dec, size=size, bands=bands)

    percentile = 97.5
    brightness_clip = unWISE_Query.calculateBrightnessClip("percentile", percentile=percentile)
    print(brightness_clip)
    unWISE_Query.displayWiseViewImage(brightness_clip=brightness_clip)
    wise_view_query = WiseViewQuery.WiseViewQuery(ra=ra, dec=dec, size=size, band=band, minbright=brightness_clip[0], maxbright=brightness_clip[1])
    #wise_view_query.generateSyntheticObject(synth_a_w2=16,synth_a_pmra=1000,synth_a_pmdec=1000)
    print(wise_view_query.generateWiseViewURL())
