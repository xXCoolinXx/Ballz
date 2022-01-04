import pygame as pyg
import measures
import pymunk

class item(pyg.sprite.Sprite):
    """Base class for the members of board.grid"""
    body_dict = {}
    def __init__(self, x_pos, y_pos = -1):
        pyg.sprite.Sprite.__init__(self)

        #Check if the item is a new instance or loaded from the json file. If new, place it at the initial y value.
        y = 0
        if y_pos == -1:
            y = measures.top_height + measures.step
        else:
            y = measures.ys[y_pos]

        self.body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        self.body.position = measures.xs[x_pos] + measures.dimension / 2, y + measures.dimension / 2
        self.initiateMove()
        self.body.velocity_func = item.velocity_func
        self.last_y_pos = y_pos

        item.body_dict[self.body] = self #Add the item to a dictionary for collision lookup

    def draw(self):
        """Handled by the child classes"""
        pass

    def initiateMove(self):
        """Start moving the item"""
        self.body.velocity = 0, 60

    def velocity_func(body, gravity, damping, dt):
        """Static method that stops the body from moving once it hits the next y_pos"""
        if body in item.body_dict: #Make sure the item has not been deleted O(1)
            if body.velocity.length != 0:
                lyp = item.body_dict[body].last_y_pos
                if lyp != 6 and body.position.y > measures.ys[lyp + 1] + measures.dimension / 2:
                    lyp += 1
                    item.body_dict[body].last_y_pos += 1
                    body.velocity = 0, 0
                    body.position = body.position.x, measures.ys[lyp] + measures.dimension / 2 
            pymunk.Body.update_velocity(body, gravity, damping, dt)

    def handle_collision():
        """Handled by the child classes"""
        pass
    
    def remove_most(self):
        measures.space.remove(self.body)
        del item.body_dict[self.body]
        self.kill()

    def remove_shape():
        pass

    def remove_all(self):
        self.remove_shape()
        self.remove_most()

