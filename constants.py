"""
Global constants
"""
from random import randint
import pygame
from pygame import constants

# Values for maze blocks
PELLET = 1
POWER_PELLET = 2
PLAYER = 3
GHOST = 4
MAZE_GATE = 8
MAZE_BLOCK = 9

# Values for character status
PLAYER_CHASER = 0
PLAYER_CHASED = 1
PLAYER_DEAD = 2
GHOST_CHASER = 0
GHOST_CHASED = 1
GHOST_DEAD = 2

# Difficulty values
GAME_SPEED = 60         #Frames per second
GHOST_SPEED = 150       #Pixels per second
GHOST_MAX = 300
PLAYER_SPEED = 200
PLAYER_MAX = 280
HUNT_FACTOR = 2         #Probability to chase
HUNT_MAX = 30
FRUIT_DELAY = 10 * GAME_SPEED  #Seconds
FRUIT_TIME = 7 * GAME_SPEED
CHASE_DURATION = 9 * GAME_SPEED 
CHASE_WARNING = 2 * GAME_SPEED
START_DELAY = 2 * GAME_SPEED
DEATH_DELAY = 2 * GAME_SPEED

# Screen size
BLOCK_SIZE = 25
SPRITE_SIZE = 45

# Directions
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
NO_INPUT = -1

# Points
PELLET_POINTS = 10
POWER_POINTS = 50
GHOST_POINTS = 200
FRUIT_POINTS = 400

CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.,_-@()#[]<>'

LIVES = 3
"""
Global functions
"""
def getLocation(inputVal):
    # Convert a block number to pixel position
    return ((inputVal * BLOCK_SIZE) - (SPRITE_SIZE-BLOCK_SIZE)//2 )

def calculateMove(currentDirection, spritePosition, targetPosition, moveDistance, totalBlocks):
    # If we have already reached the location, go no further
    if currentDirection == NO_INPUT or spritePosition == targetPosition:
        spritePosition = targetPosition
    else:
    # Otherwise move the object
        if currentDirection in [UP, LEFT]: moveDirection = -1
        else: moveDirection = 1
        spritePosition += moveDistance * moveDirection
        # ... handle warp across screen - totalBlocks is the width or height of the maze
        if (spritePosition < -BLOCK_SIZE/2) or (spritePosition > (totalBlocks + 1/2) * BLOCK_SIZE):
            spritePosition += (totalBlocks + 1) * BLOCK_SIZE * -moveDirection
        # ... handle rounding for when we are close
        if abs(spritePosition - targetPosition) < moveDistance: spritePosition = targetPosition
    return spritePosition

def directionOpposite(currentDirection, newDirection):
    # Is the new direction opposite to the current
    if abs(currentDirection - newDirection) == 2:
        return True
    else:
        return False

def directionTurn(currentDirection, newDirection):
    # Is the new direction a turn
    if abs(currentDirection - newDirection)%2 == 0:
        return False
    else:
        return True

def directionTowards(startLocation, endLocation, moveDirection, totalWidth):
        # If moving horizontally check if direction is towards .. left = 1 maps to -1, right = 3 maps to 1
        if moveDirection in [LEFT, RIGHT] and (startLocation%totalWidth - endLocation%totalWidth) * (moveDirection-2) < 0:
            return True
        # If moving vertically check if direction is towards
        elif moveDirection in [UP, DOWN] and (startLocation//totalWidth - endLocation//totalWidth) * (moveDirection-1) < 0:
            return True
        else:
            return False

def chooseRandomDirection(probabilities):
    if sum(probabilities) <= 0: return NO_INPUT
    # Take a random point in the probability array (weighted by the values of each)
    newDirection = randint(1,sum(probabilities))
    # Determine which of the directions is chosen
    for i in range(len(probabilities)):
        if probabilities[i] >= newDirection: return i
        else: newDirection -= probabilities[i]

def changeColor(image, color):
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(color)
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
    return finalImage

class SpeedControl:
    # Work out how many pixels to move in each frame (as we can't move fractions of a pixel)
    def __init__(self, low_speed, high_speed, level):
        self.steps = []
        self.stepNum = 0
    # Increment the speed after every 4 levels up to 4 times
        speed = low_speed + min(level//4,4)/4*(high_speed-low_speed)
    # Create a list of whole pixels movements
        for i in range(GAME_SPEED):
            self.steps.append(int(speed/GAME_SPEED*(i+1))-int(speed/GAME_SPEED*i))
    # retrieve next pixel in the list
    def move(self):
        self.stepNum = (self.stepNum + 1)%GAME_SPEED
        return self.steps[self.stepNum]