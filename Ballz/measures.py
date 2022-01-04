import pygame as pyg

window = (375, 585) 
window_position = (0, 0)
radius = 7
dimension = 45
step = 5 #space between each item in the grid

#border width (for the left and side borders) and height (for the top and bottom borders)
side_width = 10
top_height = 65

borders = [ pyg.Rect(0, 0, window[0], top_height),
    pyg.Rect(0, window[1] - top_height, window[0], top_height),
    pyg.Rect(0, 0, side_width, window[1]),
    pyg.Rect(window[0] - side_width, 0, side_width, window[1]) ]

border_color = (56, 56, 56)

#grid positions for the boxes and ball_adders 
xs = [side_width + step + (dimension + step)*x for x in range(0,7)]
ys = [top_height + dimension + 2*step + (dimension + step) * x for x in range(0,8)]

