from PIL import Image, ImageOps
import numpy as np
import sys
import matplotlib.pyplot as plt
#printing options for debugging
np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=180)




img = Image.open('maze.png')

img = img.resize((50,38), Image.ANTIALIAS) #width, height

#pad the image
img = ImageOps.expand(img,border=2,fill='white')

#convert to array
img_array = np.array(img)

#remove third axis by averaging out across it
img_array = img_array.mean(axis=2)

#tidy up grey edges
img_array[img_array > (255*0.66)] = 255
img_array[img_array < (255*0.66)] = 0

new_img = Image.fromarray(img_array)
new_img.show()
#plt.imshow(img_array)

#normalise
img_array = img_array/255
print(img_array)
#print(img_array.shape[1])

#for col in range(img_array.shape[1]):
