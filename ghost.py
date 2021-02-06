from pkg_resources import resource_stream
import pygame
import constants

class Ghost:
    
    ghostStatus = constants.GHOST_CHASER
    gateAllowed = True
    ghostColors = [pygame.Color('RED'),pygame.Color('CYAN'),pygame.Color('PURPLE'),pygame.Color('ORANGE')]

    def __init__(self, currentLocation, mazeWidth, mazeHeight, level, ghostNum):
        self.currentDirection = constants.NO_INPUT
        self.currentLocation = currentLocation
        self.homeLocation = currentLocation
        self.mazeWidth = mazeWidth
        self.mazeHeight = mazeHeight

        self.ghostSurf = pygame.image.load("images\\ghost.png").convert()
        self.rect = self.ghostSurf.get_rect()
        self.rect.x = constants.getLocation(self.currentLocation%self.mazeWidth)
        self.rect.y = constants.getLocation(self.currentLocation//self.mazeWidth)
        self.speed = constants.SpeedControl(constants.GHOST_SPEED, constants.GHOST_MAX, level)
        self.huntFactor = constants.HUNT_FACTOR +int(min(level//3,4)/4*(constants.HUNT_MAX-constants.HUNT_FACTOR))
        self.ghostColor = self.ghostColors[ghostNum%len(self.ghostColors)]

        self.eyesSurf = pygame.image.load("images\\eyes.png").convert()
        self.eyesList = []
        for i in range(5):
            image = pygame.Surface([constants.SPRITE_SIZE, constants.SPRITE_SIZE]).convert()
            rect = pygame.Rect(0, i * constants.SPRITE_SIZE, constants.SPRITE_SIZE, constants.SPRITE_SIZE)
            image.blit(self.eyesSurf, (0, 0), rect)
            transColor = image.get_at((0,0))
            image.set_colorkey(transColor)
            self.eyesList.append(image)

    def init(self, currentLocation):
        self.ghostStatus = constants.GHOST_CHASER
        self.currentLocation = currentLocation
        self.homeLocation = currentLocation
        self.delay = 0

    def move(self, nextDirections, playerLocation, isGate):
        # move towards target location
        self.rect.x = constants.calculateMove(self.currentDirection, self.rect.x, constants.getLocation(self.currentLocation%self.mazeWidth),
                                                self.speed.move(), self.mazeWidth)
        self.rect.y = constants.calculateMove(self.currentDirection, self.rect.y, constants.getLocation(self.currentLocation//self.mazeWidth),
                                                self.speed.move(), self.mazeHeight)

        # ... if we have arrived at the target location, choose new direction
        if self.rect.x == constants.getLocation(self.currentLocation%self.mazeWidth) and self.rect.y == constants.getLocation(self.currentLocation//self.mazeWidth):
            probabilities = []
            for i in range(len(nextDirections)):
                probability = 0
                if nextDirections[i] != 0:
        # Standard probability for the possible directions
                    if constants.directionTurn(self.currentDirection,i): probability += 6
                    elif constants.directionOpposite(self.currentDirection,i):
        # .... Only allow opposite direction if continuing is not possible
                        if nextDirections[self.currentDirection] == 0: probability += 1
                    else: probability += 6
        # Factor the chance depending on the game mode
                    if not self.gateAllowed:
                        if self.ghostStatus == constants.GHOST_CHASER: 
                            if constants.directionTowards(self.currentLocation, playerLocation, i, self.mazeWidth): probability *= self.huntFactor
                        elif self.ghostStatus == constants.GHOST_CHASED:
                            if constants.directionTowards(self.currentLocation, playerLocation, i, self.mazeWidth): probability //= 3
        # Strongly favour moving to the home location when dead
                    elif self.ghostStatus == constants.GHOST_DEAD:
                        if constants.directionTowards(self.currentLocation, self.homeLocation, i, self.mazeWidth): probability *= 30           
                probabilities.append(probability)
        # Choose one of the available directions based on calculated probabilities (if on a gate just keep moving forward)
            if not isGate or nextDirections[self.currentDirection] == 0:
                self.currentDirection = constants.chooseRandomDirection(probabilities)
            if self.currentDirection > constants.NO_INPUT:
                self.currentLocation = nextDirections[self.currentDirection]

    def draw(self, displaySurf, offsetX, offsetY, chaseTime):
        # Choose a colour depending on the status
        color = self.ghostColor
        if self.ghostStatus == constants.GHOST_CHASED:
            color = pygame.Color('BLUE')
            if chaseTime  <= constants.CHASE_WARNING and chaseTime%40 >=20: color = pygame.Color('WHITE')
        # Only print a ghost body if not dead
        if self.ghostStatus != constants.GHOST_DEAD:
            color_image = constants.changeColor(self.ghostSurf, color)
            transColor = color_image.get_at((0,0))
            color_image.set_colorkey(transColor)
            displaySurf.blit(color_image,( self.rect.x + offsetX, self.rect.y + offsetY))
        # Print the eyes separately pointing in the direction of travel
        if self.currentDirection in [constants.UP, constants.DOWN, constants.LEFT, constants.RIGHT]:
            eyesImage = self.eyesList[self.currentDirection]
        else:
            eyesImage = self.eyesList[4]
        displaySurf.blit(eyesImage,( self.rect.x + offsetX, self.rect.y + offsetY))