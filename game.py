import pygame
from pygame.locals import *
import constants
from maze import Maze
from player import Player
from frame import Frame
from frame import Banner
from ghost import Ghost
from fruit import Fruit

class Game:

    clock = pygame.time.Clock()
 
    def __init__(self, playerNum):
        self.frame = Frame()
        self.displaySurf = pygame.display.set_mode((self.frame.frameWidth, self.frame.frameHeight), pygame.HWSURFACE)
        self.maze = Maze(playerNum - 1)
        self.frame.playerText = str(playerNum) + 'UP'
        self.playerName = 'Player ' + str(playerNum)
        self.init(True, True)
 
    def init(self, nextLevel, newGame):
        
        self.pelletCount = 0
        self.chaseDuration = -1
        self.banners = []
        self.ghosts = []
        ghostCount = 0
        # Settings specific to a new game 
        if newGame:
            self.level = 0
            self.lives = constants.LIVES
            self.frame.score = 0
        # The maze contains the layouts of the levels
        if nextLevel: 
            self.level += 1
            self.maze.init(self.level)
        # The maze layout gives position and count of each object
        for i in range(self.maze.mazeWidth*self.maze.mazeHeight):
            if self.maze.cells[i] == constants.PLAYER:
                self.player = Player(self.maze.mazeWidth, self.maze.mazeHeight)
                self.player.init(i, self.level)
                self.fruit = Fruit()
                self.fruit.init(i, self.maze.mazeWidth, self.maze.mazeHeight)
            elif self.maze.cells[i] == constants.GHOST:
                self.ghosts.append(Ghost(i, self.maze.mazeWidth, self.maze.mazeHeight, self.level, ghostCount))
                ghostCount += 1
            elif self.maze.cells[i] == constants.PELLET or self.maze.cells[i] == constants.POWER_PELLET:
                self.pelletCount += 1
        # Centralise the maze in the frame
        self.frame.init()
        self.offsetX = (self.frame.frameWidth - (self.maze.mazeWidth * constants.BLOCK_SIZE))/2
        self.offsetY = (self.frame.frameHeight - (self.maze.mazeHeight * constants.BLOCK_SIZE))/2
        # Flag for starting to allow playing the intro
        self.starting = True
    
    def delay(self, delayTime, delayGhost):
        self.delayTime = delayTime
        self.delayGhost = delayGhost

    def special(self):
        # Give some thinking time before start moving
        if self.starting:
            self.starting = False
            self.delay(constants.START_DELAY, True)
            self.banners.append(Banner(constants.START_DELAY, self.playerName, 48, self.frame.frameWidth/2, self.frame.frameHeight/2 - 80))
            self.banners.append(Banner(constants.START_DELAY, 'Ready!', 48, self.frame.frameWidth/2, self.frame.frameHeight/2 + 20))
        # Handle losing a life
        if self.player.playerStatus == constants.PLAYER_DEAD and self.delayTime <= 0:
            if self.lives > 0: self.lives -= 1
        # ...If no more lives it's game over
            if self.lives <= 0: 
                self.delay (constants.DEATH_DELAY, False)
                self.banners.append(Banner(constants.DEATH_DELAY, self.playerName, 48, self.frame.frameWidth/2, self.frame.frameHeight/2 - 80))
                self.banners.append(Banner(constants.DEATH_DELAY + 1, 'Game Over!', 48, self.frame.frameWidth/2, self.frame.frameHeight/2 + 20))
            elif self.lives > 0:
                self.init(False, False)
        # Count down the delay timer
        if self.delayTime > 0: self.delayTime -= 1
        # Reset the board and the maze after completed
        if self.pelletCount <= 0 and self.delayTime <= 0: self.init(True, False)

    def move(self, inputDirection):
        if self.delayTime <= 0:
        # Pass available directions from the maze and the input direction for the player
            self.player.move(self.maze.testDirections(self.player.currentLocation, False), inputDirection)
        # For each ghost pass available maze directions and the player location (to influence chasing)
        if self.delayTime <= 0 or not self.delayGhost:
            for i in self.ghosts:
                i.move(self.maze.testDirections(i.currentLocation, i.gateAllowed), self.player.currentLocation,
                                                    self.maze.cells[i.currentLocation] == constants.MAZE_GATE)

    def interaction(self):
        if self.delayTime > 0: return
        ### Fruit interactions
        self.fruit.show(self.player.currentLocation)
        #### Banner interactions (clean up old banners)
        self.banners[:] = [i for i in self.banners if i.splashTime >= 0]
        #### Ghost/maze interactions
        for i in self.ghosts:
        # Once a chasing ghost leaves the starting pen don't allow it back (unless dead)
            if self.maze.cells[i.currentLocation] == constants.MAZE_GATE and i.ghostStatus == constants.GHOST_CHASER: i.gateAllowed = False
        #### Ghost only interactions
        for i in self.ghosts:
        # If a dead ghost makes it home, revive it
            if i.currentLocation == i.homeLocation and i.ghostStatus == constants.GHOST_DEAD: i.ghostStatus = constants.GHOST_CHASER
        # Reset the roles at the end of the chase
        if self.chaseDuration == 0:
                self.chaseDuration = -1
                if self.player.playerStatus != constants.PLAYER_DEAD: self.player.playerStatus = constants.PLAYER_CHASED
                for i in self.ghosts: 
                    if i.ghostStatus == constants.GHOST_CHASED: i.ghostStatus = constants.GHOST_CHASER
        # Only interact with player if he is alive
        if self.player.playerStatus != constants.PLAYER_DEAD:
        #### Ghost/player interaction ...
            for i in self.ghosts:
                if abs(i.rect.x - self.player.rect.x) + abs(i.rect.y - self.player.rect.y) < constants.SPRITE_SIZE//2:
        # ... if player is caught by chasing ghost, player is dead
                    if  i.ghostStatus == constants.GHOST_CHASER and not self.player.playerStatus == constants.PLAYER_DEAD:
                        self.player.playerStatus = constants.PLAYER_DEAD
                        self.delay(constants.DEATH_DELAY, True)
        # ... if ghost is being chased and caught, ghost is dead
                    elif i.ghostStatus == constants.GHOST_CHASED:
                        self.frame.score += self.ghostPoints
                        self.banners.append(Banner(constants.CHASE_WARNING, str(self.ghostPoints), 24, i.rect.x + self.offsetX, i.rect.y + self.offsetY))
                        self.ghostPoints *= 2
                        i.ghostStatus = constants.GHOST_DEAD
                        i.gateAllowed = True
                        self.delay( constants.DEATH_DELAY//4, True)
        #### Player/pellet interactions
        # Eat the pellet if alive
            if self.maze.cells[self.player.currentLocation] == constants.PELLET:
                self.maze.cells[self.player.currentLocation] = 0
                self.pelletCount -= 1
                self.frame.score += constants.PELLET_POINTS
        # Eat the power pellet and change roles
            elif self.maze.cells[self.player.currentLocation] == constants.POWER_PELLET:
                self.maze.cells[self.player.currentLocation] = 0
                self.pelletCount -= 1
                self.frame.score += constants.POWER_POINTS
                self.chaseDuration = constants.CHASE_DURATION
                self.player.playerStatus = constants.PLAYER_CHASER
                self.ghostPoints = constants.GHOST_POINTS
                for i in self.ghosts:
                    if i.ghostStatus == constants.GHOST_CHASER: i.ghostStatus = constants.GHOST_CHASED
        # Eat the fruit
            elif self.maze.cells[self.player.currentLocation] == constants.PLAYER and self.fruit.fruitCounter > 0 and self.fruit.fruitEaten == False:
                self.fruit.fruitEaten = True
                self.frame.score += constants.FRUIT_POINTS
                self.frame.fruits.append(self.fruit.fruitList[self.fruit.fruitDisplay])
            if self.pelletCount <= 0:
                self.delay(constants.DEATH_DELAY, False)
                self.banners.append(Banner(constants.DEATH_DELAY, 'Level Complete!', 48, self.frame.frameWidth/2, self.frame.frameHeight/2))
        # Reduce chase duration    
            if self.chaseDuration > 0: self.chaseDuration -= 1
            
    def draw(self):
        # Simply draw each object type on an empty background
        self.displaySurf.fill((0,0,0))
        self.frame.draw(self.displaySurf, self.lives, self.level)
        self.maze.draw(self.displaySurf, self.offsetX, self.offsetY)
        for i in self.ghosts: i.draw(self.displaySurf, self.offsetX, self.offsetY, self.chaseDuration)
        for i in self.banners: i.draw(self.displaySurf)
        self.fruit.draw(self.displaySurf, self.offsetX, self.offsetY)
        self.player.draw(self.displaySurf, self.offsetX, self.offsetY)
        pygame.display.flip()

    def onExecute(self, exitOnDie):
        
        startLives = self.lives
        while True:
            self.clock.tick(constants.GAME_SPEED)
            pygame.event.pump()
            keys = pygame.key.get_pressed()
    # Quit for a player
            if (keys[K_ESCAPE]):
                self.lives = 0
                exitOnDie = True
                self.player.playerStatus = constants.PLAYER_DEAD
                self.delay(constants.DEATH_DELAY, True)
                self.banners.append(Banner(constants.DEATH_DELAY + 1, 'Quitting!', 48, self.frame.frameWidth/2, 250))
    # Restart (in single player mode only, i.e. started from this class)
            elif not exitOnDie and (keys[K_SPACE]): self.init(True, True)
    # Character key presses
            if   (keys[K_RIGHT]): playerInput = constants.RIGHT
            elif (keys[K_LEFT]): playerInput = constants.LEFT
            elif (keys[K_UP]): playerInput = constants.UP
            elif (keys[K_DOWN]): playerInput = constants.DOWN
            else: playerInput = constants.NO_INPUT
    # Special events - losing life, completeing level, waiting for specified delay
            self.special()
    # ... handle end of game/life
            if self.lives < startLives and self.delayTime <= 0 and exitOnDie: break
    # Main activities: Move characters, calculate interactions, draw the screen
            self.move(playerInput)
            self.interaction()
            self.draw()
                    
if __name__ == "__main__" :
    theApp = Game(1)
    theApp.onExecute(False)
    pygame.quit()
