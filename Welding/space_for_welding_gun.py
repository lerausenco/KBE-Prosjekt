from utils.image_process import open_image, preprocess
import numpy as np
import copy

def find_space_for_welder(array,length,width): #,diameter
    row = 0
  #  print("First row", array[row,:])
  #  print("First coloumn", array[:,0])
  #  print("number of couloumns ", len(array[row,:]))
  #  print("number of rows  ", len(array[:,0]))
  #  print(array.shape[1])

    a = diameter


    coords = copy.deepcopy(array)
    x = np.linspace(0, width, num=coords.shape[0])
    y = np.linspace(0,length, num=coords.shape[1])
    
    
    print("x: ", x)
    print("y: ", y)
    #temp_coord = np.array( [0, 0] )
    #coords.tolist()
    print(coords)
    
    #sec[2,2] = [ x[2], y[2] ]
    #print(coords[2,2])
    for row in range(coords.shape[0]):
        for col in  range(coords.shape[1]):
            sec = coords.astype(int)[row:row+2,col:col+2]
            sec[row,col] = [ x[col], y[row] ]
            #coords
    print(coords)
    return coords

