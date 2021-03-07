#from PIL import Image, ImageOps
import numpy as np
#import sys
#import matplotlib.pyplot as plt

#printing options for debugging
#np.set_printoptions(threshold=np.inf)
#np.set_printoptions(linewidth=180)

from Wall import Wall


def left_edge(sec):
    """ 
        args: 
            sec (np.array[2x2]) - section of the matrix 
        returns: 
            bool - True if left edge encountered
    """

    left_edge = np.array([  [0,1],
                            [0,1]])

    if np.array_equal(sec, left_edge):
        return True
    else:
        return False


def right_edge(sec):
    """ 
        args: 
            sec (np.array[2x2]) - section of the matrix 
        returns: 
            bool - True if right edge encountered
        
    """
    right_edge = np.array([ [1,0],
                            [1,0]])

    if np.array_equal(sec, right_edge):
        return True
    else:
        return False


def is_wall(sec):
    """ 
        args: 
            sec (np.array[2x2]) - section of the matrix 
        returns: 
            bool - True if wall encountered
        
    """

    wall = np.array([[1,1],[1,1]])

    if np.array_equal(sec, wall):
        return True
    else:
        return False


def bottom_edge(sec):
    """ 
        args: 
            sec (np.array[2x2]) - section of the matrix 
        returns: 
            bool - True if bottom edge encountered
        
    """
    bottom_edge = np.array([    [1,1], 
                                [0,0]])

    if np.array_equal(sec, bottom_edge):
        return True
    else:
        return False


def top_edge(sec):
    """ 
        args: 
            sec (np.array[2x2]) - section of the matrix 
        returns: 
            bool - True if top edge encountered
        
    """
    top_edge = np.array([   [0,0], 
                            [1,1]])

    if np.array_equal(sec, top_edge):
        return True
    else:
        return False


def extract_walls(img_array):

    """
        Finds walls in an image and makes a list of them.
        args:
            img_array (numpy array) - normalised numpy array storing image
        returns:
            wall_list (list<Wall>) - list of Wall objects 
   """

    wall_th = 2
    length = 0
    #row = 0
    #col = 0

    wall_list = []

    #check for horizontal walls first
    for row in range(img_array.shape[0]):
        for col in  range(img_array.shape[1]):
            
            sec = img_array.astype(int)[row:row+2,col:col+2]
            
            if left_edge(sec):
                #check two steps to the right
                next_sec = img_array.astype(int)[row:row+2, col+1:col+3]
                next_next_sec = img_array.astype(int)[row:row+2, col+2:col+4]

                #if horizontal wall, get coordinates and count length
                if is_wall(next_sec) and not right_edge(next_next_sec): 
                    #record corner coordinates
                    x = col +1
                    y = row
                    while is_wall(next_sec):
                    #start counting length across, until right edge found
                        length +=1
                        col +=1
                        next_sec = img_array.astype(int)[row:row+2, col:col+2]
                    #create wall object and store in list    
                    new_wall = Wall(x,y,length,wall_th)
                    wall_list.append(new_wall)
                    length = 0

    #check for vertical walls
    for col in range(img_array.shape[1]):
        for row in range(img_array.shape[0]):

            sec = img_array.astype(int)[row:row+2,col:col+2]
            
            if top_edge(sec): 
                #check two steps below
                next_sec = img_array.astype(int)[row+1:row+3, col:col+2]
                next_next_sec = img_array.astype(int)[row+2:row+4, col:col+2]

                #if vertical wall, get coordinates and count length
                if is_wall(next_sec) and is_wall(next_next_sec):
                    x = col
                    y = row
                    while is_wall(next_sec):
                    #start counting length downwards, until bottom edge found
                        length += 1
                        row += 1
                        next_sec = img_array.astype(int)[row:row+2, col:col+2]
                    #create wall object and store in list
                    new_wall = Wall(x,y,wall_th,length)
                    wall_list.append(new_wall)
                    length = 0

    return wall_list

