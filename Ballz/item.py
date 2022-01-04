import pygame as pyg
import measures

class item(pyg.sprite.Sprite):
    """Base class for the members of board_row"""
    def __init__(self, x_pos, y_pos = -1):
        pyg.sprite.Sprite.__init__(self)

        #Check if the item is a new instance or loaded from the json file. If new, place it at the initial y value.
        y = measures.top_height + measures.step if y_pos == -1 else measures.ys[y_pos]

        self.rect = pyg.Rect(measures.xs[x_pos], y, measures.dimension, measures.dimension)
        self.stepper = 0.00
        self.moving = True #always move the item when it is created

    def initiateMove(self):
        """Start moving the item"""
        self.moving = True
        self.stepper = 0

    def update(self, step):
        if self.moving:
            #Move object
            self.stepper += step*60
            if self.stepper >= step: #Once a full step has ocurred, move the object internally. This ugly workaround is necessary because pyg.Rect.top is an int
               self.stepper  -= 1
               self.rect.top += 1

            #Check if the item has hit the next y_pos
            if self.rect.top in measures.ys:
                self.moving = False

    def draw(self):
        raise NotImplementedError

    def handle_collision(self):
        raise NotImplementedError


    #"Private" get and set center functions
    def _set_center(self, center):
        self.rect.center = center
    
    def _get_center(self):
        return pyg.math.Vector2(self.rect.center)

    center = property(_get_center, _set_center) #Property to satisfy the grid class
