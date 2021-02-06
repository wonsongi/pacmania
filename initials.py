import pygame
import pygame.draw
from pygame.locals import *
import constants

class Initials:

    clock = pygame.time.Clock()
    initialWidth = 400
    initialHeight = 200

    def __init__(self, frameWidth, frameHeight):
        pygame.font.init()
        self.labelFont = pygame.font.SysFont('Courier New', 32)
        self.labelFont.bold = True
        self.initials = [0, 0, 0]
        self.currentPosition = 0
        self.stepNumber = 0
        self.text = ''
        self.frameWidth = frameWidth
        self.frameHeight = frameHeight

    def init(self):
        pass

    def move(self, playerInput):
        if self.stepNumber > 0:
            self.stepNumber -= 1
        elif playerInput in [constants.UP, constants.DOWN]:
            if playerInput == constants.UP:          
                self.initials[self.currentPosition] += 1
            elif playerInput == constants.DOWN:          
                self.initials[self.currentPosition] -= 1
            self.initials[self.currentPosition] %= len(constants.CHARS)
            self.stepNumber = constants.GAME_SPEED/6
        elif playerInput == constants.LEFT:
            if self.currentPosition > 0:
                self.currentPosition -= 1
                self.stepNumber = constants.GAME_SPEED/3
        elif playerInput == constants.RIGHT:
            if self.currentPosition < len(self.initials) - 1:
                self.currentPosition += 1
                self.stepNumber = constants.GAME_SPEED/3
        self.text = ''
        for i in self.initials: self.text = self.text + constants.CHARS[i:i + 1]

    def draw(self, displaySurf):
        backdrop = pygame.draw.rect(displaySurf,pygame.Color('BLACK'),((self.frameWidth - self.initialWidth)/2,
                                                    (self.frameHeight - self.initialHeight)/2, self.initialWidth, self.initialHeight))
        self.screenText = self.labelFont.render('Enter Name:', False, ('WHITE'))
        textRect = self.screenText.get_rect(center=(backdrop.x + backdrop.width/2, backdrop.y + backdrop.height/2 - 10))
        displaySurf.blit(self.screenText,textRect)
        for i in range(len(self.initials)):
            text = constants.CHARS[self.initials[i]:self.initials[i] + 1]
            if i == self.currentPosition:
                self.screenText = self.labelFont.render(text, False, 'RED')
            else:
                self.screenText = self.labelFont.render(text, False, 'WHITE')
            textRect = self.screenText.get_rect(center=(backdrop.x + backdrop.width/2 + ((i - (len(self.initials) - 1)/2) * 30 ), backdrop.y + backdrop.height/2 + 30))
            displaySurf.blit(self.screenText,textRect)
        pygame.display.flip()

    def getInitials(self, displaySurf):

        # Get initials
        while True:
            self.clock.tick(constants.GAME_SPEED)
            pygame.event.pump()
            keys = pygame.key.get_pressed()
        # Quit
            if (keys[K_ESCAPE] or keys[K_KP_ENTER] or keys[K_RETURN]): return self.text
        # Character key presses
            if   (keys[K_RIGHT]): playerInput = constants.RIGHT
            elif (keys[K_LEFT]): playerInput = constants.LEFT
            elif (keys[K_UP]): playerInput = constants.UP
            elif (keys[K_DOWN]): playerInput = constants.DOWN
            else: playerInput = constants.NO_INPUT

            self.move(playerInput)
            self.draw(displaySurf)

if __name__ == "__main__" :
    theApp = Initials(800,950)
    disp = pygame.display.set_mode((800, 950), pygame.HWSURFACE)
    print (theApp.getInitials(disp))
    pygame.quit()
