import pygame
import sys
import os
from games.constants import *

# Initialize pygame with MP3 support
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init(44100, -16, 2, 2048)

# Import games
from games.slot_machine import SlotMachine
from games.claw_machine import ClawMachine

class MenuButton:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False
        
    def draw(self, screen):
        # Gradient effect when hovering
        if self.hover:
            color = (min(self.color[0] + 30, 255),
                    min(self.color[1] + 30, 255),
                    min(self.color[2] + 30, 255))
        else:
            color = self.color
            
        # Draw button with rounded corners
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        
        # Add glow effect when hovering
        if self.hover:
            glow_surface = pygame.Surface((self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*color, 100), 
                           (5, 5, self.rect.width, self.rect.height), 
                           border_radius=15)
            screen.blit(glow_surface, (self.rect.x - 5, self.rect.y - 5))
        
        # Draw text
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

def create_gradient_background(width, height, color1, color2):
    background = pygame.Surface((width, height))
    for y in range(height):
        ratio = y / height
        color = (
            int(color1[0] * (1 - ratio) + color2[0] * ratio),
            int(color1[1] * (1 - ratio) + color2[1] * ratio),
            int(color1[2] * (1 - ratio) + color2[2] * ratio)
        )
        pygame.draw.line(background, color, (0, y), (width, y))
    return background

def main():
    # Set up display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pokemon Mini-Games")
    clock = pygame.time.Clock()
    
    # Create menu buttons
    slot_button = MenuButton(300, 200, 200, 50, "Slot Machine", (147, 112, 219))  # Purple
    claw_button = MenuButton(300, 300, 200, 50, "Claw Machine", (50, 150, 255))   # Blue
    
    # Initialize games
    slot_machine = SlotMachine(screen)
    claw_machine = ClawMachine(screen)
    
    # Create background
    background = create_gradient_background(800, 600, (30, 30, 60), (60, 30, 60))
    
    # Load click sound
    try:
        click_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "stop.wav"))  # Using stop.wav for click
        click_sound.set_volume(0.2)  # Lower volume for menu clicks
    except Exception as e:
        print(f"Warning: Could not load click sound: {e}")
        click_sound = None
    
    # Load and play menu music
    try:
        pygame.mixer.music.load(os.path.join("assets", "music", "1-01-Title-Demo-_Departure-From-The.wav"))
        pygame.mixer.music.set_volume(0.4)  # Lower volume for menu music
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Warning: Could not load menu music: {e}")
    
    current_screen = "menu"
    running = True
    
    while running:
        if current_screen == "menu":
            # Draw background
            screen.blit(background, (0, 0))
            
            # Update button states
            mouse_pos = pygame.mouse.get_pos()
            slot_button.update(mouse_pos)
            claw_button.update(mouse_pos)
            
            # Draw buttons
            slot_button.draw(screen)
            claw_button.draw(screen)
            
            # Draw title
            font = pygame.font.Font(None, 48)
            title = font.render("Pokemon Mini-Games", True, (255, 255, 255))
            title_rect = title.get_rect(center=(400, 100))
            screen.blit(title, title_rect)
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if slot_button.rect.collidepoint(event.pos):
                        if click_sound:
                            click_sound.play()
                        current_screen = "slot"
                        pygame.mixer.music.stop()  # Stop menu music
                    elif claw_button.rect.collidepoint(event.pos):
                        if click_sound:
                            click_sound.play()
                        current_screen = "claw"
                        pygame.mixer.music.stop()  # Stop menu music
        
        elif current_screen == "slot":
            next_screen = slot_machine.run()
            if next_screen == "menu":
                current_screen = "menu"
                # Restart menu music
                pygame.mixer.music.load(os.path.join("assets", "music", "1-01-Title-Demo-_Departure-From-The.wav"))
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
                pygame.display.set_mode((800, 600))
        
        elif current_screen == "claw":
            next_screen = claw_machine.run()
            if next_screen == "menu":
                current_screen = "menu"
                # Restart menu music
                pygame.mixer.music.load(os.path.join("assets", "music", "1-01-Title-Demo-_Departure-From-The.wav"))
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
                pygame.display.set_mode((800, 600))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
