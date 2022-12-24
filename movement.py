import arcade
import random
import time
import math

# extend the Sprite class for the rock, paper, and scissor icons
class Weapon(arcade.Sprite):
    # constructor
    def __init__(self, filename, scale, hit_box_algorithm):
        # call the Sprite class's constructor
        super().__init__(filename = filename, scale = scale, hit_box_algorithm = hit_box_algorithm)
    
    # called when the Game class updates
    def update(self, weaponList):
        pass

# extend arcade's built in Window class
class Game(arcade.Window):
    # static variables
    # storing height and width of screen
    screenWidth = arcade.get_display_size()[0]
    screenHeight = arcade.get_display_size()[1]
    
    # constructor
    def __init__(self):
        # call the Window class's constructor
        super().__init__(Game.screenWidth, Game.screenHeight, "Example")

        # declare the sprite lists
        self.rockList = None
        self.paperList = None
        self.scissorList = None

        # set background color
        arcade.set_background_color(arcade.color.WHITE)

    
    # sets up the game, can be called multiple times to restart the game
    def setup(self):
        # initialize the sprite lists using arcade's SpriteList
        self.rockList = arcade.SpriteList()
        self.paperList = arcade.SpriteList()
        self.scissorList = arcade.SpriteList()

        rock = Weapon(filename = "Sprites/rock.png", scale = 0.25, hit_box_algorithm = "Detailed")
        # set position on screen to be random, adjust so the entire sprite is on the screen
        rock.center_x = 500
        rock.center_y = 500
        # add to sprite list
        self.rockList.append(rock)

       
        # scissor sprites
        scissor = Weapon(filename = "Sprites/scissors.png", scale = 0.25, hit_box_algorithm = "Detailed")
        # set position on screen to be random, adjust so the entire sprite is on the screen
        scissor.center_x = 200
        scissor.center_y = 250
        # add to sprite list
        self.scissorList.append(scissor)
        
    # draws things on screen 60 times a second
    def on_draw(self):
        # ready to draw
        arcade.start_render()
        # delay removing initial collisions for 2 seconds
        
        # draw all of the sprites
        self.rockList.draw()
        self.paperList.draw()
        self.scissorList.draw()
        # circle initial collisions
        # for coords in Game.collisionList:
        #     arcade.draw_circle_outline(coords[0], coords[1], 30, arcade.color.BLACK)

    # updates values 60 times a second
    def update(self, delta_time):
        for rock in self.rockList:
            nearestScissor = arcade.get_closest_sprite(rock, self.scissorList)[0]
            print((nearestScissor.center_x, nearestScissor.center_y))
            deltaX = nearestScissor.center_x - rock.center_x
            deltaY = nearestScissor.center_y - rock.center_y
            deltaMagnitude = math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))
            normalizedDeltaX = deltaX / deltaMagnitude
            normalizedDeltaY = deltaY / deltaMagnitude
            rock.center_x += normalizedDeltaX
            rock.center_y += normalizedDeltaY
        
        
def main():
    # create game window
    window = Game()
    # run game setup
    window.setup()
    # keep window open until user closes it
    arcade.run()

main()