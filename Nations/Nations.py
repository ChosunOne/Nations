import os
import sys
import pygame
from world import world
import tile
from pygame.locals import *


if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

class PyManMain:
    """The main PyMan class - this class handles the main initialization and creating of the game"""

    def __init__(self, width=800, height=400):
        #Initialize the game
        pygame.init()
        self.fpsClock = pygame.time.Clock()
        #Set the window size
        self.width = width
        self.height = height
        #Change the screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Nations')
        #Define RGB
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)
        self.fontObj = pygame.font.Font('freesansbold.ttf', 24)
        msg = 'Nations Initialized'
        #Initialize Mouse position
        self.mousex, self.mousey = (0, 0)
        #Initialize Message
        self.msg = ''
        self.earth = world(width=self.width, height=self.height, viewMode = 1)

    def MainLoop(self):
        """This is the main loop of the game"""
        tiles = self.earth.tiles
        screen = self.screen

        clickX = 0
        clickY = 0
        timer = 0
        while True:
            if timer > 10000:
                timer = 0

                    

            screen.fill(pygame.Color(0,0,0))
            w = self.width
            h = self.height

            screenArr = pygame.PixelArray(screen)
            for x in range(0, w, 1):
                for y in range(0, h, 1):
                    screenArr[x][y] = tiles[(x, y)].color
            del screenArr

            msgSurfaceObj = self.fontObj.render(self.msg, False, self.red)
            msgRectObj = msgSurfaceObj.get_rect()
            msgRectObj.topleft = (clickX, clickY)
            screen.blit(msgSurfaceObj, msgRectObj)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEMOTION:
                    self.mousex, self.mousey = event.pos

                elif event.type == MOUSEBUTTONUP:
                    clickX, clickY = event.pos
                    t = tiles[(clickX, clickY)]
                    if event.button == 1:
                        #Left Click
                        #self.msg = 'Biome: ' + str(t.biome)
                        print('Biome', str(t.biome))
                    elif event.button == 2:
                        #Middle Click
                        try:
                            #self.msg = t.owner.readout
                            t.owner.updateReadout()
                            print(t.owner.readout)
                        except:
                            #self.msg = 'Unclaimed Land'
                            print('Unclaimed Land')
                    elif event.button == 3:
                        #Right Click
                        #self.msg = 'Terrain: ' + str(t.terrain)
                        t.updateTileReadout()
                        print(t.readout)
                    elif event.button == 4:
                        #Scroll up
                        self.earth.changeViewMode(0)
                    elif event.button == 5:
                        #Scroll down
                        self.earth.changeViewMode(1)

                elif event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.msg = 'left arrow key'
                    elif event.key == K_RIGHT:
                        print('Simulating 10 years')
                        self.earth.updateYears(10)
                        self.earth.changeViewMode(1)
                    elif event.key == K_UP:
                        self.msg = 'up arrow key'
                    elif event.key == K_DOWN:
                        self.msg = 'down arrow key'
                    elif event.key == K_a:
                        self.msg = 'a key'
                    elif event.key == K_RETURN:
                        self.earth.updateWorld()
                        self.earth.changeViewMode(1)      
                    elif event.key == K_BACKQUOTE:
                        command = input('\n')
                        while command != 'quit':
                            try:
                                eval(command)
                                command = input('\n')
                            except:
                                print('Exception executing command')
                                command = input('\n')
                    elif event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))

            pygame.display.update()
            self.fpsClock.tick(30)
            timer += 1

if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()