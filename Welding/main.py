import numpy as np
from image_process import open_image, preprocess
from Wall import Wall
from wall_extraction import extract_walls
#printing options for debugging
np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=180)

img = open_image('img/maze.png')
img_array = preprocess(img)

wall_list = extract_walls(img_array)


for wall in wall_list:
    wall.print()