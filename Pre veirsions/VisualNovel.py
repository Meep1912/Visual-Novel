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
buttonstrancparency = 201
state = "start"
line_index = 0
text_line1 = ""
text_line2 = ""

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
    else:
        pass

def draw_rect_alpha(color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    screen.blit(shape_surf, rect)

def draw_image(imagefilename):
    image = pygame.image.load(imagefilename)
    imagerect = image.get_rect()
    screen.blit(image, imagerect)

def renderdialogue(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    return lines

def readlines(lines, line):
    return lines[line].strip()

# --- Setup ---
lines = renderdialogue("dialogue.txt")
Startbutton = None

# --- Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    if state == "start":
        draw_image("Startexample1280x7200x.png")
        Startbutton = Buttonify("cow.png", (500, 400), False)
        

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            if Startbutton and Startbutton[1].collidepoint(mouse):
                state = "game"

    elif state == "game":
        draw_image("backroundexample1280x720px.png")
        
        # rectangles 

        draw_rect_alpha((96, 96, 96, textboxtrancparency), (100, 550, 1000, 150)) # colour , x, y , w ,h
        draw_rect_alpha((96, 96, 96, buttonstrancparency), (900, 550, 200, 50))
        
        # hitboxes

        textbox_rect = pygame.Rect(100, 550, 1000, 150)
        undobutton = Buttonify("undo-button.png", (900, 550), False)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
    
            if undobutton and undobutton[1].collidepoint(mouse):
                if line_index > 0:
                    time.sleep(0.2)
                    line_index -= 1


        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
           (event.type == pygame.MOUSEBUTTONDOWN and textbox_rect.collidepoint(pygame.mouse.get_pos())):

                dialogue = readlines(lines, line_index)
                words = dialogue.split()
                text_line1 = ""
                text_line2 = ""
                for word in words:
                    test = text_line1 + " " + word
                    if font.size(test)[0] < 980:
                        text_line1 = test
                    else:
                        text_line2 = text_line2 + " " + word
                time.sleep(0.2)
                line_index += 1
        text_layer1 = font.render(text_line1, False, (150, 150, 150))
        text_layer2 = font.render(text_line2, False, (150, 150, 150))
        screen.blit(text_layer1, (100, 610))
        screen.blit(text_layer2, (100, 644))

    pygame.display.update()
