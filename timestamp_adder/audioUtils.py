import pygame
from time import sleep

class musicPlayer:
    def __init__(self, filepath, play_on_start = False):
        pygame.mixer.init()
        sound = pygame.mixer.Sound(filepath)
        self.length = sound.get_length()*1000


        

        pygame.mixer.music.load(filepath)
        self.music = pygame.mixer.music
        self.music.play(loops=-1) #we want the music to repeat indefinitely
        self.music.pause()
        if play_on_start:
            self.is_paused = False
            self.music.unpause()
        
        #these two variables are used to calculate the current position
        self.start_pos = 0
        self.initial_get_pos = 0
        self.seconds_playing_at_start = self.music.get_pos()

        self.is_paused = True
            
    def unpause(self):
        self.is_paused = False
        self.music.unpause()
    def pause(self):
        self.is_paused = True
        self.music.pause()
    def set_pos(self, pos):
        #input in milliseconds
        self.start_pos = pos
        self.initial_get_pos = self.music.get_pos()
        self.music.set_pos(pos/1000)
    def get_pos(self):
        #returns current position in milliseconds
        return (self.music.get_pos() - self.initial_get_pos + self.start_pos) % (self.length)
    def quit(self):
        pygame.mixer.quit()
    def play_range(self, start_time, end_time):
        # plays the audio starting at start_time, ending at end_time (both in milliseconds)
        # note that this is blocking
        self.set_pos(start_time)
        self.music.unpause()
        sleep((end_time - start_time)/1000)
        self.music.pause()


