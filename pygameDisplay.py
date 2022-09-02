import pygame, os, sys
from pygame.locals import *
import readDMX
import sendsacn
import patching
import time


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#Init Modules
pygame.init()
screen = pygame.display.set_mode((1280,1020))
pygame.display.set_caption('sACNVisu')
#file = resource_path('jestersniffer.png')
#icon = pygame.image.load(file)
#pygame.display.set_icon(icon)


#readDMX.init()
#sendsacn.init()

#Colour Consts
BLACK = (0,0,0)
WHITE = (255,255,255)
LGREY = (200,200,200)
DGREY = (50,50,50)
DRED = (150,0,0)


font = pygame.font.SysFont('Sans', 100)
extraPatch = False

def main():
    #main loop
    readDMX.init()
    while True:
        drawScreen()
        checkForEvent()
        time.sleep(0.001)

def drawScreen():
    screen.fill(BLACK)
    if readDMX.connected:
        #get dmx array from PhantomJester
        dmx = readDMX.getDMX()

        unpatchedDmx = list(dmx)

        if extraPatch:
            dmx = patching.patch(dmx)
        #send dmx array through sacn (to capture)
        #sendsacn.send(dmx)

        
        dmx = unpatchedDmx

        #Visualise DMX in Pygame window
        highlightedY = pygame.mouse.get_pos()[1]//255
        highlightedX = pygame.mouse.get_pos()[0]//10+1
        for y in range(4):
            for x in range(128):
                #if not readDMX.patched[y*128+x]:
                #    pygame.draw.rect(screen, DRED, (x*10, y*255, 10, 255))
                if y == highlightedY and x == highlightedX-1:
                    col = LGREY
                    pygame.draw.rect(screen, DGREY, (x*10, y*255, 10, 255))
                else:
                    col = WHITE
                pygame.draw.rect(screen, col, (x*10, (y*255)+(255-dmx[y*128+x]), 10, dmx[y*128+x]))
        text = font.render(str(highlightedX+128*highlightedY), True,LGREY)
        screen.blit(text, (0,0))
        try:
            text = font.render(readDMX.desk+' v'+readDMX.version, True,LGREY)
            screen.blit(text, (10,924))
        except:
            pass

    else:
        dmx = [0 for x in range(512)]
        text = font.render('Waiting for sACN signal', True,LGREY)
        screen.blit(text, (10,924))
        #readDMX.init()
    pygame.display.update()

def close():
    #Quit all modules
    readDMX.quit()
    #sendsacn.quit()
    pygame.quit()
    sys.exit()

def checkForEvent():
    global extraPatch
    #Check for key inputs
    for event in pygame.event.get():
        if event.type == QUIT:
            close()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                close()
            if event.key == K_F5:
                #Restart connection to PhantomJester
                readDMX.init()
            if event.key == K_F4:
                extraPatch = not extraPatch

if __name__ == '__main__':
    main()
