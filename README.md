# Flipbooks

A pipeline for downloading and modifying WiseView style unWISE flipbook images. Designed for the [Backyard Worlds: Cool Neighbors project] (Final Link here).
___

## Description

Flipbooks is a python package is built to use the [WiseView API](https://ascl.net/1806.004) in order to extract image blinks of Wide-field Infrared Survey Explorer (WISE) coadds, better 
known as the [unWISE](http://unwise.me/) catalogue. Using a default dictionary, as formatted by the WiseView API, users of flipbooks can change the values of various important 
parameters (see "Setting Parameters") which will be sent to WiseView. WiseView will use these parameters to interpret and generate a set of images on your local machine, otherwise 
known as a flipbook.
___

## Setup
Make sure Python 3.9 and above is installed on your local machine, then use python to install flipbooks via a GitHub pip install in the command line: 
```
pip install git+https://github.com/coolneighbors/flipbooks.git
```
If you are trying to modify flipbooks, or you just want to have an easily accessible local version, you can download flipbooks directly from [GitHub](https://github.com/coolneighbors/flipbooks/archive/refs/heads/master.zip).

Upon initialization of flipbooks, a local environment variable of PATH_TO_FLIPBOOKS is set with the working directory of your flipbooks repository. 

As of version 0.7, flipbooks requires the following packages: 
```
requests, PILLOW, imageio, time
```
___

### Setting Parameters
The primary file in flipbooks is wv.py (shorthand for WiseView). Most of the primary functionality associated with flipbooks can be found there. 

As such, lets learn how to use the WiseView API's parameter dictionary.

There's two ways to generate a WiseView parameter dictionary:

```
default_params()
    Get a default dictionary of WiseView API parameters.
    
custom_params(**kwargs):
    Provides a customized dictionary of WiseView API query parameters based on the provided keyword arguments. 
    All unchanged parameters are set to their default values in default_params.
```

The most important parameters to consider are:
```
ra: Right Ascension of the center of the images (float)
dec: Declination of the center of the images (float)
band: Which bands of WISE should be used, W1 is 1, W2 is 2, W1+W2 is 3. (int)
size: FOV of the image in arcseconds (float)
minbright: minimum brightness of the image (exact functionality not known yet) (float)
maxbright: maximum brightness of the image (exact functionality not known yet) (float)
```

Here is an example of how you would set your own parameters:
```
wise_view_parameters = wv.custom_params(ra=133.786245, dec=-7.244372, band=3, size=128, minbright=-50.0, maxbright=500.0)
```

For the full list of parameters, check the default_params function in wv.py.
___

### Generating a Flipbook
Inside wv.py, there are two ways to generate a flipbook:
* Generate a GIF
* Generate a set of PNG images

#### GIF Generation
For GIF generation, there are two ways of doing so:

* Use the wv.py one_wv_animation function directly
```
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
```

* Run the one_wiseview_gif.py script

How to use one_wiseview_gif.py to generate a GIF flipbook:

```
python one_wiseview_gif.py --help
usage: one_wiseview_gif.py [-h] [--outdir OUTDIR] [--minbright MINBRIGHT] [--maxbright MAXBRIGHT] [--duration DURATION] [--keep_pngs] ra dec gifname

generate one WiseView style unWISE image blink

positional arguments:
  ra                    RA in decimal degrees.
  dec                   Dec in decimal degrees.
  gifname               Name of output GIF animation file.

optional arguments:
  -h, --help            show this help message and exit
  --outdir OUTDIR       Output directory for PNGs.
  --minbright MINBRIGHT
                        Image rendering stretch lower bound.
  --maxbright MAXBRIGHT
                        image rendering stretch upper bound.
  --duration DURATION   Time in seconds per frame.
  --keep_pngs           Retain the PNGs after the GIF has been built?

Optional Usage:
Reading from CSV - In manifest.csv, put RA and DEC of objects in the RA and DEC column.
To do this, use CSVParser.py.
```

#### PNG Generation
For PNG generation, there is essentially one way to do so:
* Use the wv.py png_set function directly

```
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
```

Multiprocessing has been implemented for PNG generation but not GIF generation.
___

## Credits
Developed by members of the Backyard Worlds: Cool Neighbors team

[Aaron Meisner](http://aaronmeisner.com),
[Noah Schapera](https://www.linkedin.com/in/noah-schapera-86303a1b9/),
[Austin Humphreys](https://www.linkedin.com/in/austin-humphreys-b87055187/)

This work would not of been possible without the [WiseView API](https://ui.adsabs.harvard.edu/abs/2018ascl.soft06004C/abstract) and its creators.
___

## Citation
Please cite Backyard Worlds: Cool Neighbors if you found flipbooks useful in your research.

Please also cite WiseView, since this package fundamentally requires its backend functionality. A Bibtex entry for WiseView can be obtained from [NASA ADS](https://ui.adsabs.harvard.edu/abs/2018ascl.soft06004C/abstract).
___

## License

Copyright (c) 2022 Noah Schapera, Austin Humphreys, Aaron Meisner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
___