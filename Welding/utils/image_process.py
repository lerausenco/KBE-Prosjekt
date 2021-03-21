from PIL import Image, ImageOps
import numpy as np
import sys
import matplotlib.pyplot as plt


def open_image(filename):
    """
        args: filename where image is saved - string
        returns: image - Image
    """

    img = Image.open(filename)
    return img
    

def preprocess(img):
    """
        args: image to be preprocessed - Image
        returns: preprocessed image - numpy array
    """
    print("image size: ", img.size)
    img = img.resize((50,50), Image.ANTIALIAS) #width, height

    #add zero padding
    img = ImageOps.expand(img,border=1,fill='white')

    #convert to array
    img_array = np.array(img)

    #remove third axis by averaging out across it
    img_array = img_array.mean(axis=2)

    #tidy up grey edges
    img_array[img_array > (255*0.66)] = 255
    img_array[img_array < (255*0.66)] = 0

    new_img = Image.fromarray(img_array)
    #new_img.show()
    #print("Image array with 255s: ")
    #print(img_array)

    #normalise
    img_array = img_array/255

    #flip 0s and 1s so 1 is where wall is
    img_array = np.logical_not(img_array)

    #print("Image array with 1s: ")
    #print(img_array)

    return img_array
