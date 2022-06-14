#!/usr/bin/env python

from flipbooks.wv import one_wv_animation, custom_params
import argparse

if __name__=="__main__":
    descr = 'generate one WiseView style unWISE image blink'

    parser = argparse.ArgumentParser(description=descr)

    parser.add_argument('ra', type=float, nargs=1,
                        help="RA in decimal degrees.")

    parser.add_argument('dec', type=float, nargs=1,
                        help="Dec in decimal degrees.")

    parser.add_argument('gifname', type=str,
                        help="Name of output GIF animation file.")

    parser.add_argument('--outdir', type=str, default='.',
                        help="Output directory for PNGs.")

    parser.add_argument('--minbright', type=float, default=-12.5,
                        help="Image rendering stretch lower bound.")

    parser.add_argument('--maxbright', type=float, default=125.0,
                        help="image rendering stretch upper bound.")

    parser.add_argument('--duration', type=float, default=0.2,
                        help="Time in seconds per frame.")

    parser.add_argument('--keep_pngs', default=False,
                        action='store_true',
                        help="Retain the PNGs after the GIF has been built?")

    args = parser.parse_args()
    wise_view_parameters = custom_params(ra=args.ra[0],dec=args.dec[0],minbright=args.minbright,maxbright=args.maxbright)
    one_wv_animation(wise_view_parameters, args.outdir, args.gifname, duration=args.duration, delete_pngs=(not args.keep_pngs))
