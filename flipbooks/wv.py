import requests
import os
import shutil
import time
from PIL import Image
from flipbooks import mpScript

png_anim = "https://vjxontvb73.execute-api.us-west-2.amazonaws.com/png-animation"
amnh_base_url = "https://amnh-citsci-public.s3-us-west-2.amazonaws.com/"

def default_params():
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

def custom_params(**kwargs):
    """
    Provides a customized dictionary of WiseView API query parameters based on the provided keyword arguments.
    All unchanged parameters are set to their default values in default_params.

    Parameters
    ----------
        kwargs : keyword arguments
            Keyword arguments which are in default_parameters, otherwise it will raise an error. Even if the keyword
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

    params = default_params()

    for key in kwargs:
        if(key.lower() in params):
            params[key.lower()] = kwargs[key]
        else:
            raise KeyError(f"The following key is not a valid parameter: {key}")

    return params

def generate_wv_url(wise_view_parameters):
    unWISE_pixel_ratio = 2.75
    wise_view_template_url = "http://byw.tools/wiseview#ra={}&dec={}&size={}&band={}&speed={}&minbright={}&maxbright={}&window={}&diff_window={}&linear={}&color={}&zoom={}&border={}&gaia={}&invert={}&maxdyr={}&scandir={}&neowise={}&diff={}&outer_epochs={}&unique_window={}&smooth_scan={}&shift={}&pmra={}&pmdec={}&synth_a={}&synth_a_sub={}&synth_a_ra={}&synth_a_dec={}&synth_a_w1={}&synth_a_w2={}&synth_a_pmra={}&synth_a_pmdec={}&synth_a_mjd={}&synth_b={}&synth_b_sub={}&synth_b_ra={}&synth_b_dec={}&synth_b_w1={}&synth_b_w2={}&synth_b_pmra={}&synth_b_pmdec={}&synth_b_mjd={}"
    return wise_view_template_url.format(wise_view_parameters['ra'],wise_view_parameters['dec'],unWISE_pixel_ratio*wise_view_parameters['size'],wise_view_parameters['band'],500,wise_view_parameters['minbright'],wise_view_parameters['maxbright'],wise_view_parameters['window'],wise_view_parameters['diff_window'],1,"",9,0,0,wise_view_parameters['invert'],wise_view_parameters['max_dyr'],wise_view_parameters['scandir'],wise_view_parameters['neowise'],wise_view_parameters['diff'],wise_view_parameters['outer'],wise_view_parameters['unique'],wise_view_parameters['smooth_scan'],wise_view_parameters['shift'],wise_view_parameters['pmx'],wise_view_parameters['pmy'],wise_view_parameters['synth_a'],wise_view_parameters['synth_a_sub'],wise_view_parameters['synth_a_ra'],wise_view_parameters['synth_a_dec'],wise_view_parameters['synth_a_w1'],wise_view_parameters['synth_a_w2'],wise_view_parameters['synth_a_pmra'],wise_view_parameters['synth_a_pmdec'],wise_view_parameters['synth_a_mjd'],wise_view_parameters['synth_b'],wise_view_parameters['synth_b_sub'],wise_view_parameters['synth_b_ra'],wise_view_parameters['synth_b_dec'],wise_view_parameters['synth_b_w1'],wise_view_parameters['synth_b_w2'],wise_view_parameters['synth_b_pmra'],wise_view_parameters['synth_b_pmdec'],wise_view_parameters['synth_b_mjd'])

def get_urls(wise_view_parameters):
    """
    Get a list of WiseView image URLs for a desired blink.

    Parameters
    ----------
        wise_view_parameters : dict
            WiseView API query parameters for requested sky location and image stretch. Can be provided by
            default_params or custom_params.

    Returns
    -------
        urls : list
            List of string URLs gathered from the WiseView API.

    """


    res = requests.get(png_anim,params=wise_view_parameters)

    # what is going on with these printouts? do we need them?
    # can they be made better?
    #print("JSON Response:")
    #print(res.json())
    #print("PNG Links:")

    urls = []
    
    
    try:
        for lnk in res.json()["ims"]:
            url = amnh_base_url + lnk
            urls.append(url)
    except KeyError:
        print('Service Error, Trying Again')
        print("JSON Response:")
        print(res.json())
        time.sleep(1)
        urls = get_urls(wise_view_parameters)
        
    

    return urls

def _download_one_png(url, outdir, fieldName):
    """
    Download one PNG image based on its URL.

    Parameters
    ----------
        url : str
            Download URL.
        outdir : str
            Output directory.

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

    r = requests.get(url)

    open(fname_dest, 'wb').write(r.content)

    return fname_dest

def gif_from_pngs(flist, gifname, duration=0.2, scale_factor=1.0):
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
    if(scale_factor != 1.0):
        for f in flist:
            im = Image.open(f)
            size = im.size
            width = size[0]
            height = size[1]
            rescaled_size = (width * scale_factor,height * scale_factor)
            resize_png(f,rescaled_size)


    images = []
    for f in flist:
        images.append(imageio.imread(f))

    imageio.mimsave(gifname, images, duration=duration)

def png_set(wise_view_parameters, outdir, scale_factor=1.0, addGrid=False, gridSize=10):
    """
    Generates a set of PNG files for the available set of data from WiseView

    Parameters
    ----------
        wise_view_parameters : dict
            WiseView API query parameters for requested sky location and image stretch. Can be provided by
            default_params or custom_params.
        outdir : str
            Output directory of the PNG files
        scale_factor : float, optional
            PNG image size scaling factor, use integer values to avoid pixel-value interpolation.
            Uses Nearest-Neighbor algorithm.
        addGrid : bool, optional
            Boolean parameter which determines whether to overlay a grid on the PNG files
        gridSize : float, optional
            Number of pixels between each line in the grid.

    Returns
    -------
        flist : list of str
            List of (full path) file names of PNG images

    Notes
    -----
        Has the functionality that if outdir doesn't currently exist, it will create it instead of previously where we
        just asserted that it existed.
    """

    if(not os.path.exists(outdir)):
        os.mkdir(outdir)

    urls = get_urls(wise_view_parameters)

    ra = wise_view_parameters['ra']
    dec = wise_view_parameters['dec']

    flist = mpScript.downloadHandler(urls, ra, dec, outdir)

    # Rescales PNGs
    if (scale_factor != 1.0):
        mpScript.scaleHandler(flist, scale_factor)
    
    #adds grid to pngs
    if (addGrid == True):
        mpScript.gridHandler(flist, gridSize)
    

    return flist


def resize_png(filename,size):
    """
       Overwrite PNG file with a particular width and height

       Parameters
       ----------
           filename : string
               Full path filename with filetype of the desired PNG file.
           size : tuple, (int,int)
               Width and height of the new PNG

       Notes
       -----
        Should PNG files be overridden or should they just be created in addition to the original PNG?

        Resampling parameter for resizing function is something that should be considered more.
        Uses Nearest Neighbor algorithm for scaling.

        Could possibly implement a keep_aspect_ratio parameter, but our images should all be squares.
    """

    im = Image.open(filename)
    resized_image = im.resize(size,Image.Resampling.NEAREST)
    resized_image.save(filename)
    return filename

def one_wv_animation(wise_view_parameters, outdir, gifname, duration=0.2, scale_factor=1.0, delete_pngs=True):
    """
    Create one WiseView animation at a desired central sky location.

    Parameters
    ----------
        wise_view_parameters : dict
            WiseView API query parameters for requested sky location and image stretch. Can be provided by
            default_params or custom_params.
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

    urls = get_urls(wise_view_parameters)

    ra = wise_view_parameters['ra']
    dec = wise_view_parameters['dec']

    flist = []
    
    for url in urls:
        fieldName='field-RA'+str(ra)+'-DEC'+str(dec)+'-'+str(counter)+'.png'
        fname_dest = _download_one_png(url, outdir, fieldName)
        flist.append(fname_dest)
        counter += 1

    gif_from_pngs(flist, gifname, duration=duration, scale_factor=scale_factor)

    if delete_pngs:
        print('Cleaning up...')
        for f in flist:
            os.remove(f)
