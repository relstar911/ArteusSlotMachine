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
        
        # Load fonts
        try:
            self.title_font = self.font_manager.load_font("assets/fonts/Pokemon Solid.ttf", 48)
            self.challenge_font = self.font_manager.load_font("assets/fonts/Pokemon Solid.ttf", 24)
        except:
            print("Pokemon font not found, using default font")
            self.title_font = pygame.font.Font(None, 48)
            self.challenge_font = pygame.font.Font(None, 24)
        
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
        button_y = SCREEN_HEIGHT - 100
        
        # Create buttons
        self.spin_button = Button(
            SCREEN_WIDTH//2 - 60,
            button_y,
            120,
            50,
            "DREHEN",
            color=GREEN,
            hover_color=(100, 255, 100)
        )
        
        self.back_button = Button(
            20,
            button_y,
            120,
            50,
            "ZURÜCK",
            color=RED,
            hover_color=(255, 100, 100)
        )
        
        self.info_button = Button(
            SCREEN_WIDTH - 140,
            button_y,
            120,
            50,
            "INFO",
            color=PURPLE,
            hover_color=(180, 150, 255)
        )
        
        # Create info box
        self.info_box = InfoBox(
            SCREEN_WIDTH//2 - 200,
            SCREEN_HEIGHT//2 - 150,
            400,
            300,
            "Spielregeln"
        )
        
        # Define colors for different challenge levels
        easy_color = (150, 255, 150)      # Light green
        medium_color = (150, 150, 255)    # Light blue
        hard_color = (255, 150, 150)      # Light red
        jackpot_color = (255, 215, 0)     # Gold
        white = (255, 255, 255)           # White
        
        # Set info text with colors
        self.info_box.set_text([
            ("Kombinationen & Challenges:", white),
            ("", white),  # Empty line for spacing
            ("Easy Challenge:", easy_color),
            ("• 1x gleiche Symbole", easy_color),
            ("", white),
            ("Medium Challenge:", medium_color),
            ("• 2x gleiche Symbole", medium_color),
            ("", white),
            ("Hard Challenge:", hard_color),
            ("• 3x gleiche Symbole", hard_color),
            ("", white),
            ("✨ COMMUNITY JACKPOT ✨", jackpot_color),
            ("• 3x Lugia", jackpot_color),
            ("", white),
            ("Drücke DREHEN um zu starten!", white)
        ])

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            self.sound_manager.stop_music()
            return "quit"
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.spin_button.handle_event(event):
                    if not self.rolling:
                        self.start_spin()
                elif self.back_button.handle_event(event):
                    self.running = False
                    self.sound_manager.stop_music()
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
                    self.running = False
                    self.sound_manager.stop_music()
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
                    "✨ COMMUNITY JACKPOT! ✨\nEin glücklicher Zuschauer gewinnt ein Display aus der neuesten Edition!",
                    "✨ COMMUNITY JACKPOT! ✨\nEin glücklicher Zuschauer gewinnt eine Special Illustration Rare ex seiner Wahl!",
                    "✨ COMMUNITY JACKPOT! ✨\nEin glücklicher Zuschauer gewinnt ein Booster Display aus {set}!",
                    "✨ COMMUNITY JACKPOT! ✨\nEin glücklicher Zuschauer gewinnt eine Rare Karte seiner Wahl!"
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
        
        # Draw title with glow effect
        title = self.title_font.render("Pokémon Card Challenge", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        # Draw current challenge if exists
        if self.current_challenge:
            lines = self.current_challenge.split('\n')
            y = SCREEN_HEIGHT - 150
            for line in lines:
                text = self.challenge_font.render(line, True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y))
                self.screen.blit(text, text_rect)
                y += 30
        
        # Draw slot machine
        slot_y = SCREEN_HEIGHT//2 - 65
        for i in range(3):
            slot_x = SCREEN_WIDTH//2 + (i-1)*150
            
            # Add shake effect
            if self.shake_offset:
                slot_x += random.randint(-int(self.shake_offset), int(self.shake_offset))
                slot_y += random.randint(-int(self.shake_offset), int(self.shake_offset))
            
            # Draw slot background with glow effect
            glow_size = self.glow_effect if self.glow_effect > 0 else 0
            if glow_size:
                glow_surface = pygame.Surface((140 + glow_size*2, 140 + glow_size*2), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (*GOLD, 128), glow_surface.get_rect(), border_radius=10)
                self.screen.blit(glow_surface, (slot_x-5-glow_size, slot_y-5-glow_size))
            
            # Draw slot border
            pygame.draw.rect(self.screen, WHITE, (slot_x-5, slot_y-5, 140, 140), border_radius=10)
            pygame.draw.rect(self.screen, BLACK, (slot_x, slot_y, 130, 130), border_radius=8)
            
            # Draw sprite
            symbol = self.SYMBOLS[self.slots[i]]
            if symbol in self.sprites:
                sprite = self.sprites[symbol]
                self.screen.blit(sprite, (slot_x, slot_y))
        
        # Draw buttons
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
        """Cleanup resources when exiting the game"""
        super().cleanup()
        if hasattr(self, 'particle_system'):
            self.particle_system.clear()
        
        # Clear sprite references
        if hasattr(self, 'sprites'):
            self.sprites.clear()
        
        # Clear particle system
        if hasattr(self, 'particle_system'):
            self.particle_system.particles.clear()
            
        # Cleanup fonts
        if hasattr(self, 'font_manager'):
            self.font_manager.cleanup()
    
    def run(self):
        """Main game loop using parent's implementation"""
        self.running = True
        result = None
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.cleanup()
                    return None
                
                result = self.process_event(event)
                if result:
                    break
            
            if result:
                break
                
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
        
        self.cleanup()
        return result or "menu"
