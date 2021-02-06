import pygame
from pygame.locals import *
import constants
from game import Game
from splash import splashScreen

class GameStarter:
 
    clock = pygame.time.Clock()
    
    def __init__(self):
        self.splash = splashScreen()
        self.hiScore = self.splash.topScores[0][0]

    def special(self, players):
        # Start the game ...
        if not players > 0: return
        # ... create the players
        self.playerList = []
        for i in range(players):
            self.playerList.append(Game(i + 1))
        lives = 1
        # ... Play through all the lives of all the players ...
        while lives > 0:
            lives = 0
            for i in range(len(self.playerList)):
        # ... ...keep track of high scoring
                if self.hiScore > self.playerList[i].frame.hiScore: self.playerList[i].frame.hiScore = self.hiScore
        # ... ...execute the players turn
                if self.playerList[i].lives > 0:
                    self.playerList[i].onExecute(True)
                    lives += self.playerList[i].lives
                    if self.playerList[i].lives == 0:
                        self.splash.updateHiScore(self.playerList[i].frame.score, self.playerList[i].level)
        # ... ...if high score increased record it
                    if self.hiScore < self.playerList[i].frame.hiScore: self.hiScore = self.playerList[i].frame.hiScore
    
    def move(self):
        self.splash.move()

    def draw(self):
        self.splash.draw()
        pygame.display.flip()
        
    def onExecute(self):

        while True:
            self.clock.tick(constants.GAME_SPEED)
            pygame.event.pump()
            keys = pygame.key.get_pressed()
    # Keys to restart and exit within standard game
            if (keys[K_ESCAPE]): break
            players = 0
    # Character key presses
            if   (keys[K_1]) or (keys[K_KP_1]): players = 1
            elif (keys[K_2]) or (keys[K_KP_2]): players = 2
            elif (keys[K_3]) or (keys[K_KP_3]): players = 3
            elif (keys[K_4]) or (keys[K_KP_4]): players = 4

            self.special(players)
            self.move()
            self.draw()

if __name__ == "__main__" :
    theApp = GameStarter()
    theApp.onExecute()
    pygame.quit()
