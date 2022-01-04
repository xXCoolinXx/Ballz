import pygame as pyg

class button_image:
    """Literally in the name"""

    def __init__(self, left, top, image_path, pressed_image_path, color_key):
        self.regular = pyg.image.load(image_path)
        self.pressed = pyg.image.load(pressed_image_path)
        #self.regular.convert_alpha()
        #self.presssed.convert_alpha()
        self.regular.set_colorkey(color_key)
        self.pressed.set_colorkey(color_key)

        self.left = left
        self.top = left
        self.state = False

    def check_hover(self):
        rectangle = self.regular.get_rect()
        rectangle.left = self.left
        rectangle.top = self.top

        if rectangle.collidepoint(pyg.mouse.get_pos()):
            return True
        else:
            return False
    def check_click(self):
        if self.check_hover() and pyg.mouse.get_pressed()[0]:
            self.state = True
            return True
        else:
            return False
    
    def draw(self):
        display_surface = pyg.display.get_surface()
        if self.state:
            display_surface.blit(self.pressed, (self.left, self.top))  
        else:
            display_surface.blit(self.regular, (self.left, self.top))

    def update(self):
        return self.check_click()

    def clear_state(self):
        self.state = False
        





