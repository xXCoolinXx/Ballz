import pygame
from pygame._sdl2.video import Window

start_pos = pygame.Vector2(0, 0) #Initial mouse position
pressed = False #Flag that denotes when the mouse is being continuously pressed down

def move_window(window : Window, start_mouse_pos : pygame.Vector2, new_mouse_pos : pygame.Vector2) -> None:
    """Moves the window by the offset between start_mouse_pos and new_mouse_pos"""
    buffer_screen = pygame.Surface((window.size[0], window.size[1]))
    buffer_screen.blit(pygame.display.get_surface(), pygame.display.get_surface().get_rect())

    window_pos_Vec2 = pygame.Vector2(window.position)
    window.position = window_pos_Vec2 + new_mouse_pos - start_mouse_pos

    screen = pygame.display.set_mode((window.size[0], window.size[1]), pygame.NOFRAME)
    screen.blit(buffer_screen, buffer_screen.get_rect())
    pygame.display.flip()

def check_event(window : Window, event : pygame.event, move_area : pygame.Rect = pygame.Rect(-1, -1, 1, 1)) -> None:
    """Takes a window and event and updates the window position accordingly. \n
       move_area can be used to set what area of the screen can be clicked in order to move the window. \n
       move_area defaults to a dummy rect which is then internally changed to the full window."""
    global start_pos, pressed
    if move_area == pygame.Rect(-1, -1, 1, 1):
        move_area = pygame.Rect((0, 0), window.size)

    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    if move_area.collidepoint(mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = True
            start_pos = mouse_pos
        elif event.type == pygame.MOUSEMOTION and pressed:
            move_window(window, start_pos, mouse_pos)
        elif event.type == pygame.MOUSEBUTTONUP: #Pygame sometimes fails to recognize this event, make the window "stuck" to the mouse
            pressed = False
            move_window(window, start_pos, mouse_pos)
    else:
        pressed = False