import sys, pygame, random
pygame.init()
pygame.mixer.init()
# --- Settings ---
size = width, height = 960, 540
black = 0, 0, 0
BLUE = (0, 0, 255)
pygame.display.set_caption("Bright Light")  # window name
icon = pygame.image.load("Assets/Icon.png")
pygame.display.set_icon(icon)
# --- State ---
global current_playlist, character1, character2, log
textboxtrancparency = 200
buttonstrancparency = 200
state = "start"
line_index = 0
text_line1 = ""
text_line2 = ""
keyboardinput = ""
hasBG = False 
char_index = 0
full_text = ""
typespeed = 1
savepoint = 1
savestate = "Save"
loadstate = "Load"
save_timer = 0
load_timer = 0
last_char_time = 0
character1 = "Assets/Empty.png"
character2 = "Assets/Empty.png"
currentBG = "Assets\Backgrounds\warehouse_outside.png" 
current_playlist = "ambient_room"
current_track = ""
save1time = "0"
save2time = "0"
save3time = "0"
save4time = "0"
save5time = "0"
save6time = "0"
from datetime import datetime
log = []

backgrounds = {
    "school1": "Assets\Backgrounds\warehouse_outside.png",
    "school2": "Assets\Backgrounds\single bedroom.png",
    "house1": "",
    "house2": "",
}
characters = {
    "1": "Assets/referencepose\png256x288/body11.png",
    "2": "Assets/referencepose\png256x288/body12.png",
    "3": "Assets/referencepose\png256x288/body13.png",
    "bob": "Assets\Bob.png"
}
# --- Scale helpers ---
global BW, BH
BW, BH = 1280, 720
def sx(v): 
    return int(v * screen.get_width() / BW)
def sy(v): 
    return int(v * screen.get_height() / BH)
# --- Font ---
font = pygame.font.Font("Assets/Cause/static/Cause-Regular.ttf", 30)
settingsfont = pygame.font.Font("Assets/Cause/static/Cause-Regular.ttf", 30)
starttitlefont = pygame.font.Font("Assets/static/NotoSans-Regular.ttf", 40)
def reload_fonts():
    global font, settingsfont, starttitlefont
    font = pygame.font.Font("Assets/Cause/static/Cause-Regular.ttf", sy(30))
    settingsfont = pygame.font.Font("Assets/Cause/static/Cause-Regular.ttf", sy(30))
    starttitlefont = pygame.font.Font("Assets/static/NotoSans-Regular.ttf", sy(40))

# --- Screen ---
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
#screen = pygame.display.set_mode(size, pygame.RESIZABLE | pygame.NOFRAME)
reload_fonts()

# --- Functions ---
def play_background_music(playlist):
    pygame.mixer.music.set_volume(0.3)
    global current_track 
    if playlist == "ambient_room":
        playlist = [
            "Assets/Free use sounds/Room+Tones+-+Signaturesounds.org/Room Tones - Signaturesounds.org/Room-Tone 1.wav",
            "Assets/Free use sounds/Room+Tones+-+Signaturesounds.org/Room Tones - Signaturesounds.org/Room-Tone 2.wav",
            "Assets/Free use sounds/Room+Tones+-+Signaturesounds.org/Room Tones - Signaturesounds.org/Room-Tone 6.wav",
            "Assets/Free use sounds/Room+Tones+-+Signaturesounds.org/Room Tones - Signaturesounds.org/Room-Tone 7.wav",
        ]
    track_to_play = random.choice(playlist)
    if current_track == track_to_play:
        pass
    else:
        pygame.mixer.music.load(track_to_play)
        current_track = track_to_play
        pygame.mixer.music.play()
def Buttonify(Picture, coords, clicked):
    if clicked == False:
        image = pygame.image.load(Picture)
        imagerect = image.get_rect()
        imagerect.topright = coords
        screen.blit(image, imagerect)
        return (image, imagerect)
    
def wrap_text(dialogue):
    words = dialogue.split()
    line1 = ""
    line2 = ""
    for word in words:
        test = (line1 + " " + word).strip()
        if font.size(test)[0] < sx(980):
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
    image = pygame.transform.scale(image, screen.get_size())
    screen.blit(image, (0, 0))
def draw_background(imagefilename):
    global currentBG
    currentBG = imagefilename
    image = pygame.image.load(imagefilename)
    image = pygame.transform.scale(image, screen.get_size())
    screen.blit(image, (0, 0))
def renderdialogue(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    return lines
def readlines(lines, line):
    words = lines[line].strip().split()
    global hasBG, NextBG, character1, character2, speed, hasCH1, hasCH2
    to_remove = set()
    newwords = ""
    for i in words:
        newwords = newwords + i
    log.append(" " + newwords + "\n")
    print(log)
    
    for i, word in enumerate(words):
        if word == "BG":
            hasBG = True
            NextBG = backgrounds[words[i + 1]]
            speed = words[i + 2]
            to_remove.add(i)
            to_remove.add(i + 1)
            to_remove.add(i + 2)
        elif word == "CH1":
            hasCH1 = True
            character1 = characters[words[i + 1]]
            to_remove.add(i)
            to_remove.add(i + 1)
        elif word == "CH2":
            hasCH2 = True
            character2 = characters[words[i + 1]]
            to_remove.add(i)
            to_remove.add(i + 1)
        elif word != "CH1":
            hasCH1 = False
        elif word != "CH2":
            hasCH2 = False
    
    words = [w for i, w in enumerate(words) if i not in to_remove]
    return " ".join(words)

## Load a save


def load(saveslot):
    global savestate
    file = open("Assets\saves.txt", "r")
    lines = file.readlines()
    file.close()
    for i, line in enumerate(lines):
        if line.strip() == saveslot:
            try:
                saveselected = int(lines[i +1])
                return saveselected
            except ValueError:
                savestate = "No Save Detected"
                return None

def save(saveslot, line_index1):
    global save1time, save2time, save3time, save4time, save5time, save6time
    file = open("Assets\saves.txt", "r")
    lines = file.readlines()
    file.close()
    file = open("Assets\saves.txt", "w")
    for i, line in enumerate(lines):
        if line.strip() == saveslot:
            lines[i+1] = str(line_index1) + "\n"
            if saveslot == "save1":
                save1time = datetime.now().strftime("%d/%m/%Y %H:%M")
                lines[i+2] = str(save1time) + "\n"
            elif saveslot == "save2":
                save2time = datetime.now().strftime("%d/%m/%Y %H:%M")
                lines[i+2] = str(save2time) + "\n"
            elif saveslot == "save3":
                save3time = datetime.now().strftime("%d/%m/%Y %H:%M")
                lines[i+2] = str(save3time) + "\n"
            elif saveslot == "save4":
                save4time = datetime.now().strftime("%d/%m/%Y %H:%M")
                lines[i+2] = str(save4time) + "\n"
            elif saveslot == "save5":
                save5time = datetime.now().strftime("%d/%m/%Y %H:%M")
                lines[i+2] = str(save5time) + "\n"
            elif saveslot == "save6":
                save6time = datetime.now().strftime("%d/%m/%Y %H:%M")
                lines[i+2] = str(save6time) + "\n"
    file.writelines(lines)
    screen.fill((0,0,0))
    draw_image(currentBG)
    draw_characters()
    pygame.image.save(screen, f"Assets/savescreens/{saveslot}.png")
    file.close()

def refreshsaves():
    global save1time, save2time, save3time, save4time, save5time, save6time
    file = open("Assets/saves.txt", "r")
    lines = file.readlines()
    file.close()
    for i, line in enumerate(lines):
        if line.strip() == "save1":
            save1time = lines[i+2].strip()
        elif line.strip() == "save2":
            save2time = lines[i+2].strip()
        elif line.strip() == "save3":
            save3time = lines[i+2].strip()
        elif line.strip() == "save4":
            save4time = lines[i+2].strip()
        elif line.strip() == "save5":
            save5time = lines[i+2].strip()
        elif line.strip() == "save6":
            save6time = lines[i+2].strip()

# --- Draw functions ---


def draw_start():
    draw_image("Assets\Backgrounds\sky.png")
    title_text = starttitlefont.render("B R I G H T     L I G H T",False,(0,0,0))
    screen.blit(title_text, (sx(400),sx(100)))
    startoptionsbutton = draw_rect_alpha((96, 96, 96, 100), (sx(500), sy(300), sx(200), sy(40)))
    startoptionstext = font.render("O P T I O N S", False, (0,0,0))
    screen.blit(startoptionstext, (sx(500), sy(300)))
    startquitbutton = draw_rect_alpha((96, 96, 96, 100), (sx(500), sy(350), sx(200), sy(40)))
    startquitbuttontext = font.render("Q U I T", False, (0,0,0))
    screen.blit(startquitbuttontext, (sx(500), sy(350)))
    return Buttonify("Assets/Playbutton.png", (sx(650), sy(200)), False)

def draw_save_or_load(saveslot):
    draw_background(currentBG)
    draw_characters()
    draw_rect_alpha((75,75,75, 150), (sx(480), sy(250), sx(345), sy(100)))
    text = settingsfont.render(saveslot, False,(0,0,0))
    screen.blit(text, (sx(615),sy(250)))
    savetext = settingsfont.render("S A V E", False,(0,0,0))
    screen.blit(savetext, (sx(500),sy(285)))
    loadtext = settingsfont.render("L O A D", False,(0,0,0))
    screen.blit(loadtext, (sx(675),sy(285)))
    save = draw_rect_alpha((255,0,0, 100), (sx(490), sy(285), sx(150), sy(40)))
    load = draw_rect_alpha((0,0,255, 100), (sx(665), sy(285), sx(150), sy(40)))
    quitbutton = draw_rect_alpha((255, 0, 0, buttonstrancparency), (sx(805), sy(250), sx(20), sy(10)))

def draw_save_confirmation(saveslot):
    draw_background(currentBG)
    draw_characters()
    draw_rect_alpha((75,75,75, 150), (sx(480), sy(250), sx(345), sy(100)))
    text = settingsfont.render(f"Save progress in {saveslot}?", False,(0,0,0))
    screen.blit(text, (sx(480),sy(250)))
    suretext = settingsfont.render("IM SURE", False,(0,0,0))
    screen.blit(suretext, (sx(500),sy(285)))
    notsuretext = settingsfont.render("Im not sure", False,(0,0,0))
    screen.blit(notsuretext, (sx(665),sy(285)))
    sure = draw_rect_alpha((255,0,0, 100), (sx(490), sy(285), sx(150), sy(40)))
    notsure = draw_rect_alpha((0,0,255, 100), (sx(665), sy(285), sx(155), sy(40)))
    quitbutton = draw_rect_alpha((255, 0, 0, buttonstrancparency), (sx(805), sy(250), sx(20), sy(10)))                     
    
def draw_load_confirmation(saveslot):
    draw_background(currentBG)
    draw_characters()
    draw_rect_alpha((75,75,75, 150), (sx(480), sy(250), sx(345), sy(100)))
    text = settingsfont.render(f"Load {saveslot}?", False,(0,0,0))
    screen.blit(text, (sx(480),sy(250)))
    suretext = settingsfont.render("IM SURE", False,(0,0,0))
    screen.blit(suretext, (sx(500),sy(285)))
    notsuretext = settingsfont.render("Im not sure", False,(0,0,0))
    screen.blit(notsuretext, (sx(665),sy(285)))
    sure = draw_rect_alpha((255,0,0, 100), (sx(490), sy(285), sx(150), sy(40)))
    notsure = draw_rect_alpha((0,0,255, 100), (sx(665), sy(285), sx(155), sy(40)))
    quitbutton = draw_rect_alpha((255, 0, 0, buttonstrancparency), (sx(805), sy(250), sx(20), sy(10)))                     


def draw_start_options():
    draw_background(currentBG)
    draw_characters()
    draw_rect_alpha((96, 96, 96, buttonstrancparency), (sx(540), sy(100), sx(200), sy(350)))
    draw_rect_alpha((255, 0, 0, buttonstrancparency), (sx(720), sy(100), sx(20), sy(10)))

def draw_game(text_line1, text_line2):
    draw_image(currentBG)
    draw_characters()
    # text box
    draw_rect_alpha((96, 96, 96, textboxtrancparency), (sx(100), sy(550), sx(1000), sy(150)))
    logsbutton = Buttonify("Assets/undo-button1.png", (sx(900), sy(550)), False)
    Settings = Buttonify("Assets/cog.png", (sx(960), sy(550)), False)
    text_layer1 = font.render(text_line1, False, (0, 0, 0))
    text_layer2 = font.render(text_line2, False, (0, 0, 0))
    text_layer3 = font.render(keyboardinput, False, (10, 10, 10))
    screen.blit(text_layer1, (sx(100), sy(610)))
    screen.blit(text_layer2, (sx(100), sy(644)))
    screen.blit(text_layer3, (sx(10), sy(10)))
    return Settings


def draw_settings():
    draw_image(currentBG)
    draw_characters()
    draw_rect_alpha((96, 96, 96, buttonstrancparency), (sx(540), sy(100), sx(200), sy(350)))
    draw_rect_alpha((255, 0, 0, buttonstrancparency), (sx(720), sy(100), sx(20), sy(10)))
    title_text = settingsfont.render("Settings", False, (150, 150, 150))
    # Update slider positions to match current screen size
    typespeed_slider.track = pygame.Rect(sx(560), sy(200), sx(160), sy(6))
    typespeed_slider.handle.centerx = int(typespeed_slider.track.left + typespeed_slider.value * typespeed_slider.track.width)
    typespeed_slider.handle.y = sy(200) - sy(6)
    volume_slider.track = pygame.Rect(sx(560), sy(250), sx(160), sy(6))
    volume_slider.handle.centerx = int(volume_slider.track.left + volume_slider.value * volume_slider.track.width)
    volume_slider.handle.y = sy(250) - sy(6)
    typespeed_slider.draw(screen, settingsfont)
    volume_slider.draw(screen, settingsfont)
    draw_rect_alpha((96, 96, 96, buttonstrancparency), (sx(560), sy(270), sx(160), sy(40))) # load/save options button
    draw_rect_alpha((96, 96, 0, buttonstrancparency), (sx(560), sy(315), sx(160), sy(40))) # empty button
    draw_rect_alpha((96, 0, 96, buttonstrancparency), (sx(560), sy(360), sx(160), sy(40))) # quit button
    saveslashloadbuttontext = settingsfont.render("save/load", False, (150, 150, 150))
    buttontext = settingsfont.render("button", False, (150, 150, 150))
    quitbuttontext = settingsfont.render("Quit", False, (150, 150, 150))
    screen.blit(title_text, (sx(550), sy(100)))
    screen.blit(saveslashloadbuttontext, (sx(560), sy(275)))
    screen.blit(buttontext, (sx(560), sy(320)))
    screen.blit(quitbuttontext, (sx(560), sy(370)))

def draw_saveslashloadmenu():
    draw_characters()
    draw_background(currentBG)
    largebox = draw_rect_alpha((96, 96, 96, 150), (sx(50), sy(50), sx(1175), sy(600)))
    # to fit 6 boxes in a 1175 by 600 box so id do 2 layers the height of boxes would be 200
    exitbutton = draw_rect_alpha((255, 0, 0, buttonstrancparency), (sx(1205), sy(50), sx(20), sy(10)))
    box1 = draw_rect_alpha((96, 96, 96, buttonstrancparency), (sx(100), sy(100), sx(325), sy(200)))
    box2 = draw_rect_alpha((96, 96, 96, buttonstrancparency), (sx(475), sy(100), sx(325), sy(200)))
    box3 = draw_rect_alpha((96, 96, 96, buttonstrancparency), (sx(850), sy(100), sx(325), sy(200)))
    box4 = draw_rect_alpha((96, 96, 96, buttonstrancparency), (sx(100), sy(350), sx(325), sy(200)))
    box5 = draw_rect_alpha((96, 96, 96, buttonstrancparency), (sx(475), sy(350), sx(325), sy(200)))
    box6 = draw_rect_alpha((96, 96, 96, buttonstrancparency), (sx(850), sy(350), sx(325), sy(200)))
    box1label = settingsfont.render("Save 1", False, (0,0,0))
    box2label = settingsfont.render("Save 2", False, (0,0,0))
    box3label = settingsfont.render("Save 3", False, (0,0,0))
    box4label = settingsfont.render("Save 4", False, (0,0,0))
    box5label = settingsfont.render("Save 5", False, (0,0,0))
    box6label = settingsfont.render("Save 6", False, (0,0,0))
    box1time = settingsfont.render(save1time, False, (0,0,0))
    box2time = settingsfont.render(save2time, False, (0,0,0))
    box3time = settingsfont.render(save3time, False, (0,0,0))
    box4time = settingsfont.render(save4time, False, (0,0,0))
    box5time = settingsfont.render(save5time, False, (0,0,0))
    box6time = settingsfont.render(save6time, False, (0,0,0))
    try:
        save1image= pygame.image.load(f"Assets/savescreens/save1.png")
        save1image = pygame.transform.scale(save1image, (sx(325), sy(200)))
        screen.blit(save1image, (sx(100), sy(100)))
    except:
        pass
    try:
        save2image= pygame.image.load(f"Assets/savescreens/save2.png")
        save2image = pygame.transform.scale(save2image, (sx(325), sy(200)))
        screen.blit(save2image, (sx(475), sy(100)))
    except:
        pass 
    try:
        save3image= pygame.image.load(f"Assets/savescreens/save3.png")
        save3image = pygame.transform.scale(save3image, (sx(325), sy(200)))
        screen.blit(save3image, (sx(850), sy(100)))
    except:
        pass
    try:
        save4image= pygame.image.load(f"Assets/savescreens/save4.png")
        save4image = pygame.transform.scale(save4image, (sx(325), sy(200)))
        screen.blit(save4image, (sx(100), sy(350)))
    except:
        pass 
    try:
        save5image= pygame.image.load(f"Assets/savescreens/save5.png")
        save5image = pygame.transform.scale(save5image, (sx(325), sy(200)))
        screen.blit(save5image, (sx(475), sy(350)))
    except:
        pass
    try:
        save6image= pygame.image.load(f"Assets/savescreens/save4.png")
        save6image = pygame.transform.scale(save6image, (sx(325), sy(200)))
        screen.blit(save6image, (sx(850), sy(350)))
    except:
        pass 
    screen.blit(box1label, (sx(100), sy(100)))
    screen.blit(box2label, (sx(475), sy(100)))
    screen.blit(box3label, (sx(850), sy(100)))
    screen.blit(box4label, (sx(100), sy(350)))
    screen.blit(box5label, (sx(475), sy(350)))
    screen.blit(box6label, (sx(850), sy(350)))
    screen.blit(box1time, (sx(100), sy(250)))
    screen.blit(box2time, (sx(475), sy(250)))
    screen.blit(box3time, (sx(850), sy(250)))
    screen.blit(box4time, (sx(100), sy(500)))
    screen.blit(box5time, (sx(475), sy(500)))
    screen.blit(box6time, (sx(850), sy(500)))


def draw_characters():
    x, y = sx(80), sy(300)
    # first need to check if person1/2 holds a value which isnt "Empty.png"
    if character1 == "Empty.png" and character2 == "Empty.png":
        pass
    elif character1 != "Empty.png" and character2 == "Empty.png":
        character1_img = pygame.image.load(character1)
        screen.blit(character1_img, (x + sx(768), y))
    elif character1 != "Empty.png" and character2 != "Empty.png":
        character1_img = pygame.image.load(character1)
        screen.blit(character1_img, (x, y))
        character2_img = pygame.image.load(character2)
        screen.blit(character2_img, (x + sx(764), y)) # originaly 864

def fade(NextBG, currentBG, speed):
    # firstly how does one "fade" well for inputs I need current BG next BG and also fade time
    # to fade I will make a black background behind and draw it for the entire time 
    # there isnt a 100% opacity 
    # so I need to make temporary BG copies of each
    if speed == "fast":
        speed = 10
        # 30 frames i.e 30*255 = 8.5
    elif speed == "slow":
        speed =  50
        # 40 frames

    tempNextBG = pygame.image.load(NextBG)
    tempNextBG = pygame.transform.scale(tempNextBG, screen.get_size())

    tempcurrentBG = pygame.image.load(currentBG)
    tempcurrentBG = pygame.transform.scale(tempcurrentBG, screen.get_size())

    tempchar1 = pygame.image.load(character1)

    tempchar2 = pygame.image.load(character2)

    # Then to fade I need render current BG ontop of the black screen then decrease transparency then render then decrease
    for i in range(0,255,5):
        pygame.time.delay(speed)
        Transparency = 255 - i
        pygame.draw.rect(screen, "black", (sx(0),sy(0),sx(1280),sy(720)))
        
        TransparencySurface = pygame.Surface((sx(1280), sy(720)), pygame.SRCALPHA)
        TransparencySurface.blit(tempcurrentBG,(0,0))
        TransparencySurface.set_alpha(Transparency)

        if character1 == "Empty.png" and character2 == "Empty.png":
            pass
        elif character1 != "Empty.png" and character2 == "Empty.png":
            # make character1 transparent
            TransparencySurface.blit(tempchar1,(sx(80), sy(300)))
        elif character1 != "Empty.png" and character2 != "Empty.png":
            # make character1 transparent
            TransparencySurface.blit(tempchar1,(sx(80), sy(300)))
            # make character2 transparent
            TransparencySurface.blit(tempchar2,(sx(80), sy(300)))
        screen.blit(TransparencySurface,(0,0))
        pygame.display.update()
    # after this for loop ends It will be time to load in the next image
    for i in range(0,255,5):
        Transparency = i
        pygame.time.delay(speed)
        pygame.draw.rect(screen, "black", (sx(0),sy(0),sx(1280),sy(720)))

        TransparencySurface = pygame.Surface((sx(1280), sy(720)), pygame.SRCALPHA)
        TransparencySurface.blit(tempcurrentBG,(0,0))
        TransparencySurface.set_alpha(Transparency)

        if character1 == "Empty.png" and character2 == "Empty.png":
            pass
        elif character1 != "Empty.png" and character2 == "Empty.png":
            # make character1 transparent
            TransparencySurface.blit(tempchar1,(sx(80) + sx(768), sy(300)))
        elif character1 != "Empty.png" and character2 != "Empty.png":
            # make character1 transparent
            TransparencySurface.blit(tempchar1,(sx(80), sy(300)))
            # make character2 transparent
            TransparencySurface.blit(tempchar1,(sx(80), sy(300)))
        screen.blit(TransparencySurface,(0,0))
        pygame.display.update()


class Slider:
    def __init__(self, x, y, w, name):
        self.track = pygame.Rect(x, y, w, 6)
        self.handle = pygame.Rect(x, y - 6, 10, 18)
        self.name = name
        self.value = 0
        self.dragging = False
    def draw(self, screen, font):
        pygame.draw.rect(screen, (60, 60, 60), self.track)
        pygame.draw.rect(screen, (200, 200, 200), self.handle)
        label = font.render(self.name, False, (150, 150, 150))
        screen.blit(label, (self.track.x, self.track.y - 30))
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.handle.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                x = event.pos[0]
                x = max(self.track.left, min(x, self.track.right))
                self.handle.centerx = x
                self.value = (x - self.track.left) / self.track.width
    def get(self, min_val, max_val):
        return int((self.value) * (max_val - min_val)) + min_val

# --- Setup ---
lines = renderdialogue("Assets/dialogue.txt")
Startbutton = None
fastforward = None
Settings = None
typespeed_slider = Slider(sx(560), sy(200), sx(160), "Text Speed")
volume_slider = Slider(sx(560), sy(250), sx(160), "Volume")
volume_slider.value = 0.3                     
volume_slider.handle.centerx = int(volume_slider.track.left + 0.3 * volume_slider.track.width)
savebutton = None
NEXT_TRACK = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(NEXT_TRACK)
play_background_music(current_playlist)
refreshsaves()
# --- Game Loop ---
while True:
    # Recompute collision rects each frame to handle window resize
    logsbutton_rect = pygame.Rect(sx(900), sy(550),sx(50),sx(50))
    textbox_rect = pygame.Rect(sx(100), sy(600), sx(1000), sy(100))
    closesettings_rect = pygame.Rect(sx(720), sy(100), sx(20), sy(10))
    saveslashloadbutton_rect = pygame.Rect(sx(560), sy(270), sx(160), sy(40))
    button_rect = pygame.Rect(sx(560), sy(315), sx(160), sy(40))
    quitbutton_rect = pygame.Rect(sx(560), sy(360), sx(160), sy(40))
    startoptionsbutton_rect = pygame.Rect((sx(500), sy(300), sx(200), sy(40)))
    startquitbutton_rect = pygame.Rect(sx(500), sy(350), sx(200), sy(40))
    closestartsettings_rect = pygame.Rect(sx(720), sy(100), sx(20), sy(10))
    closesaveslashloadmenu_rect = pygame.Rect(sx(1205), sy(50), sx(20), sy(10))
    savebox1rect = pygame.Rect(sx(100), sy(100), sx(325), sy(200))
    savebox2rect = pygame.Rect(sx(475), sy(100), sx(325), sy(200))
    savebox3rect = pygame.Rect(sx(850), sy(100), sx(325), sy(200))
    savebox4rect = pygame.Rect(sx(100), sy(350), sx(325), sy(200))
    savebox5rect = pygame.Rect(sx(475), sy(350), sx(325), sy(200))
    savebox6rect = pygame.Rect(sx(850), sy(350), sx(325), sy(200))
    save_or_loadquitbutton_rect = pygame.Rect(sx(805), sy(250), sx(20), sy(10))
    savebutton_rect = pygame.Rect(sx(490), sy(285), sx(150), sy(40))
    loadbutton_rect = pygame.Rect(sx(665), sy(285), sx(150), sy(40))
    surerect =  pygame.Rect(sx(490), sy(285), sx(150), sy(40))
    notsurerect = pygame.Rect(sx(665), sy(285), sx(155), sy(40))
    quitbuttonrect =  pygame.Rect(sx(805), sy(250), sx(20), sy(10))                    

    keyboardinput = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            reload_fonts()
        elif event.type == NEXT_TRACK:
            play_background_music(current_playlist)
        if state == "start":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if Startbutton and Startbutton[1].collidepoint(mouse):
                    state = "game"
                elif startoptionsbutton_rect.collidepoint(mouse):
                    state = "start_options"
                elif startquitbutton_rect.collidepoint(mouse):
                    sys.exit()
        elif state == "game":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if logsbutton_rect.collidepoint(mouse):
                    state = "logs"
                elif textbox_rect.collidepoint(mouse) and not logsbutton_rect[1].collidepoint(mouse):
                    if char_index < len(full_text):
                    # First click: skip to end of current line
                        char_index = len(full_text)
                        text_line1, text_line2 = wrap_text(full_text)
                    elif line_index < len(lines) - 1:
                    # Second click: advance to next line
                        full_text = readlines(lines, line_index)
                        char_index = 0
                        line_index += 1
                        pygame.time.delay(3)
                    if hasBG == True:
                        state = "crossfading"
                elif Settings and Settings[1].collidepoint(mouse) and char_index >= len(full_text):
                    state = "settings"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and char_index >= len(full_text):
                if line_index < len(lines) - 1:
                    full_text = readlines(lines, line_index)
                    char_index = 0
                    line_index += 1
                    savepoint = line_index
                    pygame.time.delay(3)
            if hasBG == True:
                state = "crossfading"
                 # full_text = readlines(lines, line_index)
                char_index = 0
                fade(NextBG,currentBG, speed)
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
                elif quitbutton_rect.collidepoint(mouse):
                    sys.exit()
                elif saveslashloadbutton_rect.collidepoint(mouse):
                    state = "save/load menu"
            typespeed_slider.handle_event(event)
            volume_slider.handle_event(event)
            volume = volume_slider.get(1,100)
            pygame.mixer.music.set_volume((volume / 100))
            typespeed = typespeed_slider.get(100, 1)
        elif state == "save/load menu":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if closesaveslashloadmenu_rect.collidepoint(mouse):
                    state = "settings"
                elif savebox1rect.collidepoint(mouse):
                    saveslot = "save1"
                    state = "save_or_load"
                elif savebox2rect.collidepoint(mouse):
                    saveslot = "save2"
                    state = "save_or_load"
                elif savebox3rect.collidepoint(mouse):
                    saveslot = "save3"
                    state = "save_or_load"
                elif savebox4rect.collidepoint(mouse):
                    saveslot = "save4"
                    state = "save_or_load"
                elif savebox5rect.collidepoint(mouse):
                    saveslot = "save5"
                    state = "save_or_load"
                elif savebox6rect.collidepoint(mouse):
                    saveslot = "save6"
                    state = "save_or_load"
        elif state == "save_or_load":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if save_or_loadquitbutton_rect.collidepoint(mouse):
                    state = "save/load menu"
                elif savebutton_rect.collidepoint(mouse):
                    state = "save_confirmation"
                elif loadbutton_rect.collidepoint(mouse):
                    state = "load_confirmation"
        elif state == "save_confirmation":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if quitbuttonrect.collidepoint(mouse):
                    state = "save/load menu"
                elif surerect.collidepoint(mouse):
                    savestate = "saving"
                    state = "game"
                    save_timer = pygame.time.get_ticks()
                    save(saveslot, line_index)
                elif notsurerect.collidepoint(mouse):
                    state = "save_or_load"

        elif state == "load_confirmation":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if quitbuttonrect.collidepoint(mouse):
                    state = "save/load menu"
                elif surerect.collidepoint(mouse):
                    savestate = "loading"
                    load_timer = pygame.time.get_ticks()
                    result = load(saveslot)
                    if result is not None:
                        line_index = result
                        full_text = readlines(lines, line_index)
                        char_index = len(full_text)
                        state = "game"
                elif notsurerect.collidepoint(mouse):
                    state = "save_or_load"
        if savestate == "saved" and pygame.time.get_ticks() - save_timer > 500:
                savestate = "save"
        elif loadstate == "loaded" and pygame.time.get_ticks() - load_timer > 500:
                loadstate = "load"
        elif state == "start_options":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    if closestartsettings_rect.collidepoint(mouse):
                        state = "start"
        
# --- Drawing ---
    if state == "start":
        Startbutton = draw_start()
    elif state == "game":
        Settings = draw_game(text_line1, text_line2)
    elif state == "settings":
        draw_settings()
    elif state == "save/load menu":
        draw_saveslashloadmenu()
    elif state == "save_or_load":
        draw_save_or_load(saveslot)
    elif state == "save_confirmation":
        draw_save_confirmation(saveslot)
    elif state == "load_confirmation":
        draw_load_confirmation(saveslot)
    elif state == "crossfading": 
        draw_game(text_line1, text_line2)
    elif state == "start_options":
        draw_start_options()
    
    now = pygame.time.get_ticks()
    if char_index < len(full_text) and now - last_char_time >= typespeed:
        char_index += 1
        text_line1, text_line2 = wrap_text(full_text[:char_index])
        last_char_time = now
    pygame.display.update()