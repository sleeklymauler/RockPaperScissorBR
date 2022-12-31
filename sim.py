import arcade
import random
import time
import math
import sys

# TODO: stop weapons overlapping

# extend the Sprite class for the rock, paper, and scissor icons
class Weapon(arcade.Sprite):
    # static variables
    # ranges of coordinates weapons can have without going offscreen
    minX = 15
    maxX = arcade.get_display_size()[0] - 30
    minY = 50
    maxY = arcade.get_display_size()[1] - 20
    # circle radius to prevent same weapon overlap
    overlapRadius = 0
    
    # constructor
    def __init__(self, filename, scale, hit_box_algorithm, type):
        # call the Sprite class's constructor
        super().__init__(filename = filename, scale = scale, hit_box_algorithm = hit_box_algorithm)
        self.type = type
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
    # number of each type of weapon
    WEAPON_COUNT = 50
    
    # constructor
    def __init__(self):
        # call the Window class's constructor
        super().__init__(Game.screenWidth, Game.screenHeight, "Example", update_rate = 0.0416)

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
        for i in range(Game.WEAPON_COUNT):
            # rock sprites
            rock = Weapon(filename = "Sprites/rock.png", scale = 0.25, hit_box_algorithm = "Detailed", type = "rock")
            # set position on screen to be random, adjust so the entire sprite is on the screen
            # 15, 50, -30, -20
            rock.center_x = random.randrange(rock.minX, rock.maxX)
            rock.center_y = random.randrange(rock.minY, rock.maxY)
            # add to sprite list
            self.rockList.append(rock)

            # paper sprites
            paper = Weapon(filename = "Sprites/paper.png", scale = 0.25, hit_box_algorithm = "Detailed", type = "paper")
            # set position on screen to be random, adjust so the entire sprite is on the screen
            paper.center_x = random.randrange(paper.minX, paper.maxX)
            paper.center_y = random.randrange(paper.minY, paper.maxY)
            # add to sprite list
            self.paperList.append(paper)

            # scissor sprites
            scissor = Weapon(filename = "Sprites/scissors.png", scale = 0.25, hit_box_algorithm = "Detailed", type = "scissor")
            # set position on screen to be random, adjust so the entire sprite is on the screen
            scissor.center_x = random.randrange(scissor.minX, scissor.maxX)
            scissor.center_y = random.randrange(scissor.minY, scissor.maxY)
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
                    newPaper = Weapon(filename = "Sprites/paper.png", scale = 0.25, hit_box_algorithm = "Detailed", type = "paper")
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
                    newRock = Weapon(filename = "Sprites/rock.png", scale = 0.25, hit_box_algorithm = "Detailed", type = "rock")
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
                    newScissor = Weapon(filename = "Sprites/scissors.png", scale = 0.25, hit_box_algorithm = "Detailed", type = "scissor")
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

    # move every weapon toward or away from another weapon
    def moveWeapons(self):
        # list to store all the weapons
        self.weaponList = []
        for rock in self.rockList:
            self.weaponList.append(rock)
        for paper in self.paperList:
            self.weaponList.append(paper)
        for scissor in self.scissorList:
            self.weaponList.append(scissor)
        # randomize the order
        random.shuffle(self.weaponList)
        # determine closest weapons for each weapon
        for weapon in self.weaponList:
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
            
            # handle cases where there are no more opposing weapons
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
            # if all other weapons are gone, the current weapon has won
            if nearestBeatTuple == None and nearestLoseTuple == None:
                return
            # move to attack weapon that can be beat if its closer
            if (beatDistance <= loseDistance):
                # calculate x and y components of vector from rock to scissor
                deltaX = nearestBeat.center_x - weapon.center_x
                deltaY = nearestBeat.center_y - weapon.center_y
            # run away from weapon that can't be beat if its closer
            else:
                # calculate x and y components of vector from rock to paper and then reverse its direction
                deltaX = -1 * (nearestLose.center_x - weapon.center_x)
                deltaY = -1 * (nearestLose.center_y - weapon.center_y)
            # calculate magnitude of this vector
            deltaMagnitude = math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))
            # normalize the x and y components so their new magnitude is 1
            if deltaMagnitude != 0:
                normalizedDeltaX = deltaX / deltaMagnitude
                normalizedDeltaY = deltaY / deltaMagnitude
            else:
                normalizedDeltaX = 0
                normalizedDeltaY = 0
            # don't let weapons of the same type run into each other
            # for friend in selfList:
            #     if math.pow((weapon.center_x + normalizedDeltaX) - (friend.center_x), 2) + math.pow((weapon.center_y + normalizedDeltaY) - (friend.center_y), 2) <= math.pow(friend.overlapRadius, 2):
            #         normalizedDeltaX = 0
            #         normalizedDeltaY = 0
            #         break
            # don't let weapons go off screen
            if weapon.center_x + normalizedDeltaX >= weapon.maxX:
                normalizedDeltaX = weapon.maxX - weapon.center_x
            elif weapon.center_x + normalizedDeltaX <= weapon.minX:
                normalizedDeltaX = weapon.minX - weapon.center_x
            if weapon.center_y + deltaY >= weapon.maxY:
                normalizedDeltaY = weapon.maxY - weapon.center_y
            elif weapon.center_y + normalizedDeltaY <= weapon.minY:
                normalizedDeltaY = weapon.minY - weapon.center_y
            # renormalize the vectors
            deltaMagnitude = math.sqrt(math.pow(normalizedDeltaX, 2) + math.pow(normalizedDeltaY, 2))
            if deltaMagnitude != 0:
                normalizedDeltaX = normalizedDeltaX / deltaMagnitude
                normalizedDeltaY = normalizedDeltaY / deltaMagnitude
            else:
                normalizedDeltaX = 0
                normalizedDeltaY = 0
            # move the current weapon toward the weapon that can be beat or away from the weapon
            # that can't be beat by a random amount
            rate = random.uniform(0.5, 3)
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
        # for rock in self.rockList:
        #     arcade.draw_circle_outline(rock.center_x, rock.center_y, 17, arcade.color.BLACK)
        # for paper in self.paperList:
        #     arcade.draw_circle_outline(paper.center_x, paper.center_y, 20, arcade.color.BLACK)
        # for scissor in self.scissorList:
        #     arcade.draw_circle_outline(scissor.center_x, scissor.center_y, 19, arcade.color.BLACK)

    # updates values 60 times a second
    def on_update(self, delta_time):
        Game.fixInitialCollisions(self)
        Game.moveWeapons(self)
        
def main():
    # create game window
    window = Game()
    # run game setup
    window.setup()
    # keep window open until user closes it
    arcade.run()

main()