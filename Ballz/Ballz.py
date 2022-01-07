import pygame as pyg
import math
from Board import board_instance
import threading
import measures
import button
import os
import move_window
from pygame._sdl2.video import Window

#main function 
def main():
    pyg.init()

    #initialize and set the icon
    monitor = pyg.math.Vector2(pyg.display.Info().current_w, pyg.display.Info().current_h)

    display_surface = pyg.display.set_mode(size = measures.window, flags = pyg.NOFRAME)
    window = Window.from_display_module()
    window.position = ((monitor.x - measures.window[0]) / 2, (monitor.y - measures.window[1]) / 2)

    pyg.display.set_icon(pyg.image.load("Images/Icon.png"))
    pyg.display.set_caption("Ballz")
    pyg.event.set_allowed([pyg.MOUSEBUTTONDOWN, pyg.MOUSEBUTTONUP, pyg.MOUSEMOTION])

    close = button.button_image(5, 30, "Images/Close.png", "Images/Close.png", color_key=(255,255,255))

    popup_font = pyg.font.Font("Fonts/Roboto-Regular.ttf", 11)
    popup_message1 = popup_font.render("Wait until the balls/boxes", True, (255, 255, 255))
    popup_rect1 = popup_message1.get_rect()
    popup_rect1.top = close.top + close.regular.get_rect().height + 5
    popup_rect1.left = close.left
    
    popup_message2 = popup_font.render("have stopped moving.", True, (255, 255, 255))
    popup_rect2 = popup_message2.get_rect()
    popup_rect2.top = popup_rect1.top + popup_rect1.height - 1
    popup_rect2.left = popup_rect1.left

    #create game clock for keeping the framerate constant
    game_clock = pyg.time.Clock()

    #area where the user can use their mouse to move the window
    move_area = pyg.Rect(close.left + close.regular.get_rect().width, 0, \
                         board_instance.speed_button.left - close.left - close.regular.get_rect().width, measures.top_height)

    #Cache the functions to speed up the program
    loop = board_instance.loop_n
    draw = board_instance.draw
    close_update = close.update

    tick = game_clock.tick
    get_fps = game_clock.get_fps

    get_event = pyg.event.get
    fill = display_surface.fill
    blit = display_surface.blit

    floor = math.floor

    fps = 60
    last_rect_list = []

    fill((33, 33, 33))
    pyg.display.flip()

    while True:
        tick(fps) #keeps framerate at a maximum of 60
        cfps = get_fps()

        #Updates the mouse events (don't need to check others)
        for event in get_event():
            if event.type == pyg.MOUSEBUTTONDOWN or event.type == pyg.MOUSEMOTION or \
                event.type == pyg.MOUSEBUTTONUP:
                move_window.check_event(window, event, move_area)

        #Draw
        fill((33, 33, 33))

        print("FPS: ",  cfps)
        rect_list = []
        rect_list += draw()
        close.draw()
        rect_list.append(close.regular.get_rect())

        #Update everything
        #for i in range(0, board_instance.loop_count + floor((fps - get_fps()) / 20)): 
        loop(1/(fps if cfps == 0 else cfps))

        if close_update():
            if board_instance.balls_grounded and not board_instance.array_moving:
                break
            else:
                rect_list.append(blit(popup_message1, popup_rect1))
                rect_list.append(blit(popup_message2, popup_rect2))

        pyg.display.update(last_rect_list)
        pyg.display.update(rect_list)
        last_rect_list = rect_list
        #pyg.display.flip()

    board_instance.write_to_file() #Write to the file once the game is over 

    pyg.quit()

if __name__ == "__main__":
    main()