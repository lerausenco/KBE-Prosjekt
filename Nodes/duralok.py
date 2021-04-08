from shapes.Block import Block
from shapes.Cylinder import Cylinder
from shapes.Cone import Cone
from utils.Analyzer import Analyzer
from datetime import datetime
import math
from math import sin, cos, radians
import time
import random

parts_list = []

pipe_diam = 40
lock_th = pipe_diam/10



#TOP CONE
top_cone = Cone(
    x=0,y=0,z=pipe_diam/2+lock_th, 
    baseDiameter=lock_th*6+pipe_diam,
    topDiameter=pipe_diam+2*lock_th,
    height=pipe_diam/2,
    direction= [0,0,1],
    color="BLUE",
    material="Steel") 

parts_list.append(top_cone)

hollow_top_cone = Cylinder(
    x=top_cone.x,y=top_cone.y,z=top_cone.z,
    diameter=pipe_diam,
    height=top_cone.height*2,
    direction=[0,0,1],
    color="GRAY",
    material="STEEL"
)
parts_list.append(hollow_top_cone)



#TOP CYL
top_cyl = Cylinder(
    x=0,y=0,z=top_cone.z+top_cone.height,
    diameter=top_cone.topDiameter,
    height=pipe_diam/2,
    direction=[0,0,1],
    color="BLUE",
    material="Steel"
)

parts_list.append(top_cyl)

hollow_top_cyl = Cylinder(
    x=top_cyl.x,y=top_cyl.y,z=top_cyl.z,
    diameter=pipe_diam,
    height=top_cyl.height,
    direction=[0,0,1],
    color="GRAY",
    material="STEEL"
)
parts_list.append(hollow_top_cyl)


side_stiff_width = (top_cone.baseDiameter - top_cone.topDiameter)/2
w = side_stiff_width

for i in range(6):
    y = cos(radians(i*60))*(top_cone.baseDiameter-w)/2 
    x = sin(radians(i*60))*(top_cone.baseDiameter-w)/2

    side_cyl = Cylinder(
        x=x, y=y, z=top_cone.z,
        diameter=w,
        height=top_cone.height,
        color="BLUE",
        material="Steel",
        direction=[0,0,1]
    )
    parts_list.append(side_cyl)


#bottom cone 1
bottom_cone1 = Cone(
    x=0,y=0,z=-top_cone.z,
    baseDiameter=top_cone.baseDiameter,
    topDiameter=top_cone.baseDiameter*0.85,
    height=8,
    direction=[0,0,-1],
    color="BLUE",
    material="STEEL",
)

parts_list.append(bottom_cone1)

hollow_bottom_cone1 = Cylinder(
    x=0,y=0,z=bottom_cone1.z,
    diameter=pipe_diam,
    height=bottom_cone1.height,
    direction=bottom_cone1.direction,
    color="GREY",
    material="STEEL"
)
parts_list.append(hollow_bottom_cone1)


#bottom cone 2

bottom_cone2 = Cone(
    x=0,y=0,z=-top_cone.z-bottom_cone1.height,
    baseDiameter=bottom_cone1.topDiameter,
    topDiameter=pipe_diam+2*lock_th,
    height=15,
    direction=[0,0,-1],
    color="BLUE",
    material="STEEL"
)

parts_list.append(bottom_cone2)

hollow_bottom_cone2 = Cylinder(
    x=0,y=0,z=bottom_cone2.z,
    diameter=pipe_diam,
    height=bottom_cone2.height,
    direction=bottom_cone2.direction,
    color="GREY",
    material="STEEL"
)
parts_list.append(hollow_bottom_cone2)


space_between_cones = top_cone.z - bottom_cone1.z



#hollow through other crossing cyl
hollow_cross_2 = Cylinder(
    x = top_cone.x, y=top_cone.y, z=top_cone.z,
    diameter=pipe_diam,
    height=space_between_cones,
    direction=[0,0,-1],
    color="GREY",
    material="STEEL"
)

parts_list.append(hollow_cross_2)


#outer cylinder part of the construction
middle_cyl = Cylinder(
    x=0,y=0,z=bottom_cone1.z,
    diameter=bottom_cone1.baseDiameter,
    height=space_between_cones,
    direction=[0,0,1],
    color="YELLOW",
    material="STEEL"
)
parts_list.append(middle_cyl)

#hollow through middle cylinder
hollow_middle_cyl = Cylinder(
    x=0,y=0,z=middle_cyl.z,
    diameter=pipe_diam,
    height=middle_cyl.height,
    direction=middle_cyl.direction,
    color="GRAY",
    material="STEEL"
)
parts_list.append(hollow_middle_cyl)


side_opening_1 = Cylinder(
    x=-top_cone.baseDiameter/2, y=0, z = 0,
    diameter=pipe_diam+2*lock_th,
    height=top_cone.baseDiameter,
    direction=[1,0,0],
    color="YELLOW",
    material="STEEL"
)

parts_list.append(side_opening_1)


#hollow through crossing tubes
hollow_cross_1 = Cylinder(
    x = top_cone.x, y=top_cone.y, z=top_cone.z,
    diameter=pipe_diam,
    height=space_between_cones,
    direction=[0,0,-1],
    color="GREY",
    material="STEEL"
)

parts_list.append(hollow_cross_1)


#FOR SUBTRACTION
side_pipe_1 = Cylinder(
    x=-top_cone.baseDiameter/2-lock_th, y=0, z = 0,
    diameter=pipe_diam,
    height=top_cone.baseDiameter+2*lock_th,
    direction=[1,0,0],
    color="YELLOW",
    material="STEEL"
)

parts_list.append(side_pipe_1)


# more copies to perform subtraction
side_pipe_1_1 = Cylinder(
    x=-top_cone.baseDiameter/2, y=0, z = 0,
    diameter=pipe_diam,
    height=top_cone.baseDiameter,
    direction=[1,0,0],
    color="YELLOW",
    material="STEEL"
)

parts_list.append(side_pipe_1_1)


side_pipe_1_2 = Cylinder(
    x=-top_cone.baseDiameter/2, y=0, z = 0,
    diameter=pipe_diam,
    height=top_cone.baseDiameter,
    direction=[1,0,0],
    color="YELLOW",
    material="STEEL"
)

parts_list.append(side_pipe_1_2)


side_opening_2 = Cylinder(
    x=0, y=-top_cone.baseDiameter/2, z = 0,
    diameter=pipe_diam+2*lock_th,
    height=top_cone.baseDiameter,
    direction=[0,1,0],
    color="YELLOW",
    material="STEEL"
)

parts_list.append(side_opening_2)


#for subtraction
side_pipe_2 = Cylinder(
    x=0, y=-top_cone.baseDiameter/2, z = 0,
    diameter=pipe_diam,
    height=top_cone.baseDiameter,
    direction=[0,1,0],
    color="YELLOW",
    material="STEEL"
)

parts_list.append(side_pipe_2)

#need more copies to perform subtraction
side_pipe_2_1 = Cylinder(
    x=0, y=-top_cone.baseDiameter/2, z = 0,
    diameter=pipe_diam,
    height=top_cone.baseDiameter,
    direction=[0,1,0],
    color="YELLOW",
    material="STEEL"
)

parts_list.append(side_pipe_2_1)

side_pipe_2_2 = Cylinder(
    x=0, y=-top_cone.baseDiameter/2, z = 0,
    diameter=pipe_diam,
    height=top_cone.baseDiameter,
    direction=[0,1,0],
    color="YELLOW",
    material="STEEL"
)

parts_list.append(side_pipe_2_2)

for part in parts_list:
    part.initForNX()


#subtractions
hollow_top_cone.subtractFrom(top_cone)
hollow_top_cyl.subtractFrom(top_cyl) 

hollow_bottom_cone1.subtractFrom(bottom_cone1)
hollow_bottom_cone2.subtractFrom(bottom_cone2)

hollow_middle_cyl.subtractFrom(middle_cyl)


side_pipe_2_1.subtractFrom(side_opening_1)
side_pipe_1_2.subtractFrom(side_opening_1)


side_pipe_2_2.subtractFrom(side_opening_2)
side_pipe_1_1.subtractFrom(side_opening_2)


side_pipe_1.subtractFrom(middle_cyl)
side_pipe_2.subtractFrom(middle_cyl)


hollow_cross_1.subtractFrom(side_opening_1)
hollow_cross_2.subtractFrom(side_opening_2)


