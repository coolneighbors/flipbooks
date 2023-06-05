"""
Refactored on Tuesday June 28, 2022
Multiprocessing features created on Fri Jun 10 14:53:00 2022
@authors: Aaron Meisner, Noah Schapera, Austin Humphreys
"""

import os
import time

import requests
import multiprocessing as mp
from PIL import Image
from flipbooks import postProcessing

unWISE_pixel_scale = 2.75

class WiseViewQuery:

    png_anim = "https://vjxontvb73.execute-api.us-west-2.amazonaws.com/png-animation"
    amnh_base_url = "https://amnh-citsci-public.s3-us-west-2.amazonaws.com/"

    def __init__(self, **kwargs):
        self.wise_view_parameters = self.customParams(**kwargs)

        self.JSONResponse = self.getJSONResponse()
        try:
            if(self.JSONResponse["message"] == 'Service Unavailable'):
                print("WiseView Service Unavailable, Trying again...")
                self.__init__(**kwargs)
                print("Success: WiseView Service Available")
        except KeyError:
            pass


    def defaultParams(self):
        """
        Get a default dictionary of WiseView API parameters.

        Returns
        -------
            params : dict
                Default dictionary of WiseView API parameters.

        Notes
        -----
            Default (RA, Dec) are those of WISE 0855.

            Size refers to the pixel side-length of the image, which relates to FOV.
            unWise has a pixel-ratio of ~2.75 arc-seconds per pixel (Dan Caselden)
        """

        params = {
            "ra": 133.786245,
            "dec": -7.244372,
            "band": 3,
            "size": 128,
            "max_dyr": 0,
            "minbright": -50.0000,
            "maxbright": 500.0000,
            "invert": 1,
            "stretch": 1,
            "diff": 0,
            "scandir": 0,
            "outer": 0,
            "neowise": 0,
            "window": 0.5,
            "diff_window": 1,
            "unique": 1,
            "smooth_scan": 0,
            "shift": 0,
            "pmx": 0,
            "pmy": 0,
            "synth_a": 0,
            "synth_a_sub": 0,
            "synth_a_ra": "",
            "synth_a_dec": "",
            "synth_a_w1": "",
            "synth_a_w2": "",
            "synth_a_pmra": 0,
            "synth_a_pmdec": 0,
            "synth_a_mjd": "",
            "synth_b": 0,
            "synth_b_sub": 0,
            "synth_b_ra": "",
            "synth_b_dec": "",
            "synth_b_w1": "",
            "synth_b_w2": "",
            "synth_b_pmra": 0,
            "synth_b_pmdec": 0,
            "synth_b_mjd": "",
        }

        return params

    def customParams(self, **kwargs):
        """
        Provides a customized dictionary of WiseView API query parameters based on the provided keyword arguments.
        All unchanged parameters are set to their default values in default_params.

        Parameters
        ----------
            kwargs : keyword arguments
                Keyword arguments which are keys located in the dict of default parameters, otherwise it will raise an error. Even if the keyword
                argument is given in uppercase, it will still work.

        Returns
        -------
            params : dict
                WiseView API query parameters for requested sky location and image stretch.

        Notes
        -----
            This has been generalized to all possible parameters, assuming you know the names of the parameters you want to
            modify are.
        """

        params = self.defaultParams()

        for key in kwargs:
            if (key.lower() in params):
                params[key.lower()] = kwargs[key]
            else:
                raise KeyError(f"The following key is not a valid parameter: {key}. The available parameters are: {list(params.keys())}.")

        return params

    def generateSyntheticObject(self,**kwargs):
        """
        Sets the synth parameters in the current WiseView parameters dictionary and requests the corresponding JSON
        again. If parameters are left as empty, they will be set to some pre-defined default values.

        Parameters
        ----------
            kwargs : keyword arguments
                Keyword arguments which are a part of the synth parameters in default_parameters, otherwise it will
                raise an error. Even if the keyword argument is given in uppercase, it will still work.
                Defaults:
                synth_x_sub = 0
                synth_x_ra = current RA
                synth_x_dec = current DEC
                synth_x_w1 = 99.0
                synth_x_w2 = 13.0
                synth_x_mjd = mjd of the first frame
        Notes
        -----

        """

        a_keys = ["synth_a_sub", "synth_a_ra", "synth_a_dec", "synth_a_w1", "synth_a_w2", "synth_a_pmra", "synth_a_pmdec", "synth_a_mjd"]
        b_keys = ["synth_b_sub", "synth_b_ra", "synth_b_dec", "synth_b_w1", "synth_b_w2", "synth_b_pmra", "synth_b_pmdec", "synth_b_mjd"]
        valid_keys = [*a_keys, *b_keys]
        self.wise_view_parameters["synth_a"] = 1
        for key in kwargs:
            if (key.lower() in valid_keys):
                if(key.lower() in a_keys):
                    self.wise_view_parameters[key.lower()] = kwargs[key]
                elif(key.lower() in b_keys):
                    self.wise_view_parameters["synth_b"] = 1
                    self.wise_view_parameters[key.lower()] = kwargs[key]
            else:
                raise KeyError(f"The following key is not a valid parameter: {key}. The available parameters are: {valid_keys}.")

        if(self.wise_view_parameters["synth_a"] == 1):
            if(self.wise_view_parameters["synth_a_ra"] == ""):
                self.wise_view_parameters["synth_a_ra"] = self.wise_view_parameters["ra"]
            if(self.wise_view_parameters["synth_a_dec"] == ""):
                self.wise_view_parameters["synth_a_dec"] = self.wise_view_parameters["dec"]
            if (self.wise_view_parameters["synth_a_w1"] == ""):
                self.wise_view_parameters["synth_a_w1"] = 99.0
            if (self.wise_view_parameters["synth_a_w2"] == ""):
                self.wise_view_parameters["synth_a_w2"] = 13.0
            if(self.wise_view_parameters["synth_a_mjd"] == ""):
                self.wise_view_parameters["synth_a_mjd"] = self.JSONResponse["all_mjds"][0]

        if(self.wise_view_parameters["synth_b"] == 1):
            if (self.wise_view_parameters["synth_b_ra"] == ""):
                self.wise_view_parameters["synth_b_ra"] = self.wise_view_parameters["ra"]
            if (self.wise_view_parameters["synth_b_dec"] == ""):
                self.wise_view_parameters["synth_b_dec"] = self.wise_view_parameters["dec"]
            if (self.wise_view_parameters["synth_b_w1"] == ""):
                self.wise_view_parameters["synth_b_w1"] = 99.0
            if (self.wise_view_parameters["synth_b_w2"] == ""):
                self.wise_view_parameters["synth_b_w2"] = 13.0
            if (self.wise_view_parameters["synth_b_mjd"] == ""):
                self.wise_view_parameters["synth_b_mjd"] = self.JSONResponse["all_mjds"][0]

        self.JSONResponse = self.getJSONResponse()

    def getResponse(self, delay=0):
        time.sleep(delay)
        try:
            response = requests.get(self.png_anim, params=self.wise_view_parameters)
        except ConnectionResetError:
            delay *= 2
            if delay == 0:
                delay = 5
            elif delay >= 300:
                delay = 300
            print(f"AWS Connection Reset Error, Retrying in {delay} seconds...")
            response = self.getResponse(delay=delay)
            print(f'Success: Response Received')
        return response

    def getJSONResponse(self, delay=0):
        time.sleep(delay)
        try:
            json_response = self.getResponse().json()
        except requests.exceptions.JSONDecodeError:
            delay *= 2
            if delay == 0:
                delay = 5
            elif delay >= 300:
                delay = 300
            print(f"Invalid JSON response sent from WiseView, Retrying in {delay} seconds...")
            json_response = self.getJSONResponse(delay=delay)
            print(f'Success: JSON Response Received')
        return json_response

    def getURLs(self):
        """
        Get a list of WiseView image URLs for a desired blink.

        Parameters
        ----------


        Returns
        -------
            urls : list
                List of string URLs gathered from the WiseView API.

        """

        urls_endings = self.requestMetadata("ims")
        urls = []
        for url_ending in urls_endings:
            urls.append(self.amnh_base_url + url_ending)

        return urls


    def requestMetadata(self, *args):
        """
        Get requested metadata relating to the image blinks generated from self.wise_view_parameters

        Parameters
        ----------

        Returns
        -------
            singular argument or tuple of arguments : Any or tuple
                Returns the value of a single argument or returns a tuple of values from multiple arguments
        """

        valid_keys = ['ims', 'min', 'max', 'all_mjds', 'mjds', 'epochs', 'scandirs', 'CRPIX1', 'CRPIX2', 'CRVAL1','CRVAL2', 'NAXIS1', 'NAXIS2']
        requested_response_values = []
        for key in args:
            if (key in valid_keys):
                try:
                    requested_response_values.append(self.JSONResponse[key])
                except Exception as e:
                    print(f"Error in WiseViewQuery.requestMetadata: {e}, this should be investigated.")
            else:
                raise KeyError(f"The following key is not a valid parameter: {key}. The available parameters are: {valid_keys}.")
        if(len(args) == 1):
            return requested_response_values[0]
        else:
            return tuple(requested_response_values)

    @classmethod
    def getPNGDataFromURL(cls, url, delay=0):
        time.sleep(delay)
        try:
            PNG_data = requests.get(url).content
        except ConnectionResetError:
            delay *= 2
            if delay == 0:
                delay = 5
            elif delay >= 300:
                delay = 300
            print(f"AWS Request Reset Error (png download), Retrying in {delay} seconds...")
            PNG_data = WiseViewQuery.getPNGDataFromURL(url, delay=delay).content
            print('Success')
        return PNG_data

    @classmethod
    def getFITSDataFromURL(cls, url, delay=0):
        time.sleep(delay)
        try:
            FITS_data = requests.get(url).content
        except ConnectionResetError:
            delay *= 2
            if delay == 0:
                delay = 5
            elif delay >= 300:
                delay = 300
            print(f"AWS Request Reset Error (fits download), Retrying in {delay} seconds...")
            FITS_data = WiseViewQuery.getFITSDataFromURL(url, delay=delay).content
            print('Success')
        return FITS_data

    @classmethod
    def downloadPNG(cls, url, outdir, fieldName):
        """
        Download one PNG image based on its URL.

        Parameters
        ----------
            url : str
                Download URL.
            outdir : str
                Output directory.
            fieldName : str
                Name to be given to the file

        Returns
        -------
            fname_dest : str
                Destination file name to which the PNG was downloaded.

        Notes
        -----
            'url' here should be just a string, not an array or list of strings.

        """

        fname = os.path.basename(fieldName)
        fname_dest = os.path.join(outdir, fname)

        r_content = WiseViewQuery.getPNGDataFromURL(url)

        open(fname_dest, 'wb').write(r_content)

        return fname_dest

    @classmethod
    def downloadFITS(cls, url, outdir, fieldName):
        """
        Download one FITS file based on its URL.

        Parameters
        ----------
            url : str
                Download URL.
            outdir : str
                Output directory.
            fieldName : str
                Name to be given to the file

        Returns
        -------
            fname_dest : str
                Destination file name to which the FITS file was downloaded.

        Notes
        -----
            'url' here should be just a string, not an array or list of strings.

        """

        fname = os.path.basename(fieldName)
        fname_dest = os.path.join(outdir, fname)

        r_content = WiseViewQuery.getFITSDataFromURL(url)

        open(fname_dest, 'wb').write(r_content)

        return fname_dest

    @classmethod
    def downloadData(cls, url, i, ra, dec, outdir):
        fieldName = 'field-RA' + str(ra) + '-DEC' + str(dec) + '-' + str(i) + '.png'
        fname_dest = WiseViewQuery.downloadPNG(url, outdir, fieldName)
        return fname_dest

    @classmethod
    def earlyTerminationProtocol(cls, flist):
        print("Early termination protocol initiated. Deleting unfinished files.")
        for f in flist:
            if (os.path.exists(f)):
                os.remove(f)

    @classmethod
    def downloadPNGs(cls, urls, ra, dec, outdir):
        try:
            pool = mp.Pool()
            processes = [pool.apply_async(WiseViewQuery.downloadData, args=(urls[i], i, ra, dec, outdir)) for i in range(len(urls))]
            flist = [p.get() for p in processes]
        except Exception as e:
            flist = []
            for i in range(len(urls)):
                fieldName = 'field-RA' + str(ra) + '-DEC' + str(dec) + '-' + str(i) + '.png'
                fname = os.path.basename(fieldName)
                fname_dest = os.path.join(outdir, fname)
                flist.append(fname_dest)
            cls.earlyTerminationProtocol(flist)
        return flist

    def downloadWiseViewData(self, outdir, scale_factor=1.0, addGrid=False, gridCount=5, gridType = "Solid", gridColor = (0,0,0)):
        """
        Generates a set of PNG files for the available set of data from WiseView (which is from the unWISE data)

        Parameters
        ----------
            outdir : str
                Output directory of the PNG files
            scale_factor : float, optional
                PNG image size scaling factor, use integer values to avoid pixel-value interpolation.
                Uses Nearest-Neighbor algorithm.
            addGrid : bool, optional
                Boolean parameter which determines whether to overlay a grid on the PNG files. Defaults to False.
            gridCount : int, optional
                Number of grid lines to generate on the image (height and width). The default is 5.
            gridType : str, optional
                A string which determines the type of grid to overlay, with the available grid options being Solid,
                Intersection, and Dashed. Defaults to Solid.
            gridColor : tuple, optional
                A 3 integer element tuple which represents the RGB values of the color

        Returns
        -------
            flist : list of str
                List of (full path) file names of PNG images

        Notes
        -----
            Has the functionality that if outdir doesn't currently exist, it will create it instead of previously where
            we just asserted that it existed.
        """

        if (not os.path.exists(outdir)):
            os.mkdir(outdir)

        urls = self.getURLs()

        ra = self.wise_view_parameters['ra']
        dec = self.wise_view_parameters['dec']

        flist = self.downloadPNGs(urls, ra, dec, outdir)
        size_list = []
        for f in flist:
            with Image.open(f) as image:
                width = image.width * scale_factor
                height = image.height * scale_factor
                size_list.append((width,height))
        postProcessing.applyPNGModifications(flist, scale_factor, addGrid, gridCount, gridType, gridColor)

        return flist, size_list

    @classmethod
    def createGIF(cls, flist, gifname, duration=0.2, scale_factor=1.0):
        """
        Construct a GIF animation from a list of PNG files.

        Parameters
        ----------
            flist : list
                List of (full path) file names of PNG images from which to
                construct the GIF animation.
            gifname : str
                Output file name (full path) for the GIF animation.
            duration : float, optional
                Time interval in seconds for each frame in the GIF blink (?).
            scale_factor : float, optional
                PNG image size scaling factor

        Notes
        -----
             Order in which the PNGs appear in the GIF is dictated by the
             order of the file names in 'flist'.

        """

        import imageio

        # add checks on whether the files in flist actually exist?

        # Rescales PNGs
        if (scale_factor != 1.0):
            for f in flist:
                with Image.open(f) as im:
                    size = im.size
                    width = size[0]
                    height = size[1]
                    rescaled_size = (width * scale_factor, height * scale_factor)
                    postProcessing.resize_png(f, rescaled_size)

        images = []
        for f in flist:
            images.append(imageio.imread(f))

        imageio.mimsave(gifname, images, duration=duration)

    def createWiseViewGIF(self, outdir, gifname, duration=0.2, scale_factor=1.0, delete_pngs=True):
        """
        Create one WiseView animation at a desired central sky location.

        Parameters
        ----------
            outdir : str
                Output directory of the image frames.
            gifname : str
                Output path filename for the GIF animation.
            duration : float, optional
                Time interval in seconds for each frame in the GIF.
            scale_factor : float, optional
                Frame image size scaling factor.
            delete_pngs : bool, optional
                Delete downloaded PNGs after having used them to construct the GIF.

        Notes
        -----
            'gifname' and 'outdir' arguments could potentially be combined
            into one argument that gives the full desired output file path.
            Currently, the GIF gets written into the current working directory. It
            would be better to make the GIF output directory configurable.
            Would be nice to add some more 'logging' type of printouts.
        """

        # Counter, used to determine png chronology
        counter = 0

        if (not os.path.exists(outdir)):
            os.mkdir(outdir)

        urls = self.getURLs()

        ra = self.wise_view_parameters['ra']
        dec = self.wise_view_parameters['dec']

        flist = []

        for url in urls:
            fieldName = 'field-RA' + str(ra) + '-DEC' + str(dec) + '-' + str(counter) + '.png'
            fname_dest = self.downloadPNG(url, outdir, fieldName)
            flist.append(fname_dest)
            counter += 1

        self.createGIF(flist, gifname, duration=duration, scale_factor=scale_factor)

        if delete_pngs:
            print('Cleaning up...')
            for f in flist:
                os.remove(f)

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

    def generateWiseViewURL(self):
        wise_view_template_url = "http://byw.tools/wiseview#ra={}&dec={}&size={}&band={}&speed={}&minbright={}&maxbright={}&window={}&diff_window={}&linear={}&color={}&zoom={}&border={}&gaia={}&invert={}&maxdyr={}&scandir={}&neowise={}&diff={}&outer_epochs={}&unique_window={}&smooth_scan={}&shift={}&pmra={}&pmdec={}&synth_a={}&synth_a_sub={}&synth_a_ra={}&synth_a_dec={}&synth_a_w1={}&synth_a_w2={}&synth_a_pmra={}&synth_a_pmdec={}&synth_a_mjd={}&synth_b={}&synth_b_sub={}&synth_b_ra={}&synth_b_dec={}&synth_b_w1={}&synth_b_w2={}&synth_b_pmra={}&synth_b_pmdec={}&synth_b_mjd={}"

        # FOV in arcseconds
        fov = self.PixelSizeToFOV(self.wise_view_parameters['size'])

        # Duration of frames in ms
        speed = 150

        # Linear scaling factor
        linear = 1

        # Zoom factor
        zoom = 9

        # Display border on first frame
        border = 0

        # Gaia overlay
        gaia = 1

        return wise_view_template_url.format(self.wise_view_parameters['ra'], self.wise_view_parameters['dec'],fov,self.wise_view_parameters['band'], speed, self.wise_view_parameters['minbright'],self.wise_view_parameters['maxbright'], self.wise_view_parameters['window'],self.wise_view_parameters['diff_window'], linear, "", zoom, border, gaia,self.wise_view_parameters['invert'], self.wise_view_parameters['max_dyr'],self.wise_view_parameters['scandir'], self.wise_view_parameters['neowise'],self.wise_view_parameters['diff'], self.wise_view_parameters['outer'],self.wise_view_parameters['unique'], self.wise_view_parameters['smooth_scan'],self.wise_view_parameters['shift'], self.wise_view_parameters['pmx'],self.wise_view_parameters['pmy'], self.wise_view_parameters['synth_a'],self.wise_view_parameters['synth_a_sub'], self.wise_view_parameters['synth_a_ra'],self.wise_view_parameters['synth_a_dec'], self.wise_view_parameters['synth_a_w1'],self.wise_view_parameters['synth_a_w2'], self.wise_view_parameters['synth_a_pmra'],self.wise_view_parameters['synth_a_pmdec'], self.wise_view_parameters['synth_a_mjd'],self.wise_view_parameters['synth_b'], self.wise_view_parameters['synth_b_sub'],self.wise_view_parameters['synth_b_ra'], self.wise_view_parameters['synth_b_dec'],self.wise_view_parameters['synth_b_w1'], self.wise_view_parameters['synth_b_w2'],self.wise_view_parameters['synth_b_pmra'],self.wise_view_parameters['synth_b_pmdec'], self.wise_view_parameters['synth_b_mjd'])

    def generateWiseViewFITSURL(self, band='W1'):
        if(band == 'W1'):
            bands = '1'
        elif(band == 'W2'):
            bands = '2'
        wise_view_FITS_template_url = "http://byw.tools/cutout?ra={}&dec={}&size={}&band={}&epoch=0"

        return wise_view_FITS_template_url.format(self.wise_view_parameters['ra'], self.wise_view_parameters['dec'],self.wise_view_parameters['size'],bands)

    def requestWiseViewFITS(self):
        bands = ['W1','W2']
        outdir = "fits"
        if (not os.path.exists(outdir)):
            os.mkdir(outdir)
        FITS_filenames = []
        for band in bands:
            wise_view_FITS_url = self.generateWiseViewFITSURL(band)
            print(f'Requesting {band} FITS from WiseView...')
            if(band == 'W1'):
                W1_fieldName = 'W1-field-RA' + str(self.wise_view_parameters["ra"]) + '-DEC' + str(self.wise_view_parameters["dec"]) + '-' + "-epoch0" + '.fits'
                FITS_filenames.append(self.downloadFITS(wise_view_FITS_url, outdir, fieldName=W1_fieldName))
            elif(band == 'W2'):
                W2_fieldName = 'W2-field-RA' + str(self.wise_view_parameters["ra"]) + '-DEC' + str(self.wise_view_parameters["dec"]) + '-' + "-epoch0" + '.fits'
                FITS_filenames.append(self.downloadFITS(wise_view_FITS_url, outdir, fieldName=W2_fieldName))

        return FITS_filenames


    def __str__(self):
        return str(self.wise_view_parameters)