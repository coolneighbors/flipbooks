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
def rescale(file_path, scale_factor, allow_non_integer_scaling = False):
    with Image.open(file_path) as im:
        size = im.size
        width = size[0]
        height = size[1]

        if(not allow_non_integer_scaling):
            if(type(scale_factor) != int and scale_factor != int(scale_factor)):
                raise ValueError("Scale factor must be an integer if allow_non_integer_scaling is False.")

        rescaled_size = (int(width * scale_factor), int(height * scale_factor))

        resizeImage(file_path, rescaled_size)

def resizeImage(file_path, size):
    """
       Overwrite PNG file with a particular width and height

       Parameters
       ----------
           file_path : string
               Full path filename with filetype of the desired PNG file.
           size : tuple, (int, int)
               Width and height of the new PNG

       Notes
       -----
        Should PNG files be overridden or should they just be created in addition to the original PNG?

        Resampling parameter for resizing function is something that should be considered more.
        Uses Nearest Neighbor algorithm for scaling.

        Could possibly implement a keep_aspect_ratio parameter, but our images should all be squares.
    """
    with Image.open(file_path) as im:
        resized_image = im.resize(size, Image.Resampling.NEAREST)
        resized_image.save(file_path)
    return file_path

def applyGrid(file_path, grid_count = 12, grid_type = "Solid", color = (0,0,0)):
    """

    Post-processing shader that adds a grid to an image.


    Parameters
    ----------
    file_path : str
        image filename.
    grid_count : TYPE, optional
        The number of grid boxes to generate along each axis.

    Returns
    -------
    None.

    """

    with Image.open(file_path) as image:
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

        image.save(file_path)

def earlyTerminationProtocol(flist):
    print("Early termination protocol initiated. Deleting unfinished files.")
    for f in flist:
        if (os.path.exists(f)):
            os.remove(f)

def applyModificationFunctions(f, functions, function_args):

    for i in range(len(functions)):
        try:
            functions[i](f, *function_args[i])
        except Exception as e:
            print("Exception of type " + str(type(e)) + f" occurred in function '{functions[i].__name__}': " + str(e))
            return

def applyModifications(flist, functions, function_args):
    for f in flist:
        if not os.path.exists(f):
            print(f"File {f} does not exist. Exiting.")
            return

    try:
        pool = mp.Pool()
        file_processes = [pool.apply_async(applyModificationFunctions, args=(f, functions, function_args)) for f in flist]
        pool.close()
        pool.join()
    except Exception as e:
        print("Exception of type " + str(type(e)) + " occurred in applyModifications: " + str(e))
        earlyTerminationProtocol(flist)

# Post-processing functions to be used in the applyModifications function
def scaleImage(f, scale_factor, allow_non_integer_scaling=False):
    if(scale_factor != 1 and scale_factor > 0):
        rescale(f, scale_factor, allow_non_integer_scaling)

def applyGridToImage(f, addGrid, gridCount, gridType, gridColor):
    if(addGrid):
        applyGrid(f, gridCount, gridType, gridColor)



