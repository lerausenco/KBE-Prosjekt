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
        args: section of the matrix - sec:np.array[2x2]
        
        returns: if left edge encountered - bool
    """

    left_edge = np.array([[0,1],[0,1]])

    if np.array_equal(sec, left_edge):
        return True
    else:
        return False


def right_edge(sec):
    """ 
        args: section of the matrix - sec:np.array[2x2]
        
        returns: if right edge encountered - bool
        
    """
    right_edge = np.array([[1,0],[1,0]])

    if np.array_equal(sec, right_edge):
        return True
    else:
        return False


def is_wall(sec):
    """ 
        args: section of the matrix - sec:np.array[2x2]
        
        returns: if wall encountered - bool
        
    """

    wall = np.array([[1,1],[1,1]])

    if np.array_equal(sec, wall):
        return True
    else:
        return False


def bottom_edge(sec):
    """ 
        args: section of the matrix - sec:np.array[2x2]
        
        returns: if bottom_edge encountered - bool
        
    """
    bottom_edge = np.array([[1,1], [0,0]])

    if np.array_equal(sec, bottom_edge):
        return True
    else:
        return False


def top_edge(sec):
    """ 
        args: section of the matrix - sec:np.array[2x2]
        
        returns: if top_edge encountered - bool
        
    """
    top_edge = np.array([[0,0], [1,1]])

    if np.array_equal(sec, top_edge):
        return True
    else:
        return False


def extract_walls(img_array):

    wall_th = 2
    length = 0
    row = 0
    col = 0

    wall_list = []

    for row in range(img_array.shape[0]):
        for col in  range(img_array.shape[1]):
            
            sec = img_array.astype(int)[row:row+2,col:col+2]
            #print(sec)
            if left_edge(sec):
                #move filter one step to the right
                next_sec = img_array.astype(int)[row:row+2, col+1:col+3]
                next_next_sec = img_array.astype(int)[row:row+2, col+2:col+4]
                #check if wall
                if is_wall(next_sec) and not right_edge(next_next_sec): #horizontal
                    #record corner coordinates
                    x = col +1
                    y = row
                    while is_wall(next_sec):
                    #start counting length across, until right edge found
                        length +=1
                        col +=1
                        next_sec = img_array.astype(int)[row:row+2, col:col+2]
                    new_wall = Wall(x,y,length,wall_th)
                    wall_list.append(new_wall)
                    length = 0


    for col in range(img_array.shape[1]):
        for row in range(img_array.shape[0]):

            sec = img_array.astype(int)[row:row+2,col:col+2]
            
            if top_edge(sec): 
                next_sec = img_array.astype(int)[row+1:row+3, col:col+2]
                next_next_sec = img_array.astype(int)[row+2:row+4, col:col+2]

                if is_wall(next_sec) and is_wall(next_next_sec):
                    x = col
                    y = row
                    while is_wall(next_sec):
                        length += 1
                        row += 1
                        next_sec = img_array.astype(int)[row:row+2, col:col+2]
                    
                    new_wall = Wall(x,y,wall_th,length)
                    wall_list.append(new_wall)
                    length = 0

    return wall_list

