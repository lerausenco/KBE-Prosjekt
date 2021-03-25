import cv2
import numpy as np
import matplotlib.pyplot as plt


from Wall import Wall

def extract_walls():

    img = cv2.imread('img/thin-line.jpg')


    low_threshold = 50
    hight_threshold = 150

    edges = cv2.Canny(img, 200, 255)

    print(edges)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 5  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 20  # minimum number of pixels making up a line
    max_line_gap = 40  # maximum gap in pixels between connectable line segments
    line_image = np.copy(img) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)

    wall_list = []
    wall_thickness  = 2

    for line in lines:
    
        for x1,y1,x2,y2 in line:
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)
            if (x2-x1) == 0:
                wall = Wall(x1,y1,wall_thickness,abs(y2-y1))
            if (y2-y1) == 0:
                wall = Wall(x1, y1, abs(x2-x1), wall_thickness)
            wall_list.append(wall)

    # Draw the lines on the  image
    lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)


    cv2.imshow('image',line_image)
    cv2.waitKey(0)

    return wall_list