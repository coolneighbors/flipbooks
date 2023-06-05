# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 15:15:09 2022

Multiprocessing additions on Fri Jun 10 14:53:00 2022

Save state modifcations on Thurs Jun 1 16:27:00 2023

@author: Noah Schapera, Austin Humphreys
"""

from PIL import Image, ImageDraw
import multiprocessing as mp
import os




#rescales pngs
def rescale(f,scale_factor):
    with Image.open(f) as im:
        size = im.size
        width = size[0]
        height = size[1]
        rescaled_size = (width * scale_factor, height * scale_factor)
        resize_png(f, rescaled_size)


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
    with Image.open(filename) as im:
        resized_image = im.resize(size,Image.Resampling.NEAREST)
        resized_image.save(filename)
    return filename

def applyGrid(imname, grid_count = 12, grid_type = "Solid", color = (0,0,0)):
    """

    Post processing "shader" that adds a grid to an image.


    Parameters
    ----------
    imname : TYPE
        image filename.
    grid_count : TYPE, optional
        The number of grid boxes to generate along each axis.

    Returns
    -------
    None.

    """

    with Image.open(imname) as image:
        draw = ImageDraw.Draw(image)
        grid_side_length = int((image.width - (grid_count + 1)) / (grid_count))
        step_size = grid_side_length + 1
        offset = int((image.width % ((grid_side_length * grid_count) + (grid_count+1))) / 2)
        if(grid_type == "Solid"):
            for x in range(0, image.width, step_size):
                line = ((x + offset, 0), (x + offset, image.height))
                draw.line(line, fill=color)

            for y in range(0, image.height, step_size):
                line = ((0, y + offset), (image.width, y + offset))
                draw.line(line, fill=color)

        elif(grid_type == "Intersection"):
            for x in range(0, image.width+1, step_size):
                for y in range(0, image.height+1, step_size):
                    cross_size = 10
                    intersection_coordinate = (x + offset, y + offset)
                    intersection_x, intersection_y = intersection_coordinate
                    horizontal_line = ((intersection_x - cross_size, intersection_y), (intersection_x + cross_size, intersection_y))
                    vertical_line = ((intersection_x, intersection_y - cross_size), (intersection_x, intersection_y + cross_size))
                    draw.line(horizontal_line, fill=color)
                    draw.line(vertical_line, fill=color)

        elif(grid_type == "Dashed"):
            reduced_width = image.width - (grid_count + 1)
            dashes_per_grid_side = 5
            dash_spacing = 20
            dash_length = int((((reduced_width/grid_count)+2)-(dashes_per_grid_side-1)*dash_spacing)/dashes_per_grid_side)
            for x in range(0, image.width, step_size):
                for y in range(0, image.height, dash_length+dash_spacing):
                    line = ((x + offset, y + offset), (x + offset, y + offset + dash_length))
                    draw.line(line, fill=color)

            for y in range(0, image.height, step_size):
                for x in range(0, image.width, dash_length+dash_spacing):
                    line = ((x + offset, y + offset), (x + offset + dash_length, y + offset))
                    draw.line(line, fill=color)
        else:
            raise TypeError(f"Invalid Grid type: {grid_type}. Should be Solid, Intersection, or Dashed.")

        del draw

        image.save(imname)

def earlyTerminationProtocol(flist):
    print("Early termination protocol initiated. Deleting unfinished files.")
    for f in flist:
        os.remove(f)

def applyPNGModifications(flist, scale_factor, addGrid, gridCount, gridType, gridColor):
    try:
        pool = mp.Pool()
        processes = [pool.apply_async(scalePNGsAndApplyGrid, args=(f, scale_factor, addGrid, gridCount, gridType, gridColor)) for f in flist]
        # Wait for processes to complete so that the files are saved before the next step
        pool.close()
        pool.join()
    except Exception as e:
        earlyTerminationProtocol(flist)


def scalePNGsAndApplyGrid(f, scale_factor, addGrid, gridCount, gridType, gridColor):
    if(scale_factor != 1):
        rescale(f, scale_factor)
    if(addGrid):
        applyGrid(f, gridCount, gridType, gridColor)

