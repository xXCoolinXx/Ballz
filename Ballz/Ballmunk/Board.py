import pygame as pyg
from pygame import gfxdraw
import random
import item
import Box
import Ball_Adder
import ball
import button
import math
import os
import json
import measures
import pymunk
pyg.font.init()

class board:
    balls = pyg.sprite.Group() 
    grid  = pyg.sprite.Group()

    array_moving = False #Flag that is used to make sure that the balls aren't launched while the board is moving

    #game_level and its associated text
    game_level = 1
    game_level_font = pyg.font.Font("Fonts/Roboto-Regular.ttf", 30)
    game_level_rect = pyg.Rect(0, 0, 0, 0)
    game_level_text = None

    #Not the actual ball_count, just what is displayed before and while you are launching the balls (goes down each time one is launched)
    ball_count = 1
    gbc_font = pyg.font.Font("Fonts/Roboto-Regular.ttf", 15)
    gbc_rect = pyg.Rect(0,0,0,0)
    gbc_text = None

    #angle between mouse and ball.terminus and the associated text (uses game_level_font)
    ma_rect = pyg.Rect(0,0,0,0)
    ma_text = None

    #button that, when pressed, speeds up the balls
    speed_button = button.button_image(0, 0, "Images/Lightning.png", "Images/LightningPressed.png", pyg.Color(255,255,255))

    #window borders and color
    border_color = (56, 56, 56)
    borders  = {} #order: top, bottom, left, right
    draw_rect = []

    balls_grounded = True

    def init():
        #set up the borders (seperate one for drawing so that a new rect doesn't need to be calculated)
        board.draw_rect = [ pyg.Rect(0, 0, measures.window[0], measures.top_height),
    pyg.Rect(0, measures.window[1] - measures.top_height, measures.window[0], measures.top_height),
    pyg.Rect(0, 0, measures.side_width, measures.window[1]),
    pyg.Rect(measures.window[0] - measures.side_width, 0, measures.side_width, measures.window[1]) ]

        board.borders = {
            pymunk.Body(body_type=pymunk.Body.STATIC) : pymunk.Poly.create_box(None, (measures.window[0], measures.top_height)),
            pymunk.Body(body_type=pymunk.Body.STATIC) : pymunk.Poly.create_box(None, (measures.window[0], measures.top_height)),
            pymunk.Body(body_type=pymunk.Body.STATIC) : pymunk.Poly.create_box(None, (2*measures.side_width, measures.window[1])),
            pymunk.Body(body_type=pymunk.Body.STATIC) : pymunk.Poly.create_box(None, (2*measures.side_width, measures.window[1])),
        }
        keys   = list(board.borders.keys  ())
        values = list(board.borders.values())
        keys[0].position = 0 + measures.window[0]/2, 0 + measures.top_height/2
        keys[1].position = measures.window[0]/2, measures.window[1] - measures.top_height + measures.top_height/2
        keys[2].position = 0 , 0 + measures.window[1]/2
        keys[3].position = measures.window[0] - measures.side_width, 0 + measures.window[1]/2
        for body, poly in board.borders.items():
            poly.body  = body
            poly.color = board.border_color
            poly.collision_type = 5
            measures.space.add(body, poly)
        values[1].collision_type = 2

        #Reads from the file. If it doesn't find a board.json, it simply adds a new row.
        board.read_from_file()
        for x in range(0, board.ball_count):
            board.balls.add(ball.ball())
                    
        board.update_text() #updates the text otherwise the ball_count text is wonky

        #Set the position of speed_button
        board.speed_button.left = measures.window[0] - board.speed_button.regular.get_rect().width - 5
        board.speed_button.top  = (measures.top_height - board.speed_button.regular.get_rect().height) / 2
    
    def game_end():
        for sprite in board.grid:
            sprite.remove_all()
        for ball_ in board.balls:
            ball_.remove_all()
        board.game_level = 1
        board.add_row()
        board.ball_count = 1
        board.update_text()
        board.balls.add(ball.ball())

    def add_row():
        row = [0 for x in range(0, 7)] #fill with 0 as placeholder
        #Add the ball adder at a random position
        ball_adder_pos = random.randint(0, 6)
        del row[ball_adder_pos] 
        row.insert(ball_adder_pos, Ball_Adder.ball_adder(ball_adder_pos))

        #3/4 chance of being a box, 1/4 chance of being 0, 0 chance of being cool
        for i in range(0, 7):
            if row[i] == 0 and random.randint(1, 4) > 1:
                row.append(Box.box(board.game_level, i))

        #initiate move animation for existing rows
        for sprite in board.grid.sprites():
            sprite.initiateMove()
                    
        board.array_moving = True #Set the flag to be true as the items are moving down
        
        #Add the new row to the first row
        for member in row:
            if member != 0:
                board.grid.add(member) 

    def draw():
        for sprite in board.grid:
            sprite.draw()

        for ball_ in board.balls:
            ball_.draw()

        if board.balls_grounded:
            board.display_ball_path()

        for rect in board.draw_rect:
            pyg.draw.rect(pyg.display.get_surface(), board.border_color, rect)

        board.update_text()
        if not board.balls_grounded:
            board.speed_button.draw()

    def loop():
        #Update board.array_moving
        board.array_moving = False
        for sprite in board.grid:
            if sprite.body.velocity.length > 0:
                board.array_moving = True
                break

        board.balls.update()
        #update balls_grounded
        board.balls_grounded = True
        for ball_ in board.balls:
            if ball_.body.velocity.length > 0 and ball_.body.position.y != ball.ball.terminus.y:
                board.balls_grounded = False
                break

        #If they are on the ground and the first flag has been set, then all balls have just hit the ground
        if  board.balls_grounded and ball.ball.first:
            board.speed_button.clear_state()
            ball.ball.prepare_launch() #resets first, ball.speed
            board.game_level += 1 
            board.ball_count = len(board.balls) #reset ball_count
            board.add_row()

        #if thread is true, the function returns true and the game loop starts a new thread using initiaite_launch which launches 
        #the balls at a set interval
        thread = False
        if pyg.mouse.get_pressed()[0] and not board.array_moving and board.balls_grounded:
                ball.ball.prepare_launch()
                for ball_ in board.balls.sprites():
                    ball_.launching = True
                thread = True

        #check if speed_button has been pressed
        if not board.balls_grounded and board.speed_button.update():
            ball.ball.lightning()

        if thread:
            return True
        else:
            return False

    def update_text():
        display_surface = pyg.display.get_surface()
        #game level
        board.game_level_text = board.game_level_font.render(str(board.game_level), True, (255, 255, 255))

        board.game_level_rect = board.game_level_text.get_rect()
        board.game_level_rect.center = list(board.borders.keys())[0].position 
        display_surface.blit(board.game_level_text, board.game_level_rect)

        #ball count
        if board.ball_count != 0:
            board.gbc_text = board.gbc_font.render("x{}".format(str(board.ball_count)), True, (255,255,255))
            board.gbc_rect = board.gbc_text.get_rect()
            board.gbc_rect.center = (ball.ball.terminus.x, ball.ball.terminus.y - 3*measures.radius)
            display_surface.blit(board.gbc_text, board.gbc_rect)

        #mouse angle
        if board.balls_grounded:
            ball.ball.update_mouse_angle()
            board.ma_text = board.game_level_font.render(str(round(180 - (ball.ball.mouse_angle * 180)/math.pi, 1)) + "°", True, (255, 255, 255))

            board.ma_rect = board.ma_text.get_rect()
            board.ma_rect.center = list(board.borders.keys())[1].position
            display_surface.blit(board.ma_text, board.ma_rect)
        
    def initiate_launch(event):
        """Launches balls at timed intervals"""
        for ball_ in board.balls.sprites():
            event.wait(timeout=0.08)
            ball_.launch()
            board.ball_count -= 1
            event.clear()

    def display_ball_path():
        """Displays the path of the balls"""
        display_surface = pyg.display.get_surface()

        spacing = 40
        start = ball.ball.terminus
        end = pyg.math.Vector2(pyg.mouse.get_pos())
        length = (start - end).length()
        unit_vector = pyg.math.Vector2(start - end)
        if unit_vector.length != 0:
            unit_vector.normalize_ip()
        initial_ball = start - spacing*unit_vector

        while (initial_ball - start).length() <= length:
            gfxdraw.aacircle(display_surface, int(initial_ball.x), int(initial_ball.y), measures.radius, (255,255,255))
            gfxdraw.filled_circle(display_surface, int(initial_ball.x), int(initial_ball.y), measures.radius, (255,255,255))
            initial_ball -= spacing*unit_vector

    def read_from_file():
        """Read from the saved json file or, if it does not exist, then just add a row"""
        if os.path.isfile("Saves/board.json") and os.path.getsize("Saves/board.json") != 0:
            with open("Saves/board.json", 'r') as f:
                data = json.load(f)
                board.game_level     = data["game level"]
                board.ball_count     = data["ball count"]
                ball.ball.terminus.x = data["terminus"  ]
                ball.ball.new_terminus_x = ball.ball.terminus.x
                for i in range(0, data["grid length"]):
                    member = data[str(i)]
                    x = measures.xs.index(member[0])
                    y = member[1]
                    if member[2] != 0:
                        board.grid.add(Box.box(board.game_level, x, y-1, member[2]))
                    else:
                        board.grid.add(Ball_Adder.ball_adder(x, y-1))
                f.close()
        else:
            board.add_row()
        

    def write_to_file():
        """Write to the json file"""
        with open("Saves/board.json", 'w') as f:
            data = {"game level" : board.game_level, 
                    "ball count" : len(board.balls), 
                    "terminus"   : ball.ball.terminus.x, 
                    "grid length": len(board.grid)}

            for i in range(0, len(board.grid)):
                if type(board.grid.sprites()[i]) == Box.box:
                    data[i] = [board.grid.sprites()[i].body.position.x - measures.dimension / 2, 
                               board.grid.sprites()[i].last_y_pos, board.grid.sprites()[i].number]
                else:
                    data[i] = [board.grid.sprites()[i].body.position.x - measures.dimension / 2, 
                               board.grid.sprites()[i].last_y_pos, 0]

            json.dump(data, f, indent = 4)
            f.close()

#Because pymunk is stupid, collision_types can't be strings. so here is a lookup table
#Ball       | 1
#Bottom     | 2
#Box        | 3
#Ball_Adder | 4
#Border     | 5

def pre_solve_ball_normal(arbiter, space, data):
    arbiter.restitution = 1 #Sets elasticity to 1 (normally 0 since restitution is the multiplication of elasiticites, and statics/kinematics have elasiticity 0
    return True

ball_touch_border = measures.space.add_collision_handler(1, 5)
ball_touch_border.pre_solve = pre_solve_ball_normal

ball_touch_ground = measures.space.add_collision_handler(1, 2)
def begin_btg(arbiter, space, data):
    """
    index = 0 
    if arbiter.shapes[0].collision_type != 1:
        index = 1
    
    if not ball.ball.first:
        ball.ball.first = True
        ball.ball.new_terminus_x = arbiter.shapes[index].body.position.x
    #ball.ball.velocity_func(arbiter.shapes[index].body, measures.space.gravity, 1, -1/60)
    arbiter.shapes[index].body.velocity = 0, 0
    arbiter.shapes[index].body.position.y = ball.ball.terminus.y  
    print(board.game_level, "BALL TOUCH GROUND")
    """
    return False
ball_touch_ground.begin = begin_btg

box_touch_ground = measures.space.add_collision_handler(3, 2)
def begin_boxtg(arbiter, space, data):
    board.game_end()
    return False
box_touch_ground.begin = begin_boxtg

box_touch_ball = measures.space.add_collision_handler(3, 1)
def begin_boxtball(arbiter, space, data):
    if arbiter.shapes[0].body in item.item.body_dict and not board.array_moving and not ball.ball.body_dict[arbiter.shapes[1].body].collided:
       #Make sure the object has not been deleted, the array is not moving, and the ball hasn't collided yet
        ball.ball.body_dict[arbiter.shapes[1].body].collided = True #Set the flag
        if abs(arbiter.contact_point_set.points[0].point_a.x - arbiter.shapes[0].body.position.x) < measures.dimension / 2: #hit side
            arbiter.shapes[1].body.velocity = arbiter.shapes[1].body.velocity.x, -arbiter.shapes[1].body.velocity.y
        elif abs(arbiter.contact_point_set.points[0].point_a.y - arbiter.shapes[0].body.position.y) < measures.dimension / 2:
            arbiter.shapes[1].body.velocity = -arbiter.shapes[1].body.velocity.x, arbiter.shapes[1].body.velocity.y
        else:
             arbiter.shapes[1].body.velocity = -arbiter.shapes[1].body.velocity.x, -arbiter.shapes[1].body.velocity.y
    return False
def separate_boxtball(arbiter, space ,data):
    if arbiter.shapes[0].body in item.item.body_dict and not board.array_moving:
        item.item.body_dict[arbiter.shapes[0].body].handle_collision()


box_touch_ball.begin = begin_boxtball
box_touch_ball.separate = separate_boxtball



ba_touch_ball = measures.space.add_collision_handler(4, 1)
def begin_batball(arbiter, space, data):
    if arbiter.shapes[0].body in item.item.body_dict:
        item.item.body_dict[arbiter.shapes[0].body].handle_collision()
        board.balls.add(ball.ball(arbiter.shapes[0].body.position.x))
    return False
ba_touch_ball.begin = begin_batball

ball_touch_ball = measures.space.add_collision_handler(1, 1)
def begin_btb(arbiter, space, data):
    return False
ball_touch_ball.begin = begin_btb