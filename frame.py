import pygame
import constants

class Banner:

    def __init__(self, splashTime, splashText, splashSize, locationX, locationY):
        pygame.font.init()
        self.splashFont = pygame.font.SysFont('Comic Sans MS', splashSize)
        self.splashFont.bold = True
        self.splashTime = splashTime
        self.splashText = self.splashFont.render(splashText, False, 'RED')
        self.splashRect = self.splashText.get_rect(center=(locationX, locationY))

    def move(self):
        pass

    def draw(self, displaySurf):
        if self.splashTime > 0: self.splashTime -= 1
        if self.splashTime > 0:
            displaySurf.blit(self.splashText,self.splashRect)    

class Frame:

    frameWidth = 800
    frameHeight = 950
    frameHeader = 75
    frameFooter = 75
    score = 0
    hiScore = 0

    def __init__(self):
        pygame.font.init()
        self.scoreFont = pygame.font.SysFont('Courier New', 32)
        self.scoreFont.bold = True
        self.playerText = '- UP'
 
    def init(self):
        self.playerSurf = pygame.image.load("images\\player.png").convert()
        transColor = self.playerSurf.get_at((0,0))
        self.playerSurf.set_colorkey(transColor)
        self.rect = self.playerSurf.get_rect()
        self.fruits = []

    def recordInitials(self, score, level, displaySurf: pygame.Surface):
        return 'DAD'

    def move(self):
        pass
    
    def draw(self, displaySurf, lives, level):
        if self.score > self.hiScore: self.hiScore = self.score
        self.screenText = self.scoreFont.render(self.playerText, False, 'WHITE')
        textRect = self.screenText.get_rect(midright=(200, 20))
        displaySurf.blit(self.screenText,textRect)
        self.screenText = self.scoreFont.render(str(self.score), False, ('WHITE'))
        textRect = self.screenText.get_rect(midright=(200, 50))
        displaySurf.blit(self.screenText,textRect)
        self.screenText = self.scoreFont.render('HIGH SCORE', False, ('WHITE'))
        textRect = self.screenText.get_rect(center=(self.frameWidth/2, 20))
        displaySurf.blit(self.screenText,textRect)
        self.screenText = self.scoreFont.render(str(self.hiScore), False, ('WHITE'))
        textRect = self.screenText.get_rect(center=(self.frameWidth/2, 50))
        displaySurf.blit(self.screenText,textRect)
        self.screenText = self.scoreFont.render('LEVEL', False, ('WHITE'))
        textRect = self.screenText.get_rect(midleft=(self.frameWidth - 200, 20))
        displaySurf.blit(self.screenText,textRect)
        self.screenText = self.scoreFont.render(str(level), False, ('WHITE'))
        textRect = self.screenText.get_rect(midleft=(self.frameWidth - 200, 50))
        displaySurf.blit(self.screenText,textRect)
        
        positionX = 100
        for i in range(lives):
            displaySurf.blit(self.playerSurf, (positionX, self.frameHeight-self.frameFooter))
            positionX += constants.SPRITE_SIZE/1.5 + 10

        positionX = 700
        for i in range(min(len(self.fruits),5)):
            displaySurf.blit(self.fruits[i], (positionX , self.frameHeight-self.frameFooter))
            positionX -= constants.SPRITE_SIZE/1.5 + 10
