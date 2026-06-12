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
    for i, word in enumerate(words):
        if word == "BG":
            BG = backgrounds.get(words[i+1])
            BGspeed = words[i+2]
        elif word == "CH1":
            CH1 = characters.get(words[i + 1])
            CH1NAME = words[i+1]
        elif word == "CH2":
            CH2 = characters.get(words[i + 1])
            CH2NAME = words[i+1]
        elif words.index("CH1") > words.index("CH2"):
            isCH1speaking = True
        elif words.index("CH1") < words.index("CH2"):
            isCH1speaking = False


            
        else:
            text_words.append(word)
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

    


        
