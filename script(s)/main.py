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

GameFont = pygame.font.SysFont('Comic Sans MS', 30)

BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = ( 255, 0, 0)


GameOpend = False
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
BoxScale = 300, 300

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH * 1.5)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT * 3.5)
detector = htm.handDetector()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Rush!")

#title screen

begin1=pygame.image.load('../assets/begin1.png')
begin1=pygame.transform.scale(begin1,(SCREEN_WIDTH, SCREEN_HEIGHT))

begin2=pygame.image.load('../assets/begin2.png')
begin2=pygame.transform.scale(begin2,(SCREEN_WIDTH, SCREEN_HEIGHT))

beginImg=begin1

#screen2

ww1=pygame.image.load('../assets/ww1.png')
ww1=pygame.transform.scale(ww1,(SCREEN_WIDTH, SCREEN_HEIGHT))


ww2=pygame.image.load('../assets/ww2.png')
ww2=pygame.transform.scale(ww2,(SCREEN_WIDTH, SCREEN_HEIGHT))


#for screen 3

wn1=pygame.image.load('../assets/wn1.png')
wn1=pygame.transform.scale(wn1,(SCREEN_WIDTH, SCREEN_HEIGHT))

wn2=pygame.image.load('../assets/wn2.png')
wn2=pygame.transform.scale(wn2,(SCREEN_WIDTH, SCREEN_HEIGHT))


#for screen4

play1=pygame.image.load('../assets/play1.png')
play1=pygame.transform.scale(play1,(SCREEN_WIDTH, SCREEN_HEIGHT))

play2=pygame.image.load('../assets/play2.png')
play2=pygame.transform.scale(play2,(SCREEN_WIDTH, SCREEN_HEIGHT))


#not being used anymore
'''
MainMenu1 = pygame.image.load('../assets/MainMenu1.png')
MainMenu1 = pygame.transform.scale(MainMenu1, (SCREEN_WIDTH, SCREEN_HEIGHT))

MainMenu2 = pygame.image.load('../assets/MainMenu2.png')
MainMenu2 = pygame.transform.scale(MainMenu2, (SCREEN_WIDTH, SCREEN_HEIGHT))


MainMenu = pygame.image.load('../assets/MainMenu.png')
MainMenu = pygame.transform.scale(MainMenu, (SCREEN_WIDTH, SCREEN_HEIGHT))'''


#for hand and keyboard option
Option1 = pygame.image.load('../assets/Option1.png')
Option1 = pygame.transform.scale(Option1, (SCREEN_WIDTH, SCREEN_HEIGHT))

Option2 = pygame.image.load('../assets/Option2.png')
Option2 = pygame.transform.scale(Option2, (SCREEN_WIDTH, SCREEN_HEIGHT))

Option = pygame.image.load('../assets/Option.png')
Option = pygame.transform.scale(Option, (SCREEN_WIDTH, SCREEN_HEIGHT))

OptionImg = Option

WinScreen = gif_pygame.load('../assets/WinScreen.gif')
gif_pygame.transform.scale(WinScreen, (SCREEN_WIDTH, SCREEN_HEIGHT))

LoseScreen = gif_pygame.load('../assets/LoseScreen.gif')
gif_pygame.transform.scale(LoseScreen, (SCREEN_WIDTH, SCREEN_HEIGHT))

BG = pygame.image.load('../assets/bg.png')
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

MagicBox = pygame.image.load('../assets/magicBox.png')
MagicBox = pygame.transform.scale(MagicBox, BoxScale)

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
bgAudio=pygame.mixer.Sound("../assets/bgaudio.mp3")

HandSprite = OpenHandSprite

HandX, HandY = 0, 0
HandOpen = True

NPCs = []

TotalWave = 5
CurrentWave = 1
CaptureGoal = 0
CurrentCapture = 0
CharEscaped = 0
maxEscape = 3
#game over after more than 3 characters have escaped the screen

class NPC(pygame.sprite.Sprite):
    def __init__(self, charNum: int = 1, x: int = 0, y: int = 0, velRange: int = 40):
        pygame.sprite.Sprite.__init__(self)
        self.x = x - (CharScaleX / 2)
        self.y = y - (CharScaleY / 2)
        self.charNum = charNum
        self.velY = random.randint(-velRange, velRange)
        self.velX = random.randint(velRange // 2, velRange)
        self.IsAlive = True
        
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
        global CurrentCapture, CharEscaped
        #(830, 575)
        #(960, 785)
        if not self.IsAlive:
            return
        
        if (830 - self.x) < CharHitboxX and (575 - self.y) < CharHitboxY and (960 - self.x) > -CharHitboxX and (785 - self.y) > -CharHitboxY:
            self.IsAlive = False
            CurrentCapture += 1
        
        if (0 - self.x) > CharHitboxX or (0 - self.y) > CharHitboxY or (SCREEN_WIDTH - self.x) < -CharHitboxX or (SCREEN_HEIGHT - self.y) < -CharHitboxY:
            self.IsAlive = False
            CharEscaped += 1

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

#first screen 
def screen1() -> None:
    global screen, begin1, begin2, beginImg, ww1, ww2, wn1, wn2, play1, play2

    # Set up the font for the title
    font = pygame.font.Font(None, 74)
    title_text = font.render("Pixel Rush!", True, (255, 255, 255))

    # Variable to control the title display
    show_title = True

    # Variable to control the image state
    state = "begin"  # Possible states: "begin", "ww", "wn", "play"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        x, y = pygame.mouse.get_pos()

        # Handle the "Begin" button hover and click

        #300 550
        #725 710
        if state == "begin":
            if 300 <= x <= 725 and 550 <= y <= 710:
                beginImg = begin2
                if pygame.mouse.get_pressed(3)[0]:
                    pygame.mixer.Sound.play(ClickSound)
                    show_title = False
                    state = "ww"
                    print("Transitioning to ww")  # Debug message
                    pygame.time.wait(500)
            else:
                beginImg = begin1

        # Handle the "ww" state hover and click
        elif state == "ww":
            if 300 <= x <= 725 and 550 <= y <= 710:
                beginImg = ww2
                if pygame.mouse.get_pressed(3)[0]:
                    pygame.mixer.Sound.play(ClickSound)
                    state = "wn"
                    print("Transitioning to wn")  # Debug message
                    pygame.time.wait(500)
                    
            else:
                beginImg = ww1

        # Handle the "wn" state hover and click
        elif state == "wn":
            if 300 <= x <= 725 and 550 <= y <= 710:
                beginImg = wn2
                if pygame.mouse.get_pressed(3)[0]:
                    pygame.mixer.Sound.play(ClickSound)
                    state = "play"
                    print("Transitioning to play")  # Debug message
                    pygame.time.wait(500)
                    
            else:
                beginImg = wn1

        # Handle the "play" state hover and click
        elif state == "play":
            if 300 <= x <= 725 and 550 <= y <= 710:
                beginImg = play2
                if pygame.mouse.get_pressed(3)[0]:
                    pygame.mixer.Sound.play(ClickSound)
                    pygame.time.wait(100)
                    return
            else:
                beginImg = play1

        # Display the background image based on state
        screen.blit(beginImg, (0, 0))

        # Display the title if show_title is True
        if show_title:
            title_rect = title_text.get_rect(center=(screen.get_width() // 2, 100))
            screen.blit(title_text, title_rect)

        # Update the display
        pygame.display.update()


#option screen where user selects hand or keyboard
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
#win screen
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

# lose screen
def game_lose():
    global LoseScreen, screen, CurrentWave, CharEscaped

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        x, y = pygame.mouse.get_pos()

        if x >= 330 and y >= 480 and x <= 390 and y <= 525:
            if pygame.mouse.get_pressed(3)[0]:
                pygame.mixer.Sound.play(ClickSound)
                CurrentWave = 1
                CharEscaped = 0
                main()
        elif x >= 615 and y >= 480 and x <= 670 and y <= 525:
            if pygame.mouse.get_pressed(3)[0]:
                pygame.mixer.Sound.play(ClickSound)
                pygame.quit()

        LoseScreen.render(screen, (0, 0))
        pygame.display.update()


def main():
    global HandY, HandX, cTime, pTime, cap, detector, screen, HandSprite, OpenHandSprite, CloseHandSprite, NPCs, BG, HandOpen, dt, CurrentWave, TotalWave, RED, GREEN, BLACK, WHITE, GameFont, MagicBox, SCREEN_WIDTH, SCREEN_HEIGHT, BoxScale, CurrentCapture, CaptureGoal, GameOpend, CharEscaped, maxEscape

    WaveTime = 0
    running = True
    
    if not GameOpend:
        screen1()
        GameOpend = True
    option_menu()

    pygame.mixer.Sound.play(bgAudio)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        cTime = time.time()
        dt = cTime - pTime
        pTime = cTime
        WaveTime += dt

        WaveText = GameFont.render(f'Wave: {CurrentWave}/{TotalWave}', False, RED)
        CaptureText = GameFont.render(f'Capture: {CurrentCapture}/{CaptureGoal}', False, RED)
        EscapeText = GameFont.render(f'Escape: {CharEscaped}/{maxEscape}', False, RED)

        screen.blit(BG, (0, 0))
        screen.blit(MagicBox, (SCREEN_WIDTH - (BoxScale[0] / 2) - 100, SCREEN_HEIGHT - (BoxScale[0] / 2) - 125))
        update_npc(NPCs)
        screen.blit(HandSprite, (HandX, HandY))
        screen.blit(WaveText, (0, 0))
        screen.blit(CaptureText, ((SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 6), 0))
        screen.blit(EscapeText, ((SCREEN_WIDTH / 2) + (SCREEN_WIDTH / 4), 0))

        CaptureGoal = CurrentWave + (CurrentWave // 2) + 1

        if CharEscaped >= maxEscape:
            game_lose()

        if CurrentCapture >= CaptureGoal:
            CurrentCapture = 0
            CurrentWave += 1

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

            cv2.imshow("Camera", img)
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
