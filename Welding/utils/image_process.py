from PIL import Image, ImageOps
import numpy as np
import sys
import matplotlib.pyplot as plt
import cv2

scaling = 0.125

def open_image(filename):
    """
        args: filename where image is saved - string
        returns: image - Image
    """

    img = Image.open(filename)
    return img
    

def preprocess(img):
    """
        Preprocesses image.
        args: 
            img [Image] - image to be preprocessed 
        returns: 
            img_array [numpy array] - preprocessed image
    """
    print("image size: ", img.size)
   
    img = img.resize((int(img.size[0]*scaling),int(img.size[1]*scaling)), Image.ANTIALIAS) #width, height

    print("image size:", img.size)
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

    #normalise
    img_array = img_array/255

    #flip 0s and 1s so 1 is where wall is
    img_array = np.logical_not(img_array)

    #print("Image array with 1s: ")
    #print(img_array)

    return img_array

def make_feedback(feedback_array, img):
    """
        Creates and saves feedback array to file.
        args:
            feedback_array [numpy array] - array stating which areas are weldable and not
            img [numpy array] - original image array with walls
        returns:
            None
    """


    #define RGB colours to process feedback array
    red   = [0,0,255]
    green = [0,255,0]


    #flip back the processed image
    img = np.logical_not(img)

    #save it
    cv2.imwrite('img/temp/maze_pic.jpg', img*255)

    #read it again
    maze = cv2.imread('img/temp/maze_pic.jpg')

    #save the feedback array as an image
    feedback_array = feedback_array * 255
    cv2.imwrite('img/temp/feedback_array.jpg', feedback_array)

    #read it 
    im = cv2.imread('img/temp/feedback_array.jpg')
    
    #everything below 10 is black, everything above 200 is white
    im[np.all(im<(10,10,10), axis=-1)] = [0,0,0]
    im[np.all(im >(200,200,200), axis =-1)] = [255,255,255]

    #all white pixels are green, all black pixels are red
    im[np.all(im==(255,255,255), axis=-1)] = green
    im[np.all(im==(0,0,0), axis=-1)] = red


    #combine maze picture and red/green feedback picture
    overlay = maze.copy()
    combined_pic = maze.copy()
    
    cv2.addWeighted(im, 0.7, maze, 0.3, 0.3, combined_pic)    
   
    #make walls black again
    combined_pic[np.all(combined_pic<(10,10,190), axis=-1)] = [0,0,0]
    
    combined_pic = cv2.resize(combined_pic, None, fx=8,fy=8, interpolation=cv2.INTER_LINEAR)
    cv2.imwrite("img/customer_feedback.png", combined_pic)


    



