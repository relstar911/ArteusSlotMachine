import pygame
import os

# Initialize Pygame
pygame.init()

# Create sprites directory if it doesn't exist
os.makedirs('assets/sprites', exist_ok=True)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (147, 112, 219)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

def create_placeholder_sprite(name, color, size=(130, 130)):
    # Create surface
    surface = pygame.Surface(size)
    surface.fill(BLACK)
    
    # Draw a colored circle as placeholder
    pygame.draw.circle(surface, color, (size[0]//2, size[1]//2), size[0]//3)
    pygame.draw.circle(surface, WHITE, (size[0]//2, size[1]//2), size[0]//3, 2)
    
    # Add text
    font = pygame.font.Font(None, 24)
    text = font.render(name, True, WHITE)
    text_rect = text.get_rect(center=(size[0]//2, size[1]//2))
    surface.blit(text, text_rect)
    
    # Save the sprite
    pygame.image.save(surface, f'assets/sprites/{name.lower()}.png')

# Create placeholder sprites for each Pokemon
sprites = [
    ('Gengar', PURPLE),
    ('Arcanine', ORANGE),
    ('Dragonite', YELLOW),
    ('Alakazam', YELLOW),
    ('Gyarados', BLUE),
    ('Mewtwo', PURPLE),
]

for name, color in sprites:
    create_placeholder_sprite(name, color)

print("Sprite files created successfully!")

# Quit Pygame
pygame.quit()
