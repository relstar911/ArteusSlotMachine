import pygame
import random
import os
import math
import time
from utils.constants import *
from utils.font_manager import FontManager
from utils.ui_elements import Button, InfoBox, PrizeConfig, ParticleSystem, Slot, WonPrizesList
from games.prizes import JACKPOT_PRIZE, MAIN_PRIZES, DOUBLE_PRIZES, EASY_PRIZES
from utils.sound_manager import SoundManager
from utils.game_base import BaseGame
from games.constants import MAIN_HITS, EASY_WINS, MEDIUM_WINS, HARD_WINS, COMMUNITY_JACKPOT
import sys

class SlotMachine(BaseGame):
    def __init__(self, screen):
        super().__init__(screen)  # Initialize BaseGame
        self.screen = screen
        self.last_update = pygame.time.get_ticks()
        self.font_manager = FontManager()
        
        # Initialize state variables
        self.slots = [0, 0, 0]
        self.rolling = False
        self.roll_time = 0
        self.jackpot_animation = 0
        self.glow_effect = 0
        self.shake_offset = 0
        self.flash_effect = 0
        self.current_challenge = None
        self.challenges_completed = set()
        self.spin_count = 0  # Zähler für Spins
        
        # Initialize UI elements first
        self.init_ui()
        
        # Initialize other resources
        self.init_resources()
        
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
        self.spin_count = 0  # Reset Zähler für Spins
        if hasattr(self, 'particle_system'):
            self.particle_system.clear()
        
    def init_resources(self):
        """Initialize all game resources"""
        # Symbols setup
        self.SYMBOLS = ['Lugia', 'Charizard', 'Tyranitar', 'Gengar', 'Oshawott', 'Arcanine']
        # Neue Gewichtungen (Total: 100)
        self.WEIGHTS = [5,      # Lugia (5%) - Realistischer
                       23,      # Charizard (23%)
                       23,      # Tyranitar (23%)
                       23,      # Gengar (23%)
                       13,      # Oshawott (13%)
                       13]      # Arcanine (13%)
        
        # Initialize fonts
        self.title_font = self.font_manager.get_font('title')
        self.normal_font = self.font_manager.get_font('normal')
        
        # Initialize managers
        self.sound_manager = SoundManager()
        self.particle_system = ParticleSystem()
        
        # Load sprites
        self.sprites = {}
        for symbol in self.SYMBOLS:
            try:
                # Get the base path for assets
                if getattr(sys, 'frozen', False):
                    # Running as compiled executable
                    base_path = sys._MEIPASS
                else:
                    # Running in development
                    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                
                sprite_path = os.path.join(base_path, 'assets', 'sprites', f'{symbol.lower()}.png')
                self.sprites[symbol] = pygame.image.load(sprite_path).convert_alpha()
            except Exception as e:
                print(f"Error loading sprite {symbol}: {str(e)}")
                # Use a default sprite or placeholder
                self.sprites[symbol] = pygame.Surface((100, 100))
                self.sprites[symbol].fill(RED)
        
        # Load sounds
        sound_files = {
            'spin': 'spin.wav',
            'stop': 'stop.wav',
            'win': 'win.wav',
            'jackpot': 'jackpot.wav'
        }
        for name, file in sound_files.items():
            self.sound_manager.load_sound(name, file)
        
        # Set title font from font manager
        self.title_font = self.font_manager.get_font('huge')  # Use huge size for title
        
        # Load and scale sprites
        for symbol in self.SYMBOLS:
            try:
                # Get the base path for assets
                if getattr(sys, 'frozen', False):
                    # Running as compiled executable
                    base_path = sys._MEIPASS
                else:
                    # Running in development
                    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                
                sprite_path = os.path.join(base_path, 'assets', 'sprites', f'{symbol.lower()}.png')
                sprite = pygame.image.load(sprite_path).convert_alpha()
                self.sprites[symbol] = pygame.transform.scale(sprite, (130, 130))
            except Exception as e:
                print(f"Error loading sprite {symbol}: {e}")
        
        # Start background music
        self.sound_manager.load_music('background', '1-11-Route-101.wav')
        self.sound_manager.play_music('background')
        
        # Initialize prize list
        self.won_prizes_list = WonPrizesList(
            20,                 # x position
            100,               # y position
            200,               # width
            SCREEN_HEIGHT - 200, # height
            self.normal_font
        )
        self.won_prizes_list.slot_machine = self  # Setze Referenz zur SlotMachine
        self.won_prizes_list.load_prizes()
        
        # Update positions based on screen size
        if hasattr(self, 'scale_x'):
            self.won_prizes_list.update_position(self.scale_x, self.scale_y)
        
    def init_ui(self):
        """Initialize all UI elements"""
        # Button dimensions and positioning
        button_width = 150
        button_height = 50
        padding = 20
        button_spacing = 20
        button_y = SCREEN_HEIGHT - button_height - padding
        
        self.back_button = Button(
            padding,  # Left-most button
            button_y,
            button_width,
            button_height,
            "ZURÜCK",
            color=RED,
            hover_color=(255, 100, 100),
            font=self.font_manager.get_font('normal')
        )
        
        self.info_button = Button(
            padding + button_width + button_spacing,  # Second button
            button_y,
            button_width,
            button_height,
            "INFO",
            color=PURPLE,
            hover_color=(180, 150, 255),
            font=self.font_manager.get_font('normal')
        )
        
        self.spin_button = Button(
            padding + (2 * button_width) + (2 * button_spacing),  # Third button
            button_y,
            button_width,
            button_height,
            "DREHEN",
            color=GREEN,
            hover_color=(100, 255, 100),
            font=self.font_manager.get_font('normal')
        )
        
        self.config_button = Button(
            padding + (3 * button_width) + (3 * button_spacing),  # Right-most button
            button_y,
            button_width,
            button_height,
            "CONFIG",
            color=BLUE,
            hover_color=(100, 100, 255),
            font=self.font_manager.get_font('normal')
        )
        
        # Center the slots in the screen
        slot_size = 128  # Size of each slot
        slot_spacing = 20  # Space between slots
        total_slot_width = (3 * slot_size) + (2 * slot_spacing)
        slot_start_x = (SCREEN_WIDTH - total_slot_width) // 2
        slot_y = (SCREEN_HEIGHT - slot_size - button_height - (2 * padding)) // 2
        
        # Create slots with even spacing
        self.slots = []
        for i in range(3):
            x = slot_start_x + (i * (slot_size + slot_spacing))
            self.slots.append(Slot(x, slot_y, slot_size))
        
        # Create info box with responsive size
        info_width = int(SCREEN_WIDTH * 0.5)  # 50% of screen width
        info_height = int(SCREEN_HEIGHT * 0.6)  # 60% of screen height
        info_x = (SCREEN_WIDTH - info_width) // 2
        info_y = (SCREEN_HEIGHT - info_height) // 2
        
        self.info_box = InfoBox(
            info_x, info_y,
            info_width, info_height,
            "Information",
            font=self.font_manager.get_font('normal')
        )
        
        # Create config window
        config_width = int(SCREEN_WIDTH * 0.4)
        config_height = int(SCREEN_HEIGHT * 0.7)
        self.prize_config = PrizeConfig(
            SCREEN_WIDTH//2 - config_width//2,
            SCREEN_HEIGHT//2 - config_height//2,
            config_width,
            config_height,
            self.font_manager.get_font('normal')
        )
        
        # Define colors for different challenge levels
        easy_color = (150, 255, 150)      # Light green
        medium_color = (150, 150, 255)    # Light blue
        hard_color = (255, 150, 150)      # Light red
        jackpot_color = (255, 215, 0)     # Gold
        white = (255, 255, 255)           # White
        
        # Set info text with colors
        self.info_box.set_text([
            ("🎰 POKEMON CARD SLOT", jackpot_color),
            ("", white),
            ("🎯 STEUERUNG", white),
            ("• SPACE: Drehen der Walzen", (200, 200, 200)),
            ("• ESC: Zurück zum Menü", (200, 200, 200)),
            ("", white),
            ("💫 GEWINNE & CHANCEN", white),
            ("• Verschiedene Symbole", easy_color),
            ("  1x Japanisches Boosterpack", (200, 200, 200)),
            ("", white),
            ("• 2x Gleiche Symbole", medium_color),
            ("  70% = 3x Japanische Booster", (200, 200, 200)),
            ("  30% = Illustration/Secret Rare", (200, 200, 200)),
            ("  Chance: ~48% (Fast jeder 2. Spin)", (180, 180, 180)),
            ("", white),
            ("• 3x Gleiche Symbole", hard_color),
            ("  Pokemon Karte im Wert", (200, 200, 200)),
            ("  von bis zu 25€!", (200, 200, 200)),
            ("  Chance: ~4% (Etwa alle 25 Spins)", (180, 180, 180)),
            ("", white),
            ("🏆 HAUPTGEWINN", jackpot_color),
            ("• 3x Lugia = Hauptpreis", (255, 223, 0)),
            ("• Aktuell:", (255, 223, 0)),
            (f"  {JACKPOT_PRIZE}", (255, 223, 0)),
            ("  Chance: ~0.01% (Etwa alle 125 Spins)", (255, 223, 0)),
            ("", white),
            ("💡 TIPP", white),
            ("Jeder Spin gewinnt mindestens", (200, 200, 200)),
            ("ein japanisches Boosterpack!", (200, 200, 200))
        ])
        
    def process_event(self, event):
        """Handle all game events"""
        if event.type == pygame.QUIT:
            self.running = False
            
        # Handle button events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.info_box.visible:
                self.info_box.handle_event(event)
                return
                
            if self.prize_config.visible:
                if self.prize_config.handle_event(event):
                    # Update prizes if changed
                    prizes = self.prize_config.get_prizes()
                    if prizes['jackpot']:
                        global JACKPOT_PRIZE
                        JACKPOT_PRIZE = prizes['jackpot']
                    if prizes['main']:
                        global MAIN_PRIZES
                        MAIN_PRIZES[:] = prizes['main']
                    if prizes['double']:
                        global DOUBLE_PRIZES
                        DOUBLE_PRIZES[:] = prizes['double']
                    if prizes['easy']:
                        global EASY_PRIZES
                        EASY_PRIZES[:] = prizes['easy']
                return
                
            if self.won_prizes_list.handle_event(event):
                return True
                
            if self.spin_button.handle_event(event):
                if not self.prize_config.visible:
                    self.start_spin()
            elif self.back_button.handle_event(event):
                self.cleanup_to_menu()
                return "menu"
            elif self.info_button.handle_event(event):
                self.info_box.visible = True
            elif self.config_button.handle_event(event):
                self.prize_config.visible = True
                
        # Handle keyboard events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.prize_config.visible:
                    self.prize_config.visible = False
                elif self.info_box.visible:
                    self.info_box.visible = False
                else:
                    self.running = False
                    return "menu"
            if self.prize_config.visible:
                self.prize_config.handle_event(event)
                return
                
            if self.info_box.visible:
                if event.key == pygame.K_ESCAPE:
                    self.info_box.visible = False
                else:
                    self.info_box.handle_event(event)
                return
                
            if event.key == pygame.K_SPACE:
                if not self.prize_config.visible:
                    self.start_spin()
            elif event.key == pygame.K_F11:  # F11 für Vollbild
                self.is_fullscreen = not self.is_fullscreen
                self.init_display()
            elif event.key == pygame.K_ESCAPE:
                self.running = False
                
        elif event.type == pygame.MOUSEWHEEL:
            if self.info_box.visible:
                self.info_box.handle_event(event)
        elif event.type == pygame.VIDEORESIZE and not self.is_fullscreen:
            self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            self.actual_width = event.w
            self.actual_height = event.h
            self.scale_x = self.actual_width / SCREEN_WIDTH
            self.scale_y = self.actual_height / SCREEN_HEIGHT
            self.init_resources()
            return True

    def start_spin(self):
        if not self.rolling:
            self.spin_count += 1  # Erhöhe Zähler bei jedem Spin
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
        """Check win condition and return prize"""
        # Count symbols
        counts = {}
        for slot in self.slots:
            symbol = slot.symbol
            counts[symbol] = counts.get(symbol, 0) + 1
            
        # Check for 3 Lugia (Jackpot)
        if counts.get(0, 0) == 3:  # Lugia ist Index 0
            self.sound_manager.play_sound('jackpot')
            self.create_win_effects()
            win_text = f" HAUPTGEWINN!\n• {JACKPOT_PRIZE}\n• Herzlichen Glückwunsch!"
            self.won_prizes_list.add_prize(f"Jackpot: {JACKPOT_PRIZE}")
            return win_text
            
        # Check for 3 of any other symbol
        for symbol, count in counts.items():
            if count == 3:
                prize = MAIN_PRIZES[symbol - 1] if symbol > 0 and symbol <= len(MAIN_PRIZES) else "Kein Preis konfiguriert"
                self.sound_manager.play_sound('win')
                self.create_win_effects()
                symbol_name = self.SYMBOLS[symbol]
                win_text = f" SUPER GEWINN!\n• 3x {symbol_name}\n• {prize}"
                self.won_prizes_list.add_prize(f"{symbol_name}: {prize}")
                return win_text
                
        # Check for 2 of any symbol
        for symbol, count in counts.items():
            if count == 2:
                prize = random.choice(DOUBLE_PRIZES) if DOUBLE_PRIZES else "Kein Preis konfiguriert"
                self.sound_manager.play_sound('win')
                return f" GEWONNEN!\n• {prize}\n• Viel Spaß!"
                
        # No matches
        prize = random.choice(EASY_PRIZES) if EASY_PRIZES else "Kein Preis konfiguriert"
        self.sound_manager.play_sound('win')
        return f" GEWONNEN!\n• {prize}\n• Viel Spaß!"

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
                    self.slots[i].symbol = random.choices(range(len(self.SYMBOLS)), weights=self.WEIGHTS)[0]
            
            # Check if rolling should stop
            if self.roll_time >= 2.5:  # Total roll time
                self.rolling = False
                self.sound_manager.play_sound('stop')
                self.current_challenge = self.check_win()

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
        """Draw the game state"""
        try:
            # Draw background
            self.screen.fill(BLACK)
            
            # Calculate responsive title position
            title_y = int(SCREEN_HEIGHT * 0.1)  # 10% from top
            
            # Draw title with glow effect
            title = self.title_font.render("Arteus Pokémon Slot", True, GOLD)
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
                slot_x = SCREEN_WIDTH//2 - slot_spacing + 150 + (i-1)*slot_spacing
                
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
                symbol = self.SYMBOLS[self.slots[i].symbol]
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
            if hasattr(self, 'spin_button'):
                self.spin_button.draw(self.screen)
            if hasattr(self, 'back_button'):
                self.back_button.draw(self.screen)
            if hasattr(self, 'info_button'):
                self.info_button.draw(self.screen)
            if hasattr(self, 'config_button'):
                self.config_button.draw(self.screen)
            
            # Draw won prizes list
            self.won_prizes_list.draw(self.screen)
            
            # Draw info box if visible
            if hasattr(self, 'info_box') and self.info_box.visible:
                self.info_box.draw(self.screen, self.font_manager)
                
            # Draw prize config if visible
            if hasattr(self, 'prize_config') and self.prize_config.visible:
                self.prize_config.draw(self.screen)
            
            # Draw particles
            if hasattr(self, 'particle_system'):
                self.particle_system.draw(self.screen)
            
            # Update display
            pygame.display.flip()
            
        except Exception as e:
            print(f"Error in draw(): {str(e)}")

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
            if hasattr(self, 'prize_config'):
                self.prize_config.visible = False
            if hasattr(self, 'sound_manager'):
                self.sound_manager.stop_music()
                
            # Reset all states
            self.rolling = False
            self.roll_time = 0
            self.current_challenge = None
            self.jackpot_animation = 0
            self.glow_effect = 0
            self.shake_offset = 0
            self.flash_effect = 0
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
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.prize_config.visible:
                            self.prize_config.visible = False
                        elif self.info_box.visible:
                            self.info_box.visible = False
                        else:
                            self.cleanup_to_menu()
                            return "menu"
                            
                result = self.process_event(event)
                if result:
                    return result
                    
            self.update()
            self.draw()
            pygame.time.wait(10)
