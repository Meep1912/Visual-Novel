global current_playlist, log, character1, character2, CH1NAME, CH2NAME

import sys, pygame
from Sound import *
from TextFormatting import *
from DrawFunctions import *
from datetime import datetime

pygame.init()
pygame.mixer.init()

# --- Settings ---


size = width, height = 960, 540
black = 0, 0, 0
white = 255,255,255

pygame.display.set_caption("Bright Light")  # window name
icon = pygame.image.load("Assets/Icon.png")
pygame.display.set_icon(icon)


# --- State ---


state = "start"
line_index = 0
line = 0
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
playlist = "ambient_room"
CH1NAME = ""
CH2NAME = ""
log = ""
scroll_offset = 0
log = []


# --- Functions ---

def wrap_textbox_text(dialogue):
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

def wrap_logbox_text(log, isCH1speaking):
    logbox_size = 600
    words = log["text"].split()
    lines = []
    if log["name"] is not None:
        current_line = log["name"] + " : "
    else:
        current_line = ""
    for word in words:
        test = current_line + word + " "
        if font.size(test)[0] <= logbox_size:
            current_line = test
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    return lines


def draw_logs(log,scroll_offset):
    draw_image(currentBG)
    count = 0
    for entry in log:
        wrapped_lines = wrap_logbox_text(entry,isCH1speaking)
    
        for line in wrapped_lines:
            count += 1
            draw_textline(line, count,scroll_offset)
    largebox = draw_rect_alpha((96, 96, 96, 100), (sx(50), sy(50)+scroll_offset, sx(1175), sy(200)+(count*30)))
    exitbutton = draw_rect_alpha((255, 0, 0, 50), (sx(1205) , sy(50)+scroll_offset, sx(20), sy(10)))
    logstitle = settingsfont.render("L O G S", False, (black))
    screen.blit(logstitle, (sx(75), sy(75) + scroll_offset))

def format_logdata(data):
    isCH1speaking = data["isCH1speaking"]
    if data["isCH1speaking"] == True:
        new_log = {
            "name" : data["CH1NAME"],
            "text" : data["dialogue"]
        }
    else:
        new_log = {
            "name" : data["CH2NAME"],
            "text" : data["dialogue"]
        }
    return new_log, isCH1speaking

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
    screen.fill((black))
    draw_image(currentBG)
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


def fade(NextBG, currentBG, speed):
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

    for i in range(0,255,5):
        pygame.time.delay(speed)
        Transparency = 255 - i
        pygame.draw.rect(screen, "black", (sx(0),sy(0),sx(1280),sy(720)))
        
        TransparencySurface = pygame.Surface((sx(1280), sy(720)), pygame.SRCALPHA)
        TransparencySurface.blit(tempcurrentBG,(0,0))
        TransparencySurface.set_alpha(Transparency)

        if character1 == "Assets/Empty.png" and character2 == "Assets/Empty.png":
            pass
        elif character1 != "Assets/Empty.png" and character2 == "Assets/Empty.png":
            # make character1 transparent
            TransparencySurface.blit(tempchar1,(sx(80), sy(300)))
        elif character1 != "Assets/Empty.png" and character2 != "Assets/Empty.png":
            # make character1 transparent
            TransparencySurface.blit(tempchar1,(sx(80), sy(300)))
            # make character2 transparent
            TransparencySurface.blit(tempchar2,(sx(80), sy(300)))

        screen.blit(TransparencySurface,(0,0))
        pygame.display.update()
    
    for i in range(0,255,5):
    
        Transparency = i
        pygame.time.delay(speed)
        pygame.draw.rect(screen, "black", (sx(0),sy(0),sx(1280),sy(720)))

        TransparencySurface = pygame.Surface((sx(1280), sy(720)), pygame.SRCALPHA)
        TransparencySurface.blit(tempcurrentBG,(0,0))
        TransparencySurface.set_alpha(Transparency)

        if character1 == "Assets/Empty.png" and character2 == "Assets/Empty.png":
            pass
        elif character1 != "Assets/Empty.png" and character2 == "Assets/Empty.png":
            # make character1 transparent
            TransparencySurface.blit(tempchar1,(sx(80) + sx(768), sy(300)))
        elif character1 != "Assets/Empty.png" and character2 != "Assets/Empty.png":
            # make character1 transparent
            TransparencySurface.blit(tempchar1,(sx(80), sy(300)))
            # make character2 transparent
            TransparencySurface.blit(tempchar1,(sx(80), sy(300)))

        screen.blit(TransparencySurface,(0,0))
        pygame.display.update()



# --- Setup ---
lines = readfile("Assets\dialogue.txt")
data = readlines(lines,line)
new_log,isCH1speaking = format_logdata(data)
log.append(new_log)
Startbutton = None
fastforward = None
Settings = None
savebutton = None
NEXT_TRACK = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(NEXT_TRACK)
play_background_music(playlist)
refreshsaves()
# --- Game Loop ---
while True:
        textbox_rect = pygame.Rect(sx(100), sy(600), sx(1000), sy(100))
        closesettings_rect = pygame.Rect(sx(720), sy(100), sx(20), sy(10))
        saveslashloadbutton_rect = pygame.Rect(sx(560), sy(270), sx(160), sy(40))
        button_rect = pygame.Rect(sx(560), sy(315), sx(160), sy(40))
        quitbutton_rect = pygame.Rect(sx(560), sy(360), sx(160), sy(40))
        menubutton_rect = pygame.Rect(sx(560), sy(315), sx(160), sy(40))
        startoptionsbutton_rect = pygame.Rect((sx(500), sy(300), sx(200), sy(40)))
        startquitbutton_rect = pygame.Rect(sx(500), sy(350), sx(200), sy(40))
        closestartsettings_rect = pygame.Rect(sx(720), sy(100), sx(20), sy(10))
        closesaveslashloadmenu_rect = pygame.Rect(sx(1205), sy(50), sx(20), sy(10))
        closelogsbutton_rect = pygame.Rect(sx(1205), sy(50), sx(20), sy(10))
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                reload_fonts()
            elif event.type == NEXT_TRACK:
                play_background_music("ambient_room")

    # start state

            if state == "start":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    if Startbutton and Startbutton[1].collidepoint(mouse):
                        state = "game"
                    elif startoptionsbutton_rect.collidepoint(mouse):
                        state = "start_options"
                    elif startquitbutton_rect.collidepoint(mouse):
                        sys.exit()

    # sub state of start (parent: start)

            elif state == "start_options":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse = pygame.mouse.get_pos()
                        if closestartsettings_rect.collidepoint(mouse):
                            state = "start"

    # game state 

            elif state == "game":

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    if logsbutton and logsbutton[1].collidepoint(mouse) and char_index >= len(full_text):
                        state = "logs"

                    elif Settings and Settings[1].collidepoint(mouse) and char_index >= len(full_text):
                        state = "settings"

                    elif textbox_rect.collidepoint(mouse):

                        #skip text if still typing
                        if char_index < len(full_text):
                            char_index = len(full_text)
                            text_line1, text_line2 = wrap_textbox_text(full_text)

                        #Otherwise advance dialogue
                        elif line_index < len(lines) - 1:
                            line_index += 1
                            data = readlines(lines,line_index)
                            new_log,isCH1speaking = format_logdata(data)
                            log.append(new_log)

                            full_text = data["dialogue"]
                            char_index = 0

                            if data["BG"]:
                                fade(data["BG"], currentBG, data["BGspeed"])
                                currentBG = data["BG"]

                            if data["CH1"] is not None:
                                character1 = data["CH1"]

                            if data["CH2"] is not None:
                                character2 = data["CH2"]

                            if data["CH1NAME"] is not None:
                                CH1NAME = data["CH1NAME"]

                            if data["CH2NAME"] is not None:
                                CH2NAME = data["CH2NAME"]

                # SPACE = same as clicking
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and char_index >= len(full_text):
                    if line_index < len(lines) - 1:
                        line_index += 1
                        data = readlines(lines,line_index)
                        new_log,isCH1speaking = format_logdata(data)
                        log.append(new_log)

                        full_text = data["dialogue"]
                        char_index = 0
                        if data["CH1"] is not None:
                            character1 = data["CH1"]
                        if data["CH2"] is not None:
                            character2 = data["CH2"]
                        if data["CH1NAME"] is not None:   
                            CH1NAME = data["CH1NAME"]
                        if data["CH2NAME"] is not None:
                            CH2NAME = data["CH2NAME"]



    # settings state 

            elif state == "settings":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame .mouse.get_pos()
                    if closesettings_rect.collidepoint(mouse):
                        state = "game"
                    elif Settings and Settings[1].collidepoint(mouse):
                        state = "game"
                    elif menubutton_rect.collidepoint(mouse):
                        state = "start"
                    elif quitbutton_rect.collidepoint(mouse):
                        sys.exit()
                    elif saveslashloadbutton_rect.collidepoint(mouse):
                        state = "save/load menu"
                typespeed_slider.handle_event(event)
                volume_slider.handle_event(event)
                volume = volume_slider.get(1,100)
                pygame.mixer.music.set_volume((volume / 100))
                typespeed = typespeed_slider.get(100, 1)

    # sub state of settings (parent settings)

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

    # sub state of save/load (parent settings)

            elif state == "save_or_load":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    if save_or_loadquitbutton_rect.collidepoint(mouse):
                        state = "save/load menu"
                    elif savebutton_rect.collidepoint(mouse):
                        state = "save_confirmation"
                    elif loadbutton_rect.collidepoint(mouse):
                        state = "load_confirmation"

        # sub state of save_or_load (parent settings)

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

        # sub state of save_or_load (parent settings)

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
            
    # logs state

            elif state == "logs":
                closelogsbutton_rect = pygame.Rect(sx(1205), sy(50) + scroll_offset, sx(20), sy(10))
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    if closelogsbutton_rect.collidepoint(mouse):
                        state = "game"
                elif event.type == pygame.MOUSEWHEEL:
                    scroll_offset += event.y * 30



            
    # --- Drawing ---
        if state == "start":
            Startbutton = draw_start()
        elif state == "game":
            draw_image(currentBG)
            draw_characters(character1,character2)
            Settings, logsbutton = draw_game(text_line1, text_line2, CH1NAME,CH2NAME)
        elif state == "settings":
            draw_image(currentBG)
            draw_characters(character1,character2)
            draw_settings()
        elif state == "save/load menu":
            draw_image(currentBG)
            draw_characters(character1,character2)
            draw_saveslashloadmenu()
        elif state == "save_or_load":
            draw_image(currentBG)
            draw_characters(character1,character2)
            draw_save_or_load(saveslot)
        elif state == "save_confirmation":
            draw_image(currentBG)
            draw_characters(character1,character2)
            draw_save_confirmation(saveslot)
        elif state == "load_confirmation":
            draw_image(currentBG)
            draw_characters(character1,character2)
            draw_load_confirmation(saveslot)
        elif state == "start_options":
            draw_start_options()
        elif state == "logs":
            draw_image(currentBG)
            draw_logs(log,scroll_offset)
        
        now = pygame.time.get_ticks()
        if char_index < len(full_text) and now - last_char_time >= typespeed:
            char_index += 1
            text_line1, text_line2 = wrap_textbox_text(full_text[:char_index])
            last_char_time = now
        clock = pygame.time.Clock()
        clock.tick(60)
        pygame.display.update()
        