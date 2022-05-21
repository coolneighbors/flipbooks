import requests

png_anim = "https://vjxontvb73.execute-api.us-west-2.amazonaws.com/png-animation"
import os
import imageio

def default_params():
    params = {
        "ra": 133.786245,
        "dec": -7.244372,
        "band": 3,
        "size": 64,
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

def custom_params(ra, dec, minbright=None, maxbright=None):

    params = default_params()
    params['ra'] = ra
    params['dec'] = dec
    if minbright is not None:
        params['minbright'] = minbright
    if maxbright is not None:
        params['maxbright'] = maxbright

    return params

def get_radec_pngs(ra, dec, outdir, gifname, minbright=None, maxbright=None):

    assert(os.path.exists(outdir))

    params = custom_params(ra, dec, minbright=minbright, maxbright=maxbright)

    res = requests.get(png_anim,params=params)
    print("JSON Response:")
    print(res.json())
    print("PNG Links:")
    urls = []
    for lnk in res.json()["ims"]:
        url = "https://amnh-citsci-public.s3-us-west-2.amazonaws.com/"+lnk
        urls.append(url)

    print(urls)
    flist = []
    for url in urls:
        cmd = 'wget ' + url
        print(cmd)
        os.system('wget ' + url)
        fname = os.path.basename(url)
        fname_dest = os.path.join(outdir, fname)
        os.rename(fname, fname_dest)
        flist.append(fname_dest)

    images = []
    for f in flist:
        images.append(imageio.imread(f))

    imageio.mimsave(gifname, images, duration=0.2)

def wise0855():
    
  ra = 133.786245
  dec = -7.244372

  outdir = 'w0855'
  gifname = 'w0855.gif'
  get_radec_pngs(ra, dec, outdir, gifname)

def w1930():

  # byw example at ~1.5 asec/yr
  ra = 292.725665
  dec = -20.998843

  outdir = 'w1930'
  gifname = 'w1930.gif'

  get_radec_pngs(ra, dec, outdir, gifname, minbright=-12.5, maxbright=125)

def w2243():

  # byw example at ~0.5+ asec/yr
  ra = 340.8321592 
  dec = -14.9839027

  outdir = 'w2243'
  gifname = 'w2243.gif'

  get_radec_pngs(ra, dec, outdir, gifname, minbright=-12.5, maxbright=125)

def w1553():

    # byw example showing blending

    ra = 238.44587574
    dec = 69.56790675

    outdir = 'w1553'
    gifname = 'w1553.gif'

    get_radec_pngs(ra, dec, outdir, gifname, minbright=-12.5, maxbright=125)

def j0002():

    # melina's wd companion in the galactic plane

    ra = 0.6225026
    dec = 63.8712344

    outdir = 'w0002'
    gifname = 'w0002.gif'

    get_radec_pngs(ra, dec, outdir, gifname, minbright=-12.5, maxbright=125)

def j1936():
    # maybe a better crowded field example...

    ra = 294.233532
    dec = 4.134037

    outdir = 'w1936'
    gifname = 'w1936.gif'

    get_radec_pngs(ra, dec, outdir, gifname, minbright=-12.5, maxbright=125)

def _ghost():
    

    ra = 12.4397
    dec = -13.5258

    outdir = 'ghost'
    gifname = 'ghost.gif'

    get_radec_pngs(ra, dec, outdir, gifname, minbright=-12.5, maxbright=125)

def _diff_spike():

    ra = 34.2739
    dec = -4.1872

    outdir = 'diff_spike'
    gifname = 'diffraction_spike.gif'

    get_radec_pngs(ra, dec, outdir, gifname, minbright=-12.5, maxbright=125)
