import pygame
import sys
from utils.font_manager import FontManager
from utils.ui_elements import Button
from games.slot_machine import SlotMachine
from games.constants import *

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_manager = FontManager()
        self.title_font = self.font_manager.get_font('title')
        self.normal_font = self.font_manager.get_font('normal')
        
        # Create buttons
        button_width = BUTTON_WIDTH
        button_height = BUTTON_HEIGHT
        button_x = (screen.get_width() - button_width) // 2
        
        self.buttons = {
            'slot': Button(
                button_x, 250, button_width, button_height,
                text='Arteus Slot Machine',
                color=BLUE,
                hover_color=(100, 180, 255),
                text_color=WHITE,
                font=self.normal_font
            ),
            'quit': Button(
                button_x, 350, button_width, button_height,
                text='Spiel Beenden',
                color=RED,
                hover_color=(255, 100, 100),
                text_color=WHITE,
                font=self.normal_font
            )
        }
    
    def draw(self, screen):
        # Draw background
        screen.fill(BLACK)
        
        # Draw title
        title = self.title_font.render("Pokemon Card Slot", True, GOLD)
        title_rect = title.get_rect(centerx=screen.get_width()//2, y=150)
        screen.blit(title, title_rect)
        
        # Draw buttons
        for button in self.buttons.values():
            button.draw(screen)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        for name, button in self.buttons.items():
                            if button.handle_event(event):
                                return name
                
                # Update button hover states
                if event.type == pygame.MOUSEMOTION:
                    for button in self.buttons.values():
                        button.handle_event(event)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "quit"
            
            self.draw(self.screen)
            pygame.time.wait(10)

def main():
    pygame.init()
    pygame.display.set_caption("Pokemon Card Slot")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    menu = MainMenu(screen)
    slot_machine = None
    current_screen = "menu"
    
    try:
        # Main game loop
        running = True
        while running:
            if current_screen == "menu":
                current_screen = menu.run()
            elif current_screen == "slot":
                if slot_machine is None:
                    slot_machine = SlotMachine(screen)
                current_screen = slot_machine.run()
                if current_screen != "slot":
                    slot_machine = None
            elif current_screen == "quit":
                running = False
            
            # Small delay to prevent high CPU usage
            pygame.time.wait(10)
    
    except Exception as e:
        print(f"Critical error: {e}")
    
    finally:
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()
