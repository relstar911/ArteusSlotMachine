import pygame
import sys
from utils.font_manager import FontManager
from utils.ui_elements import Button
from games.slot_machine import SlotMachine
from games.claw_machine import ClawMachine
import time

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_manager = FontManager()
        self.title_font = self.font_manager.get_font('title')
        self.normal_font = self.font_manager.get_font('normal')
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_x = (screen.get_width() - button_width) // 2
        
        self.buttons = {
            'slot': Button(
                button_x, 200, button_width, button_height,
                text='Slot Machine',
                color=(50, 150, 255),
                hover_color=(100, 180, 255),
                text_color=(255, 255, 255)
            ),
            'claw': Button(
                button_x, 300, button_width, button_height,
                text='Claw Machine',
                color=(255, 100, 100),
                hover_color=(255, 150, 150),
                text_color=(255, 255, 255)
            ),
            'quit': Button(
                button_x, 400, button_width, button_height,
                text='Quit Game',
                color=(150, 150, 150),
                hover_color=(180, 180, 180),
                text_color=(255, 255, 255)
            )
        }
    
    def draw(self, screen):
        # Draw background
        screen.fill((30, 30, 40))
        
        # Draw title
        title = self.title_font.render("Pokemon Card Games", True, (255, 215, 0))
        title_rect = title.get_rect(centerx=screen.get_width()//2, y=100)
        screen.blit(title, title_rect)
        
        # Draw buttons
        for button in self.buttons.values():
            button.draw(screen)
        
        # Draw version info
        version_text = self.normal_font.render("v1.0.0", True, (200, 200, 200))
        version_rect = version_text.get_rect(right=screen.get_width()-10, bottom=screen.get_height()-10)
        screen.blit(version_text, version_rect)
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        for name, button in self.buttons.items():
                            if button.handle_event(event):
                                if name == "quit":
                                    return "quit"
                                return name
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "quit"
                
                # Update button hover states
                if event.type == pygame.MOUSEMOTION:
                    for button in self.buttons.values():
                        button.handle_event(event)
            
            self.draw(self.screen)
            pygame.display.flip()
            clock.tick(60)

def main():
    pygame.init()
    pygame.display.set_caption("Pokemon Card Games")
    screen = pygame.display.set_mode((800, 600))
    
    menu = MainMenu(screen)
    slot_machine = None
    claw_machine = None
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
            elif current_screen == "claw":
                if claw_machine is None:
                    claw_machine = ClawMachine(screen)
                current_screen = claw_machine.run()
                if current_screen != "claw":
                    claw_machine = None
            elif current_screen == "quit":
                running = False
            
            # Small delay to prevent high CPU usage
            pygame.time.wait(10)
    
    except Exception as e:
        print(f"Critical error: {e}")
    
    finally:
        # Final cleanup
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()
