
import pygame
import random

current_track = None

def play_background_music(playlist): # line 81
    global current_track 
    pygame.mixer.music.set_volume(0.3)

    if playlist == "ambient_room":
        playlist = [
            "Assets/Free use sounds/Room+Tones+-+Signaturesounds.org/Room Tones - Signaturesounds.org/Room-Tone 1.wav",
            "Assets/Free use sounds/Room+Tones+-+Signaturesounds.org/Room Tones - Signaturesounds.org/Room-Tone 2.wav",
            "Assets/Free use sounds/Room+Tones+-+Signaturesounds.org/Room Tones - Signaturesounds.org/Room-Tone 6.wav",
            "Assets/Free use sounds/Room+Tones+-+Signaturesounds.org/Room Tones - Signaturesounds.org/Room-Tone 7.wav",
        ]
    track_to_play = random.choice(playlist)

    if current_track != track_to_play:
        pygame.mixer.music.load(track_to_play)
        current_track = track_to_play
        pygame.mixer.music.play()