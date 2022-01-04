import pygame as pyg
import random
from item import item
import measures
pyg.font.init() #Throws an error when declaring box.box_font if it is not called

class box(item):
    box_font = pyg.font.Font("Fonts/Roboto-Light.ttf", 20)

    def __init__(self, game_level, x_pos, y_pos=-1, number = 0):
        item.__init__(self, x_pos, y_pos)

        #Check if this is a new box instance or loaded from a json file. If new, assign it with a 3/4 of being game_level, 
        #and a 1/4 chance of being 2*game_level 
        if number == 0:
            self.number = random.randint(1, 4)
            self.number = 2*game_level if self.number == 1 else game_level
        else:
            self.number = number

        self.number_text = box.box_font.render(str(self.number), True, (0,0,0))

        #Pick the color
        self.color = pyg.Color(0,0,0)
        
        if self.number <= 5:
            self.color = pyg.Color(245, 181, 46)
        elif 5 < self.number <= 12:
            self.color = pyg.Color(129, 197, 64)
        elif 12 < self.number <= 31:
            self.color = pyg.Color(234, 34, 94)
        elif 31 < self.number < 50:
            self.color = pyg.Color(196, 34, 132)
        elif 50 <= self.number:
            self.color = pyg.Color(22, 116, 188)
        
    def handle_collision(self):
        """decrements the number and updates the text to match it. If number <= 0, kill()"""
        self.number -= 1
        self.number_text = box.box_font.render(str(self.number), True, (0,0,0))
        self.color.r = min(self.color.r + 10, 255)

        if self.number <= 0:
            self.kill()            

    def draw(self):
        """Draws the rect and the text centered on the rect"""
        number_text_rect = self.number_text.get_rect()
        number_text_rect.center = self.rect.center

        display_surface = pyg.display.get_surface()

        rect = pyg.draw.rect(display_surface, self.color, self.rect)
        display_surface.blit(self.number_text, number_text_rect)
        return rect