from operator import __not__
import sys, pygame
import time
pygame.init()

# --- Settings ---
size = width, height = 1280, 720
black = 0, 0, 0
BLUE = (0, 0, 255)

# --- State ---
textboxtrancparency = 200
buttonstrancparency = 200
state = "start"
line_index = 0
text_line1 = ""
text_line2 = ""
keyboardinput = ""
hasBG = False
currentBG = "backroundexample1280x720px.png"


# --- Font ---
font = pygame.font.SysFont('Comic Sans MS', 30)

# --- Screen ---
screen = pygame.display.set_mode(size)

# --- Functions ---
def Buttonify(Picture, coords, clicked):
    if clicked == False:
        image = pygame.image.load(Picture)
        imagerect = image.get_rect()
        imagerect.topright = coords
        screen.blit(image, imagerect)
        return (image, imagerect)
    

def wrap_text(lines, line_index):
    dialogue = readlines(lines, line_index)
    words = dialogue.split()
    line1 = ""
    line2 = ""
    for word in words:
        test = (line1 + " " + word).strip()
        if font.size(test)[0] < 980:
            line1 = test
        else:
            line2 = (line2 + " " + word).strip()
    return line1, line2

def draw_rect_alpha(color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    screen.blit(shape_surf, rect)

def draw_image(imagefilename):
    image = pygame.image.load(imagefilename)
    imagerect = image.get_rect()
    screen.blit(image, imagerect)

def draw_background(imagefilename):
    global currentBG
    currentBG = imagefilename
    image = pygame.image.load(imagefilename)
    imagerect = image.get_rect()
    screen.blit(image, imagerect)

def renderdialogue(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    return lines

def readlines(lines, line):
    words = lines[line].strip().split()
    Ithasabg = 0
    for i in words:
        if i == "BG":
            Ithasabg = 1
            global hasBG
            hasBG = True
            WhereIsBG = words.index("BG")
            WhereisBackground = WhereIsBG + 1
            global NextBG
            NextBG = words[WhereisBackground]
    if Ithasabg == 1:
        words.pop()
        words.pop()
        sentence = ""
        for x in words:
            sentence = sentence + " " + x
        Ithasabg = 0
        return sentence.strip()
    return lines[line].strip()

        


# --- Draw functions ---
def draw_start():
    draw_image("Startexample1280x7200x.png")
    return Buttonify("Playbutton.png", (500, 400), False)
    

def draw_game(text_line1, text_line2):
    draw_image(currentBG)
    draw_rect_alpha((96, 96, 96, textboxtrancparency), (100, 550, 1000, 150))
    #draw_rect_alpha((96, 96, 96, buttonstrancparency), (900, 550, 200, 50))
    fastforward = Buttonify("undo-button1.png", (900, 550), False)
    Settings = Buttonify("cog.png",(960,550), False)
    text_layer1 = font.render(text_line1, False, (150, 150, 150))
    text_layer2 = font.render(text_line2, False, (150, 150, 150))
    text_layer3 = font.render(keyboardinput, False, (10, 10, 10))
    screen.blit(text_layer1, (100, 610))
    screen.blit(text_layer2, (100, 644))
    screen.blit(text_layer3, (10,10))
    return fastforward, Settings

def draw_settings():
    draw_image(currentBG)
    draw_rect_alpha((96, 96, 96, buttonstrancparency), (540, 100, 200, 300)) # x, y, w, h
    draw_rect_alpha((255,0,0, buttonstrancparency), (720, 100, 20, 10)) # x, y, w, h 
    #draw_rect_alpha((0,0,0, buttonstrancparency), (380, 100, 20, 10)) # x, y, w, h
    # save button
    # load button
    # volume
    # type speed
    # full screen



def fade(NextBG, currentBG):
    old = pygame.image.load(currentBG).convert_alpha()
    new = pygame.image.load(NextBG).convert_alpha()
    for alpha in range(0, 256):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return
        screen.fill((0, 0, 0))
        temp_old = old.copy()
        temp_old.fill((255, 255, 255, 255 - alpha), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(temp_old, (0, 0))
        temp_new = new.copy()
        temp_new.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(temp_new, (0, 0))
        pygame.display.flip()
        pygame.time.delay(4)



# --- Setup ---
lines = renderdialogue("dialogue.txt")
Startbutton = None
fastforward = None
Settings = None
textbox_rect = pygame.Rect(100, 600, 1000, 100)
closesettings_rect = pygame.Rect(720, 100, 20, 10)

# --- Game Loop ---
while True:
    keyboardinput = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if state == "start":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if Startbutton and Startbutton[1].collidepoint(mouse):
                    state = "game"

        elif state == "game":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if fastforward and fastforward[1].collidepoint(mouse):
                        if line_index > 0:
                            line_index += 1
                            text_line1, text_line2 = wrap_text(lines, line_index)
                            pygame.time.delay(3)
                elif textbox_rect.collidepoint(mouse):
                        if line_index < len(lines) - 1:
                            text_line1, text_line2 = wrap_text(lines, line_index)
                            line_index += 1
                        pygame.time.delay(3)
                elif Settings and Settings[1].collidepoint(mouse):
                    state = "settings"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                keyboardinput = "space"

                if line_index < len(lines) - 1:
                    text_line1, text_line2 = wrap_text(lines, line_index)
                    line_index += 1
                    time.sleep(0.2)
                    if hasBG == True:
                        state = "crossfading"

            if hasBG == True:
                text_line1, text_line2 = wrap_text(lines, line_index)
                fade(NextBG,currentBG)
                currentBG = NextBG
                hasBG = False
                state = "game"

        elif state == "settings":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if closesettings_rect.collidepoint(mouse):
                    state = "game"
                elif Settings and Settings[1].collidepoint(mouse):
                    state = "game"




    # --- Drawing ---
    if state == "start":
        Startbutton = draw_start()
    elif state == "game":
        fastforward, Settings = draw_game(text_line1, text_line2)
    elif state == "settings":
        closesettings = draw_settings()

    pygame.display.update()