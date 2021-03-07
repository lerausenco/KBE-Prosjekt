import numpy as np
from image_process import open_image, preprocess
from Wall import Wall
#from wall_extraction import extract_walls
from CV_extract import extract_walls
#from Shapes.Block import Block
#printing options for debugging
np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=180)

img = open_image('img/maze.png')
img_array = preprocess(img)
print(img_array.astype(int))
#wall_list = extract_walls(img_array)
wall_list = extract_walls()


scaling_fac = 10
f = open("param_vals.txt", "a")

for wall in wall_list:
    f.write(str(wall.params()) + "\n")