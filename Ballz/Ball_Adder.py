import pygame as pyg
from pygame import gfxdraw
from item import item
import measures

class ball_adder(item):
    outer_width = 2
    outer_radius = measures.radius + 8

    def __init__(self, x_pos, y_pos = -1):
        item.__init__(self, x_pos, y_pos)

    def draw(self):
        """Draws the inner circle and the outer ring"""
        display_surface = pyg.display.get_surface()
        rect_center = self.rect.center

        gfxdraw.aacircle(display_surface, rect_center[0], rect_center[1], measures.radius, (255,255,255))
        gfxdraw.filled_circle(display_surface, rect_center[0], rect_center[1], measures.radius, (255, 255, 255))

        aacircle = lambda i : gfxdraw.aacircle(display_surface, rect_center[0], rect_center[1], \
                            ball_adder.outer_radius - i, (255,255,255))
        aacircle(0 - 1)
        aacircle(ball_adder.outer_width)
        pyg.draw.circle(display_surface, (255, 255, 255), self.rect.center, \
            int(ball_adder.outer_radius + ball_adder.outer_width / 2), ball_adder.outer_width)
        return self.rect

    def handle_collision(self):
        """If there is a collision, disappear"""
        self.kill()