import arcade
import random

# extend the Sprite class for the rock, paper, and scissor icons
class Weapon(arcade.Sprite):
    # constructor
    def __init__(self, filename, scale, hit_box_algorithm):
        # call the Sprite class's constructor
        super().__init__(filename = filename, scale = scale, hit_box_algorithm = hit_box_algorithm)

    def update(self):
        pass

# extend arcade's built in Window class
class Game(arcade.Window):
    # static variables
    # storing height and width of screen
    screenWidth = arcade.get_display_size()[0]
    screenHeight = arcade.get_display_size()[1]
    # storing collision coordinates (remove this later?)
    collisionList = []
    
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

        # create all of the sprites
        # SPRITES ARE 120 X 120 PIXELS
        for i in range(33):
            # rock sprites
            rock = Weapon(filename = "Sprites/rock.png", scale = 0.25, hit_box_algorithm = "Detailed")
            # set position on screen to be random, adjust so the entire sprite is on the screen
            rock.center_x = random.randrange(60, Game.screenWidth - 60)
            rock.center_y = random.randrange(60, Game.screenHeight - 60)
            # add to sprite list
            self.rockList.append(rock)

            # paper sprites
            paper = Weapon(filename = "Sprites/paper.png", scale = 0.25, hit_box_algorithm = "Detailed")
            # set position on screen to be random
            paper.center_x = random.randrange(60, Game.screenWidth - 60)
            paper.center_y = random.randrange(60, Game.screenHeight - 60)
            # add to sprite list
            self.paperList.append(paper)

            # scissor sprites
            scissor = Weapon(filename = "Sprites/scissors.png", scale = 0.25, hit_box_algorithm = "Detailed")
            # set position on screen to be random
            scissor.center_x = random.randrange(60, Game.screenWidth - 60)
            scissor.center_y = random.randrange(60, Game.screenHeight - 60)
            # add to sprite list
            self.scissorList.append(scissor)

        # check for initial collisions
        # rock and paper collisions
        for rock in self.rockList:
            for collision in arcade.check_for_collision_with_list(rock, self.paperList):
                Game.collisionList.append((rock.center_x, rock.center_y))

        # rock and scissor collisions
        for rock in self.rockList:
            for collision in arcade.check_for_collision_with_list(rock, self.scissorList):
                Game.collisionList.append((rock.center_x, rock.center_y))

        # paper and scissor collisions
        for paper in self.paperList:
            for collision in arcade.check_for_collision_with_list(paper, self.scissorList):
                Game.collisionList.append((paper.center_x, paper.center_y))

    # draws things on screen 60 times a second
    def on_draw(self):
        # ready to start drawing
        arcade.start_render()

        # draw all of the sprites
        self.rockList.draw()
        self.paperList.draw()
        self.scissorList.draw()

        for coords in Game.collisionList:
            arcade.draw_circle_outline(coords[0], coords[1], 30, arcade.color.BLACK)

    # updates values 60 times a second
    def update(self, delta_time):
        pass

def main():
    # create game window
    window = Game()
    # run game setup
    window.setup()
    # keep window open until user closes it
    arcade.run()

main()