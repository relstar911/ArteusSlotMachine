import pygame
import os
import sys

class SoundManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized') or not self.initialized:
            pygame.mixer.init()
            self.sounds = {}
            self.music = None
            self.music_tracks = {}
            self.sound_volume = 0.5
            self.music_volume = 0.3
            self.initialized = True
    
    def load_sound(self, name, filename):
        """Load a sound file with error handling"""
        try:
            # Get the base path for assets
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                base_path = sys._MEIPASS
            else:
                # Running in development
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            sound_path = os.path.join(base_path, 'assets', 'sounds', filename)
            if not os.path.exists(sound_path):
                print(f"Warning: Sound file not found: {sound_path}")
                return False
            
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(self.sound_volume)
            self.sounds[name] = sound
            return True
        except Exception as e:
            print(f"Error loading sound {name}: {e}")
            return False
    
    def play_sound(self, name):
        """Play a sound effect by name"""
        try:
            if name in self.sounds:
                self.sounds[name].play()
        except Exception as e:
            print(f"Error playing sound {name}: {e}")
    
    def stop_sound(self, name):
        """Stop a specific sound"""
        try:
            if name in self.sounds:
                self.sounds[name].stop()
        except Exception as e:
            print(f"Error stopping sound {name}: {e}")
    
    def stop_all_sounds(self):
        """Stop all currently playing sound effects"""
        try:
            for sound in self.sounds.values():
                sound.stop()
        except Exception as e:
            print(f"Error stopping sounds: {e}")
    
    def set_sound_volume(self, volume):
        """Set volume for sound effects (0.0 to 1.0)"""
        try:
            self.sound_volume = max(0.0, min(1.0, volume))
            for sound in self.sounds.values():
                sound.set_volume(self.sound_volume)
        except Exception as e:
            print(f"Error setting sound volume: {e}")
    
    def load_music(self, name, filename):
        """Load background music file"""
        try:
            # Get the base path for assets
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                base_path = sys._MEIPASS
            else:
                # Running in development
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            music_path = os.path.join(base_path, 'assets', 'music', filename)
            if not os.path.exists(music_path):
                print(f"Warning: Music file not found: {music_path}")
                return False
            
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.music_volume)
            self.music_tracks[name] = music_path
            return True
        except Exception as e:
            print(f"Error loading music: {e}")
            return False
    
    def play_music(self, name=None, loops=-1):
        """Play background music"""
        try:
            if name is None:
                if self.music is not None:
                    pygame.mixer.music.load(self.music)
                    pygame.mixer.music.play(loops)
            elif name in self.music_tracks:
                pygame.mixer.music.load(self.music_tracks[name])
                pygame.mixer.music.play(loops)
        except Exception as e:
            print(f"Error playing music: {e}")
    
    def stop_music(self):
        """Stop the currently playing music"""
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"Error stopping music: {e}")
    
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
            self.music_tracks.clear()
        except Exception as e:
            print(f"Error during sound cleanup: {e}")
