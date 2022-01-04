import pymunk
space = pymunk.Space()
space.gravity = 0, 0

window = (375, 585)
radius = 7
offset = 4 #Bounding box of the ball is radius+offset so that it doesn't go into the boxes
dimension = 45
step = 5 #space between each item in the grid

#border width (for the left and side borders) and height (for the top and bottom borders)
side_width = 10
top_height = 65

#grid positions for the boxes and ball_adders 
xs = [side_width + step + (dimension + step)*x for x in range(0,7)]
ys = [top_height + dimension + 2*step + (dimension + step) * x for x in range(0,7)]

