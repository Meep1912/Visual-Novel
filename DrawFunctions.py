
global black, white, character1, character2, CH1NAME, CH2NAME, BW, BH
import pygame
pygame.init()

size = width, height = 960, 540
black = 0, 0, 0
white = 255,255,255
textboxtrancparency = 200
buttonstrancparency = 200
currentBG = "Assets\Backgrounds\warehouse_outside.png" 
character1 = "Assets/Empty.png"
character2 = "Assets/Empty.png"
CH1NAME = ""
CH2NAME = ""
save1time = "0"
save2time = "0"
save3time = "0"
save4time = "0"
save5time = "0"
save6time = "0"

backgrounds = {
    "school1": "Assets\Backgrounds\warehouse_outside.png",
    "school2": "Assets\Backgrounds\single bedroom.png",
    "house1": "",
    "house2": "",
}
characters = {
    "name": "Assets/referencepose\png256x288/body11.png",
    "2": "Assets/referencepose\png256x288/body12.png",
    "3": "Assets/referencepose\png256x288/body13.png",
    "bob": "Assets\Bob.png"
}

screen = pygame.display.set_mode(size, pygame.RESIZABLE)

# --- Scaling ---

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
reload_fonts()


def Buttonify(Picture, coords, clicked):
    if clicked == False:
        image = pygame.image.load(Picture)
        imagerect = image.get_rect()
        imagerect.topright = coords
        screen.blit(image, imagerect)
        return (image, imagerect)

def draw_rect_alpha(color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    screen.blit(shape_surf, rect)

def draw_image(imagefilename):
    image = pygame.image.load(imagefilename)
    image = pygame.transform.scale(image, screen.get_size())
    screen.blit(image, (0, 0))

def draw_background_start(imagefilename):
    image = pygame.image.load(imagefilename)
    image = pygame.transform.scale(image, screen.get_size())
    screen.blit(image, (0, 0))

def draw_background(imagefilename):
    global currentBG
    currentBG = imagefilename
    image = pygame.image.load(imagefilename)
    image = pygame.transform.scale(image, screen.get_size())
    screen.blit(image, (0, 0))

def draw_start():
    draw_image("Assets\Backgrounds\sky.png")
    title_text = starttitlefont.render("B R I G H T     L I G H T",False,(black))
    screen.blit(title_text, (sx(400),sx(100)))
    startoptionsbutton = draw_rect_alpha((96, 96, 96, 100), (sx(500), sy(300), sx(200), sy(40)))
    startoptionstext = font.render("O P T I O N S", False, (black))
    screen.blit(startoptionstext, (sx(500), sy(300)))
    startquitbutton = draw_rect_alpha((96, 96, 96, 100), (sx(500), sy(350), sx(200), sy(40)))
    startquitbuttontext = font.render("Q U I T", False, (black))
    screen.blit(startquitbuttontext, (sx(500), sy(350)))
    return Buttonify("Assets/Playbutton.png", (sx(650), sy(200)), False)

def draw_start_options():
    draw_background_start("Assets\Backgrounds\sky.png")
    draw_rect_alpha((96, 96, 96, buttonstrancparency), (sx(540), sy(100), sx(200), sy(350)))
    draw_rect_alpha((255, 0, 0, buttonstrancparency), (sx(720), sy(100), sx(20), sy(10)))

def draw_game(text_line1, text_line2,CH1NAME,CH2NAME):
    textbox = draw_rect_alpha((96, 96, 96, textboxtrancparency), (sx(100), sy(550), sx(1000), sy(150)))
    logsbutton = Buttonify("Assets\open-book.png", (sx(900), sy(550)), False)
    Settings = Buttonify("Assets/cog.png", (sx(980), sy(550)), False)

    text_layer1 = font.render(text_line1, False, (0, 0, 0))
    text_layer2 = font.render(text_line2, False, (0, 0, 0))
    if CH1NAME is not None:
        CH1NAMEbox = draw_rect_alpha((96, 96, 96, textboxtrancparency), (sx(100), sy(520), sx(150), sy(30)))
        CH1NAME_text = font.render(CH1NAME, False, (black))
        screen.blit(CH1NAME_text, (sx(100), sy(520)))

    if CH2NAME is not None:
        CH2NAMEbox = draw_rect_alpha((96, 96, 96, textboxtrancparency), (sx(950), sy(520), sx(150), sy(30)))
        CH2NAME_text = font.render(CH2NAME, False, (black))
        screen.blit(CH2NAME_text, (sx(950), sy(520)))

    screen.blit(text_layer1, (sx(100), sy(610)))
    screen.blit(text_layer2, (sx(100), sy(644)))
    return Settings, logsbutton

def draw_settings():
    draw_image(currentBG)
    draw_rect_alpha((96, 96, 96, buttonstrancparency), (sx(540), sy(100), sx(200), sy(350)))
    draw_rect_alpha((255, 0, 0, buttonstrancparency), (sx(720), sy(100), sx(20), sy(10)))
    title_text = settingsfont.render("Settings", False, (150, 150, 150))
    typespeed_slider.track = pygame.Rect(sx(560), sy(200), sx(160), sy(6))
    typespeed_slider.handle.centerx = int(typespeed_slider.track.left + typespeed_slider.value * typespeed_slider.track.width)
    typespeed_slider.handle.y = sy(200) - sy(6)
    volume_slider.track = pygame.Rect(sx(560), sy(250), sx(160), sy(6))
    volume_slider.handle.centerx = int(volume_slider.track.left + volume_slider.value * volume_slider.track.width)
    volume_slider.handle.y = sy(250) - sy(6)
    typespeed_slider.draw(screen, settingsfont)
    volume_slider.draw(screen, settingsfont)
    draw_rect_alpha((96, 96, 96, buttonstrancparency), (sx(560), sy(270), sx(160), sy(40))) # load/save options button
    draw_rect_alpha((96, 96, 0, buttonstrancparency), (sx(560), sy(315), sx(160), sy(40))) # main menu button
    draw_rect_alpha((96, 0, 96, buttonstrancparency), (sx(560), sy(360), sx(160), sy(40))) # quit button
    saveslashloadbuttontext = settingsfont.render("save/load", False, (150, 150, 150))
    buttontext = settingsfont.render("Main", False, (150, 150, 150))
    quitbuttontext = settingsfont.render("Quit", False, (150, 150, 150))
    screen.blit(title_text, (sx(550), sy(100)))
    screen.blit(saveslashloadbuttontext, (sx(560), sy(275)))
    screen.blit(buttontext, (sx(560), sy(320)))
    screen.blit(quitbuttontext, (sx(560), sy(370)))

def draw_saveslashloadmenu():
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
    box1label = settingsfont.render("Save 1", False, (black))
    box2label = settingsfont.render("Save 2", False, (black))
    box3label = settingsfont.render("Save 3", False, (black))
    box4label = settingsfont.render("Save 4", False, (black))
    box5label = settingsfont.render("Save 5", False, (black))
    box6label = settingsfont.render("Save 6", False, (black))
    box1time = settingsfont.render(save1time, False, (black))
    box2time = settingsfont.render(save2time, False, (black))
    box3time = settingsfont.render(save3time, False, (black))
    box4time = settingsfont.render(save4time, False, (black))
    box5time = settingsfont.render(save5time, False, (black))
    box6time = settingsfont.render(save6time, False, (black))
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

def draw_save_or_load(saveslot):
    draw_background(currentBG)
    draw_rect_alpha((75,75,75, 150), (sx(480), sy(250), sx(345), sy(100)))
    text = settingsfont.render(saveslot, False,(black))
    screen.blit(text, (sx(615),sy(250)))
    savetext = settingsfont.render("S A V E", False,(black))
    screen.blit(savetext, (sx(500),sy(285)))
    loadtext = settingsfont.render("L O A D", False,(black))
    screen.blit(loadtext, (sx(675),sy(285)))
    save = draw_rect_alpha((255,0,0, 100), (sx(490), sy(285), sx(150), sy(40)))
    load = draw_rect_alpha((0,0,255, 100), (sx(665), sy(285), sx(150), sy(40)))
    quitbutton = draw_rect_alpha((255, 0, 0, buttonstrancparency), (sx(805), sy(250), sx(20), sy(10)))

def draw_save_confirmation(saveslot):
    draw_background(currentBG)
    draw_rect_alpha((75,75,75, 150), (sx(480), sy(250), sx(345), sy(100)))
    text = settingsfont.render(f"Save progress in {saveslot}?", False,(black))
    screen.blit(text, (sx(480),sy(250)))
    suretext = settingsfont.render("IM SURE", False,(black))
    screen.blit(suretext, (sx(500),sy(285)))
    notsuretext = settingsfont.render("Im not sure", False,(black))
    screen.blit(notsuretext, (sx(665),sy(285)))
    sure = draw_rect_alpha((255,0,0, 100), (sx(490), sy(285), sx(150), sy(40)))
    notsure = draw_rect_alpha((0,0,255, 100), (sx(665), sy(285), sx(155), sy(40)))
    quitbutton = draw_rect_alpha((255, 0, 0, buttonstrancparency), (sx(805), sy(250), sx(20), sy(10)))                     
    
def draw_load_confirmation(saveslot):
    draw_characters(character1,character2)
    draw_rect_alpha((75,75,75, 150), (sx(480), sy(250), sx(345), sy(100)))
    text = settingsfont.render(f"Load {saveslot}?", False,(black))
    screen.blit(text, (sx(480),sy(250)))
    suretext = settingsfont.render("IM SURE", False,(black))
    screen.blit(suretext, (sx(500),sy(285)))
    notsuretext = settingsfont.render("Im not sure", False,(black))
    screen.blit(notsuretext, (sx(665),sy(285)))
    sure = draw_rect_alpha((255,0,0, 100), (sx(490), sy(285), sx(150), sy(40)))
    notsure = draw_rect_alpha((0,0,255, 100), (sx(665), sy(285), sx(155), sy(40)))
    quitbutton = draw_rect_alpha((255, 0, 0, buttonstrancparency), (sx(805), sy(250), sx(20), sy(10)))       

def draw_characters(character1,character2):
    x, y = sx(80), sy(300)
    if character1 == "Assets/Empty.png" and character2 == "Assets/Empty.png":
        pass
    elif character1 != "Assets/Empty.png" and character2 == "Assets/Empty.png":
        character1_img = pygame.image.load(character1)
        screen.blit(character1_img, (x, y))
    elif character1 != "Assets/Empty.png" and character2 != "Assets/Empty.png":
        character1_img = pygame.image.load(character1)
        screen.blit(character1_img, (x, y))
        character2_img = pygame.image.load(character2)
        screen.blit(character2_img, (x + sx(764), y))


def draw_textline(line,count,scroll_offset):
    text = line
    line_ = font.render(text, False, (white))
    screen.blit(line_, (sx(100),sy(100) + count * sy(35) + scroll_offset))


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
    
typespeed_slider = Slider(sx(560), sy(200), sx(160), "Text Speed")
volume_slider = Slider(sx(560), sy(250), sx(160), "Volume")
volume_slider.value = 0.3                     
volume_slider.handle.centerx = int(volume_slider.track.left + 0.3 * volume_slider.track.width)