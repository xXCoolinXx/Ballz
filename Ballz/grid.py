import item
import pygame as pyg
from enum import Enum
import bisect

class Team(Enum):
    RED  = 1
    BLUE = 2

class Grid():
    """General grid bipartite collision class"""
    class Cell():
        """Grid subclass that holds a few variables"""
        def __init__(self, coordinates, size):
            self.red   = pyg.sprite.Group()
            self.blue  = pyg.sprite.Group()
            self.coordinates = coordinates
            self.size = size

        def add(self, sprite, team_color):
            self.red.add(sprite) if team_color == Team.RED else self.blue.add(sprite)

        def remove(self, sprite, team_color):
            self.red.remove(sprite) if team_color == Team.RED else self.blue.remove(sprite)

    def __init__(self, size, start, cell_size, collision_func):
        """
        tuple(size), tuple(start), int(spacing) -> None \n
        Constructor for the grid class.
        Cells are always squares.
        Sprites must have a center property.
        """
        self.collision = collision_func

        self.cell_dict = {} #tuple -> cell

        #Central object storage
        self.red  = pyg.sprite.Group()
        self.blue = pyg.sprite.Group()

        #Used for insertion lookup
        self.x_values = [start[0] + i * cell_size for i in range(0, size[0] + 1)]
        self.y_values = [start[1] + i * cell_size for i in range(0, size[1] + 1)]

        #Generate cells
        self.size = size

        for i in range(0, size[0]):
            for j in range(0, size[1]):
                self.cell_dict[(i, j)] = Grid.Cell((self.x_values[i], self.y_values[j]), cell_size)
                
    def sweep_collisions(self):
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                for i_ in range(i - 1, i + 1 + 1):     #Check all cells around the cell, too
                    for j_ in range(j - 1, j + 1 + 1): #Assumes that red does not interact with red
                        if (i_, j_) in self.cell_dict.keys(): 
                            pyg.sprite.groupcollide(self.cell_dict[(i, j)].red, self.cell_dict[(i_, j_)].blue, False, False, self.collision)

    def insert(self, member, team_color):
        """
        pygame.sprite.Sprite (member), Team (team_color) -> None \n
        Add the member into both the grid and its appropriate cell.
        """
        self.red.add(member) if team_color == Team.RED else self.blue.add(member)
        self.add(member, team_color)

    def add(self, member, team_color):
        """
        pygame.sprite.Sprite (member), Team (team_color) -> None \n
        Insert the member into its cell. The member MUST have a center attribute (can be created using property)
        """
        key = (bisect.bisect_left(self.x_values, member.center.x), bisect.bisect_left(self.y_values, member.center.y))
        print(key)
        if key[0] != self.size[0] and key[1] != self.size[1]:
            print(self.x_values[key[0]], member.center.x)
            self.cell_dict[key].red.add(member) if team_color == Team.RED else self.cell_dict[key].blue.add(member)

    def update_member_cell(self, member, team_color):
        """
        pygame.sprite.Sprite (member), Team (team_color) -> None \n
        Change the cell the member has been placed in if it has moved.
        """
        cell = member.groups()[1] #The first group is the grid group, and the second will be the cell group 

        if not (cell.location.x < member.center.x <= cell.location.x + cell.size and \
                cell.location.y < member.center.y <= cell.location.y + cell.size):
            self.remove(member, team_color)
            self.add(member, team_color)
    
    def remove(self, member, team_color):
        """
        pygame.sprite.Sprite (member), Team (team_color) -> None \n
        Remove the member from its cell.
        """
        member.add(self.red) if team_color == Team.RED else member.add(self.blue) #sprite.add automatically removes the sprite from all groups

    def full_remove(self, member, team_color):
        """
        pygame.sprite.Sprite (member), Team (team_color) -> None \n
        Simply calls the kill() function of member 
        """
        member.kill()

    def clear(self):
        for sprite in self.blue:
            sprite.kill()
        for sprite in self.red:
            sprite.kill()

        