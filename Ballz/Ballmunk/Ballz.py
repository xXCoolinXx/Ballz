import pygame as pyg
import Board
import threading
import measures
import pymunk
import pymunk.pygame_util as ppu

#main function
def main():
    pyg.init()

    #initialize and set the icon
    pyg.display.set_mode(measures.window)
    pyg.display.set_icon(pyg.image.load("Images/Icon.png"))
    pyg.display.set_caption("Ballz")

    display_surface = pyg.display.get_surface()

    #create game clock for keeping the framerate constant
    game_clock = pyg.time.Clock()
    dt = 1/60 #Simulation time step
    accumulator = 0

    Board.board.init()
    
    running = True
    while running:
        frame_time = game_clock.tick(60) / 1000 #keeps framerate at a maximum of 60, sets the frame time in seconds
        #accumulator += frame_time
        #Handle events
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                running = False
                break

        #Draw
        try: #In place because sometimes, when I exit the program during debug, this particular section triggers an error.
            display_surface.fill((33, 33, 33))
        except:
            break
        #while accumulator > dt:
            #deltaTime = min(accumulator, dt)
        measures.space.step(dt / 2)
        measures.space.step(dt / 2)
            #accumulator -= deltaTime
        
        Board.board.draw()

        thread = False
        event = threading.Event()
        if Board.board.loop():    
            ball_launch = threading.Thread(target=Board.board.initiate_launch, args=(event,))
            ball_launch.start()
 
        event.set()

        pyg.display.flip()
        print("FPS: ",  int(game_clock.get_fps()))

    Board.board.write_to_file() #Write to the file once the game is over 

    pyg.quit()

if __name__ == "__main__":
    main()