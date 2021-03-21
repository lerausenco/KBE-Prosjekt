from utils.image_process import open_image, preprocess
import cv2
import numpy as np
import copy

def find_space_for_welder(img_array,model_height,model_length, wall_height ,gun_diam, gun_length):

  """
      Checks if maze is weldable.
      args:
          img_array [numpy array] - image containing geometry in img_array form
          model__height [int] - height of model as shown on UI in m
          model_length [int] - length of model as shown on UI in m
          wall_height [int] - height of walls to weld in m
          gun_diam: [int] - diameter of welding gun in mm
          gun_length: [int] - length of welding gun in mm 
      returns:
          feedback_array [numpy array]
  """
  #mm and m conversion
  if wall_height > gun_length:
      return None

  coords = copy.deepcopy(img_array)
   

    #convert welding gun size to pixel size
  d_pixels_x = int((gun_diam/1000)/model_length * img_array.shape[0])
  d_pixels_y = int((gun_diam/1000)/model_height * img_array.shape[1])
  print("gun size", d_pixels_x, " ", d_pixels_y)
  #d_pixels_x = 5
  #d_pixels_y = 5
  #d_pixels = 3
  if d_pixels_x == 0:
    d_pixels_x = 1
  if d_pixels_y == 0:
    d_pixels_y = 1
    #make check array
  gun_array = np.zeros((d_pixels_y,d_pixels_x))
    
  feedback_array = np.zeros(img_array.shape)
  
  for i in range(d_pixels_x):
      #start scanning from 0th...d_pixeles'th index in array
    print("I", i)  
    for row in range(i, coords.shape[0]-d_pixels_y, d_pixels_y):
        for col in  range(coords.shape[1]-d_pixels_x):
            sec = coords.astype(int)[row:row+d_pixels_y,col:col+d_pixels_x]

            if np.array_equal(sec,gun_array):
              #mark section as ok
              feedback_array[row:row+d_pixels_y, col:col+d_pixels_x] = np.ones((d_pixels_y, d_pixels_x)) 
              

  return feedback_array
    
  
"""
  for i in range(d_pixels_y):
    for col in range(i, coords.shape[1]-d_pixels_x, d_pixels_x):
      for row in range(coords.shape[0]-d_pixels_y):
      
        sec = coords.astype(int)[row:row+d_pixels_y,col:col+d_pixels_x]
        
        if np.array_equal(sec,gun_array):
          #mark section as ok
          feedback_array[row:row+d_pixels_y, col:col+d_pixels_x] = np.ones((d_pixels_y, d_pixels_x))   

  
 
  return feedback_array
          """