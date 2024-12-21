import pygame
import os
import sys

class FontManager:
    _instance = None
    initialized = False
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = FontManager()
        return cls._instance
    
    def __init__(self):
        """Initialize the font manager with optimized font sizes."""
        if not self.initialized:
            self.fonts = {}
            self.font_sizes = {
                'huge': 64,      # For main titles
                'title': 48,     # For section titles
                'subtitle': 36,  # For sub-sections
                'large': 32,     # For important text
                'medium': 24,    # For normal text
                'normal': 20,    # For button text
                'small': 16,     # For descriptions
                'tiny': 12       # For additional info
            }
            self._init_default_fonts()
            self.initialize()
            self.initialized = True
    
    def _init_default_fonts(self):
        """Initialize with system default font as fallback"""
        default_sizes = {
            'huge': pygame.font.Font(None, 64),
            'title': pygame.font.Font(None, 48),
            'subtitle': pygame.font.Font(None, 36),
            'large': pygame.font.Font(None, 32),
            'medium': pygame.font.Font(None, 24),
            'normal': pygame.font.Font(None, 20),
            'small': pygame.font.Font(None, 16),
            'tiny': pygame.font.Font(None, 12)
        }
        self.fonts.update(default_sizes)
    
    def initialize(self):
        """Load Pokemon font in all sizes"""
        try:
            # Get the base path for assets
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                base_path = sys._MEIPASS
            else:
                # Running in development
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            font_path = os.path.join(base_path, 'assets', 'fonts', 'PocketMonk-15ze.ttf')
            
            if os.path.exists(font_path):
                pokemon_fonts = {
                    size_name: pygame.font.Font(font_path, size)
                    for size_name, size in self.font_sizes.items()
                }
                self.fonts.update(pokemon_fonts)
                print("Pokemon font loaded successfully")
            else:
                print(f"Pokemon font file not found at: {font_path}")
        except Exception as e:
            print(f"Error loading Pokemon font: {e}")
    
    def get_font(self, size_name='normal'):
        """Get font of specified size"""
        return self.fonts.get(size_name, self.fonts['normal'])

    def cleanup(self):
        """Cleanup font resources"""
        self.fonts.clear()
        self.initialized = False
        FontManager._instance = None
