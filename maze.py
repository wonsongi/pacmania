import pygame
import constants
from levels import Level

class Maze:

    mazeColors = [pygame.Color('BLUE'),pygame.Color('YELLOW'),pygame.Color('WHITE'),pygame.Color('GREEN')]

    def __init__(self, playerNum):
        self.levels = Level()
        self.blockSurf = pygame.image.load("images\\blocks.png").convert()
        self.blockList = []
        for i in range(16):
            image = pygame.Surface([constants.BLOCK_SIZE, constants.BLOCK_SIZE]).convert()
            rect = pygame.Rect(0, i * constants.BLOCK_SIZE, constants.BLOCK_SIZE, constants.BLOCK_SIZE)
            image.blit(self.blockSurf, (0, 0), rect)
            self.blockList.append(image)
        self.pelletSurf = pygame.image.load("images\\pellet.png").convert()
        transColor = self.pelletSurf.get_at((0,0))
        self.pelletSurf.set_colorkey(transColor)
        self.mazeColor = self.mazeColors[playerNum%len(self.mazeColors)]
        self.cells = []

    def init(self, level):
        # Loop around the levels
        mazeNum = level%len(self.levels.mazes) - 1
        self.cells = []
        # Copy the cells from the level and the blocks
        for i in self.levels.mazes[mazeNum].cells:
            self.cells.append(i)
        self.mazeWidth = self.levels.mazes[mazeNum].mazeWidth
        self.mazeHeight = self.levels.mazes[mazeNum].mazeHeight

    def testDirections(self, currentLocation, gateAllowed):
        nextDirection = [-self.mazeWidth,  -1, self.mazeWidth,1] # Postion: 0 = Up, 1 = Left, 2 = Down, 3 = Right
        nextLocation = []
        for i in nextDirection:
            nextLocation.append(self.testDirection( currentLocation, i, gateAllowed))
        return nextLocation

    def testDirection(self, currentLocation, locationAdjustment, gateAllowed):
        nextLocation = currentLocation + locationAdjustment
        # Handle teleport if we go off the end of a row
        if currentLocation//self.mazeWidth != nextLocation//self.mazeWidth and currentLocation%self.mazeWidth != nextLocation%self.mazeWidth:
            nextLocation += (-locationAdjustment * self.mazeWidth)
        # Handle teleport if we go off the top/bottom
        if nextLocation < 0 or nextLocation >= self.mazeWidth*self.mazeHeight:
            nextLocation += (-locationAdjustment * self.mazeHeight)
        # Check next square is not part of the maze walls
        if self.cells[nextLocation] == constants.MAZE_BLOCK:
            return 0
        elif self.cells[nextLocation] == constants.MAZE_GATE:
        # For gate check if allowed (i.e. only ghosts)
            if gateAllowed: return nextLocation
            else: return 0
        else: return nextLocation

    def getBlockType(self,currentLocation):
        # Determine which block type to draw based on connections required to blocks around it
        blockTest = [0]*9
        # ... Identify blocks within a 3*3 square around the currentLocation
        for i in range(9):
            nextLocation = currentLocation + (i//3 - 1) * self.mazeWidth + i%3 - 1
        # ... ... outside maze vertically
            if nextLocation < 0 or nextLocation > (self.mazeWidth * self.mazeHeight) - 1: blockTest[i] = -1
        # ... ...outside maze horizontally (i.e. we are in first column and move left or last column and move right)
            elif currentLocation%self.mazeWidth == 0 and i%3 == 0: blockTest[i] = -1
            elif currentLocation%self.mazeWidth == self.mazeWidth - 1 and i%3 == 2: blockTest[i] = -1
        # ... ...in maze as a block (i.e. requires a connection)
            elif self.cells[nextLocation] in [constants.MAZE_BLOCK, constants.MAZE_GATE]: blockTest[i] = 1

        # Determine which of the directions reqire connection
        factor = 1 #Use a binary notation for required connections ... 1 UP, 2 LEFT, 4 DOWN, 8 RIGHT
        blockType = 0
        for i in range(4):
        # ...Require connection if the block above is filled, but not everything around it
            adjacentBlocks = 0
            for j in range(6):
                if blockTest[j] == 0: adjacentBlocks += 1
            if blockTest[1] == 1 and adjacentBlocks > 0: blockType += factor
        # ...reset the maze for the next check 
        # by rotating it 90 degrees, so we cycle through UP, LEFT, DOWN, RIGHT
            rotateTest = [0]*9
            for k in range(9): rotateTest[(3* k) + 2 - (10 * (k//3))] = blockTest[k]
            blockTest = rotateTest
            factor *= 2 # ...next direction (*2 in binary)
        return blockType

    def move(self):
        pass
    
    def draw(self, displaySurf, offsetX, offsetY):
        for i in range(0,self.mazeWidth*self.mazeHeight):
            if self.cells[i] == constants.MAZE_BLOCK:                    
                color = self.mazeColor
                color_image = self.blockList[self.getBlockType(i)]
                color_image = constants.changeColor(color_image,color)
                displaySurf.blit(color_image,((i%self.mazeWidth * constants.BLOCK_SIZE) + offsetX , (i//self.mazeWidth * constants.BLOCK_SIZE) + offsetY))
            elif self.cells[i] == constants.MAZE_GATE:
                color = pygame.Color('MAGENTA')
                color_image = self.blockList[self.getBlockType(i)]
                color_image = constants.changeColor(color_image,color)
                displaySurf.blit(color_image,((i%self.mazeWidth * constants.BLOCK_SIZE) + offsetX , (i//self.mazeWidth * constants.BLOCK_SIZE) + offsetY))
            elif self.cells[i] == constants.PELLET:
                displaySurf.blit(self.pelletSurf,((i%self.mazeWidth * constants.BLOCK_SIZE) + offsetX , (i//self.mazeWidth * constants.BLOCK_SIZE) + offsetY))
            elif self.cells[i] == constants.POWER_PELLET:
                color = pygame.Color('MAGENTA')
                color_image = constants.changeColor(self.pelletSurf, color)
                transColor = color_image.get_at((0,0))
                color_image.set_colorkey(transColor)
                displaySurf.blit(color_image,((i%self.mazeWidth * constants.BLOCK_SIZE) + offsetX , (i//self.mazeWidth * constants.BLOCK_SIZE) + offsetY))
