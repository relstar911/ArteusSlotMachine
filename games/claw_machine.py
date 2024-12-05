import pygame
import random
import math
import sys
import os
from .constants import *
import time

class Capsule:
    def __init__(self, x, y, difficulty):
        self.x = x
        self.y = y
        self.difficulty = difficulty
        # Farben basierend auf Schwierigkeit
        self.colors = {
            "easy": (255, 200, 200),    # Hellrot
            "medium": (255, 100, 100),  # Mittelrot
            "hard": (255, 0, 0),        # Dunkelrot
            "jackpot": (255, 215, 0)    # Gold
        }
        self.radius = 20
        self.grabbed = False

    def draw(self, screen):
        color = self.colors[self.difficulty]
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)
        # Glanzeffekt
        pygame.draw.circle(screen, (255, 255, 255), (self.x - 5, self.y - 5), 5)

class ClawMachine:
    def __init__(self, screen):
        self.screen = screen
        self.WINDOW_WIDTH = screen.get_width()
        self.WINDOW_HEIGHT = screen.get_height()
        
        # Farben
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 50, 50)
        self.GREEN = (50, 255, 50)
        self.YELLOW = (255, 255, 50)
        self.GOLD = (255, 215, 0)
        self.BLUE = (50, 150, 255)
        self.PURPLE = (147, 112, 219)
        self.NEON_BLUE = (50, 150, 255)
        self.NEON_PINK = (255, 50, 150)
        
        # UI Einstellungen
        self.BUTTON_WIDTH = 120
        self.BUTTON_HEIGHT = 40
        self.BUTTON_RADIUS = 10
        
        # Animation Einstellungen
        self.particles = []
        self.glow_effect = 0
        self.neon_offset = 0
        self.capsule_glow = 0
        
        # Buttons
        self.back_button = pygame.Rect(
            20,
            self.WINDOW_HEIGHT - 60,
            self.BUTTON_WIDTH,
            self.BUTTON_HEIGHT
        )
        
        self.drop_button = pygame.Rect(
            self.WINDOW_WIDTH//2 - self.BUTTON_WIDTH//2,
            self.WINDOW_HEIGHT - 60,
            self.BUTTON_WIDTH,
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
        
        # Sets für die Challenges
        self.SETS = [
            "Scarlet & Violet - 151",
            "Paldea Evolved",
            "Scarlet & Violet Base Set",
            "Obsidian Flames",
            "Paradise Lost",
            "Paradox Rift"
        ]

        # Challenge Pools
        self.CHALLENGES = {
            "easy": [
                "Finde die Commons für dein Deck aus {set}! (Öffne Packs bis du sie hast)",
                "Sammle 4 verschiedene Energien aus {set}! (Öffne Packs bis du sie hast)",
                "Finde 3 verschiedene Trainer-Karten aus {set}! (Öffne Packs bis du sie hast)",
                "Sammle 2 verschiedene Stage-1 Pokémon aus {set}! (Öffne Packs bis du sie hast)",
                "Finde 3 verschiedene Basic-Pokémon aus {set}! (Öffne Packs bis du sie hast)"
            ],
            "medium": [
                "Sammle 2 Reverse Holo Trainer aus {set}! (Öffne Packs bis du sie hast)",
                "Finde 1 Illustration Rare (IR) aus {set}! (Öffne Packs bis du sie hast)",
                "Sammle 2 Holo-Rare Pokémon aus {set}! (Öffne Packs bis du sie hast)",
                "Finde 1 Ultra Rare ex-Pokémon aus {set}! (Öffne Packs bis du sie hast)",
                "Sammle 1 Full Art Trainer aus {set}! (Öffne Packs bis du sie hast)"
            ],
            "hard": [
                "Finde 1 Alternative Art ex aus {set}! (Öffne Packs bis du sie hast)",
                "Sammle 1 Secret Rare aus {set}! (Öffne Packs bis du sie hast)",
                "Finde 1 Special Illustration Rare (SIR) aus {set}! (Öffne Packs bis du sie hast)",
                "Sammle 1 Gold Secret Rare aus {set}! (Öffne Packs bis du sie hast)",
                "Finde 1 Hyper Rare Rainbow aus {set}! (Öffne Packs bis du sie hast)"
            ],
            "jackpot": [
                "MEGA JACKPOT! Öffne eine ganze Box {set} für die Community!",
                "ULTRA JACKPOT! Öffne eine Elite Trainer Box {set} für die Community!",
                "MASTER JACKPOT! Öffne ein Premium Collection Display {set} für die Community!",
                "TERA JACKPOT! Öffne ein Build & Battle Stadium {set} für die Community!"
            ]
        }
        
        # Sound initialization
        try:
            # Load sound effects using working sound files
            self.DROP_SOUND = pygame.mixer.Sound(os.path.join("assets", "sounds", "stop.wav"))  # Using stop.wav for drop
            self.GRAB_SOUND = pygame.mixer.Sound(os.path.join("assets", "sounds", "spin.wav"))  # Using spin.wav for grab
            self.WIN_SOUND = pygame.mixer.Sound(os.path.join("assets", "sounds", "jackpot.wav"))
            self.CLICK_SOUND = pygame.mixer.Sound(os.path.join("assets", "sounds", "stop.wav"))  # Using stop.wav for click
            
            # Set sound volumes
            if self.DROP_SOUND: self.DROP_SOUND.set_volume(0.3)
            if self.GRAB_SOUND: self.GRAB_SOUND.set_volume(0.3)
            if self.WIN_SOUND: self.WIN_SOUND.set_volume(0.5)
            if self.CLICK_SOUND: self.CLICK_SOUND.set_volume(0.2)  # Lower volume for click
            
            # Load and start background music
            pygame.mixer.music.load(os.path.join("assets", "music", "1-11-Route-101.wav"))
            pygame.mixer.music.set_volume(0.4)  # Lower volume for background music
            pygame.mixer.music.play(-1)  # Loop indefinitely
        except Exception as e:
            print(f"Warning: Some sound files could not be loaded: {e}")
            self.DROP_SOUND = None
            self.GRAB_SOUND = None
            self.WIN_SOUND = None
            self.CLICK_SOUND = None
        
        # Claw state
        self.claw_x = self.WINDOW_WIDTH // 2
        self.claw_y = 100
        self.claw_speed = 5
        self.claw_state = "idle"  # idle, dropping, grabbing, rising
        self.target_y = 100
        self.grab_timer = 0
        self.initial_claw_y = 100
        
        # Challenge capsules
        self.capsules = []
        self.grabbed_capsule = None
        self.current_challenge = None
        self.generate_capsules()
    
    def generate_capsules(self):
        # Erstelle eine Mischung aus verschiedenen Schwierigkeitsgraden
        difficulties = ["easy"] * 15 + ["medium"] * 10 + ["hard"] * 5 + ["jackpot"] * 1
        random.shuffle(difficulties)
        
        for i, diff in enumerate(difficulties):
            x = random.randint(200, self.WINDOW_WIDTH - 200)
            y = random.randint(400, self.WINDOW_HEIGHT - 150)
            self.capsules.append(Capsule(x, y, diff))
    
    def get_challenge(self, difficulty):
        selected_set = random.choice(self.SETS)
        if difficulty in self.CHALLENGES:
            challenge = random.choice(self.CHALLENGES[difficulty])
            return challenge.format(set=selected_set)
        return "Versuche es nochmal!"
    
    def move_claw(self):
        keys = pygame.key.get_pressed()
        
        if self.claw_state == "idle":
            # Bewegung nur im idle-Zustand erlauben
            if keys[pygame.K_LEFT] and self.claw_x > 100:
                self.claw_x -= self.claw_speed
            if keys[pygame.K_RIGHT] and self.claw_x < self.WINDOW_WIDTH - 100:
                self.claw_x += self.claw_speed
            if keys[pygame.K_SPACE]:
                self.handle_grab()
        
        elif self.claw_state == "dropping":
            # Greifarm nach unten bewegen
            self.claw_y += self.claw_speed
            if self.claw_y >= self.target_y:
                self.claw_state = "grabbing"
                self.grab_timer = 20  # Timer für die Greif-Animation
                
        elif self.claw_state == "grabbing":
            self.grab_timer -= 1
            if self.grab_timer <= 0:
                self.claw_state = "rising"
                # Prüfen ob eine Kapsel gegriffen wurde
                for capsule in self.capsules:
                    if abs(capsule.x - self.claw_x) < 40 and abs(capsule.y - self.claw_y) < 40:
                        self.grabbed_capsule = capsule
                        self.capsules.remove(capsule)
                        self.current_challenge = self.get_challenge(capsule.difficulty)
                        break
        
        elif self.claw_state == "rising":
            # Greifarm nach oben bewegen
            self.claw_y -= self.claw_speed
            if self.grabbed_capsule:
                self.grabbed_capsule.x = self.claw_x
                self.grabbed_capsule.y = self.claw_y + 40
            
            if self.claw_y <= 100:  # Ursprüngliche Position
                self.claw_state = "idle"
                self.grabbed_capsule = None  # Kapsel loslassen
    
    def draw_neon_line(self, surface, color, start_pos, end_pos, width=2):
        """Draw a neon-style line with glow effect"""
        # Äußerer Glow
        glow_color = (*color, 50)  # Semi-transparent
        for i in range(3):
            offset = i * 2
            pygame.draw.line(surface, glow_color, 
                           (start_pos[0]-offset, start_pos[1]), 
                           (end_pos[0]-offset, end_pos[1]), 
                           width+4)
        # Innere helle Linie
        pygame.draw.line(surface, color, start_pos, end_pos, width)
        # Weißer Kern
        pygame.draw.line(surface, self.WHITE, start_pos, end_pos, max(1, width-2))

    def draw(self):
        # Hintergrund mit Gradient
        gradient = self.create_gradient((20, 20, 40), (40, 40, 80), self.WINDOW_HEIGHT)
        self.screen.blit(gradient, (0, 0))
        
        # Titel mit Glow-Effekt
        title_shadow = self.title_font.render("Pokémon Claw Machine", True, (0, 0, 0))
        title = self.title_font.render("Pokémon Claw Machine", True, self.GOLD)
        glow = math.sin(time.time() * 3) * 0.5 + 0.5
        title_pos = (self.WINDOW_WIDTH//2 - title.get_width()//2, 20)
        self.screen.blit(title_shadow, (title_pos[0] + 2, title_pos[1] + 2))
        self.screen.blit(title, title_pos)
        
        # Maschinen-Gehäuse mit Neon-Effekt
        machine_rect = pygame.Rect(50, 100, self.WINDOW_WIDTH-100, self.WINDOW_HEIGHT-200)
        pygame.draw.rect(self.screen, (30, 30, 50), machine_rect)
        
        # Neon-Umrandung
        neon_offset = math.sin(time.time() * 5) * 2
        neon_points = [
            (machine_rect.left, machine_rect.top),
            (machine_rect.right, machine_rect.top),
            (machine_rect.right, machine_rect.bottom),
            (machine_rect.left, machine_rect.bottom),
            (machine_rect.left, machine_rect.top)
        ]
        for i in range(len(neon_points)-1):
            self.draw_neon_line(self.screen, self.NEON_BLUE, 
                              neon_points[i], neon_points[i+1])
        
        # Kapseln zeichnen mit Glow
        for capsule in self.capsules:
            # Glow-Effekt
            glow_radius = math.sin(time.time() * 3 + capsule.x) * 2 + 5
            glow_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*self.GOLD, 100), (15, 15), glow_radius)
            self.screen.blit(glow_surface, (capsule.x-15, capsule.y-15))
            
            # Kapsel
            color = self.get_difficulty_color(capsule.difficulty)
            pygame.draw.circle(self.screen, color, (capsule.x, capsule.y), 10)
            pygame.draw.circle(self.screen, self.WHITE, (capsule.x, capsule.y), 5)
        
        # Greifarm mit Neon-Effekt
        claw_color = self.NEON_BLUE
        if self.grabbed_capsule:
            claw_color = self.GOLD
        
        self.draw_neon_line(self.screen, claw_color,
                           (self.claw_x, 0),
                           (self.claw_x, self.claw_y))
        
        # Greifer
        claw_points = [
            (self.claw_x, self.claw_y),
            (self.claw_x - 20, self.claw_y + 20),
            (self.claw_x + 20, self.claw_y + 20)
        ]
        for i in range(len(claw_points)-1):
            self.draw_neon_line(self.screen, claw_color,
                              claw_points[i], claw_points[i+1])
        
        # Back Button mit Hover-Effekt
        mouse_pos = pygame.mouse.get_pos()
        back_color = self.PURPLE if self.back_button.collidepoint(mouse_pos) else self.RED
        self.draw_rounded_rect(self.screen, back_color, self.back_button, self.BUTTON_RADIUS)
        back_text = self.button_font.render("ZURÜCK", True, self.WHITE)
        back_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_rect)
        
        # Drop Button mit Hover-Effekt
        drop_color = self.BLUE if self.drop_button.collidepoint(mouse_pos) else self.RED
        if self.claw_state == "idle":
            self.draw_rounded_rect(self.screen, drop_color, self.drop_button, self.BUTTON_RADIUS)
            drop_text = self.button_font.render("GREIFEN", True, self.WHITE)
            drop_rect = drop_text.get_rect(center=self.drop_button.center)
            self.screen.blit(drop_text, drop_rect)
        
        # Challenge Text mit Animation
        if self.current_challenge:
            # Text in mehrere Zeilen aufteilen
            words = self.current_challenge.split()
            lines = []
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                if self.challenge_font.size(test_line)[0] > machine_rect.width - 40:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)
            lines.append(' '.join(current_line))
            
            # Zeilen rendern mit Schatten
            y_offset = machine_rect.bottom + 20
            for line in lines:
                text_shadow = self.challenge_font.render(line, True, (0, 0, 0))
                text = self.challenge_font.render(line, True, self.WHITE)
                text_rect = text.get_rect(center=(self.WINDOW_WIDTH//2, y_offset))
                self.screen.blit(text_shadow, (text_rect.x + 2, text_rect.y + 2))
                self.screen.blit(text, text_rect)
                y_offset += 30
        
        # Partikel-Effekte
        for particle in self.particles:
            alpha = int((particle['life'] / 60) * 255)
            particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            particle_color = (*particle['color'], alpha)
            pygame.draw.circle(particle_surface, particle_color, (2, 2), 2)
            self.screen.blit(particle_surface, (particle['x'], particle['y']))
        
        pygame.display.flip()

    def get_difficulty_color(self, difficulty):
        """Get color based on difficulty"""
        if difficulty == "easy":
            return self.GREEN
        elif difficulty == "medium":
            return self.YELLOW
        elif difficulty == "hard":
            return self.RED
        return self.WHITE

    def create_gradient(self, color1, color2, height):
        """Create a vertical gradient"""
        gradient = pygame.Surface((self.WINDOW_WIDTH, height))
        for i in range(height):
            ratio = i / height
            color = tuple(int(channel1 + ratio * (channel2 - channel1)) for channel1, channel2 in zip(color1, color2))
            pygame.draw.line(gradient, color, (0, i), (self.WINDOW_WIDTH, i))
        return gradient

    def draw_rounded_rect(self, surface, color, rect, radius):
        """Draw a rounded rectangle"""
        pygame.draw.rect(surface, color, rect)
        pygame.draw.circle(surface, color, (rect.left, rect.top), radius)
        pygame.draw.circle(surface, color, (rect.right, rect.top), radius)
        pygame.draw.circle(surface, color, (rect.left, rect.bottom), radius)
        pygame.draw.circle(surface, color, (rect.right, rect.bottom), radius)

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

    def handle_grab(self):
        """Handle the claw grab action"""
        if self.claw_state == "idle":
            if self.DROP_SOUND:
                self.DROP_SOUND.play()
            self.claw_state = "dropping"
            self.target_y = self.WINDOW_HEIGHT - 150
            
    def update_claw(self):
        """Update claw position and state"""
        if self.claw_state == "dropping":
            if self.claw_y < self.target_y:
                self.claw_y += 5
            else:
                if self.GRAB_SOUND:
                    self.GRAB_SOUND.play()
                self.claw_state = "rising"
                
        elif self.claw_state == "rising":
            if self.claw_y > self.initial_claw_y:
                self.claw_y -= 5
            else:
                if self.grabbed_capsule:  # Nur Sound abspielen wenn wir eine Kapsel haben
                    if self.WIN_SOUND:
                        self.WIN_SOUND.play()
                    # Challenge setzen
                    difficulty = self.grabbed_capsule.difficulty
                    self.current_challenge = self.get_challenge(difficulty)
                    self.grabbed_capsule = None
                    # Partikel für erfolgreichen Grab
                    self.add_particles(self.claw_x, self.claw_y, self.get_difficulty_color(difficulty))
                
                self.claw_state = "idle"
                self.claw_y = self.initial_claw_y

    def check_capsule_grab(self):
        """Check if claw grabbed a capsule"""
        for capsule in self.capsules:
            if abs(self.claw_x - capsule.x) < 20 and abs(self.claw_y - capsule.y) < 20:
                self.grabbed_capsule = capsule
                self.capsules.remove(capsule)
                self.claw_state = "rising"
                self.target_y = 100
                
                # Add particles when grabbing capsule
                self.add_particles(capsule.x, capsule.y, self.GOLD)
                
                if self.GRAB_SOUND:
                    self.GRAB_SOUND.play()
                
                return capsule.difficulty
        return None

    def update(self):
        """Update game state"""
        # Update particles
        self.update_particles()
        
        # Update claw position based on state
        self.update_claw()
        
        # Check if claw grabbed a capsule
        if self.claw_state == "rising" and not self.grabbed_capsule:
            self.check_capsule_grab()
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Handle back button
                    if self.back_button.collidepoint(mouse_pos):
                        if self.CLICK_SOUND:
                            self.CLICK_SOUND.play()
                        return "menu"
                    
                    # Handle drop button
                    if self.drop_button.collidepoint(mouse_pos) and self.claw_state == "idle":
                        self.handle_grab()
            
            # Handle keyboard input for claw movement
            keys = pygame.key.get_pressed()
            if self.claw_state == "idle":
                if keys[pygame.K_LEFT] and self.claw_x > 100:
                    self.claw_x -= 5
                if keys[pygame.K_RIGHT] and self.claw_x < self.WINDOW_WIDTH - 100:
                    self.claw_x += 5
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Cap the framerate
            clock.tick(60)
        
        return "menu"
