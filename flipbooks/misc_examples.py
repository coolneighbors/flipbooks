from flipbooks import WiseViewQuery

def wise0855():
    
  ra = 133.786245
  dec = -7.244372

  outdir = 'w0855'
  gifname = 'w0855.gif'
  wise_view_query = WiseViewQuery.WiseViewQuery(ra=ra,dec=dec)
  wise_view_query.createWiseViewGIF(outdir, gifname)

def w1930():

  # byw example at ~1.5 asec/yr
  ra = 292.725665
  dec = -20.998843

  outdir = 'w1930'
  gifname = 'w1930.gif'

  wise_view_query = WiseViewQuery.WiseViewQuery(ra=ra, dec=dec, minbright=-12.5, maxbright=125)
  wise_view_query.createWiseViewGIF(outdir, gifname)

def w2243():

  # byw example at ~0.5+ asec/yr
  ra = 340.8321592 
  dec = -14.9839027

  outdir = 'w2243'
  gifname = 'w2243.gif'

  wise_view_query = WiseViewQuery.WiseViewQuery(ra=ra, dec=dec, minbright=-12.5, maxbright=125)
  wise_view_query.createWiseViewGIF(outdir, gifname)

def w1553():

    # byw example showing blending

    ra = 238.44587574
    dec = 69.56790675

    outdir = 'w1553'
    gifname = 'w1553.gif'

    wise_view_query = WiseViewQuery.WiseViewQuery(ra=ra, dec=dec, minbright=-12.5, maxbright=125)
    wise_view_query.createWiseViewGIF(outdir, gifname)

def j0002():

    # melina's wd companion in the galactic plane

    ra = 0.6225026
    dec = 63.8712344

    outdir = 'w0002'
    gifname = 'w0002.gif'

    wise_view_query = WiseViewQuery.WiseViewQuery(ra=ra, dec=dec, minbright=-12.5, maxbright=125)
    wise_view_query.createWiseViewGIF(outdir, gifname)

def j1936():
    # maybe a better crowded field example...

    ra = 294.233532
    dec = 4.134037

    outdir = 'w1936'
    gifname = 'w1936.gif'

    wise_view_query = WiseViewQuery.WiseViewQuery(ra=ra, dec=dec, minbright=-12.5, maxbright=125)
    wise_view_query.createWiseViewGIF(outdir, gifname)

def _ghost():
    

    ra = 12.4397
    dec = -13.5258

    outdir = 'ghost'
    gifname = 'ghost.gif'

    wise_view_query = WiseViewQuery.WiseViewQuery(ra=ra, dec=dec, minbright=-12.5, maxbright=125)
    wise_view_query.createWiseViewGIF(outdir, gifname)

def _diff_spike():

    ra = 34.2739
    dec = -4.1872

    outdir = 'diff_spike'
    gifname = 'diffraction_spike.gif'

    wise_view_query = WiseViewQuery.WiseViewQuery(ra=ra, dec=dec, minbright=-12.5, maxbright=125)
    wise_view_query.createWiseViewGIF(outdir, gifname)
