from random import randint
import pygame
import constants

class Fruit:

    fruitCounter = 0
    fruitDisplay = 0
    fruitEaten = False
    fruitFactor = 1.5
    fruitDelay = constants.FRUIT_DELAY
    fruitPoints = constants.FRUIT_POINTS
    
    def __init__(self):
        # Load images for the player character
        self.fruitSurf = pygame.image.load("images\\fruits.png").convert()
        self.fruitList = []
        self.fruitImages = 4
       # ... Images for movement
        for i in range(self.fruitImages):
            image = pygame.Surface([constants.SPRITE_SIZE, constants.SPRITE_SIZE]).convert()
            rect = pygame.Rect(0, i * constants.SPRITE_SIZE, constants.SPRITE_SIZE, constants.SPRITE_SIZE)
            image.blit(self.fruitSurf, (0, 0), rect)
            transColor = image.get_at((0,0))
            image.set_colorkey(transColor)
            self.fruitList.append(image)
        self.rect = self.fruitSurf.get_rect()
        self.fruitDisplay = len(self.fruitList) - 1

    def init(self, currentLocation, mazeWidth, mazeHeight):
        self.fruitLocation = currentLocation
        self.mazeWidth = mazeWidth
        self.mazeHeight = mazeHeight
        self.rect.x = constants.getLocation(currentLocation%self.mazeWidth)
        self.rect.y = constants.getLocation(currentLocation//self.mazeWidth)

    def show(self, playerLocation):
        if self.fruitCounter > 0:
            self.fruitCounter -= 1
        elif self.fruitDelay <= 0:
            if abs(playerLocation%self.mazeWidth - self.fruitLocation%self.mazeWidth) + abs(playerLocation//self.mazeWidth - self.fruitLocation//self.mazeWidth) > 6 and randint(1,100) > 50:
                self.fruitCounter = constants.FRUIT_TIME
                self.fruitDelay = int(constants.FRUIT_DELAY * self.fruitFactor)
                self.fruitFactor *= self.fruitFactor
                self.fruitEaten = False
                self.fruitDisplay = (self.fruitDisplay + 1)%len(self.fruitList)
            else:
                self.fruitDelay = constants.GAME_SPEED
        else:
            self.fruitDelay -= 1

    def draw(self, displaySurf, offsetX, offsetY):
        if self.fruitCounter > 0 and not self.fruitEaten:
            displaySurf.blit(self.fruitList[self.fruitDisplay], (self.rect.x + offsetX, self.rect.y + offsetY))

