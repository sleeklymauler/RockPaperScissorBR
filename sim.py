import arcade
import random
import time
import math
import sys

# extend the Sprite class for the rock, paper, and scissor icons
class Weapon(arcade.Sprite):
    
    # static variables
    
    # ranges of coordinates weapons can have without going offscreen
    minX = 15
    maxX = arcade.get_display_size()[0] - 30
    minY = 50
    maxY = arcade.get_display_size()[1] - 20
    # used to draw circles around sprites for debugging
    overlapRadius = 0
    
    # constructor
    def __init__(self, filename, scale, hit_box_algorithm, type):
        
        # call the Sprite class's constructor
        super().__init__(filename = filename, scale = scale, hit_box_algorithm = hit_box_algorithm)
        self.type = type
        
        # custom circle radii to fit icons
        if type == "rock":
            Weapon.overlapRadius = 17
        elif type == "paper":
            Weapon.overlapRadius = 20
        elif type == "scissor":
            Weapon.overlapRadius = 19
        else:
            print("Error! Couldn't determine radius of overlap circle")
    
    # called when the Game class updates
    def update(self, deltaX, deltaY):
        pass

# extend arcade's built in Window class
class Game(arcade.Window):
    
    # static variables
    
    # storing height and width of screen
    screenWidth = arcade.get_display_size()[0]
    screenHeight = arcade.get_display_size()[1]

    # number of each type of weapon
    WEAPON_COUNT = 30
    
    # constructor
    def __init__(self):
        
        # call the Window class's constructor
        super().__init__(Game.screenWidth, Game.screenHeight, "Example", update_rate = 0.0416)

        # declare the sprite lists
        self.rockList = None
        self.paperList = None
        self.scissorList = None
        self.wallList = None

        # set background color
        arcade.set_background_color(arcade.color.WHITE)

    
    # sets up the game, can be called multiple times to restart the game
    def setup(self):
        
        # initialize the sprite lists using arcade's SpriteList
        self.rockList = arcade.SpriteList()
        self.paperList = arcade.SpriteList()
        self.scissorList = arcade.SpriteList()
        self.wallList = arcade.SpriteList()

        # create all of the weapon sprites
        # SPRITES ARE 120 X 120 PIXELS
        for i in range(Game.WEAPON_COUNT):
            
            # rock sprites
            
            rock = Weapon(filename = "Sprites/rock.png", scale = 0.25, hit_box_algorithm = "Detailed", type = "rock")
            # set position on screen to be random, adjust so the entire sprite is on the screen
            rock.center_x = random.randrange(rock.minX, rock.maxX)
            rock.center_y = random.randrange(rock.minY, rock.maxY)
            self.rockList.append(rock)

            # paper sprites
            
            paper = Weapon(filename = "Sprites/paper.png", scale = 0.25, hit_box_algorithm = "Detailed", type = "paper")
            # set position on screen to be random, adjust so the entire sprite is on the screen
            paper.center_x = random.randrange(paper.minX, paper.maxX)
            paper.center_y = random.randrange(paper.minY, paper.maxY)
            self.paperList.append(paper)

            # scissor sprites
            
            scissor = Weapon(filename = "Sprites/scissors.png", scale = 0.25, hit_box_algorithm = "Detailed", type = "scissor")
            # set position on screen to be random, adjust so the entire sprite is on the screen
            scissor.center_x = random.randrange(scissor.minX, scissor.maxX)
            scissor.center_y = random.randrange(scissor.minY, scissor.maxY)
            self.scissorList.append(scissor)
        
        # set up walls
        topWall = arcade.Sprite(filename = "Sprites/wall.png", image_width = Game.screenWidth, image_height = 5, center_x = Game.screenWidth / 2, center_y = Game.screenHeight)
        self.wallList.append(topWall)
        bottomWall = arcade.Sprite(filename = "Sprites/wall.png", image_width = Game.screenWidth, image_height = 5, center_x = Game.screenWidth / 2, center_y = 30)
        self.wallList.append(bottomWall)
        leftWall = arcade.Sprite(filename = "Sprites/wall.png", image_width = 5, image_height = Game.screenHeight, center_x = 3, center_y = Game.screenHeight / 2)
        self.wallList.append(leftWall)
        rightWall = arcade.Sprite(filename = "Sprites/wall.png", image_width = 5, image_height = Game.screenHeight, center_x = Game.screenWidth - 10, center_y = Game.screenHeight / 2)
        self.wallList.append(rightWall)
    
    # the following 3 functions handle collisions between different weapons
    
    # iterate through paperList, detect collisions with rocks and resolve them
    def paperRockCollision(self):
        
        for paper in self.paperList:
            collisionList = arcade.check_for_collision_with_list(paper, self.rockList)
            if len(collisionList) != 0:
                for rock in collisionList:
                    # create new paper at location of rock
                    newPaper = Weapon(filename = "Sprites/paper.png", scale = 0.25, hit_box_algorithm = "Detailed", type = "paper")
                    newPaper.center_x = rock.center_x
                    newPaper.center_y = rock.center_y

                    # update sprite lists
                    self.paperList.append(newPaper)
                    self.rockList.remove(rock)

    # iterate through rockList, detect collisions with scissors and resolve them
    def rockScissorCollision(self):
        
        for rock in self.rockList:
            collisionList = arcade.check_for_collision_with_list(rock, self.scissorList)
            if len(collisionList) != 0:
                for scissor in collisionList:
                    # create new rock at location of scissor
                    newRock = Weapon(filename = "Sprites/rock.png", scale = 0.25, hit_box_algorithm = "Detailed", type = "rock")
                    newRock.center_x = scissor.center_x
                    newRock.center_y = scissor.center_y

                    # update sprite lists
                    self.rockList.append(newRock)
                    self.scissorList.remove(scissor)
        
    # iterate through scissorList, detect collisions with papers and resolve them
    def scissorPaperCollision(self):
        
        for scissor in self.scissorList:
            collisionList = arcade.check_for_collision_with_list(scissor, self.paperList)
            if len(collisionList) != 0:
                for paper in collisionList:
                    # create new scissor at location of paper
                    newScissor = Weapon(filename = "Sprites/scissors.png", scale = 0.25, hit_box_algorithm = "Detailed", type = "scissor")
                    newScissor.center_x = paper.center_x
                    newScissor.center_y = paper.center_y

                    # update sprite lists
                    self.scissorList.append(newScissor)
                    self.paperList.remove(paper)
    
    # update weapons as they collide with each other in a random order
    def resolveCollisions(self):

        order = random.randint(1, 6)
        if order == 1:
            Game.paperRockCollision(self)
            Game.rockScissorCollision(self)
            Game.scissorPaperCollision(self)
        elif order == 2:
            Game.paperRockCollision(self)
            Game.scissorPaperCollision(self)
            Game.rockScissorCollision(self)
        elif order == 3:
            Game.rockScissorCollision(self)
            Game.paperRockCollision(self)
            Game.scissorPaperCollision(self)
        elif order == 4:
            Game.rockScissorCollision(self)
            Game.scissorPaperCollision(self)
            Game.paperRockCollision(self)
        elif order == 5:
            Game.scissorPaperCollision(self)
            Game.rockScissorCollision(self)
            Game.paperRockCollision(self)
        elif order == 6:
            Game.scissorPaperCollision(self)
            Game.paperRockCollision(self)
            Game.rockScissorCollision(self)
        else:
            print("Error! Couldn't determine order of initial collisions")

    # move weapons
    def moveWeapons(self):
        
        # list to store all the weapons
        self.weaponList = arcade.SpriteList()
        for rock in self.rockList:
            self.weaponList.append(rock)
        for paper in self.paperList:
            self.weaponList.append(paper)
        for scissor in self.scissorList:
            self.weaponList.append(scissor)
        # randomize the order
        self.weaponList.shuffle()
        
        for weapon in self.weaponList:
            # figure out the 2 closest weapons of different type
            if weapon.type == "rock":
                # rock beats scissors but loses to paper
                nearestBeatTuple = arcade.get_closest_sprite(weapon, self.scissorList)
                nearestLoseTuple = arcade.get_closest_sprite(weapon, self.paperList)
                selfList = self.rockList
            elif weapon.type == "paper":
                # paper beats rock but loses to scissors
                nearestBeatTuple = arcade.get_closest_sprite(weapon, self.rockList)
                nearestLoseTuple = arcade.get_closest_sprite(weapon, self.scissorList)
                selfList = self.paperList
            elif weapon.type == "scissor":
                # scissor beats paper but loses to rock
                nearestBeatTuple = arcade.get_closest_sprite(weapon, self.paperList)
                nearestLoseTuple = arcade.get_closest_sprite(weapon, self.rockList)
                selfList = self.scissorList
            else:
                print("Error! Couldn't determine type of weapon")
            
            # handling when closest 2 weapons can't be found
            if nearestBeatTuple == None:
                nearestBeat = None
                beatDistance = sys.maxsize
            else:
                nearestBeat = nearestBeatTuple[0]
                beatDistance = nearestBeatTuple[1]
            if nearestLoseTuple == None:
                nearestLose = None
                loseDistance = sys.maxsize
            else:
                nearestLose = nearestLoseTuple[0]
                loseDistance = nearestLoseTuple[1]
            if nearestBeatTuple == None and nearestLoseTuple == None:
                # win condition
                return
            
            # calculate x and y components of "velocity" vector from current weapon to weapon it can beat/lose to based on distance
            if (beatDistance <= loseDistance):
                deltaX = nearestBeat.center_x - weapon.center_x
                deltaY = nearestBeat.center_y - weapon.center_y
            else:
                # reverse vector so weapon runs away from what it loses to
                deltaX = -1 * (nearestLose.center_x - weapon.center_x)
                deltaY = -1 * (nearestLose.center_y - weapon.center_y)
            
            # calculate magnitude of this velocity vector
            deltaMagnitude = math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))
            
            # normalize the velocity vector components
            if deltaMagnitude != 0:
                normalizedDeltaX = deltaX / deltaMagnitude
                normalizedDeltaY = deltaY / deltaMagnitude
            
            # avoid collisions between weapons of the same type and with walls
            
            scale = 0.9
            originalNDX = normalizedDeltaX
            originalNDY = normalizedDeltaY
            # temporarily remove the current weapon from its own weapon list so it isn't detecting itself
            selfList.remove(weapon)
            while arcade.get_sprites_at_point((weapon.center_x + normalizedDeltaX, weapon.center_y + normalizedDeltaY), selfList)\
            or arcade.get_sprites_at_point((weapon.center_x + normalizedDeltaX, weapon.center_y + normalizedDeltaY), self.wallList):
                if scale == 0:
                    break
                normalizedDeltaX = scale * originalNDX
                normalizedDeltaY = scale * originalNDY
                scale -= 0.1
            selfList.append(weapon)

            # finally! update weapon's position
            
            #rate = random.uniform(0.5, 3)
            rate = 1
            weapon.center_x += rate * normalizedDeltaX
            weapon.center_y += rate * normalizedDeltaY
        
    # draws things on screen 60 times a second
    def on_draw(self):
        # ready to draw
        arcade.start_render()
        
        # draw all of the sprites
        self.rockList.draw()
        self.paperList.draw()
        self.scissorList.draw()
        self.wallList.draw()

    # updates values 24 times a second
    def on_update(self, delta_time = 0.0416):
        Game.resolveCollisions(self)
        Game.moveWeapons(self)
        
def main():
    # create game window
    window = Game()
    
    # run game setup
    window.setup()
    
    # keep window open until user closes it
    arcade.run()

main()