import pygame as pyg
from pygame import gfxdraw
import math
import measures
import pymunk
import pymunk.pygame_util as ppu

class ball(pyg.sprite.Sprite):
    terminus = pyg.math.Vector2(measures.window[0] // 2, 
                                measures.window[1] - measures.top_height - measures.radius - measures.offset - 1) 
    #/\ initial launching point
    new_terminus_x = measures.window[0] // 2 + 0.00
    first = False #Flag that determines whether or not to update new_terminus_x upon hitting the ground
    speed = 600.00 
    mouse_angle = 0

    body_dict = {}

    def __init__(self, x=0, y=0):
        pyg.sprite.Sprite.__init__(self)

        self.launching = False #Flag that says whether or not the ball is launching (updated in board and the launch thread)

        #If it is not 0, it is "dropped" from a ball_adder onto the correct x value, instead of at terminus.x
        if x == 0:
            x = ball.terminus.x
        if y == 0:
            y = ball.terminus.y

        self.body = pymunk.Body(mass = 100, moment = 5000)
        self.body.position = x, y
        self.body.velocity_func = ball.velocity_func
        #self.body.position_func = ball.position_func
        self.circle = pymunk.Circle(self.body, measures.radius + measures.offset)
        self.circle.color = (255, 255, 255)
        self.circle.elasticity = 1.00
        self.circle.collision_type = 1
        measures.space.add(self.body, self.circle)
        ball.body_dict[self.body] = self 

        self.collided = False # Flag that ensures that a ball doesn't hit two boxes in the same loop

    def launch(self):
        self.launching = False #Not launching if you have already launched
        self.body.velocity = -ball.speed*math.cos(ball.mouse_angle), -ball.speed*math.sin(ball.mouse_angle)
        self.body.position = ball.terminus

    def draw(self):
        display_surface = pyg.display.get_surface()

        gfxdraw.aacircle(display_surface, int(self.body.position.x), int(self.body.position.y), measures.radius, (255,255,255))
        gfxdraw.filled_circle(display_surface, int(self.body.position.x), int(self.body.position.y), measures.radius, (255,255,255))

    def velocity_func(body, gravity, damping, dt):
        if body in ball.body_dict: #Makes sure that the ball has not been deleted
            if body.position.y > ball.terminus.y: #Checks if the ball has hit the ground
                body.velocity = 0, 0
                body.position = body.position.x, ball.terminus.y
                if not ball.first:
                    ball.first = True
                    ball.new_terminus_x = body.position.x
            elif body.position.y == ball.terminus.y and not ball.body_dict[body].launching: #Checks if the ball is on ground (not launching)
                #Once the ball hits the ground, slide it over to new_terminus_x
                body.position.y = ball.terminus.y
                if abs(body.position.x - ball.new_terminus_x) < ball.speed*dt:
                    body.position = ball.new_terminus_x, body.position.y
                    body.velocity = 0, 0
                elif body.position.x < ball.new_terminus_x:
                    body.velocity = ball.speed, 0.00
                    #print("MOVING RIGHT")
                elif body.position.x > ball.new_terminus_x:
                    body.velocity = -ball.speed, 0.00
                    #print("MOVING LEFT")
            elif body.velocity.x > 0 or body.velocity.y > 0: #Check if the ball is in the air
                if body.velocity.length != ball.speed:
                    body.velocity *= ball.speed / body.velocity.length
            pymunk.Body.update_velocity(body, gravity, 1, dt)
               
    def update(self):
        self.collided = False
    
    def prepare_launch():
        """Resets the speed and first value (used as a flag to determine whether to change new_terminus_x)"""
        ball.first = False
        ball.terminus.x = ball.new_terminus_x
        ball.speed = 600.00
    
    def update_mouse_angle():
         #update to the angle between mouse and terminus
         ball.mouse_angle = 0
         mouse_pos = pyg.mouse.get_pos()
         if mouse_pos[1] < ball.terminus.y - measures.radius: 
            try:
                ball.mouse_angle = math.atan((mouse_pos[1] - ball.terminus.y)/(mouse_pos[0] - ball.terminus.x))          
            except:
                ball.mouse_angle = math.pi /2
         else:
            ball.mouse_angle = 3*math.pi / 180
            if pyg.mouse.get_pos()[0] > ball.terminus.x:
                ball.mouse_angle *= -1
            
         if pyg.mouse.get_pos()[0] > ball.terminus.x:
            ball.mouse_angle += math.pi

    def lightning():
        ball.speed = 1000.00

    def remove_all(self):
        self.kill()
        del ball.body_dict[self.body]
        measures.space.remove(self.body)
        measures.space.remove(self.circle)
        