import requests
import os

png_anim = "https://vjxontvb73.execute-api.us-west-2.amazonaws.com/png-animation"
amnh_base_url = "https://amnh-citsci-public.s3-us-west-2.amazonaws.com/"

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

def get_radec_urls(ra, dec, minbright=None, maxbright=None):
    params = custom_params(ra, dec, minbright=minbright, maxbright=maxbright)

    res = requests.get(png_anim,params=params)
    print("JSON Response:")
    print(res.json())
    print("PNG Links:")
    urls = []
    for lnk in res.json()["ims"]:
        url = amnh_base_url + lnk
        urls.append(url)

    return urls

def _download_one_png(url, outdir):
    # url here should be just a string, not an array or list of strings

    fname = os.path.basename(url)
    fname_dest = os.path.join(outdir, fname)

    r = requests.get(url)

    open(fname_dest, 'wb').write(r.content)

    return fname_dest

def gif_from_pngs(flist, gifname, duration=0.2):

    import imageio

    # add checks on whether the files in flist actually exist?

    images = []
    for f in flist:
        images.append(imageio.imread(f))

    imageio.mimsave(gifname, images, duration=duration)

def one_wv_animation(ra, dec, outdir, gifname, minbright=None,
                     maxbright=None, duration=0.2):

    assert(os.path.exists(outdir))

    urls = get_radec_urls(ra, dec, minbright=None, maxbright=None)

    flist = []
    for url in urls:
        fname_dest = _download_one_png(url, outdir)
        flist.append(fname_dest)

    gif_from_pngs(flist, gifname, duration=duration)
