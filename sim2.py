import arcade
import random
import math
import sys

# TODO: look at on_update() in Game for functions to complete

# extend the Sprite class for the rock, paper, and scissor icons
class Weapon(arcade.Sprite):
        
    # constructor
    def __init__(self, filename, scale, hit_box_algorithm, type):
        
        # call the Sprite class's constructor
        super().__init__(filename = filename, scale = scale, hit_box_algorithm = hit_box_algorithm)
        
        self.type = type
    
    # called when the Game class updates
    def on_update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

# extend arcade's built in Window class
class Game(arcade.Window):
    
    # static variables
    
    # storing height and width of screen
    screenWidth = arcade.get_display_size()[0]
    screenHeight = arcade.get_display_size()[1]

    # number of each type of weapon
    WEAPON_COUNT = 30

    # ranges of coordinates weapons can have without going offscreen
    minX = 20
    maxX = screenWidth - 20
    minY = 70
    maxY = screenHeight - 10
    
    # constructor
    def __init__(self):
        
        # call the Window class's constructor
        super().__init__(width = Game.screenWidth, height = Game.screenHeight, title = "Example", update_rate = 1 / 24)

        # declare the sprite lists
        
        # holds all the weapons
        self.weaponList = None

        # hold specific weapons
        self.rockList = None
        self.paperList = None
        self.scissorList = None

        # wall sprites to prevent weapons from running offscreen
        self.wallList = None

        # keep track of sprites that will/won't be updated in the current frame
        self.updateList = None
        self.stasisList = None

        # set background color
        arcade.set_background_color(arcade.color.WHITE)

    # sets up the game, can be called multiple times to restart the game
    def setup(self):
        
        # initialize the weapon lists using arcade's SpriteList
        self.weaponList = arcade.SpriteList(use_spatial_hash = True)
        self.rockList = arcade.SpriteList(use_spatial_hash = True)
        self.paperList = arcade.SpriteList(use_spatial_hash = True)
        self.scissorList = arcade.SpriteList(use_spatial_hash = True)

        # create all of the weapon sprites
        # SPRITES ARE 30 x 30 PIXELS
        for i in range(Game.WEAPON_COUNT):
            
            # rock sprites
            
            rock = Weapon(filename = "Sprites/rock.png", scale = 0.25, hit_box_algorithm = "Detailed", type = "rock")
            # set position on screen to be random, adjust so the entire sprite is on the screen
            rock.center_x = random.randrange(Game.minX + 20, Game.maxX - 20)
            rock.center_y = random.randrange(Game.minY + 20, Game.maxY - 20)
            self.weaponList.append(rock)
            self.rockList.append(rock)

            # paper sprites
            
            paper = Weapon(filename = "Sprites/paper.png", scale = 0.25, hit_box_algorithm = "Detailed", type = "paper")
            # set position on screen to be random, adjust so the entire sprite is on the screen
            paper.center_x = random.randrange(Game.minX + 20, Game.maxX - 20)
            paper.center_y = random.randrange(Game.minY + 20, Game.maxY - 20)
            self.weaponList.append(paper)
            self.paperList.append(paper)

            # scissor sprites
            
            scissor = Weapon(filename = "Sprites/scissors.png", scale = 0.25, hit_box_algorithm = "Detailed", type = "scissor")
            # set position on screen to be random, adjust so the entire sprite is on the screen
            scissor.center_x = random.randrange(Game.minX + 20, Game.maxX - 20)
            scissor.center_y = random.randrange(Game.minY + 20, Game.maxY - 20)
            self.weaponList.append(scissor)
            self.scissorList.append(scissor)

        # set up updateList
        self.updateList = [weapon for weapon in self.weaponList]
        
        # set up walls
        self.wallList = arcade.SpriteList()
        topWall = arcade.Sprite(filename = "Sprites/wall.png", image_width = Game.screenWidth, image_height = 5, center_x = Game.screenWidth / 2, center_y = Game.maxY)
        self.wallList.append(topWall)
        bottomWall = arcade.Sprite(filename = "Sprites/wall.png", image_width = Game.screenWidth, image_height = 5, center_x = Game.screenWidth / 2, center_y = Game.minY)
        self.wallList.append(bottomWall)
        leftWall = arcade.Sprite(filename = "Sprites/wall.png", image_width = 5, image_height = Game.screenHeight, center_x = Game.minX, center_y = Game.screenHeight / 2)
        self.wallList.append(leftWall)
        rightWall = arcade.Sprite(filename = "Sprites/wall.png", image_width = 5, image_height = Game.screenHeight, center_x = Game.maxX, center_y = Game.screenHeight / 2)
        self.wallList.append(rightWall)
    
    
    # update weapons as they collide with each other in a random order
    def resolveWeaponCollisions(self):
        # the following 3 functions handle collisions between different weapons
        #######################################################################
    
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
                        self.weaponList.append(newPaper)
                        rock.remove_from_sprite_lists()
                        del rock

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
                        self.weaponList.append(newRock)
                        scissor.remove_from_sprite_lists()
                        del scissor
            
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
                        self.weaponList.append(newScissor)
                        paper.remove_from_sprite_lists()
                        del paper
        #######################################################################

        # handle collisions in a random order to keep it fair
        order = random.randint(1, 6)
        if order == 1:
            paperRockCollision(self)
            rockScissorCollision(self)
            scissorPaperCollision(self)
        elif order == 2:
            paperRockCollision(self)
            scissorPaperCollision(self)
            rockScissorCollision(self)
        elif order == 3:
            rockScissorCollision(self)
            paperRockCollision(self)
            scissorPaperCollision(self)
        elif order == 4:
            rockScissorCollision(self)
            scissorPaperCollision(self)
            paperRockCollision(self)
        elif order == 5:
            scissorPaperCollision(self)
            rockScissorCollision(self)
            paperRockCollision(self)
        elif order == 6:
            scissorPaperCollision(self)
            paperRockCollision(self)
            rockScissorCollision(self)
        else:
            print("Error! Couldn't determine order of initial collisions")

    # update velocities of all weapons on update list
    def updateWeaponVelocities(self):
        for weapon in self.updateList:
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
            if nearestBeatTuple != None:
                nearestBeat = nearestBeatTuple[0]
                beatDistance = nearestBeatTuple[1]
                
            else:
                nearestBeat = None
                beatDistance = sys.maxsize
            if nearestLoseTuple != None:
                nearestLose = nearestLoseTuple[0]
                loseDistance = nearestLoseTuple[1]
            else:
                nearestLose = None
                loseDistance = sys.maxsize
            if nearestBeatTuple == None and nearestLoseTuple == None:
                # win condition
                return
            
            # calculate x and y components of velocity vector from current weapon to weapon it can beat/lose to based on distance
            if (beatDistance <= loseDistance):
                deltaX = nearestBeat.center_x - weapon.center_x
                deltaY = nearestBeat.center_y - weapon.center_y
            else:
                # reverse vector so weapon runs away from what it loses to
                deltaX = -1 * (nearestLose.center_x - weapon.center_x)
                deltaY = -1 * (nearestLose.center_y - weapon.center_y)
            
            # using components of velocity vector, calculate angle w.r.t. positive x-axis
            angle = math.atan2(deltaY, deltaX)
            
            # set velocities of weapon, using angle to normalize the components
            weapon.change_x = math.cos(angle)
            weapon.change_y = math.sin(angle)

    # move weapons
    def moveWeapons(self):
        
        # randomize the order
        self.weaponList.shuffle()

        self.weaponList.on_update(delta_time = 1 / 24)
        
    # draws things on screen 24 times a second
    def on_draw(self):
        # ready to draw
        arcade.start_render()
        
        # draw all of the sprites
        self.weaponList.draw()
        self.wallList.draw()

    # updates values 24 times a second
    def on_update(self, delta_time = 1 / 24):
        Game.resolveWeaponCollisions(self)
        # resolve wallCollisions()
            # update reflection velocities
            # add to stasisList / remove from updateList
        Game.updateWeaponVelocities(self)
        Game.moveWeapons(self)
        # update updateList and stasisList

def main():
    # create game window
    window = Game()
    
    # run game setup
    window.setup()
    
    # keep window open until user closes it
    arcade.run()

main()
        