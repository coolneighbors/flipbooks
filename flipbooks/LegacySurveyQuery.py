# TODO: Add all the functionality provided in "https://www.legacysurvey.org/svtips/"

class LegacySurveyQuery:
    def __init__(self, **kwargs):
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
            "layer": "ls-dr10",
            "ra": 133.786245,
            "dec": -7.244372,
            "zoom": 10,
            "pixel_scale": 0.262,
            "bands": "grz",
            "size": 512,
            "width": 512,
            "height": 512,
            "decamfoot": (None, None),
            "bricks": False,
            "ccds10": False,
            "exps10": False,
            "ccds9": False,
            "ccds9n": False,
            "ccds9s": False,
            "exps9": False,
            "masks-dr9": False,
            "ccds8": False,
            "ccds8n": False,
            "ccds8s": False,
            "exps8": False,
            "ccds7": False,
            "exps7": False,
            "exps5": False,
            "ccds6": False,
            "ccds5": False,
            "ccdssdss": False,
            "unwise_tile": False,
            "sources-dr10": False,
            "sources-dr10-south": False,
            "sources-dr9": False,
            "sources-dr9n": False,
            "sources-dr9s": False,
            "sources-dr8": False,
            "sources-dr8n": False,
            "sources-dr8s": False,
            "sources-dr7": False,
            "sources-dr6": False,
            "sources-dr5": False,
            "gaia-dr2": False,
            "gaia-edr3": False,
            "hsc-dr2-cosmos": False,
            "sdss-cat": False,
            "manga": False,
            "spectra": False,
            "sdss-plates": False,
            "spectra-deep2": False,
            "desifoot": (None, None),
            "desifiber": (None, None),
            "desi-tiles-edr": False,
            "desi-spec-edr": False,
            "targets-dr9-main-dark": False,
            "targets-dr9-main-bright": False,
            "targets-dr9-main-sec-dark": False,
            "targets-dr9-main-sec-bright": False,
            "targets-dr9-sv3-dark": False,
            "targets-dr9-sv3-bright": False,
            "targets-dr9-sv3-sec-dark": False,
            "targets-dr9-sv3-sec-bright": False,
            "targets-dr9-sv1-dark": False,
            "targets-dr9-sv1-bright": False,
            "targets-dr9-sv1-sec-dark": False,
            "targets-dr9-sv1-sec-bright": False,
            "bright": False,
            "tycho2": False,
            "GCs-PNe": False,
            "ngc": False,
            "sga": False,
            "sga-parent": False,
            "photoz-dr9": False,
            "const": False
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

        special_formating_params = {
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
                    print("OVERLAY: ", overlay)
                    print("valid_overlays: ", valid_overlays)
                    if(overlay in valid_overlays):
                        if(overlay in special_formating_params):
                            arg_value_list = []
                            for arg in special_formating_params[overlay]:
                                arg_value = params[arg]
                                arg_value_list.append(arg_value)
                            params[overlay] = tuple(arg_value_list)
                        else:
                            params[overlay] = True

                    elif(overlay in overlay_dictionary):

                        if(overlay in special_formating_params):
                            arg_value_list = []
                            for arg in special_formating_params[overlay]:
                                arg_value = params[arg]
                                arg_value_list.append(arg_value)
                            params[overlay_dictionary[overlay]] = tuple(arg_value_list)
                        else:
                            params[overlay_dictionary[overlay]] = True
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
                    url += f"{key}={self.legacy_survey_parameters[key]}&"
        return url

    def get



