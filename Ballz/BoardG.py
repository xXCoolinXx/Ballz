import pygame as pyg
from pygame import gfxdraw
import random
import Box
import Ball_Adder
import ball
import button
import math
import os
import json
import measures
import threading
import grid
pyg.font.init()

def pointOfIntersect(r_center, r_size, c_center):
        """Determines the closest point of a rectangle to a circle"""
        v2_c_center = pyg.math.Vector2(c_center)
        v2_r_center = pyg.math.Vector2(r_center)

        offset = v2_c_center - v2_r_center
        if offset.x == 0 and offset.y == 0:
            return [v2_c_center, v2_r_center]

        if offset.x == 0:   
            ratio = r_size[1] / abs(offset.y)
        elif offset.y == 0: 
            ratio = r_size[0] / abs(offset.x)
        else:
            ratio  = min(r_size[0] / abs(offset.x), r_size[1] / abs(offset.y))
        ratio *= 0.5

        return v2_r_center + (offset * ratio)

class board:
    def __init__(self):
        #set up the borders
        self.grid = grid.Grid((7, 7), (measures.side_width + measures.step / 2, measures.ys[0] - measures.step), \
            measures.dimension + measures.step / 2, self.collision)
    
        self.array_moving = False #Flag that is used to make sure that the balls aren't launched while the board is moving

        #game_level and its associated text
        self.game_level = 1
        self.game_level_font = pyg.font.Font("Fonts/Roboto-Regular.ttf", 30)
        self.game_level_rect = pyg.Rect(0, 0, 0, 0)
        self.game_level_text = None

        #Not the actual ball_count, just what is displayed before and while you are launching the balls (goes down each time one is launched)
        self.ball_count = 1
        self.gbc_font = pyg.font.Font("Fonts/Roboto-Regular.ttf", 15)
        self.gbc_rect = pyg.Rect(0,0,0,0)
        self.gbc_text = None

        #mouse angle text
        self.ma_rect = pyg.Rect(0,0,0,0)
        self.ma_text = None

        #button that, when pressed, speeds up the balls
        self.speed_button = button.button_image(0, 0, "Images/Lightning.png", "Images/LightningPressed.png", pyg.Color(255,255,255))
        self.loop_count = 2
    
        self.balls_grounded = True
        
        #Reads from the file. If it doesn't find a board.json, it simply adds a new row.
        self.read_from_file()
        #Add the necessary number of balls
        for i in range(0, max(self.ball_count, 1)):
            self.grid.insert(ball.ball(), grid.Team.BLUE)
        
        self.update_all_text() #updates the text otherwise the ball_count text is wonky

        #Set the position of speed_button
        self.speed_button.left = measures.window[0] - self.speed_button.regular.get_rect().width - 5
        self.speed_button.top  = (measures.borders[0].height - self.speed_button.regular.get_rect().height) / 2

    def add_row(self):
        #3/4 chance of being a box, 1/4 chance of being 0, 0 chance of being cool
        row = [0 if random.randint(1, 4) == 1 else Box.box(self.game_level, i) for i in range(0, 7)]

        #add the ball adder to the list at a random spot
        pos = random.randint(0,6)
        row[pos] = Ball_Adder.ball_adder(pos)

        #initiate move animation for existing rows
        for sprite in self.grid.red:
            sprite.initiateMove()
                    
        self.array_moving = True #Set the flag to be true as the items are moving down
        
        #Add the new row to the first row
        for member in row:
            if member != 0:
                self.grid.insert(member, grid.Team.RED)

    def new_level(self):
        self.speed_button.clear_state()
        ball.ball.prepare_launch() #resets first
        self.loop_count = 2
        self.game_level += 1 
        self.update_level_text()
        self.ball_count = len(self.grid.blue) #reset ball_count
        self.update_ball_text()
        self.add_row() #add another row    

    def game_end(self):
        self.grid.clear()
        self.game_level = 1
        self.add_row()
        self.ball_count = 1
        self.update_all_text()
        self.grid.insert(ball.ball(), grid.Team.BLUE)

    def draw(self):
        for sprite in self.grid.red:
            sprite.draw()
        for sprite in self.grid.blue:
            sprite.draw()

        if self.balls_grounded:
            self.display_ball_path()

        for border in measures.borders:
            pyg.draw.rect(pyg.display.get_surface(), measures.border_color, border)

        if not self.balls_grounded:
            self.speed_button.draw()
        self.draw_text()
            
            
    def loop(self, step):
        #Set it to be false
        # print(self.grid.red.sprites())
        self.grid.red.update(step)
        self.array_moving = self.grid.red.sprites()[0].moving #update the moving function
        
        self.grid.sweep_collisions()

        self.grid.blue.update(step)
        self.balls_grounded = True

        for _ball in self.grid.blue:
            if _ball.moving:
                self.balls_grounded = False
                break

        #If they are on the ground and the first flag has been set, then all balls have hit the ground just after being launched
        if  self.balls_grounded and ball.ball.first:
            self.new_level()

        #Update the mouse angle
        if self.balls_grounded:
            ball.ball.update_mouse_angle()
            self.update_angle_text()

        #check if speed_button has been pressed
        if not self.balls_grounded and self.speed_button.update():
            self.loop_count = 4

        #if thread is true, the function returns true and the game loop starts a new thread using initiaite_launch which launches 
        #the balls at a set interval
        if not self.array_moving and self.balls_grounded and not self.grid.blue.sprites()[0].launching \
            and pyg.mouse.get_pressed()[0] and pyg.mouse.get_pos()[1] > measures.top_height:
            ball.ball.prepare_launch()
            for ball_ in self.grid.blue.sprites():
                ball_.launching = True
            ball_launch = threading.Thread(target=self.initiate_launch)
            ball_launch.start()
 
    def collision(self, ball_, item):
        print("bruh")
        """Just handles the collisions"""
        if type(item) == Box.box:
            #convenience
            left = item.rect.left
            right = left + item.rect.width
            top = item.rect.top
            bottom = top + item.rect.height
            center = ball_.center

            #move foward 1 iteration (done so that the collisions are better)
            center -= ball.ball.speed*ball_.vector

            #rule out impossible collisions
            if center.x + measures.radius <= left or center.x - measures.radius >= right or center.y + measures.radius <= top \
                or center.y - measures.radius >= bottom:
                center += ball.ball.speed*ball_.vector #move back one iteration
                return None # exit the function

            #find the closest point
            closest = pointOfIntersect(item.rect.center, (item.rect.width, item.rect.height), center)
            difference = center - closest

            #move back 1 iteration
            center += ball.ball.speed*ball_.vector

            #handle the collsion
            if difference.x**2 + difference.y**2 <= measures.radius**2:
                item.handle_collision()
                #find the closest point again because otherwise weird stuff happens
                closest = pointOfIntersect(item.rect.center, (item.rect.width, item.rect.height), center)

                #top/bottom
                if top - 1 <= closest.y <= top + 1 or bottom - 1 <= closest.y <= bottom + 1:
                    ball_.vector.y *= -1
                #left/right
                elif left - 1 <= closest.x <= left + 1 or right - 1 <= closest.x <= right + 1:
                    ball_.vector.x *= -1
        elif type(item) == Ball_Adder.ball_adder:
            if math.hypot(ball_.center.x - item.rect.center[0], ball_.center.y - item.rect.center[1]) < measures.radius + Ball_Adder.ball_adder.outer_radius:
                self.grid.blue.add(ball.ball(item.rect.center[0]))
                item.handle_collision()

    def update_all_text(self):
        self.update_angle_text()
        self.update_ball_text()
        self.update_level_text()

    def update_ball_text(self):
        self.gbc_text = self.gbc_font.render("x{}".format(self.ball_count), True, (255,255,255))
        self.gbc_rect = self.gbc_text.get_rect()
        self.gbc_rect.center = (ball.ball.terminus.x, ball.ball.terminus.y - 3*measures.radius)

    def update_angle_text(self):
        self.ma_text = self.game_level_font.render("{}°".format( \
                str(round(180 - (ball.ball.mouse_angle * 180)/math.pi, 1))), True, (255, 255, 255))
        self.ma_rect = self.ma_text.get_rect()
        self.ma_rect.center = measures.borders[1].center

    def update_level_text(self):
        self.game_level_text = self.game_level_font.render(str(self.game_level), True, (255, 255, 255))
        self.game_level_rect = self.game_level_text.get_rect()
        self.game_level_rect.center = measures.borders[0].center 
 
    def draw_text(self):
        display_surface = pyg.display.get_surface()

        display_surface.blit(self.game_level_text, self.game_level_rect)
        if self.ball_count != 0:
            display_surface.blit(self.gbc_text, self.gbc_rect)
        if self.balls_grounded:
            display_surface.blit(self.ma_text , self.ma_rect )

    def initiate_launch(self):
        """Launches balls at timed intervals"""
        event = threading.Event()
        event.set()
        for ball_ in self.grid.blue:
            event.wait(timeout=0.08)
            ball_.center = pyg.math.Vector2(ball.ball.terminus)
            ball_.launch()
            self.ball_count -= 1
            self.update_ball_text()
            event.clear()

    @staticmethod
    def display_ball_path():
        """Displays the path of the balls"""
        display_surface = pyg.display.get_surface()
        spacing = 40
        start = pyg.math.Vector2(ball.ball.terminus.x, ball.ball.terminus.y)
        end = pyg.math.Vector2(pyg.mouse.get_pos())
        length = (start - end).length()
        unit_vector = pyg.math.Vector2(math.cos(ball.ball.mouse_angle), math.sin(ball.ball.mouse_angle)) 
        unit_vector.normalize_ip()
        initial_ball = start - spacing*unit_vector

        while (initial_ball - start).length() <= length:
            gfxdraw.aacircle(display_surface, int(initial_ball.x), int(initial_ball.y), measures.radius, (255,255,255))
            gfxdraw.filled_circle(display_surface, int(initial_ball.x), int(initial_ball.y), measures.radius, (255,255,255))
            initial_ball -= spacing*unit_vector

    def read_from_file(self):
        """Read from the saved json file or, if it does not exist, then just add a row"""
        if os.path.isfile("Saves/board.json") and os.path.getsize("Saves/board.json") != 0:
            with open("Saves/board.json", 'r') as f:
                data = json.load(f)
                self.game_level = data["game level"]
                self.ball_count = data["ball count"]
                ball.ball.terminus.x   = data  ["terminus"]
                ball.ball.new_terminus_x = ball.ball.terminus.x
                
                for i in range(0, self.grid.size[0]):
                    for j in range(0, self.grid.size[1]):
                        member = data[(i, j)]
                        x = measures.xs.index(member[0]) 
                        if member[1] != 0:
                            self.grid.insert(Box.box(self.game_level, x, j - 1, member[1])) 
                        else:
                            self.grid.insert(Ball_Adder.ball_adder(x, j - 1))
                f.close()
        else:
            self.add_row()
        

    def write_to_file(self):
        """Write to the json file"""
        with open("Saves/board.json", 'w') as f:
            data = {"game level" : self.game_level, 
                    "ball count" : len(self.grid.blue), 
                    "terminus"   : ball.ball.terminus.x}

            for i in range(0, self.grid.size[0]):
                for j in range(0, self.grid.size[1]):
                    if sprite := self.grid.cell_dict[(i, j)].red.sprites()[0]:
                        data[(i, j)] = (sprite.rect.left, sprite.number) if type(sprite) == Box.box else (sprite.rect.left, 0)

            json.dump(data, f, indent = 4)
            f.close()

#Only instance of the board class
board_instance = board()