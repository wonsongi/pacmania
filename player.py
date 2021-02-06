import pygame
import constants

class Player:
    currentLocation = 0
    currentDirection = constants.NO_INPUT
    playerStatus = constants.PLAYER_CHASED

    def __init__(self, mazeWidth, mazeHeight):
        # Load images for the player character
        self.playerSurf = pygame.image.load("images\\players.png").convert()
        self.playerList = []
        self.playerFrames = 8
        self.dyingFrames = 16
        # ... Images for movement
        for i in range(self.playerFrames * 4):
            image = pygame.Surface([constants.SPRITE_SIZE, constants.SPRITE_SIZE]).convert()
            rect = pygame.Rect(i//self.playerFrames * constants.SPRITE_SIZE, i%self.playerFrames * constants.SPRITE_SIZE, constants.SPRITE_SIZE, constants.SPRITE_SIZE)
            image.blit(self.playerSurf, (0, 0), rect)
            transColor = image.get_at((0,0))
            image.set_colorkey(transColor)
            self.playerList.append(image)
        # ... Images for dying
        self.playerSurf = pygame.image.load("images\\dying.png").convert()
        for i in range(self.dyingFrames):
            image = pygame.Surface([constants.SPRITE_SIZE, constants.SPRITE_SIZE]).convert()
            rect = pygame.Rect(0, i * constants.SPRITE_SIZE, constants.SPRITE_SIZE, constants.SPRITE_SIZE)
            image.blit(self.playerSurf, (0, 0), rect)
            transColor = image.get_at((0,0))
            image.set_colorkey(transColor)
            self.playerList.append(image)
        self.playerSurf = self.playerList[self.playerFrames]
        self.rect = self.playerSurf.get_rect()
        self.mazeWidth = mazeWidth
        self.mazeHeight = mazeHeight
        self.imageStep = 0
        self.speed = None

    def init(self, currentLocation, level):
        self.speed = constants.SpeedControl(constants.PLAYER_SPEED, constants.PLAYER_MAX, level)
        self.playerStatus = constants.PLAYER_CHASED
        self.currentLocation = currentLocation
        self.rect.x = constants.getLocation(self.currentLocation%self.mazeWidth)
        self.rect.y = constants.getLocation(self.currentLocation//self.mazeWidth)
        self.imageStep = 0

    def move(self, nextDirections, inputDirection):
        # Don't move if dead!
        if self.playerStatus == constants.PLAYER_DEAD: return
        # move towards location
        self.rect.x = constants.calculateMove(self.currentDirection, self.rect.x, constants.getLocation(self.currentLocation%self.mazeWidth),
                                                self.speed.move(), self.mazeWidth)
        self.rect.y = constants.calculateMove(self.currentDirection, self.rect.y, constants.getLocation(self.currentLocation//self.mazeWidth),
                                                self.speed.move(), self.mazeHeight)
        
        # Allow opposite direction at any time
        if constants.directionOpposite(self.currentDirection, inputDirection) and inputDirection >= 0 and nextDirections[inputDirection] != 0:
                self.currentDirection = inputDirection
                self.currentLocation = nextDirections[self.currentDirection]
        # Only allow turning once we have arrived at the destination
        elif self.rect.x == constants.getLocation(self.currentLocation%self.mazeWidth) and self.rect.y == constants.getLocation(self.currentLocation//self.mazeWidth):
            if inputDirection >= 0 and nextDirections[inputDirection] != 0:
                self.currentDirection = inputDirection
                self.currentLocation = nextDirections[self.currentDirection]
        # If no valid direction given, keep on going
            elif self.currentDirection >= 0 and nextDirections[self.currentDirection] != 0:
                self.currentLocation = nextDirections[self.currentDirection]

    def draw(self, displaySurf, offsetX, offsetY):
        if self.playerStatus == constants.PLAYER_DEAD:
            if self.imageStep > self.dyingFrames * 9 - 1: self.imageStep = 0
            imageNum = (self.playerFrames * 4) + self.imageStep//9
        else:
        # Protect against no current direction
            if self.currentDirection in [constants.UP, constants.LEFT, constants.DOWN, constants.RIGHT]: direction = self.currentDirection 
            else: direction = constants.RIGHT
            if self.imageStep > (self.playerFrames - 1)* 4: self.imageStep = 0
            imageNum = direction * self.playerFrames + (self.playerFrames - 1 - abs((self.playerFrames - 1) - self.imageStep//2))

        # Each direction has 8 animations, cycle through them 0...7...0 etc. As refresh rate is high only change every 2nd frame to slow down
        displaySurf.blit(self.playerList[imageNum], (self.rect.x + offsetX, self.rect.y + offsetY))
        self.imageStep += 1