import pygame
import constants
from frame import Frame
from player import Player
from ghost import Ghost
from initials import Initials

class splashScreen:

    topScores = [[50000, 'AAA', 10],
                 [45000, 'BBB', 9],
                 [40000, 'CCC', 8],
                 [35000, 'DDD', 7],
                 [30000, 'EEE', 6],
                 [25000, 'FFF', 5],
                 [20000, 'GGG', 4],
                 [15000, 'HHH', 3],
                 [10000, 'III', 2],
                 [5000,  'JJJ', 1]]

    def __init__(self):

        self.frame = Frame()
        self.displaySurf = pygame.display.set_mode((self.frame.frameWidth, self.frame.frameHeight), pygame.HWSURFACE)

        self.titleSurf = pygame.image.load("images\\title.png").convert()
        transColor = self.titleSurf.get_at((0,0))
        self.titleSurf.set_colorkey(transColor)

        self.initials = Initials(self.frame.frameWidth, self.frame.frameHeight)

        pygame.font.init()
        self.scoreFont = pygame.font.SysFont('Courier New', 24)
        self.scoreFont.bold = True

        # Pretent the whole screen is a maze in order we can animate the characters 
        self.mazeWidth = self.frame.frameWidth//constants.BLOCK_SIZE
        self.frameHeight = self.frame.frameHeight//constants.BLOCK_SIZE

        # set parameters for characters
        self.playerStartBlock = 30 * self.mazeWidth + 24
        self.playerEndBlock = 30 * self.mazeWidth + 2
        self.player = Player(self.mazeWidth, self.frameHeight)
        self.player.init(self.playerStartBlock,1)
        self.ghosts = []
        for i in range(4):
            self.ghosts.append(Ghost(self.playerStartBlock + 2 + i, self.mazeWidth, self.frameHeight, 7, i))

    def updateHiScore(self, newScore, level):

        topScoreTemp = []
        for i in self.topScores:
            if newScore > i[0]:
                topScoreTemp.append([newScore, self.initials.getInitials(self.displaySurf), level])
                newScore = 0
            topScoreTemp.append(i)
        self.topScores = []
        for i in range(10): self.topScores.append(topScoreTemp[i])

    def move(self):
        # Splash screen animations...
        # ... player
        if self.player.currentDirection in [constants.LEFT, constants.NO_INPUT]:
            location, direction = [0,self.playerEndBlock,0,0], constants.LEFT
            if self.player.rect.x <= self.playerEndBlock%self.mazeWidth * constants.BLOCK_SIZE: location, direction = [0,0,0,self.playerStartBlock], constants.RIGHT
        else:
            location, direction = [0,0,0,self.playerStartBlock], constants.RIGHT
            if self.player.rect.x >= (self.playerStartBlock - 1)%self.mazeWidth * constants.BLOCK_SIZE: location, direction = [0,self.playerEndBlock,0,0], constants.LEFT
        self.player.move(location, direction)
        # ... ghost
        for i in range(len(self.ghosts)):
            if self.player.currentDirection == constants.LEFT:
                location, ghostStatus = [0,(self.playerEndBlock+ 5 + i),0,0], constants.GHOST_CHASER
            else:
                location, ghostStatus = [0,0,0,(self.playerStartBlock + 2 + i)], constants.GHOST_CHASED
            self.ghosts[i].ghostStatus = ghostStatus
            self.ghosts[i].move(location, 1, False)

    def draw(self):
        self.displaySurf.fill((0,0,0))
        titleRect = self.titleSurf.get_rect(center=(self.frame.frameWidth/2, 100))
        self.displaySurf.blit(self.titleSurf, titleRect)
        # Print Highscore Table
        self.screenText = self.scoreFont.render('{:>7}  {:^6}  {:<4}'.format('Score', 'Player', 'Level'), False, 'RED')
        textRect = self.screenText.get_rect(center=(self.frame.frameWidth/2, 250))
        self.displaySurf.blit(self.screenText,textRect)
        for i in range(len(self.topScores)):
            self.screenText = self.scoreFont.render('{:>7}  {:^6}  {:<4}'.format(self.topScores[i][0], self.topScores[i][1], self.topScores[i][2]), False, 'WHITE')
            textRect = self.screenText.get_rect(center=(self.frame.frameWidth/2, 40*i + 300))
            self.displaySurf.blit(self.screenText,textRect)

        self.player.draw(self.displaySurf, 0, 0)
        for i in self.ghosts: i.draw(self.displaySurf, 0, 0, 1000)

        self.screenText = self.scoreFont.render('Select 1-4 players to start a game', False, 'RED')
        textRect = self.screenText.get_rect(center=(self.frame.frameWidth/2, self.frame.frameHeight - 100))
        self.displaySurf.blit(self.screenText,textRect)
