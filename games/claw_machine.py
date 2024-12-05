import pygame
import random
import math
import os
from utils.game_base import BaseGame
from utils.font_manager import FontManager
from utils.sound_manager import SoundManager
from utils.ui_elements import Button, InfoBox
from games.claw_constants import *
from typing import List, Dict, Any

class ChallengeBox:
    def __init__(self, screen, font_manager):
        self.screen = screen
        self.font_manager = font_manager
        self.visible = False
        self.text = ""
        self.width = 400
        self.height = 300
        self.x = (screen.get_width() - self.width) // 2
        self.y = (screen.get_height() - self.height) // 2
        self.fade_in = 0
        self.fade_out = 0
    
    def show(self, text):
        """Show the challenge box with the given text"""
        self.text = text
        self.visible = True
        self.fade_in = 255
    
    def hide(self):
        """Hide the challenge box"""
        self.visible = False
        self.fade_in = 0
    
    def update(self):
        """Update animation states"""
        if self.fade_in > 0:
            self.fade_in = max(0, self.fade_in - 10)
    
    def draw(self, screen):
        """Draw the challenge box if visible"""
        if not self.visible:
            return
            
        # Draw semi-transparent background
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        alpha = min(200, self.fade_in if self.fade_in > 0 else 200)
        pygame.draw.rect(surface, (0, 0, 0, alpha), surface.get_rect(), border_radius=15)
        
        # Split text into lines
        lines = self.text.split('\n')
        y_offset = 20
        
        # Draw title with title font
        title_font = self.font_manager.get_font('subtitle')
        title_surface = title_font.render(lines[0], True, GOLD)
        title_rect = title_surface.get_rect(centerx=self.width//2, y=y_offset)
        surface.blit(title_surface, title_rect)
        
        # Draw challenge text with normal font
        y_offset += 60
        normal_font = self.font_manager.get_font('normal')
        for line in lines[1:]:
            if line.strip():  # Only render non-empty lines
                text_surface = normal_font.render(line, True, WHITE)
                text_rect = text_surface.get_rect(centerx=self.width//2, y=y_offset)
                surface.blit(text_surface, text_rect)
                y_offset += 30
        
        # Draw the surface to screen
        screen.blit(surface, (self.x, self.y))

class Pokeball:
    def __init__(self, x, y, ball_type, info):
        self.x = x
        self.y = y
        self.info = info
        self.ball_type = ball_type
        self.grabbed = False
        self.rotation = 0
        self.swing_angle = 0
        
        # Load sprite
        try:
            self.sprite = pygame.image.load(f"assets/sprites/pokeballs/{info['sprite']}")
            self.sprite = pygame.transform.scale(self.sprite, (30, 30))
        except Exception as e:
            print(f"Error loading sprite for {ball_type}: {e}")
            # Create a default colored circle as fallback
            self.sprite = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(self.sprite, (255, 0, 0), (15, 15), 15)
    
    def update(self):
        if self.grabbed:
            self.rotation += ROTATION_SPEED
            self.swing_angle = math.sin(pygame.time.get_ticks() * SWING_SPEED) * 30
    
    def draw(self, screen):
        # Create a copy of the sprite for rotation
        rotated = pygame.transform.rotate(self.sprite, self.rotation + self.swing_angle)
        # Get the rect for centered rotation
        rect = rotated.get_rect(center=(self.x, self.y))
        # Draw the rotated sprite
        screen.blit(rotated, rect)

class InfoBox:
    def __init__(self, x, y, width, height, title):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.visible = False
        self.scroll_y = 0
        self.text = []
        
    def set_text(self, text):
        self.text = text
        
    def handle_scroll(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_y += event.y * 10
    
    def draw(self, screen, font_manager):
        if not self.visible:
            return
        
        # Draw semi-transparent background
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, (0, 0, 0, 200), (0, 0, self.width, self.height), border_radius=15)
        
        # Draw title with title font
        title_font = font_manager.get_font('title')
        title_surface = title_font.render(self.title, True, (255, 215, 0))
        title_rect = title_surface.get_rect(centerx=self.width//2, y=20)
        surface.blit(title_surface, title_rect)
        
        # Draw text
        y_offset = 60
        for line, color in self.text:
            text_surface = font_manager.get_font('normal').render(line, True, color)
            text_rect = text_surface.get_rect(centerx=self.width//2, y=y_offset)
            surface.blit(text_surface, (self.width//2 - text_surface.get_width()//2, y_offset + self.scroll_y))
            y_offset += 30
        
        # Draw the surface to screen
        screen.blit(surface, (self.x, self.y))

class ClawMachine(BaseGame):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.WINDOW_WIDTH = screen.get_width()
        self.WINDOW_HEIGHT = screen.get_height()
        
        # Initialize font manager
        self.font_manager = FontManager()
        
        # Initialize game state
        self.score = 0
        self.claw_state = "idle"
        self.claw_x = self.WINDOW_WIDTH // 2
        self.claw_y = 100
        self.grabbed_ball = None
        self.pokeballs = []
        self.particles = []
        self.current_challenge = None
        
        # Initialize challenge box
        self.challenge_box = ChallengeBox(self.screen, self.font_manager)
        self.challenge_box.visible = False
        
        # Initialize buttons
        self.init_buttons()
        
        # Initialize resources
        self.init_game_resources()
        
        # Create initial pokeballs
        self.spawn_pokeballs()

    def init_buttons(self):
        """Initialize game buttons"""
        button_width = 120
        button_height = 40
        padding = 20
        
        # Create info box
        self.info_box = InfoBox(
            self.WINDOW_WIDTH//2 - 200,  # x position
            self.WINDOW_HEIGHT//2 - 150,  # y position
            400,  # width
            300,  # height
            "Spielregeln"  # title
        )
        
        # Define colors for different ball types
        normal_color = (255, 100, 100)    # Red
        hisui_color = (100, 100, 255)     # Blue
        ultra_color = (150, 150, 150)     # Gray
        beast_color = (147, 112, 219)     # Purple
        master_color = (255, 215, 0)      # Gold
        white = (255, 255, 255)           # White
        
        # Set info text with colors
        self.info_box.set_text([
            ("🎮 CLAW MACHINE REGELN", (255, 215, 0)),
            ("", (255, 255, 255)),
            ("🎯 SPIELABLAUF", (255, 215, 0)),
            ("• Bewege den Greifer mit den PFEILTASTEN", (255, 255, 255)),
            ("• Drücke SPACE zum Greifen", (255, 255, 255)),
            ("• Fange Pokebälle für Belohnungen", (255, 255, 255)),
            ("", (255, 255, 255)),
            ("⚡ POKEBÄLLE", (255, 215, 0)),
            ("• POKEBALL: Common bis Stage 1 Karten", (255, 100, 100)),
            ("• SUPERBALL: Holo bis Full Art Karten", (100, 100, 255)),
            ("• HYPERBALL: Special Art bis Gold Karten", (150, 150, 150)),
            ("• MEISTERBALL: Community Present", (255, 215, 0)),
            ("", (255, 255, 255)),
            ("💫 POWER-UPS", (255, 215, 0)),
            ("• Sammle Items für bessere Greifkraft", (255, 255, 255)),
            ("• Mehr Greifkraft = Bessere Bälle", (255, 255, 255)),
            ("", (255, 255, 255)),
            ("🎮 Spielablauf", (255, 215, 0)),
            ("1. Bewege die Klaue über den Ball", (255, 255, 255)),
            ("2. Drücke Leertaste zum Greifen", (255, 255, 255)),
            ("3. Die Klaue senkt sich automatisch", (255, 255, 255)),
            ("4. Fangchance basiert auf Balltyp", (255, 255, 255)),
            ("5. Erfolgreiche Fänge = Punkte!", (255, 255, 255)),
            ("", (255, 255, 255)),
            ("💡 Profi-Tipp", (255, 215, 0)),
            ("Time deinen Griff genau!", (255, 255, 255))
        ])
        
        # Create buttons
        self.buttons = {
            'back': Button(
                padding,  # x position
                padding,  # y position
                button_width,
                button_height,
                "Zurück",
                color=(200, 50, 50),  # Red
                text_color=(255, 255, 255)  # White
            ),
            'reset': Button(
                self.WINDOW_WIDTH - button_width - padding - button_width - padding,  # x position
                padding,  # y position
                button_width,
                button_height,
                "Neu",
                color=(50, 200, 50),  # Green
                text_color=(255, 255, 255)  # White
            ),
            'info': Button(
                self.WINDOW_WIDTH - button_width - padding,  # x position
                padding,  # y position
                button_width,
                button_height,
                "Info",
                color=(100, 100, 200),  # Blue
                text_color=(255, 255, 255)  # White
            )
        }
        
    def init_game_resources(self):
        """Initialize game resources"""
        try:
            # Load Pokeball sprites
            self.POKEBALL_IMAGES = {}
            for category, balls in POKEBALLS.items():
                img_path = f"assets/sprites/pokeballs/{balls['sprite']}"
                if os.path.exists(img_path):
                    image = pygame.image.load(img_path)
                    image = pygame.transform.scale(image, (POKEBALL_SIZE, POKEBALL_SIZE))
                    self.POKEBALL_IMAGES[balls['sprite']] = image
            
            # Try to load claw sprite, create fallback if not found
            try:
                self.CLAW_IMAGE = pygame.image.load("assets/sprites/claw.png")
                self.CLAW_IMAGE = pygame.transform.scale(self.CLAW_IMAGE, (CLAW_SIZE, CLAW_SIZE))
            except:
                # Create a simple claw shape as fallback
                self.CLAW_IMAGE = pygame.Surface((CLAW_SIZE, CLAW_SIZE), pygame.SRCALPHA)
                pygame.draw.polygon(self.CLAW_IMAGE, (200, 200, 200), [
                    (CLAW_SIZE//2, 0),  # Top point
                    (0, CLAW_SIZE//2),   # Left point
                    (CLAW_SIZE//2, CLAW_SIZE),  # Bottom point
                    (CLAW_SIZE, CLAW_SIZE//2)   # Right point
                ])
            
            # Load sounds with fallback
            try:
                self.DROP_SOUND = pygame.mixer.Sound("assets/sounds/drop.wav")
                self.GRAB_SOUND = pygame.mixer.Sound("assets/sounds/grab.wav")
                self.WIN_SOUND = pygame.mixer.Sound("assets/sounds/win.wav")
            except:
                self.DROP_SOUND = None
                self.GRAB_SOUND = None
                self.WIN_SOUND = None
                print("Sound files not found, continuing without sound")
        
        except Exception as e:
            print(f"Error loading resources: {e}")
            self.DROP_SOUND = None
            self.GRAB_SOUND = None
            self.WIN_SOUND = None

    def generate_pokeballs(self):
        """Generate a mix of different Pokéballs"""
        num_balls = random.randint(15, 25)
        total_weight = sum(ball['weight'] for ball in POKEBALLS.values())
        
        for _ in range(num_balls):
            # Random position within the machine
            x = random.randint(100, self.WINDOW_WIDTH - 100)
            y = random.randint(200, self.WINDOW_HEIGHT - 150)
            
            # Select ball type based on weights
            rand = random.uniform(0, total_weight)
            current_weight = 0
            
            for ball_type, info in POKEBALLS.items():
                current_weight += info['weight']
                if rand <= current_weight:
                    self.pokeballs.append(Pokeball(x, y, ball_type, info))
                    break
    
    def create_particles(self, x, y):
        """Create particles for grab effect"""
        particles = []
        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            particle = {
                'x': x,
                'y': y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': random.randint(20, 30),
                'color': (255, 215, 0)
            }
            particles.append(particle)
        return particles
    
    def update_particles(self):
        """Update particle positions and remove dead particles"""
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw_particles(self, screen):
        """Draw particles"""
        for particle in self.particles:
            alpha = min(255, particle['life'] * 8)
            pygame.draw.circle(
                screen,
                particle['color'] + (alpha,),
                (int(particle['x']), int(particle['y'])),
                2
            )
    
    def draw_gradient_background(self, screen):
        """Draw gradient background"""
        for y in range(self.WINDOW_HEIGHT):
            progress = y / self.WINDOW_HEIGHT
            color = (
                int(20 + progress * 20),
                int(20 + progress * 20),
                int(35 + progress * 35)
            )
            pygame.draw.line(screen, color, (0, y), (self.WINDOW_WIDTH, y))
    
    def draw_claw(self, screen):
        """Draw the claw"""
        # Draw claw base
        pygame.draw.rect(screen, (100, 100, 100), 
                        (self.claw_x - 5, 0, 10, self.claw_y))
        
        # Draw claw parts
        claw_points = [
            (self.claw_x - 15, self.claw_y + 20),
            (self.claw_x + 15, self.claw_y + 20),
            (self.claw_x, self.claw_y)
        ]
        pygame.draw.polygon(screen, (150, 150, 150), claw_points)
    
    def check_collision(self, ball):
        """Check if claw collides with ball"""
        claw_rect = pygame.Rect(self.claw_x - 15, self.claw_y, 30, 30)
        ball_rect = pygame.Rect(ball.x - 15, ball.y - 15, 30, 30)
        return claw_rect.colliderect(ball_rect)
    
    def handle_grab(self):
        """Handle the grab action"""
        if self.claw_state == "idle":
            self.claw_state = "dropping"
            if hasattr(self, 'DROP_SOUND') and self.DROP_SOUND:
                self.DROP_SOUND.play()
    
    def generate_challenge(self):
        """Generate a random challenge based on the grabbed ball"""
        if self.grabbed_ball and self.grabbed_ball.info.get('challenges'):
            return random.choice(self.grabbed_ball.info['challenges'])
        return None
    
    def reset_game(self):
        """Reset the game state"""
        self.claw_state = "idle"
        self.claw_x = self.WINDOW_WIDTH // 2
        self.claw_y = 100
        self.grabbed_ball = None
        self.pokeballs.clear()
        self.particles.clear()
        self.generate_pokeballs()
    
    def update(self):
        """Update game state"""
        # Update particles
        self.update_particles()
        
        # Update challenge box
        if self.challenge_box:
            self.challenge_box.update()
        
        # Handle keyboard controls for claw movement
        if self.claw_state == "idle" and not self.challenge_box.visible:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.claw_x > 100:
                self.claw_x -= CLAW_SPEED
            if keys[pygame.K_RIGHT] and self.claw_x < self.WINDOW_WIDTH - 100:
                self.claw_x += CLAW_SPEED
            if keys[pygame.K_SPACE]:
                self.claw_state = "dropping"
                if self.DROP_SOUND:
                    self.DROP_SOUND.play()
        
        # Update claw position and handle ball grabbing
        if self.claw_state == "dropping":
            self.claw_y += CLAW_DROP_SPEED
            # Check for collisions with Pokeballs
            for ball in self.pokeballs:
                if not ball.grabbed and self.check_collision(ball):
                    # Random chance to grab based on ball category
                    grab_chance = GRAB_CHANCES.get(ball.info['category'], 0.5)
                    if random.random() < grab_chance:
                        ball.grabbed = True
                        self.grabbed_ball = ball
                        self.particles.extend(self.create_particles(ball.x, ball.y))
                        if self.GRAB_SOUND:
                            self.GRAB_SOUND.play()
                    self.claw_state = "rising"
                    break
            
            # Check if claw reached bottom
            if self.claw_y >= self.WINDOW_HEIGHT - 150:
                self.claw_state = "rising"
        
        elif self.claw_state == "rising":
            self.claw_y -= CLAW_SPEED
            if self.grabbed_ball:
                # Update grabbed ball position
                self.grabbed_ball.x = self.claw_x
                self.grabbed_ball.y = self.claw_y + 30
                self.grabbed_ball.update()
            
            # Check if claw reached top
            if self.claw_y <= 100:
                self.claw_state = "idle"
                if self.grabbed_ball:
                    # Show challenge for grabbed ball
                    self.show_challenge(self.grabbed_ball)
                    self.grabbed_ball = None
        
        # Update all pokeballs
        for ball in self.pokeballs:
            if not ball.grabbed:
                ball.update()

    def process_event(self, event):
        """Process pygame events"""
        if event.type == pygame.QUIT:
            return "quit"
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.info_box.visible = not self.info_box.visible
            elif event.key == pygame.K_ESCAPE:
                if self.info_box.visible:
                    self.info_box.visible = False
                else:
                    return "menu"
            if event.key == pygame.K_SPACE:
                if self.challenge_box.visible:
                    self.challenge_box.hide()
                    self.reset_game()
    
        # Handle scrolling in info box
        if self.info_box.visible:
            self.info_box.handle_scroll(event)
    
        # Handle button events
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Don't process buttons if challenge is showing
            if not self.challenge_box.visible:
                # Handle buttons
                for button_name, button in self.buttons.items():
                    if button.handle_event(event):
                        if button_name == 'back':
                            return "menu"
                        elif button_name == 'reset':
                            self.reset_game()
                        elif button_name == 'info':
                            self.info_box.visible = True
                            self.info_box.set_text([
                                ("🎮 CLAW MACHINE REGELN", (255, 215, 0)),
                                ("", (255, 255, 255)),
                                ("🎯 SPIELABLAUF", (255, 215, 0)),
                                ("• Bewege den Greifer mit den PFEILTASTEN", (255, 255, 255)),
                                ("• Drücke SPACE zum Greifen", (255, 255, 255)),
                                ("• Fange Pokebälle für Belohnungen", (255, 255, 255)),
                                ("", (255, 255, 255)),
                                ("⚡ POKEBÄLLE", (255, 215, 0)),
                                ("• POKEBALL: Common bis Stage 1 Karten", (255, 100, 100)),
                                ("• SUPERBALL: Holo bis Full Art Karten", (100, 100, 255)),
                                ("• HYPERBALL: Special Art bis Gold Karten", (150, 150, 150)),
                                ("• MEISTERBALL: Community Present", (255, 215, 0)),
                                ("", (255, 255, 255)),
                                ("💫 POWER-UPS", (255, 215, 0)),
                                ("• Sammle Items für bessere Greifkraft", (255, 255, 255)),
                                ("• Mehr Greifkraft = Bessere Bälle", (255, 255, 255)),
                                ("", (255, 255, 255)),
                                ("🎮 Spielablauf", (255, 215, 0)),
                                ("1. Bewege die Klaue über den Ball", (255, 255, 255)),
                                ("2. Drücke Leertaste zum Greifen", (255, 255, 255)),
                                ("3. Die Klaue senkt sich automatisch", (255, 255, 255)),
                                ("4. Fangchance basiert auf Balltyp", (255, 255, 255)),
                                ("5. Erfolgreiche Fänge = Punkte!", (255, 255, 255)),
                                ("", (255, 255, 255)),
                                ("💡 Profi-Tipp", (255, 215, 0)),
                                ("Time deinen Griff genau!", (255, 255, 255))
                            ])
    
        # Update button hover states
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons.values():
                button.handle_event(event)
    
        return None

    def draw(self, screen):
        """Draw the game state"""
        # Draw background
        screen.fill((30, 30, 40))  # Dark blue-gray background
        
        # Draw buttons
        for button in self.buttons.values():
            button.draw(screen)
    
        # Draw score with large font
        score_text = self.font_manager.get_font('large').render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 70))  # Moved down to not overlap with buttons
        
        # Draw title with title font
        title = self.font_manager.get_font('title').render("Pokémon Claw Machine", True, (255, 215, 0))
        title_rect = title.get_rect(center=(self.WINDOW_WIDTH//2, 50))
        screen.blit(title, title_rect)
        
        # Draw Pokeballs
        for ball in self.pokeballs:
            if not ball.grabbed:
                if hasattr(ball, 'sprite') and ball.sprite:
                    rotated_sprite = pygame.transform.rotate(ball.sprite, ball.rotation)
                    screen.blit(rotated_sprite, (ball.x - rotated_sprite.get_width()//2, 
                                            ball.y - rotated_sprite.get_height()//2))
                else:
                    # Fallback: draw a colored circle
                    pygame.draw.circle(screen, (255, 0, 0), (int(ball.x), int(ball.y)), POKEBALL_SIZE//2)
    
        # Draw claw
        self.draw_claw(screen)
    
        # Draw grabbed ball if any
        if self.grabbed_ball:
            if hasattr(self.grabbed_ball, 'sprite') and self.grabbed_ball.sprite:
                screen.blit(self.grabbed_ball.sprite, 
                        (self.grabbed_ball.x - self.grabbed_ball.sprite.get_width()//2,
                         self.grabbed_ball.y - self.grabbed_ball.sprite.get_height()//2))
            else:
                # Fallback: draw a colored circle
                pygame.draw.circle(screen, (255, 0, 0), 
                               (int(self.grabbed_ball.x), int(self.grabbed_ball.y)), 
                               POKEBALL_SIZE//2)
    
        # Draw particles
        for particle in self.particles:
            pygame.draw.circle(screen, particle['color'], 
                           (int(particle['x']), int(particle['y'])), 
                           3)
    
        # Draw challenge box if visible
        if self.challenge_box:
            self.challenge_box.draw(screen)
        
        # Draw info box if visible
        if self.info_box.visible:
            self.info_box.draw(screen, self.font_manager)

        # Update display
        pygame.display.flip()

    def show_challenge(self, pokeball):
        """Display challenge based on pokeball type"""
        if pokeball and hasattr(pokeball, 'info'):
            category = pokeball.info['category']
            challenges = pokeball.info['challenges']
            description = pokeball.info['description']
            
            # Select a random challenge
            challenge_text = random.choice(challenges)
            
            # Format the challenge text with description
            full_text = f"✨ {description} ✨\n\n{challenge_text}"
            
            # Create or update challenge box
            if self.challenge_box is None:
                self.challenge_box = ChallengeBox(self.screen, self.font_manager)
            
            self.challenge_box.show(full_text)
            self.current_challenge = challenge_text
            
            # Play win sound
            if self.WIN_SOUND:
                self.WIN_SOUND.play()
    
    def spawn_pokeballs(self):
        """Spawn new pokeballs in the machine"""
        self.pokeballs.clear()  # Clear existing pokeballs
        num_balls = random.randint(MIN_BALLS, MAX_BALLS)
        total_weight = sum(ball['weight'] for ball in POKEBALLS.values())
        
        for _ in range(num_balls):
            # Random position within the machine area
            x = random.randint(100, self.WINDOW_WIDTH - 100)
            y = random.randint(200, self.WINDOW_HEIGHT - 150)
            
            # Select ball type based on weights
            rand = random.uniform(0, total_weight)
            current_weight = 0
            
            for ball_type, info in POKEBALLS.items():
                current_weight += info['weight']
                if rand <= current_weight:
                    self.pokeballs.append(Pokeball(x, y, ball_type, info))
                    break

    def cleanup(self):
        """Cleanup resources when exiting the game"""
        try:
            # Call parent cleanup first
            if hasattr(super(), 'cleanup'):
                super().cleanup()
            
            # Clear all game objects
            if hasattr(self, 'pokeballs'):
                self.pokeballs.clear()
            if hasattr(self, 'particles'):
                self.particles.clear()
            self.grabbed_ball = None
            
            # Stop all sounds
            if hasattr(self, 'DROP_SOUND') and self.DROP_SOUND:
                try:
                    self.DROP_SOUND.stop()
                except:
                    pass
                self.DROP_SOUND = None
                
            if hasattr(self, 'GRAB_SOUND') and self.GRAB_SOUND:
                try:
                    self.GRAB_SOUND.stop()
                except:
                    pass
                self.GRAB_SOUND = None
                
            if hasattr(self, 'WIN_SOUND') and self.WIN_SOUND:
                try:
                    self.WIN_SOUND.stop()
                except:
                    pass
                self.WIN_SOUND = None
            
            # Clear image references
            if hasattr(self, 'POKEBALL_IMAGES'):
                self.POKEBALL_IMAGES.clear()
            if hasattr(self, 'CLAW_IMAGE'):
                self.CLAW_IMAGE = None
            
            # Clear UI elements
            if hasattr(self, 'buttons'):
                self.buttons.clear()
            if hasattr(self, 'challenge_box'):
                self.challenge_box = None
            
            # Clear font manager last
            if hasattr(self, 'font_manager') and self.font_manager:
                try:
                    self.font_manager.cleanup()
                except:
                    pass
                self.font_manager = None
                
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def run(self):
        """Main game loop"""
        try:
            clock = pygame.time.Clock()
            running = True
            
            while running:
                # Handle events
                for event in pygame.event.get():
                    result = self.process_event(event)
                    if result == "quit":
                        running = False
                        break
                    elif result == "menu":
                        self.cleanup()  # Clean up before returning to menu
                        return "menu"
                
                # Update game state
                self.update()
                
                # Draw everything
                self.draw(self.screen)
                
                # Cap the framerate
                clock.tick(60)
            
            # Clean up before quitting
            self.cleanup()
            return "quit"
            
        except Exception as e:
            print(f"Error in game loop: {e}")
            self.cleanup()  # Ensure cleanup happens even on error
            return "menu"
