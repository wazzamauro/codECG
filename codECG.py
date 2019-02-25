import numpy as np
from PIL import Image
import tkinter
import tkinter.filedialog
from pdf2image import convert_from_path
import os
import ast

#
# Step to get the pdf or ecg file from dialog window
#
root = tkinter.Tk()
root.withdraw()
file_path = tkinter.filedialog.askopenfilename()
dir_path = os.path.dirname(os.path.realpath(file_path))

#
# Condition to recognize pdf or ecg file
#

# If pdf selected
if file_path.endswith(".pdf"):

    print ("You choose a pdf file, i'm working..")

    # conversion from pdf to image
    pages = convert_from_path(file_path)
    png = ""
    for page in pages:
        png = page

    # Crop of ecg area
    areaTOT = (39, 314, 1614, 2204)
    png = png.crop(areaTOT)

    # Create the pixel map
    pixels = png.load()

    # Changing the pixel value in black or white
    # For every pixel in map:
    for i in range(png.size[0]):
        for j in range(png.size[1]):
            if pixels[i,j] > (90, 90, 90):
                pixels[i,j] = (255, 255, 255)
            else:
                pixels[i, j] = (0, 0, 0)

    # Creating numpy array with coordinates of non-white pixels
    arr = np.asarray(png)
    black_pixels = np.array(np.where(arr != 255))
    black_pixel_coordinates = list(zip(black_pixels[0], black_pixels[1]))

    # Creating the output file with codified ecg in it
    file = open(dir_path + os.path.sep + "codified_ecg.ecg", "w")
    file.write( str(black_pixel_coordinates) )
    file.close()

    print ("End of pdf process transformation, check for a ecg file.")

# If ecg selected
elif file_path.endswith(".ecg"):

    print ("You choose a ecg file, i'm working..")

    # Getting the string in ecg file
    p = file_path
    data = []
    with open(p, "r") as f:
        for i in f.readlines():
            data.append(ast.literal_eval(i.strip()))

    # Transform the string in numpy array
    data = np.array(data)
    data = data[0]

    # Getting the max values in the array
    size =  np.amax(data, axis=0)
    width = size[0]
    height = size[1]

    # Removing duplicate pixels coordinates
    data = np.unique(data, axis=0)

    # Create a new white image
    img = Image.new('RGB', (height+1, width+1), color=(255, 255, 255))

    # Set the black pixels by coordinates
    for i in data:
        img.putpixel((i[1], i[0]), (0,0,0))
    img.save(dir_path + os.path.sep + "ecg_from_kardia.png")

    print ("End of ecg process transformation, check for a png file.")
