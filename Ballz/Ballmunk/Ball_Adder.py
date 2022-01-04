import pygame as pyg
from pygame import gfxdraw
from item import item
import measures
import pymunk

class ball_adder(item):
    outer_width = 2
    outer_radius = measures.radius + 8

    def __init__(self, x_pos, y_pos = -1):
        item.__init__(self, x_pos, y_pos)
        self.circle = pymunk.Circle(self.body, ball_adder.outer_radius)
        self.circle.sensor = True
        self.circle.collision_type = 4
        self.circle.color = (33, 33, 33) #Makes it the same as the background
        measures.space.add(self.body, self.circle)

    def draw(self):
        """Draws the inner circle and the outer ring"""
        display_surface = pyg.display.get_surface()
        center = (int(self.body.position.x), int(self.body.position.y))

        gfxdraw.aacircle     (display_surface, center[0], center[1], ball_adder.outer_radius, (255,255,255))
        
        #create the outline width since pygame doesn't implement it that.
        for i in range(1, ball_adder.outer_width):
           gfxdraw.aacircle    (display_surface, center[0], center[1], ball_adder.outer_radius - i, (255,255,255))

        gfxdraw.aacircle     (display_surface, center[0], center[1], ball_adder.outer_radius - ball_adder.outer_width, (255,255,255))

        gfxdraw.aacircle     (display_surface, center[0], center[1], measures.radius, (255,255,255))
        gfxdraw.filled_circle(display_surface, center[0], center[1], measures.radius, (255, 255, 255))

    def handle_collision(self):
        """If there is a collision, disappear"""
        self.remove_all()

    def remove_shape(self):
        measures.space.remove(self.circle)

