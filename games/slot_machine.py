import pygame
import random
import os
import math
import time
import sys
from utils.constants import *
from utils.game_base import BaseGame
from utils.sound_manager import SoundManager
from utils.ui_elements import Button, ParticleSystem, InfoBox
from utils.font_manager import FontManager

class SlotMachine(BaseGame):
    def __init__(self, screen):
        super().__init__(screen)  # Initialize BaseGame
        self.screen = screen
        self.last_update = pygame.time.get_ticks()
        self.font_manager = FontManager()
        self.reset_game_state()
        self.init_resources()
        self.init_ui()
        
    def reset_game_state(self):
        """Initialize/Reset all game state variables"""
        self.slots = [0, 0, 0]
        self.rolling = False
        self.roll_time = 0
        self.jackpot_animation = 0
        self.glow_effect = 0
        self.shake_offset = 0
        self.flash_effect = 0
        self.current_challenge = None
        self.challenges_completed = set()
        if hasattr(self, 'particle_system'):
            self.particle_system.clear()
        
    def init_resources(self):
        """Initialize all game resources"""
        # Symbols setup
        self.SYMBOLS = ['Charizard', 'Lugia', 'Tyranitar', 'Gengar', 'Oshawott', 'Arcanine']
        self.WEIGHTS = [15, 5, 20, 20, 20, 20]
        
        # Initialize managers
        self.sound_manager = SoundManager()
        self.particle_system = ParticleSystem()
        
        # Load sounds
        sound_files = {
            'spin': 'spin.wav',
            'stop': 'stop.wav',
            'win': 'win.wav',
            'jackpot': 'jackpot.wav'
        }
        for name, file in sound_files.items():
            self.sound_manager.load_sound(name, f'assets/sounds/{file}')
        self.sound_manager.load_music('background', 'assets/music/1-11-Route-101.wav')
        
        # Set title font from font manager
        self.title_font = self.font_manager.get_font('huge')  # Use huge size for title
        
        # Load and scale sprites
        self.sprites = {}
        for symbol in self.SYMBOLS:
            try:
                sprite_path = os.path.join('assets', 'sprites', f'{symbol.lower()}.png')
                sprite = pygame.image.load(sprite_path).convert_alpha()
                self.sprites[symbol] = pygame.transform.scale(sprite, (130, 130))
            except Exception as e:
                print(f"Error loading sprite {symbol}: {e}")
        
        # Start background music
        self.sound_manager.play_music('background', -1)
        
    def init_ui(self):
        """Initialize all UI elements"""
        # Calculate responsive button positions
        button_width = int(SCREEN_WIDTH * 0.15)  # 15% of screen width
        button_height = int(SCREEN_HEIGHT * 0.08)  # 8% of screen height
        padding = int(SCREEN_WIDTH * 0.02)  # 2% of screen width
        button_y = SCREEN_HEIGHT - button_height - padding
        
        # Create buttons with improved styling
        self.spin_button = Button(
            SCREEN_WIDTH//2 - button_width//2,
            button_y,
            button_width,
            button_height,
            "DREHEN",
            color=GREEN,
            hover_color=(100, 255, 100),
            font=self.font_manager.get_font('normal')
        )
        
        self.back_button = Button(
            padding,
            button_y,
            button_width,
            button_height,
            "ZURÜCK",
            color=RED,
            hover_color=(255, 100, 100),
            font=self.font_manager.get_font('normal')
        )
        
        self.info_button = Button(
            SCREEN_WIDTH - button_width - padding,
            button_y,
            button_width,
            button_height,
            "INFO",
            color=PURPLE,
            hover_color=(180, 150, 255),
            font=self.font_manager.get_font('normal')
        )
        
        # Create info box with responsive size
        info_width = int(SCREEN_WIDTH * 0.5)  # 50% of screen width
        info_height = int(SCREEN_HEIGHT * 0.6)  # 60% of screen height
        self.info_box = InfoBox(
            SCREEN_WIDTH//2 - info_width//2,
            SCREEN_HEIGHT//2 - info_height//2,
            info_width,
            info_height,
            "Spielregeln",
            font=self.font_manager.get_font('medium')
        )
        
        # Define colors for different challenge levels
        easy_color = (150, 255, 150)      # Light green
        medium_color = (150, 150, 255)    # Light blue
        hard_color = (255, 150, 150)      # Light red
        jackpot_color = (255, 215, 0)     # Gold
        white = (255, 255, 255)           # White
        
        # Set info text with colors
        self.info_box.set_text([
            ("🎰 SLOT MACHINE REGELN", jackpot_color),
            ("", white),
            ("🎯 STEUERUNG", white),
            ("• SPACE: Drehen der Walzen", (200, 200, 200)),
            ("• PFEILTASTEN: Walzen stoppen", (200, 200, 200)),
            ("• ESC: Spiel beenden", (200, 200, 200)),
            ("", white),
            ("💫 BELOHNUNGEN", white),
            ("• 1x Symbol = Easy Challenge", easy_color),
            ("  Common & Stage 1 Karten", (200, 200, 200)),
            ("• 2x Symbol = Medium Challenge", medium_color),
            ("  Holo & Full Art Karten", (200, 200, 200)),
            ("• 3x Symbol = Hard Challenge", hard_color),
            ("  Special Art & Gold Karten", (200, 200, 200)),
            ("", white),
            ("🏆 COMMUNITY JACKPOT", jackpot_color),
            ("• 3x Lugia = Jackpot", (255, 223, 0)),
            ("• Gewinne exklusive Community", (255, 223, 0)),
            ("  Presents als Belohnung!", (255, 223, 0)),
            ("", white),
            ("💡 TIPP", white),
            ("Stoppe die Walzen im richtigen", (200, 200, 200)),
            ("Moment für bessere Chancen!", (200, 200, 200))
        ])

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.cleanup()
            return "quit"
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.spin_button.handle_event(event):
                    if not self.rolling:
                        self.start_spin()
                elif self.back_button.handle_event(event):
                    self.cleanup_to_menu()
                    self.running = False
                    return "menu"
                elif self.info_button.handle_event(event):
                    self.info_box.toggle()
        
        # Handle info box scrolling
        if self.info_box.visible:
            self.info_box.handle_scroll(event)
        
        # Update button hover states
        if event.type == pygame.MOUSEMOTION:
            self.spin_button.handle_event(event)
            self.back_button.handle_event(event)
            self.info_button.handle_event(event)
        
        # Handle keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.info_box.visible:
                    self.info_box.visible = False
                else:
                    self.cleanup_to_menu()
                    self.running = False
                    return "menu"
            elif event.key == pygame.K_SPACE and not self.rolling:
                self.start_spin()
        
        return None

    def start_spin(self):
        if not self.rolling:
            self.rolling = True
            self.roll_time = 0
            self.current_challenge = None
            self.sound_manager.play_sound('spin')
            
    def create_win_effects(self):
        """Create visual effects for winning"""
        self.glow_effect = 30
        self.shake_offset = 5
        self.flash_effect = 20
        self.jackpot_animation = 255
        
        # Create particles at random positions around the winning symbols
        for i in range(20):  # Number of particles
            x = random.randint(200, 600)
            y = random.randint(100, 300)
            color = (255, 215, 0, 255)  # Gold color with alpha
            velocity = [random.uniform(-100, 100), random.uniform(-100, 100)]
            self.particle_system.add_particle(
                x, y, color, velocity,
                lifetime=1.0, size=3
            )

    def check_win(self):
        # Count occurrences of each symbol
        symbol_counts = {}
        for slot in self.slots:
            symbol = self.SYMBOLS[slot]
            symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
        
        # Check for special combinations
        max_matches = max(symbol_counts.values())
        
        if max_matches == 3:  # Three of a kind
            symbol = [s for s, count in symbol_counts.items() if count == 3][0]
            if symbol == 'Lugia':  # Jackpot
                jackpot_challenges = [
                    "🏆 COMMUNITY JACKPOT!\n• Ein glücklicher Zuschauer gewinnt ein Display aus der neuesten Edition!\n• Viel Glück an alle!",
                    "🌟 COMMUNITY JACKPOT!\n• Ein glücklicher Zuschauer gewinnt eine Special Illustration Rare ex!\n• Freie Kartenwahl!",
                    "✨ COMMUNITY JACKPOT!\n• Ein glücklicher Zuschauer gewinnt ein Booster Display aus {set}!\n• Brandneue Edition!",
                    "💫 COMMUNITY JACKPOT!\n• Ein glücklicher Zuschauer gewinnt eine Rare Karte!\n• Freie Auswahl garantiert!"
                ]
                self.current_challenge = random.choice(jackpot_challenges).format(set=random.choice(BOOSTER_SETS))
                self.sound_manager.play_sound('jackpot')
                self.create_win_effects()
                return True
            else:  # Hard challenge
                self.current_challenge = random.choice(HARD_CHALLENGES).format(set=random.choice(BOOSTER_SETS))
                self.sound_manager.play_sound('win')
                self.create_win_effects()
                return True
        elif max_matches == 2:  # Two of a kind - Medium challenge
            self.current_challenge = random.choice(MEDIUM_CHALLENGES).format(set=random.choice(BOOSTER_SETS))
            self.sound_manager.play_sound('win')
            self.create_win_effects()
            return True
        else:  # Single symbol - Easy challenge
            self.current_challenge = random.choice(EASY_CHALLENGES).format(set=random.choice(BOOSTER_SETS))
            self.sound_manager.play_sound('win')
            return True

    def update(self):
        # Calculate delta time
        current_time = pygame.time.get_ticks()
        dt = (current_time - self.last_update) / 1000.0  # Convert to seconds
        self.last_update = current_time

        if self.rolling:
            self.roll_time += dt
            
            # Update slots
            for i in range(len(self.slots)):
                if self.roll_time > i * 0.5:  # Stagger the slot stops
                    self.slots[i] = random.choices(range(len(self.SYMBOLS)), weights=self.WEIGHTS)[0]
            
            # Check if rolling should stop
            if self.roll_time >= 2.5:  # Total roll time
                self.rolling = False
                self.sound_manager.play_sound('stop')
                self.check_win()

        # Update effects
        if self.particle_system:
            self.particle_system.update(dt)
        
        # Update info box if it exists
        if hasattr(self, 'info_box'):
            self.info_box.update()
        
        # Update effects
        if self.glow_effect > 0:
            self.glow_effect = max(0, self.glow_effect - 1)
        if self.shake_offset > 0:
            self.shake_offset = max(0, self.shake_offset - 0.5)
        if self.flash_effect > 0:
            self.flash_effect = max(0, self.flash_effect - 1)
        if self.jackpot_animation > 0:
            self.jackpot_animation = max(0, self.jackpot_animation - 2)
        
    def draw(self):
        # Draw background
        self.screen.fill(BLACK)
        
        # Calculate responsive title position
        title_y = int(SCREEN_HEIGHT * 0.1)  # 10% from top
        
        # Draw title with glow effect
        title = self.title_font.render("Pokémon Card Challenge", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, title_y))
        
        # Add title glow effect
        if self.glow_effect > 0:
            glow_surface = pygame.Surface((title.get_width() + 20, title.get_height() + 20), pygame.SRCALPHA)
            glow_color = (*GOLD, int(128 * (self.glow_effect / 30)))
            pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), border_radius=10)
            self.screen.blit(glow_surface, (title_rect.x - 10, title_rect.y - 10))
        
        self.screen.blit(title, title_rect)
        
        # Calculate responsive slot positions
        slot_size = int(min(SCREEN_WIDTH * 0.15, SCREEN_HEIGHT * 0.25))  # Responsive slot size
        slot_spacing = int(slot_size * 1.2)  # Space between slots
        slot_y = SCREEN_HEIGHT//2 - slot_size//2
        
        # Draw slot machine
        for i in range(3):
            slot_x = SCREEN_WIDTH//2 + (i-1)*slot_spacing
            
            # Add shake effect
            if self.shake_offset:
                slot_x += random.randint(-int(self.shake_offset), int(self.shake_offset))
                slot_y += random.randint(-int(self.shake_offset), int(self.shake_offset))
            
            # Draw slot background with glow effect
            glow_size = self.glow_effect if self.glow_effect > 0 else 0
            if glow_size:
                glow_surface = pygame.Surface((slot_size + glow_size*2, slot_size + glow_size*2), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (*GOLD, 128), glow_surface.get_rect(), border_radius=15)
                self.screen.blit(glow_surface, (slot_x-5-glow_size, slot_y-5-glow_size))
            
            # Draw slot border with improved styling
            pygame.draw.rect(self.screen, WHITE, (slot_x-5, slot_y-5, slot_size+10, slot_size+10), border_radius=15)
            pygame.draw.rect(self.screen, BLACK, (slot_x, slot_y, slot_size, slot_size), border_radius=12)
            
            # Draw sprite with proper scaling
            symbol = self.SYMBOLS[self.slots[i]]
            if symbol in self.sprites:
                sprite = pygame.transform.scale(self.sprites[symbol], (slot_size-20, slot_size-20))
                sprite_rect = sprite.get_rect(center=(slot_x + slot_size//2, slot_y + slot_size//2))
                self.screen.blit(sprite, sprite_rect)
        
        # Draw current challenge with improved positioning
        if self.current_challenge:
            challenge_font = self.font_manager.get_font('medium')
            lines = self.current_challenge.split('\n')
            
            # Calculate total height needed
            total_height = len(lines) * int(SCREEN_HEIGHT * 0.05)  # 5% spacing between lines
            start_y = int(SCREEN_HEIGHT * 0.75) - total_height // 2  # Center vertically in bottom quarter
            
            # Draw each line with proper spacing and effects
            for i, line in enumerate(lines):
                # Größere Schrift für Überschriften (erste Zeile jeder Challenge)
                if i == 0:
                    text = self.font_manager.get_font('subtitle').render(line, True, GOLD)
                # Kleinere Schrift für Details (mit Aufzählungszeichen)
                else:
                    text = challenge_font.render(line, True, WHITE)
                
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, start_y + i * int(SCREEN_HEIGHT * 0.05)))
                
                # Add glow effect for important text
                if self.glow_effect > 0:
                    glow_surface = pygame.Surface((text.get_width() + 10, text.get_height() + 10), pygame.SRCALPHA)
                    glow_color = (255, 255, 255, int(64 * (self.glow_effect / 30)))
                    pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), border_radius=5)
                    self.screen.blit(glow_surface, (text_rect.x - 5, text_rect.y - 5))
                
                self.screen.blit(text, text_rect)
        
        # Draw UI elements
        self.spin_button.draw(self.screen)
        self.back_button.draw(self.screen)
        self.info_button.draw(self.screen)
        
        # Draw info box if visible
        if self.info_box.visible:
            self.info_box.draw(self.screen, self.font_manager)
        
        # Draw particles
        self.particle_system.draw(self.screen)
        
        # Update display
        pygame.display.flip()
    
    def cleanup(self):
        """Clean up resources before closing completely"""
        try:
            if hasattr(self, 'info_box'):
                self.info_box.visible = False
            if hasattr(self, 'sound_manager'):
                self.sound_manager.stop_music()
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def cleanup_to_menu(self):
        """Clean up resources when returning to menu"""
        try:
            if hasattr(self, 'info_box'):
                self.info_box.visible = False
            if hasattr(self, 'sound_manager'):
                self.sound_manager.stop_music()
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def run(self):
        """Main game loop using parent's implementation"""
        self.running = True
        result = None
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.cleanup()
                    return "quit"
                
                result = self.process_event(event)
                if result:
                    break
            
            if result:
                break
                
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
        
        if result == "menu":
            self.cleanup_to_menu()
        else:
            self.cleanup()
        return result
