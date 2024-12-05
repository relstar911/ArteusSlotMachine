import pygame
import time
from utils.font_manager import FontManager
from utils.sound_manager import SoundManager

class BaseGame:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.last_update = pygame.time.get_ticks()
        
        # Initialize managers
        self.font_manager = FontManager()
        self.sound_manager = SoundManager()
        
    def handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.cleanup()
                self.running = False
            self.process_event(event)
    
    def process_event(self, event):
        """Override this method in child classes"""
        pass
    
    def update(self):
        """Override this method in child classes"""
        # Calculate delta time for smooth animations
        current_time = pygame.time.get_ticks()
        self.dt = (current_time - self.last_update) / 1000.0  # Convert to seconds
        self.last_update = current_time
    
    def draw(self):
        """Override this method in child classes"""
        pass
    
    def cleanup(self):
        """Clean up resources before exiting"""
        try:
            if hasattr(self, 'sound_manager'):
                self.sound_manager.stop_music()
                self.sound_manager.stop_all_sounds()
            
            # Clear pygame resources
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            
            # Clear any cached resources
            if hasattr(self, 'sprites'):
                self.sprites.clear()
            
        except Exception as e:
            print(f"Warning: Error during cleanup: {e}")
    
    def reset(self):
        """Reset game state and reinitialize resources"""
        self.cleanup()
        self.running = True
        self.last_update = pygame.time.get_ticks()
        if hasattr(self, 'reset_game_state'):
            self.reset_game_state()
        if hasattr(self, 'init_resources'):
            self.init_resources()
        if hasattr(self, 'init_ui'):
            self.init_ui()
    
    def run(self):
        """Main game loop"""
        self.running = True
        result = None
        
        while self.running:
            self.handle_events()
            
            if not self.running:
                break
                
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)
        
        self.cleanup()
        return result
