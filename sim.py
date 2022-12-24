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
    def update(self, deltaX, deltaY):
        # self.center_x += deltaX
        # self.center_y += deltaY
        pass

# extend arcade's built in Window class
class Game(arcade.Window):
    # static variables
    # storing height and width of screen
    screenWidth = arcade.get_display_size()[0]
    screenHeight = arcade.get_display_size()[1]
    # storing collision coordinates (remove this later?)
    collisionList = []
    # counter to delay start of main loop
    counter = 0
    
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
        for i in range(50):
            # rock sprites
            rock = Weapon(filename = "Sprites/rock.png", scale = 0.25, hit_box_algorithm = "Detailed")
            # set position on screen to be random, adjust so the entire sprite is on the screen
            rock.center_x = random.randrange(60, Game.screenWidth - 60)
            rock.center_y = random.randrange(60, Game.screenHeight - 60)
            # add to sprite list
            self.rockList.append(rock)

            # paper sprites
            paper = Weapon(filename = "Sprites/paper.png", scale = 0.25, hit_box_algorithm = "Detailed")
            # set position on screen to be random, adjust so the entire sprite is on the screen
            paper.center_x = random.randrange(60, Game.screenWidth - 60)
            paper.center_y = random.randrange(60, Game.screenHeight - 60)
            # add to sprite list
            self.paperList.append(paper)

            # scissor sprites
            scissor = Weapon(filename = "Sprites/scissors.png", scale = 0.25, hit_box_algorithm = "Detailed")
            # set position on screen to be random, adjust so the entire sprite is on the screen
            scissor.center_x = random.randrange(60, Game.screenWidth - 60)
            scissor.center_y = random.randrange(60, Game.screenHeight - 60)
            # add to sprite list
            self.scissorList.append(scissor)

    # the following 3 functions handle collisions between different weapons
    # iterates through rock list and changes all rocks that collide with paper to paper
    def rockPaperCollision(self):
        for paper in self.paperList:
            for rock in self.rockList:
                if arcade.check_for_collision(paper, rock):
                    Game.collisionList.append((rock.center_x, rock.center_y))
                    # create new paper weapon where rock weapon originally was
                    newPaper = Weapon(filename = "Sprites/paper.png", scale = 0.25, hit_box_algorithm = "Detailed")
                    newPaper.center_x = rock.center_x
                    newPaper.center_y = rock.center_y
                    # add new paper to paperList and remove the old rock from rockList
                    self.paperList.append(newPaper)
                    self.rockList.remove(rock)
    # iterates through scissor list and removes all scissors that collide with rock
    def scissorRockCollision(self):
        for rock in self.rockList:
            for scissor in self.scissorList:
                if arcade.check_for_collision(rock, scissor):
                    Game.collisionList.append((scissor.center_x, scissor.center_y))
                    # create new rock weapon where scissor weapon originally was
                    newRock = Weapon(filename = "Sprites/rock.png", scale = 0.25, hit_box_algorithm = "Detailed")
                    newRock.center_x = scissor.center_x
                    newRock.center_y = scissor.center_y
                    # add new rock to rockList and remove the old scissor from scissorList
                    self.rockList.append(newRock)
                    self.scissorList.remove(scissor)
    # iterates through paper list and removes all paper that collides with scissors
    def paperScissorCollision(self):
        for scissor in self.scissorList:
            for paper in self.paperList:
                if arcade.check_for_collision(scissor, paper):
                    Game.collisionList.append((paper.center_x, paper.center_y))
                    # create new scissor weapon where paper weapon originally was
                    newScissor = Weapon(filename = "Sprites/scissors.png", scale = 0.25, hit_box_algorithm = "Detailed")
                    newScissor.center_x = paper.center_x
                    newScissor.center_y = paper.center_y
                    # add new scissor to scissorList and remove the old paper from paperList
                    self.scissorList.append(newScissor)
                    self.paperList.remove(paper)
    
    # calls the above 3 functions in a random order to fix weapon overlap at the start of the game
    def fixInitialCollisions(self):
        # randomize order to fix collisions to keep all sides balanced
        # potential collision orders are:
        # 1) rock-paper, scissor-rock, paper-scissor
        # 2) rock-paper, paper-scissor, scissor-rock
        # 3) scissor-rock, rock-paper, paper-scissor
        # 4) scissor-rock, paper-scissor, rock-paper
        # 5) paper-scissor, scissor-rock, rock-paper
        # 6) paper-scissor, rock-paper, scissor-rock

        order = random.randint(1, 6)
        if order == 1:
            Game.rockPaperCollision(self)
            Game.scissorRockCollision(self)
            Game.paperScissorCollision(self)
        elif order == 2:
            Game.rockPaperCollision(self)
            Game.paperScissorCollision(self)
            Game.scissorRockCollision(self)
        elif order == 3:
            Game.scissorRockCollision(self)
            Game.rockPaperCollision(self)
            Game.paperScissorCollision(self)
        elif order == 4:
            Game.scissorRockCollision(self)
            Game.paperScissorCollision(self)
            Game.rockPaperCollision(self)
        elif order == 5:
            Game.paperScissorCollision(self)
            Game.scissorRockCollision(self)
            Game.rockPaperCollision(self)
        elif order == 6:
            Game.paperScissorCollision(self)
            Game.rockPaperCollision(self)
            Game.scissorRockCollision(self)
        else:
            print("Error! Couldn't determine order of initial collisions")

    # the following 3 functions handle moving weapons toward other weapons
    # moving rocks toward scissors
    def moveRocks(self):
        for rock in self.rockList:
            # get nearest scissor
            nearestScissorTuple = arcade.get_closest_sprite(rock, self.scissorList)
            # all scissors have been destroyed
            if (nearestScissorTuple == None):
                return
            nearestScissor = nearestScissorTuple[0]
            # calculate x and y components of vector from rock to scissor
            deltaX = nearestScissor.center_x - rock.center_x
            deltaY = nearestScissor.center_y - rock.center_y
            # calculate magnitude of this vector
            deltaMagnitude = math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))
            # normalize the x and y components so their new magnitude is 1
            if deltaMagnitude != 0:
                normalizedDeltaX = deltaX / deltaMagnitude
                normalizedDeltaY = deltaY / deltaMagnitude
            else:
                normalizedDeltaX = 0
                normalizedDeltaY = 0
            # move the rock toward the scissor at a rate of 1 unit of distance per second
            rock.center_x += normalizedDeltaX
            rock.center_y += normalizedDeltaY
    # moving papers towards rocks
    def movePapers(self):
        for paper in self.paperList:
            # get nearest rock
            nearestRockTuple = arcade.get_closest_sprite(paper, self.rockList)
            # all rocks have been destroyed
            if nearestRockTuple == None:
                return
            nearestRock = nearestRockTuple[0]
            # calculate x and y components of vector from paper to rock
            deltaX = nearestRock.center_x - paper.center_x
            deltaY = nearestRock.center_y - paper.center_y
            # calculate magnitude of this vector
            deltaMagnitude = math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))
            # normalize the x and y components so their new magnitude is 1
            if deltaMagnitude != 0:
                normalizedDeltaX = deltaX / deltaMagnitude
                normalizedDeltaY = deltaY / deltaMagnitude
            else:
                normalizedDeltaX = 0
                normalizedDeltaY = 0
            # move the paper toward the rock at a rate of 1 unit of distance per second
            paper.center_x += normalizedDeltaX
            paper.center_y += normalizedDeltaY
    # moving scissors towards papers
    def moveScissors(self):
        for scissor in self.scissorList:
            # get nearest paper
            nearestPaperTuple = arcade.get_closest_sprite(scissor, self.paperList)
            # all papers have been destroyed
            if nearestPaperTuple == None:
                return
            nearestPaper = nearestPaperTuple[0]
            # calculate x and y components of vector from paper to rock
            deltaX = nearestPaper.center_x - scissor.center_x
            deltaY = nearestPaper.center_y - scissor.center_y
            # calculate magnitude of this vector
            deltaMagnitude = math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))
            # normalize the x and y components so their new magnitude is 1
            if deltaMagnitude != 0:
                normalizedDeltaX = deltaX / deltaMagnitude
                normalizedDeltaY = deltaY / deltaMagnitude
            else:
                normalizedDeltaX = 0
                normalizedDeltaY = 0
            # move the paper toward the rock at a rate of 1 unit of distance per second
            scissor.center_x += normalizedDeltaX
            scissor.center_y += normalizedDeltaY
        
    # draws things on screen 60 times a second
    def on_draw(self):
        # ready to draw
        arcade.start_render()
        # draw all of the sprites
        self.rockList.draw()
        self.paperList.draw()
        self.scissorList.draw()
        # circle initial collisions
        # for coords in Game.collisionList:
        #     arcade.draw_circle_outline(coords[0], coords[1], 30, arcade.color.BLACK)

    # updates values 60 times a second
    def update(self, delta_time):
        Game.fixInitialCollisions(self)
        Game.moveRocks(self)
        Game.movePapers(self)
        Game.moveScissors(self)
        
def main():
    # create game window
    window = Game()
    # run game setup
    window.setup()
    # keep window open until user closes it
    arcade.run()

main()