import pygame
import os
from utils.constants import DEFAULT_SOUND_VOLUME, DEFAULT_MUSIC_VOLUME

class SoundManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if not self.initialized:
            self.sounds = {}
            self.music = None
            self.sound_volume = DEFAULT_SOUND_VOLUME
            self.music_volume = DEFAULT_MUSIC_VOLUME
            self.initialized = True
    
    def load_sound(self, name, path):
        """Load a sound file with error handling"""
        try:
            if not os.path.exists(path):
                print(f"Warning: Sound file not found: {path}")
                return False
                
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.sound_volume)
            self.sounds[name] = sound
            return True
        except Exception as e:
            print(f"Error loading sound {name}: {e}")
            return False
    
    def load_music(self, name, path):
        """Load background music file"""
        try:
            if not os.path.exists(path):
                print(f"Warning: Music file not found: {path}")
                return False
                
            self.music = path
            return True
        except Exception as e:
            print(f"Error loading music {name}: {e}")
            return False
    
    def play_sound(self, sound_name):
        """Play a sound effect by name"""
        try:
            if sound_name in self.sounds:
                self.sounds[sound_name].play()
        except Exception as e:
            print(f"Error playing sound {sound_name}: {e}")
    
    def stop_all_sounds(self):
        """Stop all currently playing sound effects"""
        try:
            for sound in self.sounds.values():
                sound.stop()
        except Exception as e:
            print(f"Error stopping sounds: {e}")
    
    def play_music(self, name, loops=-1):
        """Play background music with error handling"""
        try:
            if self.music and os.path.exists(self.music):
                pygame.mixer.music.load(self.music)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loops)
            else:
                print(f"Warning: No music file loaded for {name}")
        except Exception as e:
            print(f"Error playing music {name}: {e}")
    
    def stop_music(self):
        """Stop currently playing music"""
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"Error stopping music: {e}")
    
    def set_sound_volume(self, volume):
        """Set volume for sound effects (0.0 to 1.0)"""
        try:
            self.sound_volume = max(0.0, min(1.0, volume))
            for sound in self.sounds.values():
                sound.set_volume(self.sound_volume)
        except Exception as e:
            print(f"Error setting sound volume: {e}")
    
    def set_music_volume(self, volume):
        """Set volume for background music (0.0 to 1.0)"""
        try:
            self.music_volume = max(0.0, min(1.0, volume))
            pygame.mixer.music.set_volume(self.music_volume)
        except Exception as e:
            print(f"Error setting music volume: {e}")
            
    def cleanup(self):
        """Clean up sound resources"""
        try:
            self.stop_music()
            self.stop_all_sounds()
            self.sounds.clear()
            self.music = None
        except Exception as e:
            print(f"Error during sound cleanup: {e}")
