# TODO: Add all the functionality provided in "https://www.legacysurvey.org/svtips/"
import os
from io import BytesIO

import requests
from astropy.io import fits
from PIL import Image
import numpy as np

class LegacySurveyQuery:
    def __init__(self, **kwargs):
        self.input_parameters = kwargs
        self.legacy_survey_parameters = self.customParams(**kwargs)

    def defaultParams(self):
        """
        Get a default dictionary of the Legacy Survey API parameters.

        Returns
        -------
            params : dict
                Default dictionary of the Legacy Survey API parameters.

        Notes
        -----
            Default (RA, DEC) are those of WISE 0855.

            Default pixel_scale is 0.262 arcseconds per pixel: "if you set the pixscale=0.262, then you will get images in the same units as
            our data release coadd image products, which are in "nanomaggy" units, ie, fluxes with a zeropoint of 22.5
            mag in the AB system." -https://www.legacysurvey.org/svtips/

        """

        params = {
            "layer": "ls-dr10", # Image layer to display
            "ra": 133.786245, # Right Ascension: Float in the range [0, 360]
            "dec": -7.244372, # Declination: Float in the range [-90, 90]
            "zoom": 10, # Zoom parameter: Integer in the range [1, 16]
            "pixel_scale": 0.262, # Arcseconds per pixel (0.262 is the default and recommended value)
            "bands": False, # Bands to display
            "size": False, # Max size is 512
            "width": False, # Max width is 512
            "height": False, # Max height is 512
            "blink": False, # Layer to blink to from the main layer
            "overlays": [], # List of overlays to add to the viewer. Each overlay is a string or a dictionary with one key-value pair (for special cases).
            "mark": False, # Mark points on the image (Format: [(RA1, DEC1), (RA2, DEC2), ...])
            "poly": False, # Draw polygons on the image (or just lines) (Format: [[(RA1, DEC1), (RA2, DEC2), ...], [(RA1, DEC1), (RA2, DEC2), ...], ...])
            "subimage": False, # 'Instead of getting a resampled image, you will get sub-images cut out from our data release' -https://www.legacysurvey.org/svtips/
        }

        return params

    def customParams(self, **kwargs):
        """
        Get a custom dictionary of the Legacy Survey API parameters.

        Parameters
        ----------
            **kwargs : dict
                Keyword arguments which are keys located in the dict of default parameters, otherwise it will raise an error. Even if the keyword
                argument is given in uppercase, it will still work.

        Returns
        -------
            params : dict
                Custom dictionary of the Legacy Survey API parameters.

        Notes
        -----
            Default (RA, Dec) are those of WISE 0855.
        """

        special_dict_params = {
            "decamfoot": ("ra", "dec"),
            "desifoot": ("ra", "dec"),
            "desifiber": ("ra", "dec"),
        }

        valid_layers = {
            "ls-dr10": None,
            "ls-dr10-model": None,
            "ls-dr10-resid": None,
            "ls-dr10-south": None,
            "ls-dr10-south-model": None,
            "ls-dr10-south-resid": None,
            "ls-dr10-grz": None,
            "ls-dr10-model-grz": None,
            "ls-dr10-resid-grz": None,
            "ls-dr10-south-grz": None,
            "ls-dr10-south-model-grz": None,
            "ls-dr10-south-resid-grz": None,
            "ls-dr9": None,
            "ls-dr9-model": None,
            "ls-dr9-resid": None,
            "ls-dr9.1.1": None,
            "ls-dr9.1.1-model": None,
            "ls-dr9.1.1-resid": None,
            "ls-dr9-north": None,
            "ls-dr9-north-model": None,
            "ls-dr9-north-resid": None,
            "ls-dr9-south": None,
            "ls-dr9-south-model": None,
            "ls-dr9-south-resid": None,
            "ls-dr8": None,
            "ls-dr8-model": None,
            "ls-dr8-resid": None,
            "ls-dr8-north": None,
            "ls-dr8-north-model": None,
            "ls-dr8-north-resid": None,
            "ls-dr8-south": None,
            "ls-dr8-south-model": None,
            "ls-dr8-south-resid": None,
            "ls-dr67": None,
            "decals-dr7": None,
            "decals-dr7-model": None,
            "decals-dr7-resid": None,
            "mzls+bass-dr6": None,
            "mzls+bass-dr6-model": None,
            "mzls+bass-dr6-resid": None,
            "decals-dr5": None,
            "decals-dr5-model": None,
            "decals-dr5-resid": None,
            "unwise-neo7": None,
            "unwise-neo6": None,
            "unwise-neo4": None,
            "unwise-cat-model": None,
            "wssa": None,
            "des-dr1": None,
            "decaps2": None,
            "decaps2-model": None,
            "decaps2-resid": None,
            "decaps2-riy": None,
            "decaps2-model-riy": None,
            "decaps2-resid-riy": None,
            "galex": None,
            "halpha": None,
            "hsc-dr2": None,
            "hsc-dr3": None,
            "sdss": None,
            "sfd": None,
            "vlass1.2": None,
        }

        valid_overlays = {
            "decamfoot": None,
            "bricks": None,
            "ccds10": None,
            "exps10": None,
            "ccds9": None,
            "ccds9n": None,
            "ccds9s": None,
            "exps9": None,
            "masks-dr9": None,
            "ccds8": None,
            "ccds8n": None,
            "ccds8s": None,
            "exps8": None,
            "ccds7": None,
            "exps7": None,
            "exps5": None,
            "ccds6": None,
            "ccds5": None,
            "ccdssdss": None,
            "unwise_tile": None,
            "sources-dr10": None,
            "sources-dr10-south": None,
            "sources-dr9": None,
            "sources-dr9n": None,
            "sources-dr9s": None,
            "sources-dr8": None,
            "sources-dr8n": None,
            "sources-dr8s": None,
            "sources-dr7": None,
            "sources-dr6": None,
            "sources-dr5": None,
            "gaia-dr2": None,
            "gaia-edr3": None,
            "hsc-dr2-cosmos": None,
            "sdss-cat": None,
            "manga": None,
            "spectra": None,
            "sdss-plates": None,
            "spectra-deep2": None,
            "desifoot": (None, None),
            "desifiber": (None, None),
            "desi-tiles-edr": None,
            "desi-spec-edr": None,
            "targets-dr9-main-dark": None,
            "targets-dr9-main-bright": None,
            "targets-dr9-main-sec-dark": None,
            "targets-dr9-main-sec-bright": None,
            "targets-dr9-sv3-dark": None,
            "targets-dr9-sv3-bright": None,
            "targets-dr9-sv3-sec-dark": None,
            "targets-dr9-sv3-sec-bright": None,
            "targets-dr9-sv1-dark": None,
            "targets-dr9-sv1-bright": None,
            "targets-dr9-sv1-sec-dark": None,
            "targets-dr9-sv1-sec-bright": None,
            "bright": None,
            "tycho2": None,
            "GCs-PNe": None,
            "ngc": None,
            "sga": None,
            "sga-parent": None,
            "photoz-dr9": None,
            "const": None
        }

        layer_dictionary = {
            "Legacy Surveys DR10 images": "ls-dr10",
            "Legacy Surveys DR10 models": "ls-dr10-model",
            "Legacy Surveys DR10 residuals": "ls-dr10-resid",
            "Legacy Surveys DR10-south images": "ls-dr10-south",
            "Legacy Surveys DR10-south models": "ls-dr10-south-model",
            "Legacy Surveys DR10-south residuals": "ls-dr10-south-resid",
            "Legacy Surveys DR10 images (grz)": "ls-dr10-grz",
            "Legacy Surveys DR10 models (grz)": "ls-dr10-model-grz",
            "Legacy Surveys DR10 residuals (grz)": "ls-dr10-resid-grz",
            "Legacy Surveys DR10-south images (grz)": "ls-dr10-south-grz",
            "Legacy Surveys DR10-south models (grz)": "ls-dr10-south-model-grz",
            "Legacy Surveys DR10-south residuals (grz)": "ls-dr10-south-resid-grz",
            "Legacy Surveys DR9 images": "ls-dr9",
            "Legacy Surveys DR9 models": "ls-dr9-model",
            "Legacy Surveys DR9 residuals": "ls-dr9-resid",
            "Legacy Surveys DR9.1.1 COSMOS deep images": "ls-dr9.1.1",
            "Legacy Surveys DR9.1.1 COSMOS deep models": "ls-dr9.1.1-model",
            "Legacy Surveys DR9.1.1 COSMOS deep residuals": "ls-dr9.1.1-resid",
            "Legacy Surveys DR9-north images": "ls-dr9-north",
            "Legacy Surveys DR9-north models": "ls-dr9-north-model",
            "Legacy Surveys DR9-north residuals": "ls-dr9-north-resid",
            "Legacy Surveys DR9-south images": "ls-dr9-south",
            "Legacy Surveys DR9-south models": "ls-dr9-south-model",
            "Legacy Surveys DR9-south residuals": "ls-dr9-south-resid",
            "Legacy Surveys DR8 images": "ls-dr8",
            "Legacy Surveys DR8 models": "ls-dr8-model",
            "Legacy Surveys DR8 residuals": "ls-dr8-resid",
            "Legacy Surveys DR8-north images": "ls-dr8-north",
            "Legacy Surveys DR8-north models": "ls-dr8-north-model",
            "Legacy Surveys DR8-north residuals": "ls-dr8-north-resid",
            "Legacy Surveys DR8-south images": "ls-dr8-south",
            "Legacy Surveys DR8-south models": "ls-dr8-south-model",
            "Legacy Surveys DR8-south residuals": "ls-dr8-south-resid",
            "Legacy Surveys DR6+DR7": "ls-dr67",
            "DECaLS DR7 images": "decals-dr7",
            "DECaLS DR7 models": "decals-dr7-model",
            "DECaLS DR7 residuals": "decals-dr7-resid",
            "MzLS+BASS DR6 images": "mzls+bass-dr6",
            "MzLS+BASS DR6 models": "mzls+bass-dr6-model",
            "MzLS+BASS DR6 residuals": "mzls+bass-dr6-resid",
            "DECaLS DR5 images": "decals-dr5",
            "DECaLS DR5 models": "decals-dr5-model",
            "DECaLS DR5 residuals": "decals-dr5-resid",
            "unWISE W1/W2 NEO7": "unwise-neo7",
            "unWISE W1/W2 NEO6": "unwise-neo6",
            "unWISE W1/W2 NEO4": "unwise-neo4",
            "unWISE Catalog model": "unwise-cat-model",
            "WISE 12-micron dust map": "wssa",
            "DES DR1": "des-dr1",
            "DECaPS2 images": "decaps2",
            "DECaPS2 models": "decaps2-model",
            "DECaPS2 residuals": "decaps2-resid",
            "DECaPS2 images (riY)": "decaps2-riy",
            "DECaPS2 models (riY)": "decaps2-model-riy",
            "DECaPS2 residuals (riY)": "decaps2-resid-riy",
            "GALEX": "galex",
            "Halpha maps": "halpha",
            "HSC DR2": "hsc-dr2",
            "HSC DR3": "hsc-dr3",
            "SDSS": "sdss",
            "SFD Dust": "sfd",
            "VLASS 1.2": "vlass1.2",
        }

        overlay_dictionary = {
            "DECam Footprint": "decamfoot",
            "Legacy Surveys Bricks": "bricks",
            "Legacy Surveys DR10 CCDs": "ccds10",
            "Legacy Surveys DR10 Exposures": "exps10",
            "Legacy Surveys DR9 CCDs": "ccds9",
            "Legacy Surveys DR9-north CCDs": "ccds9n",
            "Legacy Surveys DR9-south CCDs": "ccds9s",
            "Legacy Surveys DR9-south Exposures": "exps9",
            "All masks (LS-DR9)": "masks-dr9",
            "Legacy Surveys DR8 CCDs": "ccds8",
            "Legacy Surveys DR8-north CCDs": "ccds8n",
            "Legacy Surveys DR8-south CCDs": "ccds8s",
            "Legacy Surveys DR8-south Exposures": "exps8",
            "DECaLS DR7 CCDs": "ccds7",
            "DECaLS DR7 Exposures": "exps7",
            "DECaLS DR5 Exposures": "exps5",
            "MzLS+BASS DR6 CCDs": "ccds6",
            "DECaLS DR5 CCDs": "ccds5",
            "SDSS CCDs": "ccdssdss",
            "unWISE tiles": "unwise_tile",
            "Legacy Surveys DR10 Catalog": "sources-dr10",
            "Legacy Surveys DR10-south Catalog": "sources-dr10-south",
            "Legacy Surveys DR9 Catalog": "sources-dr9",
            "Legacy Surveys DR9-north Catalog": "sources-dr9n",
            "Legacy Surveys DR9-south Catalog": "sources-dr9s",
            "Legacy Surveys DR8 Catalog": "sources-dr8",
            "Legacy Surveys DR8-north Catalog": "sources-dr8n",
            "Legacy Surveys DR8-south Catalog": "sources-dr8s",
            "DECaLS DR7 catalog": "sources-dr7",
            "MzLS+BASS DR6 Catalog": "sources-dr6",
            "DECaLS DR5 Catalog": "sources-dr5",
            "Gaia DR2 catalog": "gaia-dr2",
            "Gaia EDR3 catalog": "gaia-edr3",
            "HSC DR2 COSMOS catalog": "hsc-dr2-cosmos",
            "SDSS catalog": "sdss-cat",
            "MaNGa IFU Spectra": "manga",
            "SDSS Spectra (DR16)": "spectra",
            "SDSS Spectro Plates": "sdss-plates",
            "DEEP2 Spectra": "spectra-deep2",
            "DESI Footprint": "desifoot",
            "DESI Fibers": "desifiber",
            "DESI EDR tiles": "desi-tiles-edr",
            "DESI EDR spectra": "desi-spec-edr",
            "DESI Dark-time Targets (DR9/Main)": "targets-dr9-main-dark",
            "DESI Bright-time Targets (DR9/Main)": "targets-dr9-main-bright",
            "DESI Dark-time Secondary Targets (DR9/Main)": "targets-dr9-main-sec-dark",
            "DESI Bright-time Secondary Targets (DR9/Main)": "targets-dr9-main-sec-bright",
            "DESI Dark-time Targets (DR9/SV3)": "targets-dr9-sv3-dark",
            "DESI Bright-time Targets (DR9/SV3)": "targets-dr9-sv3-bright",
            "DESI Dark-time Secondary Targets (DR9/SV3)": "targets-dr9-sv3-sec-dark",
            "DESI Bright-time Secondary Targets (DR9/SV3)": "targets-dr9-sv3-sec-bright",
            "DESI Dark-time Targets (DR9/SV1)": "targets-dr9-sv1-dark",
            "DESI Bright-time Targets (DR9/SV1)": "targets-dr9-sv1-bright",
            "DESI Dark-time Secondary Targets (DR9/SV1)": "targets-dr9-sv1-sec-dark",
            "DESI Bright-time Secondary Targets (DR9/SV1)": "targets-dr9-sv1-sec-bright",
            "Bright stars": "bright",
            "Tycho-2 stars": "tycho2",
            "Star clusters & Planetary Nebulae": "GCs-PNe",
            "NGC/IC galaxies": "ngc",
            "Siena Galaxy Atlas": "sga",
            "HyperLEDA/SGA galaxies": "sga-parent",
            "DR9 Photo-z": "photoz-dr9",
            "Constellations": "const",
        }

        params = self.defaultParams()

        if("overlays" in kwargs):
            overlays = kwargs["overlays"]
            if(type(overlays) == list):
                for overlay in overlays:
                    overlay_dict = {}
                    if(isinstance(overlay, dict)):
                        overlay_dict = overlay
                        if(len(overlay_dict) != 1):
                            raise ValueError("The dictionary must have only one key-value pair.")
                        overlay = list(overlay_dict.keys())[0]

                    if(overlay in overlay_dictionary):
                        old_overlay = overlay
                        overlay = overlay_dictionary[overlay]

                        if(overlay_dict != {}):
                            overlay_dict = {overlay: overlay_dict[old_overlay]}

                    if(overlay in valid_overlays):
                        if(overlay in special_dict_params):
                            argument_list = overlay_dict[overlay]
                            overlay_string = overlay + "="

                            for arg in argument_list:
                                overlay_string += f"{arg},"
                            overlay_string = overlay_string[:-1]
                            params["overlays"].append(overlay_string)
                        else:
                            params["overlays"].append(overlay)
                    else:
                        raise ValueError(f"The following overlay is not valid: {overlay}. The available overlays are: {list(valid_overlays.keys())}.")
            else:
                raise ValueError("The overlays parameter must be a list.")

        kwargs.pop("overlays", None)

        if("layer" in kwargs):
            layer = kwargs["layer"]
            if(layer in valid_layers):
                params["layer"] = layer
            elif(layer in layer_dictionary):
                params["layer"] = layer_dictionary[layer]
            else:
                raise ValueError(f"The following layer is not valid: {layer}. The available layers are: {list(valid_layers.keys())}.")

        kwargs.pop("layer", None)

        for key in kwargs:
            if (key.lower() in params):
                params[key.lower()] = kwargs[key]
            else:

                valid_kwargs = list(params.keys())
                # Remove all the keys which are in valid_overlays
                for key in valid_overlays:
                    valid_kwargs.remove(key)

                valid_kwargs.append("layer")
                valid_kwargs.append("overlays")

                raise KeyError(f"The following key is not a valid parameter: {key}. The available parameters are: {valid_kwargs}.")

        # Verify that the zoom parameter is an integer in the range [1, 16]
        if(params["zoom"] < 1 or params["zoom"] > 16):
            raise ValueError("The zoom parameter must be an integer in the range [1, 16].")

        if("blink" in kwargs):
            blink_layer = kwargs["blink"]
            if(blink_layer in layer_dictionary):
                blink_layer = layer_dictionary[blink_layer]

            if(blink_layer in valid_layers):
                params["blink"] = blink_layer
            else:
                raise ValueError(f"The following blink layer is not valid: {blink_layer}. The available layers are: {list(valid_layers.keys())}.")

        if("mark" in kwargs):
            point_list = kwargs["mark"]
            mark_string = ""

            if(type(point_list) != list):
                raise ValueError("The mark parameter must be a list iterables with two elements.")

            for point_tuple in point_list:
                if(len(point_tuple) != 2):
                    raise ValueError("The point tuple must have two elements.")
                else:
                    mark_string += f"{point_tuple[0]},{point_tuple[1]};"
            params["mark"] = mark_string[:-1]

        if("poly" in kwargs):
            poly_list = kwargs["poly"]
            poly_string = ""

            if(type(poly_list) != list):
                raise ValueError("The poly parameter must be a list of lists of tuples with two elements.")

            poly_string += ""
            for point_list in poly_list:
                for poly_point in point_list:

                    if(len(poly_point) != 2):
                        raise ValueError("The polygon tuple must have 2 elements.")
                    else:
                        poly_string += f"{poly_point[0]},{poly_point[1]},"
                poly_string = poly_string[:-1] + ";"

            params["poly"] = poly_string[:-1]

        return params

    def getParameters(self):
        return self.legacy_survey_parameters

    def getViewerURL(self):
        viewer_url_base = "https://www.legacysurvey.org/viewer?"
        viewer_url = self.addParametersToURL(viewer_url_base)
        return viewer_url

    def getJPGCutoutURL(self):
        cutout_url_base = "https://www.legacysurvey.org/viewer/jpeg-cutout?"
        cutout_url = self.addParametersToURL(cutout_url_base)
        return cutout_url

    def getFITSCutoutURL(self):
        cutout_url_base = "https://www.legacysurvey.org/viewer/fits-cutout?"
        cutout_url = self.addParametersToURL(cutout_url_base)
        return cutout_url

    def addParametersToURL(self, url_base):
        url = url_base
        for key in self.legacy_survey_parameters:
            if(self.legacy_survey_parameters[key] != False and self.legacy_survey_parameters[key] != (None, None)):
                if(type(self.legacy_survey_parameters[key]) == tuple):
                    tuple_str = str(self.legacy_survey_parameters[key])[1:-1]
                    url += f"{key}={tuple_str}&"
                elif(type(self.legacy_survey_parameters[key]) == bool):
                    url += f"{key}&"
                else:
                    # Handle special cases

                    if(key == "overlays"):
                        for overlay in self.legacy_survey_parameters[key]:
                            url += f"{overlay}&"
                    else:
                        url += f"{key}={self.legacy_survey_parameters[key]}&"
        return url

    def getImage(self, output_directory=None, filename=None):
        """
        Get the image in the specified format.

        Returns
        -------
        image_filepath : str
            The filepath of the image.
        """

        if(output_directory is None):
            output_directory = os.getcwd()

        if (filename is None):
            filename = "RA" + str(self.legacy_survey_parameters["ra"]) + "_DEC" + str(self.legacy_survey_parameters["dec"]) + f"layer{self.legacy_survey_parameters['layer']}" + ".png"

        image_format = filename.split(".")[-1]

        if(image_format.lower() not in ["jpg", "jpeg", "png",]):
            raise ValueError(f"Invalid image format: {image_format}. The available formats are: jpg, jpeg, png.")

        if(self.legacy_survey_parameters["subimage"]):
            query_url = self.getFITSCutoutURL()
        else:
            query_url = self.getJPGCutoutURL()

        response = requests.get(query_url)

        # Verify that the response is valid
        if not response.ok:
            raise ValueError(f"Invalid response: {response.status_code}")

        if (self.legacy_survey_parameters["subimage"]):
            fits_filename = filename.replace(image_format.lower(), ".fits")

            # Use the response bytes to create a FITS file
            with open(f"{output_directory}/{fits_filename}", "wb") as file:
                file.write(response.content)

            # Create an image from the FITS file
            image_filepath = self.convertFITS(f"{output_directory}/{fits_filename}", output_directory, filename, format=image_format)
            os.remove(f"{output_directory}/{fits_filename}")
            return image_filepath
        else:
            image = Image.open(BytesIO(response.content))

            # Verify that the output directory exists
            if not os.path.exists(output_directory):
                raise FileNotFoundError(f"The output directory {output_directory} does not exist.")

            image_filepath = f"{output_directory}/{filename}"

            # Save the image
            image.save(image_filepath)

            return image_filepath

    def getBlink(self, output_directory=None, filename=None, blink_speed=0.5):
        """
        Get the blink gif between the main layer and the blink layer.

        Parameters
        ----------
        output_directory : str
            The directory to save the image.
        filename : str
            The name of the gif file.
        blink_speed : float
            The loop speed of the gif in seconds.

        Returns
        -------
        image_filepath : str
            The filepath of the image.
        """

        if(self.legacy_survey_parameters["blink"] == False):
            raise ValueError("The blink parameter must be set to a valid layer.")

        if (output_directory is None):
            output_directory = os.getcwd()

        if (filename is None):
            filename = "RA" + str(self.legacy_survey_parameters["ra"]) + "_DEC" + str(self.legacy_survey_parameters["dec"]) + f"layer{self.legacy_survey_parameters['layer']}" + ".png"

        primary_layer_image_filepath = self.getImage(output_directory, "primary.png")

        # Create a new LegacySurveyQuery object with the blink layer as the main layer

        # Get the parameters of the current object but replace the layer with the blink layer
        blink_parameters = self.input_parameters.copy()
        blink_parameters["layer"] = self.legacy_survey_parameters["blink"]
        blink_lsq = LegacySurveyQuery(**blink_parameters)

        blink_layer_image_filepath = blink_lsq.getImage(output_directory, "blink.png")

        # Create a gif from the two images using PIL
        gif_filepath = f"{output_directory}/{filename.split('.')[0]}.gif"

        try:
            # Open the two images
            image1 = Image.open(primary_layer_image_filepath)
            image2 = Image.open(blink_layer_image_filepath)

            # Ensure both images are in the same mode and size
            image1 = image1.convert('RGBA')
            image2 = image2.convert('RGBA')
            image2 = image2.resize(image1.size)

            # Create a list of images
            images = [image1, image2]

            # Set the duration for each frame (in milliseconds)
            duration = int(blink_speed * 1000)  # Convert seconds to milliseconds

            # Save as GIF with looping
            images[0].save(gif_filepath, save_all=True, append_images=images[1:], duration=duration, loop=0)

        except Exception as e:
            print(f"An error occurred: {e}")

        return gif_filepath


    @staticmethod
    def convertFITS(fits_filepath, output_directory=None, filename=None, format="PNG"):
        """
        Convert a FITS file to another image format.

        Parameters
        ----------
        fits_filepath : str
            The filepath of the FITS file.

        output_directory : str
            The directory to save the image.
        filename : str
            The name of the image file.

        Returns
        -------
        image_filepath : str
            The filepath of the image.
        """

        if(output_directory is None):
            output_directory = os.getcwd()

        if(filename is None):
            filename = os.path.basename(fits_filepath)

        # Remove the extension from the filename
        filename = os.path.splitext(filename)[0] + f".{format.lower()}"

        # Open the FITS file
        with fits.open(fits_filepath) as hdul:
            data = hdul[1].data

        # Normalize the data to the range 0-255
        data = np.nan_to_num(data)  # Convert NaNs to zero
        data_min = np.min(data)
        data_max = np.max(data)
        data = (data - data_min) / (data_max - data_min) * 255
        data = data.astype(np.uint8)

        # Convert to an image
        image = Image.fromarray(data)

        # Save the image as a JPG
        filepath = f"{output_directory}/{filename}"
        image.save(filepath, format=format)

        return filepath




