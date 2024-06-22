import pygame, gif_pygame
import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import random

# Initialize Pygame
pygame.init()
pygame.font.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = ( 255, 0, 0)

GameFont = pygame.font.SysFont('Comic Sans MS', 30)

HandTracking = False

pTime = 0
cTime = 0
dt = 0

    
OpenHandScale = 80
CloseHandScale = 80

CharScaleY = 77
CharScaleX = 90
CharHitboxY = 60
CharHitboxX = 48


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH * 1.5)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT * 3.5)
detector = htm.handDetector()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("gud GAME")

MainMenu1 = pygame.image.load('../assets/MainMenu1.png')
MainMenu1 = pygame.transform.scale(MainMenu1, (SCREEN_WIDTH, SCREEN_HEIGHT))

MainMenu2 = pygame.image.load('../assets/MainMenu2.png')
MainMenu2 = pygame.transform.scale(MainMenu2, (SCREEN_WIDTH, SCREEN_HEIGHT))


MainMenu = pygame.image.load('../assets/MainMenu.png')
MainMenu = pygame.transform.scale(MainMenu, (SCREEN_WIDTH, SCREEN_HEIGHT))

MainMenuImg = MainMenu

Option1 = pygame.image.load('../assets/Option1.png')
Option1 = pygame.transform.scale(Option1, (SCREEN_WIDTH, SCREEN_HEIGHT))

Option2 = pygame.image.load('../assets/Option2.png')
Option2 = pygame.transform.scale(Option2, (SCREEN_WIDTH, SCREEN_HEIGHT))

Option = pygame.image.load('../assets/Option.png')
Option = pygame.transform.scale(Option, (SCREEN_WIDTH, SCREEN_HEIGHT))

OptionImg = Option

WinScreen = gif_pygame.load('../assets/WinScreen.gif')
gif_pygame.transform.scale(WinScreen, (SCREEN_WIDTH, SCREEN_HEIGHT))

BG = pygame.image.load('../assets/bg.png')
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

Char1 = pygame.image.load('../assets/char1.png')
Char1 = pygame.transform.scale(Char1, (CharScaleX, CharScaleY))

Char2 = pygame.image.load('../assets/char2.png')
Char2 = pygame.transform.scale(Char2, (CharScaleX, CharScaleY))

Char3 = pygame.image.load('../assets/char3.png')
Char3 = pygame.transform.scale(Char3, (CharScaleX, CharScaleY))

Char4 = pygame.image.load('../assets/char4.png')
Char4 = pygame.transform.scale(Char4, (CharScaleX, CharScaleY))

Char5 = pygame.image.load('../assets/char5.png')
Char5 = pygame.transform.scale(Char5, (CharScaleX, CharScaleY))


OpenHandSprite = pygame.image.load('../assets/open.png')
OpenHandSprite = pygame.transform.scale(OpenHandSprite, (OpenHandScale, OpenHandScale))
CloseHandSprite = pygame.image.load('../assets/close.png')
CloseHandSprite = pygame.transform.scale(CloseHandSprite, (CloseHandScale, CloseHandScale))

ClickSound = pygame.mixer.Sound("../assets/Beep.mp3")

HandSprite = OpenHandSprite

HandX, HandY = 0, 0
HandOpen = True

NPCs = []

TotalWave = 5
CurrentWave = 1

class NPC(pygame.sprite.Sprite):
    def __init__(self, charNum: int = 1, x: int = 0, y: int = 0, velRange: int = 40):
        pygame.sprite.Sprite.__init__(self)
        self.x = x - (CharScaleX / 2)
        self.y = y - (CharScaleY / 2)
        self.charNum = charNum
        self.velY = random.randint(-velRange, velRange)
        self.velX = random.randint(velRange // 2, velRange)
        
        match self.charNum:
            case 1:
                self.char = Char1
            case 2:
                self.char = Char2
            case 3:
                self.char = Char3
            case 4:
                self.char = Char4
            case 5:
                self.char = Char5
            case _:
                self.char = Char1


    def update(self):
        NotMove = False

        if not HandOpen:
            if (HandX - self.x) < CharHitboxX and (HandY - self.y) < CharHitboxY and (HandX - self.x) > -CharHitboxX and (HandY - self.y) > -CharHitboxY:
                self.x, self.y = HandX - ((CharScaleX / 2) - (CharScaleX / 2.1)), HandY - ((CharScaleY / 2) - (CharScaleY / 2.1))
                NotMove = True

        if not NotMove:
            self.move()

        screen.blit(self.char, (self.x, self.y))

    def move(self):
        if dt > 20: # bug fix
            return

        self.x += self.velX * dt
        self.y += self.velY * dt


def spawn_char(charNum: int = 1, x: int = SCREEN_WIDTH / 2, y: int = SCREEN_HEIGHT / 2, velRange: int = 40) -> None:
    global NPCs

    NPCs.append(NPC(charNum, x, y, velRange))


def update_npc(NPCs: list) -> None:
    for npc in NPCs:
        npc.update()

def main_menu() -> None:
    global screen, MainMenuImg, MainMenu, MainMenu1, MainMenu2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        x, y = pygame.mouse.get_pos()

        if x >= 95 and y >= 100 and x <= 430 and y <= 300:
            MainMenuImg = MainMenu2
            if pygame.mouse.get_pressed(3)[0]:
                pygame.mixer.Sound.play(ClickSound)
                return #530 460 860 660
        elif x >= 530 and y >= 460 and x <= 860 and y <= 600:
            MainMenuImg = MainMenu1
            if pygame.mouse.get_pressed(3)[0]:
                pygame.mixer.Sound.play(ClickSound)
                pygame.quit()
        else:
            MainMenuImg = MainMenu

        screen.blit(MainMenuImg, (0, 0))
        pygame.display.update()

def option_menu() -> None:
    global screen, OptionImg, Option, Option1, Option2, HandTracking

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        x, y = pygame.mouse.get_pos()

        if x >= 80 and y >= 365 and x <= 360 and y <= 520:
            OptionImg = Option1
            if pygame.mouse.get_pressed(3)[0]:
                pygame.mixer.Sound.play(ClickSound)
                HandTracking = True
                return
        elif x >= 510 and y >= 370 and x <= 930 and y <= 520:
            OptionImg = Option2
            if pygame.mouse.get_pressed(3)[0]:
                pygame.mixer.Sound.play(ClickSound)
                HandTracking = False
                return
        else:
            OptionImg = Option

        screen.blit(OptionImg, (0, 0))
        pygame.display.update()

def game_won():
    #330 480, 390 525 - yes
    #615 480, 670 525 - no
    global WinScreen, screen, CurrentWave

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        x, y = pygame.mouse.get_pos()

        if x >= 330 and y >= 480 and x <= 390 and y <= 525:
            if pygame.mouse.get_pressed(3)[0]:
                pygame.mixer.Sound.play(ClickSound)
                CurrentWave = 1
                main()
        elif x >= 615 and y >= 480 and x <= 670 and y <= 525:
            if pygame.mouse.get_pressed(3)[0]:
                pygame.mixer.Sound.play(ClickSound)
                pygame.quit()

        WinScreen.render(screen, (0, 0))
        pygame.display.update()


def main():
    global HandY, HandX, cTime, pTime, cap, detector, screen, HandSprite, OpenHandSprite, CloseHandSprite, NPCs, BG, HandOpen, dt, CurrentWave, TotalWave, RED, GREEN, BLACK, WHITE, GameFont

    WaveTime = 0
    running = True
 
    main_menu()
    option_menu()


    #### TEMP ######
    # spawn_char(1, 300, 300)
    # spawn_char(2, 300, 300)
    # spawn_char(3, 300, 300)
    # spawn_char(4, 300, 300)
    # spawn_char(5, 300, 300)
    ################
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                

        cTime = time.time()
        dt = cTime - pTime
        pTime = cTime
        WaveTime += dt

        WaveText = GameFont.render(f'Wave: {CurrentWave}/{TotalWave}', False, RED)

        screen.blit(BG, (0, 0))
        update_npc(NPCs)
        screen.blit(HandSprite, (HandX, HandY))
        screen.blit(WaveText, (0, 0))

        if CurrentWave > TotalWave:
            game_won()

        if WaveTime >= (TotalWave + 1 - CurrentWave): 
            spawn_char(random.randint(1, CurrentWave), 300, 300)
            WaveTime = 0
        
        if HandTracking:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img = detector.findHands(img, draw=True)
            lmList = detector.findPosition(img)

            if len(lmList) != 0:
                pos = lmList[0]
                HandX = pos[1]
                HandY = pos[2]
            
            if detector.isHandClosed(lmList):
                HandOpen = False
            else:
                HandOpen = True

            cv2.imshow("gud game Image", img)
            cv2.waitKey(1)

        else:
            HandX, HandY = pygame.mouse.get_pos()
            HandX, HandY = (HandX - OpenHandScale / 2), (HandY - OpenHandScale / 2)

            if pygame.mouse.get_pressed(3)[0]:
                HandOpen = False
            else:
                HandOpen = True


        if not HandOpen:
            HandSprite = CloseHandSprite
        else:
            HandSprite = OpenHandSprite

        # print(HandX, HandY)

        
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
