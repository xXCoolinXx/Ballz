import pygame as pyg
from pygame import gfxdraw
import math
import measures

class ball(pyg.sprite.Sprite):
    radius = 7
    terminus = pyg.math.Vector2(measures.window[0] // 2, measures.window[1] - measures.top_height - measures.radius - 1) #launching point
    new_terminus_x = measures.window[0] // 2
    first = False #Flag that determines whether or not to update new_terminus_x upon hitting the ground
    speed = 300
    mouse_angle = 0.00

    def __init__(self, x=0):
        pyg.sprite.Sprite.__init__(self)

        self.rect = pyg.Rect(0,0,0,0)
        self.vector = pyg.math.Vector2(0,0)
        self.moving = False 
        self.launching = False 
        #Launching flag that says whether or not the ball is launching (updated in ball.board_ref and the launch thread)

        #If it is 0, it is "dropped" from a ball_adder onto the correct x value, instead of at terminus.x
        x = ball.terminus.x if x == 0 else x

        self.center = pyg.math.Vector2(x, ball.terminus.y)

    def draw(self):
        """Draw"""
        display_surface = pyg.display.get_surface()
        gfxdraw.aacircle     (display_surface, int(self.center.x), int(self.center.y), measures.radius, (255,255,255))
        gfxdraw.filled_circle(display_surface, int(self.center.x), int(self.center.y), measures.radius, (255,255,255))
        rect = pyg.Rect(0, 0, measures.radius, measures.radius)
        rect.center = self.center
        return rect

    def launch(self):
        self.moving = True
        self.change_vector(ball.mouse_angle)
        self.launching = False #Not launching if you have already launched

    def update(self, step):
        if self.moving:
            #Move along the vector
            self.center -= step*ball.speed*self.vector

            #Detects collision with the border
            #right side
            if self.center.x + 7 >= measures.borders[3].left:
                self.center.x = measures.borders[3].left - measures.radius
                self.vector.x *= -1
            #left side
            elif self.center.x - 7 <= measures.borders[2].left + measures.borders[2].width:
                self.center.x = measures.borders[2].left + measures.borders[2].width + measures.radius
                self.vector.x *= -1
            #top
            elif self.center.y - 7 <= measures.borders[0].top + measures.borders[0].height:
                self.center.y = measures.borders[0].top + measures.borders[0].height + measures.radius
                self.vector.y *= -1
            #bottom
            elif self.center.y + 7 >= measures.borders[1].top:
                self.moving = False
                #If the first variable is false, then that means no other ball has set it to be true. Set it true and update new_terminus_x
                if not ball.first:
                    ball.first = True
                    ball.new_terminus_x = self.center.x

        elif not self.launching and self.center != pyg.math.Vector2(ball.new_terminus_x, ball.terminus.y):
            #Once the ball hits the ground, slide it over to new_terminus_x
            if abs(self.center.x - ball.new_terminus_x) < ball.speed/2:
                self.center = pyg.math.Vector2(ball.new_terminus_x, ball.terminus.y)
            if self.center.x < ball.new_terminus_x:
                self.center = pyg.math.Vector2(self.center.x + ball.speed, ball.terminus.y)
            elif self.center.x > ball.new_terminus_x:
                self.center = pyg.math.Vector2(self.center.x - ball.speed, ball.terminus.y) 
    
    def change_vector(self, angle):
        """Takes input angle and updates the direction vector"""
        self.vector = pyg.math.Vector2(math.cos(angle), math.sin(angle))

    def get_rect(self):
        rect = pyg.Rect(0, 0, 2*ball.radius, 2*ball.radius)
        rect.center = self.center
        return rect

    @classmethod
    def prepare_launch(cls):
        """Resets the speed and first value (used as a flag to determine whether to change new_terminus_x)"""
        cls.first = False
        cls.terminus.x = cls.new_terminus_x

    @classmethod
    def update_mouse_angle(cls):
        """update the direction vector according to the angle between mouse and terminus"""
        cls.mouse_angle = 0
        mouse_pos = pyg.mouse.get_pos()
        if mouse_pos[1] < cls.terminus.y - \
            (pyg.math.Vector2(mouse_pos) - cls.terminus).length() * math.sin(3 * math.pi / 180): 
            if mouse_pos[0] - cls.terminus.x != 0:
                cls.mouse_angle = math.atan((mouse_pos[1] - cls.terminus.y)/(mouse_pos[0] - cls.terminus.x))          
            else:
                cls.mouse_angle = math.pi /2
        else:
            cls.mouse_angle = 3*math.pi / 180
            if pyg.mouse.get_pos()[0] > cls.terminus.x:
                cls.mouse_angle *= -1
            
        if pyg.mouse.get_pos()[0] > cls.terminus.x:
            cls.mouse_angle += math.pi