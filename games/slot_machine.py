import pygame
import random
import os
import sys
from pygame import mixer
from .constants import *
import math
import time

class SlotMachine:
    def __init__(self, screen):
        self.screen = screen
        self.WINDOW_WIDTH = screen.get_width()
        self.WINDOW_HEIGHT = screen.get_height()
        self.running = True
        self.slots = [0, 0, 0]
        self.rolling = False
        self.roll_time = 0
        self.jackpot_animation = 0
        self.jackpot_particles = []
        
        # Constants
        self.SLOT_WIDTH = 150
        self.SLOT_HEIGHT = 150
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GOLD = (255, 215, 0)
        self.BLUE = (50, 150, 255)
        self.PURPLE = (147, 112, 219)
        
        # UI Settings
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 50
        self.BUTTON_RADIUS = 10
        
        # Animation Settings
        self.particles = []
        self.glow_effect = 0
        self.shake_offset = 0
        self.flash_effect = 0
        
        # Buttons
        button_y = self.WINDOW_HEIGHT - 100
        self.spin_button = pygame.Rect(
            self.WINDOW_WIDTH//2 - self.BUTTON_WIDTH//2,
            button_y,
            self.BUTTON_WIDTH,
            self.BUTTON_HEIGHT
        )
        
        self.back_button = pygame.Rect(
            20,
            button_y,
            120,
            self.BUTTON_HEIGHT
        )
        
        # Fonts
        try:
            self.title_font = pygame.font.Font("assets/fonts/Pokemon Solid.ttf", 48)
            self.button_font = pygame.font.Font("assets/fonts/Pokemon Solid.ttf", 24)
            self.challenge_font = pygame.font.Font("assets/fonts/Pokemon Solid.ttf", 20)
        except:
            self.title_font = pygame.font.Font(None, 48)
            self.button_font = pygame.font.Font(None, 24)
            self.challenge_font = pygame.font.Font(None, 20)
        
        # Booster Sets
        self.SETS = [
            "Scarlet & Violet - 151",
            "Paldea Evolved",
            "Scarlet & Violet Base Set",
            "Obsidian Flames",
            "Paradise Lost",
            "Paradox Rift"
        ]

        # Challenge Lists
        self.EASY_CHALLENGES = [
            "Aus Obsidian Flames: Ziehe 1 Basic-Pokémon mit Feuer-Energie ",
            "Aus Paldea Evolved: Ziehe 1 Trainer mit Unterstützer-Symbol ",
            "Aus Paradise Lost: Ziehe 1 Item-Karte mit Werkzeug ",
            "Aus SV Base Set: Ziehe 1 Basic-Pokémon mit Fähigkeit ",
            "Aus Paradox Rift: Ziehe 1 Reverse Holo Trainer ",
            "Aus SV-151: Ziehe 1 Basic-Pokémon der 1. Generation ",
            "Aus Obsidian Flames: Ziehe 1 Spezial-Energie ",
            "Aus Paradise Lost: Ziehe 1 Stadion-Karte ",
            "Aus Paldea Evolved: Ziehe 1 Tera-Basic-Pokémon ",
            "Aus Paradox Rift: Ziehe 1 Zukunfts-Pokémon "
        ]

        self.MEDIUM_CHALLENGES = [
            "Aus Obsidian Flames: Ziehe 1 Illustration Rare (IR) ",
            "Aus Paldea Evolved: Ziehe 1 Full Art Trainer ",
            "Aus SV-151: Ziehe 1 Holo-Rare der 1. Generation ",
            "Aus Paradise Lost: Ziehe 1 Special Art Rare (SAR) ",
            "Aus Paradox Rift: Ziehe 1 Double Rare (2x) ",
            "Aus Obsidian Flames: Ziehe 1 Ultra Rare ex-Pokémon ",
            "Aus Paldea Evolved: Ziehe 1 Trainer Gallery Rare ",
            "Aus SV Base Set: Ziehe 1 Full Art ex-Pokémon ",
            "Aus Paradise Lost: Ziehe 1 Ancient/Future Rare ",
            "Aus Paradox Rift: Ziehe 1 Tera Type ex-Pokémon "
        ]

        self.HARD_CHALLENGES = [
            "Aus Obsidian Flames: Ziehe 1 Alternative Art ex ",
            "Aus Paldea Evolved: Ziehe 1 Secret Rare Trainer ",
            "Aus SV-151: Ziehe 1 Special Illustration Rare (SIR) ",
            "Aus Paradise Lost: Ziehe 1 Gold Secret Rare ",
            "Aus Paradox Rift: Ziehe 1 Hyper Rare Rainbow ",
            "Aus Obsidian Flames: Ziehe 1 Alternative Art Tera ex ",
            "Aus Paldea Evolved: Ziehe 1 Gold Energy ",
            "Aus SV Base Set: Ziehe 1 Special Art Rare (SAR) ex ",
            "Aus Paradise Lost: Ziehe 1 Gold Ultra Rare ",
            "Aus Paradox Rift: Ziehe 1 Alternative Art Ancient/Future "
        ]

        self.COMMUNITY_PRESENTS = [
            "Eine Elite Trainer Box Obsidian Flames + Display Paradox Rift! ",
            "Ein Booster Bundle (10 Packs) aus jedem Scarlet & Violet Set! ",
            "Ein 151 Premium Collection Display + ETB! ",
            "Eine Tera Charizard-ex Premium Collection + Display Paldea Evolved! ",
            "Ein Komplett-Set Trainer Gallery aus Paradise Lost! ",
            "Eine Paradox Rift Ultra-Premium Collection! ",
            "Ein Master Set Commons/Uncommons aus allen S&V Sets! ",
            "Eine Japanese Box + English Booster Bundle! "
        ]

        # Challenge Tracking
        self.current_challenge = None

        # Sound initialization
        try:
            # Load sound effects
            self.ROLL_SOUND = pygame.mixer.Sound(os.path.join("assets", "sounds", "spin.wav"))
            self.STOP_SOUND = pygame.mixer.Sound(os.path.join("assets", "sounds", "stop.wav"))
            self.JACKPOT_SOUND = pygame.mixer.Sound(os.path.join("assets", "sounds", "jackpot.wav"))
            self.CLICK_SOUND = pygame.mixer.Sound(os.path.join("assets", "sounds", "stop.wav"))  # Using stop.wav for click
            
            # Set sound volumes
            if self.ROLL_SOUND: self.ROLL_SOUND.set_volume(0.3)
            if self.STOP_SOUND: self.STOP_SOUND.set_volume(0.3)
            if self.JACKPOT_SOUND: self.JACKPOT_SOUND.set_volume(0.5)
            if self.CLICK_SOUND: self.CLICK_SOUND.set_volume(0.2)  # Lower volume for click
            
            # Load and start background music
            pygame.mixer.music.load(os.path.join("assets", "music", "1-11-Route-101.wav"))
            pygame.mixer.music.set_volume(0.4)  # Lower volume for background music
            pygame.mixer.music.play(-1)  # Loop indefinitely
        except Exception as e:
            print(f"Warning: Some sound files could not be loaded: {e}")
            self.ROLL_SOUND = None
            self.STOP_SOUND = None
            self.JACKPOT_SOUND = None
            self.CLICK_SOUND = None
        
        # Slot symbols (neue Pokemon)
        self.SYMBOLS = ['Charizard', 'Oshawott', 'Tyranitar', 'Lugia']
        
        # Load Pokemon sprites
        self.sprites = {}
        for symbol in self.SYMBOLS:
            try:
                sprite_path = os.path.join('assets', 'sprites', f'{symbol.lower()}.png')
                sprite = pygame.image.load(sprite_path)
                sprite = pygame.transform.scale(sprite, (self.SLOT_WIDTH-20, self.SLOT_HEIGHT-20))
                self.sprites[symbol] = sprite
            except Exception as e:
                print(f"Error loading sprite for {symbol}: {e}")
                sprite = pygame.Surface((self.SLOT_WIDTH-20, self.SLOT_HEIGHT-20))
                sprite.fill(self.BLACK)
                pygame.draw.rect(sprite, (50, 50, 50), sprite.get_rect(), 3)
                font = pygame.font.Font(None, 24)
                text = font.render(symbol, True, (100, 100, 100))
                text_rect = text.get_rect(center=sprite.get_rect().center)
                sprite.blit(text, text_rect)
                self.sprites[symbol] = sprite

    def create_particles(self):
        self.jackpot_particles = []
        for _ in range(50):
            particle = {
                'x': self.WINDOW_WIDTH // 2,
                'y': self.WINDOW_HEIGHT // 2,
                'dx': random.uniform(-5, 5),
                'dy': random.uniform(-5, 5),
                'life': 255
            }
            self.jackpot_particles.append(particle)
    
    def update_particles(self):
        for particle in self.jackpot_particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 3
            if particle['life'] <= 0:
                self.jackpot_particles.remove(particle)
    
    def roll(self):
        if not self.rolling:
            self.rolling = True
            self.roll_time = pygame.time.get_ticks()
            if self.ROLL_SOUND:
                self.ROLL_SOUND.play()
    
    def check_win(self):
        symbols = self.slots
        
        # Count occurrences of each symbol
        symbol_counts = {}
        for symbol in symbols:
            if symbol in symbol_counts:
                symbol_counts[symbol] += 1
            else:
                symbol_counts[symbol] = 1
        
        # Check for Lugia Jackpot (3 Lugias)
        if symbol_counts.get("Lugia", 0) == 3:
            self.current_challenge = f" JACKPOT! \nEin glücklicher Zuschauer gewinnt:\n{random.choice(self.COMMUNITY_PRESENTS)}"
            return "jackpot"
        
        # Get the maximum number of matching symbols
        max_matches = max(symbol_counts.values())
        
        if max_matches == 1:  # Alle Symbole verschieden = Leicht
            self.current_challenge = random.choice(self.EASY_CHALLENGES)
            return "easy"
        elif max_matches == 2:  # 2 gleiche Symbole = Mittel
            self.current_challenge = random.choice(self.MEDIUM_CHALLENGES)
            return "medium"
        elif max_matches == 3:  # 3 gleiche Symbole (außer Lugia) = Schwer
            self.current_challenge = random.choice(self.HARD_CHALLENGES)
            return "hard"
        
        self.current_challenge = "Versuche es nochmal!"
        return None

    def get_challenge(self, difficulty):
        # Select a random set
        selected_set = random.choice(self.SETS)
        
        if difficulty == "jackpot":
            return f" JACKPOT! \nEin glücklicher Zuschauer gewinnt:\n{random.choice(self.COMMUNITY_PRESENTS)}".format(set=selected_set)
        elif difficulty == "easy":
            return random.choice(self.EASY_CHALLENGES).format(set=selected_set)
        elif difficulty == "medium":
            return random.choice(self.MEDIUM_CHALLENGES).format(set=selected_set)
        elif difficulty == "hard":
            return random.choice(self.HARD_CHALLENGES).format(set=selected_set)
        return "Versuche es nochmal!"
    
    def update(self):
        if self.rolling:
            current_time = pygame.time.get_ticks()
            if current_time - self.roll_time > 2000:  # Roll for 2 seconds
                self.rolling = False
                # Generate final results
                self.slots = [random.choice(self.SYMBOLS) for _ in range(3)]
                if self.STOP_SOUND:
                    self.STOP_SOUND.play()
                # Check for jackpot
                if self.check_win() == "jackpot":
                    if self.JACKPOT_SOUND:
                        self.JACKPOT_SOUND.play()
                    self.jackpot_animation = 255
                    self.create_particles()
            else:
                # Update spinning animation
                self.slots = [random.choice(self.SYMBOLS) for _ in range(3)]
        
        # Update jackpot animation
        if self.jackpot_animation > 0:
            self.jackpot_animation = max(0, self.jackpot_animation - 2)
            self.update_particles()
    
    def draw_rounded_rect(self, surface, color, rect, radius):
        """Draw a rounded rectangle"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)
        
    def create_gradient(self, color1, color2, height):
        """Create a vertical gradient surface"""
        gradient = pygame.Surface((self.WINDOW_WIDTH, height))
        for i in range(height):
            factor = i / height
            gradient_color = (
                color1[0] + (color2[0] - color1[0]) * factor,
                color1[1] + (color2[1] - color1[1]) * factor,
                color1[2] + (color2[2] - color1[2]) * factor
            )
            pygame.draw.line(gradient, gradient_color, (0, i), (self.WINDOW_WIDTH, i))
        return gradient
        
    def add_particles(self, x, y, color):
        """Add particles for effects"""
        for _ in range(10):
            speed = random.uniform(2, 5)
            angle = random.uniform(0, 2 * math.pi)
            self.particles.append({
                'x': x,
                'y': y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'color': color,
                'life': 60
            })
            
    def update_particles(self):
        """Update particle positions and life"""
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)

    def draw(self):
        # Hintergrund mit Gradient
        gradient = self.create_gradient((30, 30, 50), (50, 50, 80), self.WINDOW_HEIGHT)
        self.screen.blit(gradient, (0, 0))
        
        # Titel mit Glow-Effekt
        title_shadow = self.title_font.render("Pokémon Card Challenge", True, (0, 0, 0))
        title = self.title_font.render("Pokémon Card Challenge", True, self.GOLD)
        glow = math.sin(time.time() * 3) * 0.5 + 0.5
        title_pos = (self.WINDOW_WIDTH//2 - title.get_width()//2, 20)
        self.screen.blit(title_shadow, (title_pos[0] + 2, title_pos[1] + 2))
        self.screen.blit(title, title_pos)
        
        # Slot Machine Bereich mit Schatten
        slot_bg = pygame.Surface((self.SLOT_WIDTH * 3 + 60, self.SLOT_HEIGHT + 40))
        slot_bg.fill((40, 40, 60))
        slot_bg_rect = slot_bg.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2))
        pygame.draw.rect(self.screen, (30, 30, 40), slot_bg_rect.inflate(10, 10))
        self.screen.blit(slot_bg, slot_bg_rect)
        
        # Slots zeichnen mit Shake-Effekt
        shake_x = random.randint(-self.shake_offset, self.shake_offset)
        shake_y = random.randint(-self.shake_offset, self.shake_offset)
        for i in range(3):
            # Slot background
            slot_rect = pygame.Rect(
                self.WINDOW_WIDTH//2 - (self.SLOT_WIDTH * 1.5) + (i * self.SLOT_WIDTH),
                self.WINDOW_HEIGHT//2 - self.SLOT_HEIGHT//2,
                self.SLOT_WIDTH,
                self.SLOT_HEIGHT
            )
            
            # Add shake effect during rolling
            if self.rolling:
                offset = random.randint(-2, 2)
                slot_rect.y += offset
            
            pygame.draw.rect(self.screen, self.BLACK, slot_rect)
            pygame.draw.rect(self.screen, self.WHITE, slot_rect, 2)
            
            # Draw Pokemon sprite
            if self.sprites.get(self.slots[i]):
                sprite = self.sprites[self.slots[i]]
                sprite_rect = sprite.get_rect(center=slot_rect.center)
                self.screen.blit(sprite, sprite_rect)
        
        # Buttons mit Hover-Effekt
        mouse_pos = pygame.mouse.get_pos()
        
        # Spin Button
        spin_color = self.BLUE if self.spin_button.collidepoint(mouse_pos) else self.RED
        self.draw_rounded_rect(self.screen, spin_color, self.spin_button, self.BUTTON_RADIUS)
        spin_text = self.button_font.render("SPIN", True, self.WHITE)
        spin_rect = spin_text.get_rect(center=self.spin_button.center)
        self.screen.blit(spin_text, spin_rect)
        
        # Back Button
        back_color = self.PURPLE if self.back_button.collidepoint(mouse_pos) else self.RED
        self.draw_rounded_rect(self.screen, back_color, self.back_button, self.BUTTON_RADIUS)
        back_text = self.button_font.render("ZURÜCK", True, self.WHITE)
        back_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_rect)
        
        # Challenge Text mit Animation
        if self.current_challenge:
            text_color = self.WHITE
            if self.flash_effect > 0:
                text_color = self.GOLD
                self.flash_effect -= 1
            
            # Text in mehrere Zeilen aufteilen
            words = self.current_challenge.split()
            lines = []
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                if self.challenge_font.size(test_line)[0] > self.WINDOW_WIDTH - 40:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)
            lines.append(' '.join(current_line))
            
            # Zeilen rendern mit Schatten
            y_offset = self.WINDOW_HEIGHT - 180
            for line in lines:
                text_shadow = self.challenge_font.render(line, True, (0, 0, 0))
                text = self.challenge_font.render(line, True, text_color)
                text_rect = text.get_rect(center=(self.WINDOW_WIDTH//2, y_offset))
                self.screen.blit(text_shadow, (text_rect.x + 2, text_rect.y + 2))
                self.screen.blit(text, text_rect)
                y_offset += 30
        
        # Partikel-Effekte zeichnen
        for particle in self.particles:
            alpha = int((particle['life'] / 60) * 255)
            particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            particle_color = (*particle['color'], alpha)
            pygame.draw.circle(particle_surface, particle_color, (2, 2), 2)
            self.screen.blit(particle_surface, (particle['x'], particle['y']))
        
        pygame.display.flip()

    def handle_win(self, difficulty):
        """Handle win effects"""
        if difficulty == "jackpot":
            self.flash_effect = 30
            self.shake_offset = 5
            for _ in range(5):
                self.add_particles(
                    random.randint(0, self.WINDOW_WIDTH),
                    random.randint(0, self.WINDOW_HEIGHT),
                    self.GOLD
                )
        elif difficulty == "hard":
            self.flash_effect = 20
            self.shake_offset = 3
            self.add_particles(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2, self.RED)
        elif difficulty == "medium":
            self.flash_effect = 15
            self.shake_offset = 2
            self.add_particles(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2, self.BLUE)
        elif difficulty == "easy":
            self.flash_effect = 10
            self.shake_offset = 1
            self.add_particles(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2, self.WHITE)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.spin_button.collidepoint(event.pos) and not self.rolling:
                self.roll()
            elif self.back_button.collidepoint(event.pos):
                self.running = False
        elif event.type == pygame.QUIT:
            self.running = False
            pygame.quit()
            sys.exit()
    
    def run(self):
        clock = pygame.time.Clock()
        current_challenge = None
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Zurück-Button
                    if self.back_button.collidepoint(mouse_pos):
                        return "menu"
                    
                    # Spin-Button
                    if self.spin_button.collidepoint(mouse_pos) and not self.rolling:
                        self.roll()
                        current_challenge = None  # Challenge zurücksetzen
                        if self.ROLL_SOUND:
                            self.ROLL_SOUND.play()
            
            self.update()
            self.draw()
            
            # Challenge nur anzeigen wenn Slots gestoppt sind
            if not self.rolling and current_challenge is None:
                difficulty = self.check_win()
                if difficulty:
                    current_challenge = self.get_challenge(difficulty)
            
            pygame.display.flip()
            clock.tick(60)
        
        return "menu"
