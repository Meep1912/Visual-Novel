import pygame

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
    "bob": "Assets/Bob.png"
}


def readfile(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    return lines

def readlines(lines,line):

    words = lines[line].strip().split()

    text_words = []

    BG = None
    BGspeed = None
    CH1 = None
    CH2 = None
    CH1NAME = None
    CH2NAME = None
    isCH1speaking = None
    hasCH1 = False
    hasCH2 = False
    CH1_place = None
    CH2_place = None

    i = 0
    while i < len(words):
        word = words[i]
        if word == "BG":
            BG = backgrounds.get(words[i+1])
            BGspeed = words[i+2]
            i += 3

        elif word == "CH1":
            CH1 = characters.get(words[i + 1])
            CH1NAME = words[i+1]
            hasCH1 = True
            CH1_place = i
            i += 2
            

        elif word == "CH2":
            CH2 = characters.get(words[i + 1])
            CH2NAME = words[i+1]
            hasCH2 = True
            CH2_place = i
            i += 2
            
        else:
            text_words.append(word)
            i += 1

    if CH1_place is not None and CH2_place is not None:
            if CH1_place > CH2_place:
                isCH1speaking = True
            else:
                isCH1speaking = False
    elif CH1_place is not None:
        isCH1speaking = True
    elif CH2_place is not None:
        isCH1speaking = False
    return {

        "isCH1speaking" : isCH1speaking,
        "dialogue" : " ".join(text_words),
        "CH1": CH1,
        "CH2": CH2,
        "CH1NAME": CH1NAME,
        "CH2NAME": CH2NAME,
        "BG": BG,
        "BGspeed": BGspeed
    }
