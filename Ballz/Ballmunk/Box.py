import pygame as pyg
import random
from item import item
import pymunk
import measures
pyg.font.init() #Throws an error when declaring box.box_font if it is not called

class box(item):
    box_font = pyg.font.Font("Fonts/Roboto-Light.ttf", 20)

    def __init__(self, game_level, x_pos, y_pos=-1, number = 0):
        item.__init__(self, x_pos, y_pos)
        self.box = pymunk.Poly.create_box(self.body, (measures.dimension, measures.dimension), 1)
        self.box.collision_type = 3
        measures.space.add(self.body, self.box)

        #Check if this is a new box instance or loaded from a json file. If new, assign it with a 3/4 of being game_level, 
        #and a 1/4 chance of being 2*game_level 
        if number == 0:
            self.number = random.randint(1, 4)
            if self.number == 1:
                self.number = 2*game_level 
            else:
                self.number = game_level
        else:
            self.number = number

        self.number_text = box.box_font.render(str(self.number), True, (0,0,0))

        #Pick the color
        color = (0,0,0)
        if self.number <= 5:
            color = (245, 181, 46)
        elif 5 < self.number <= 12:
            color = (129, 197, 64)
        elif 12 < self.number <= 31:
            color = (234, 34, 94)
        elif 31 < self.number < 50:
            color = (196, 34, 132)
        elif 50 <= self.number:
            color = (22, 116, 188)
        self.box.color = color
        
    def handle_collision(self):
        """decrements the number and updates the text to match it. If number <= 0, kill()"""
        self.number -= 1
        if self.number <= 0:
            self.remove_all()
        else:
            self.number_text = box.box_font.render(str(self.number), True, (0,0,0))
            self.box.color = (min(self.box.color[0] + 10, 255), self.box.color[1], self.box.color[2])

    def draw(self):
        """Draws the rect and the text centered on the rect"""
        number_text_rect = self.number_text.get_rect()
        number_text_rect.center = self.body.position

        display_surface = pyg.display.get_surface()

        draw_rect = pyg.Rect(self.body.position.x - measures.dimension / 2, self.body.position.y - measures.dimension / 2, 
                             measures.dimension, measures.dimension)
        pyg.draw.rect(display_surface, self.box.color, draw_rect)
        display_surface.blit(self.number_text, number_text_rect)

    def remove_shape(self):
        measures.space.remove(self.box)
        
