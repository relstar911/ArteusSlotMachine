from pygame.locals import *
import pygame
import sys
import math
from utils.constants import *
from utils.font_manager import FontManager
from games.prizes import JACKPOT_PRIZE, MAIN_PRIZES, DOUBLE_PRIZES, EASY_PRIZES

class Button:
    def __init__(self, x, y, width, height, text='', color=(170, 170, 170), hover_color=(200, 200, 200), text_color=(255, 255, 255), font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font = font
        self.is_hovered = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            return self.is_hovered
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                return self.rect.collidepoint(event.pos)
        return False
        
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=12)  # White border
        
        if self.text != '':
            if self.font:
                text_surface = self.font.render(self.text, True, self.text_color)
                text_rect = text_surface.get_rect(center=self.rect.center)
                screen.blit(text_surface, text_rect)

class TextDisplay:
    def __init__(self, x, y, text='', color=(255, 255, 255), size='normal'):
        self.pos = (x, y)
        self.text = text
        self.color = color
        self.font_manager = FontManager()
        self.font = self.font_manager.get_font(size)
        
    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, self.pos)
        
    def update_text(self, new_text):
        self.text = new_text

class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.max_particles = 100  # Prevent excessive particles
    
    def add_particle(self, x, y, color, velocity, lifetime=1.0, size=5):
        """Add a new particle to the system"""
        if len(self.particles) < self.max_particles:
            self.particles.append({
                'pos': [x, y],
                'vel': velocity,
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'color': color,
                'size': size
            })
    
    def update(self, dt):
        """Update all particles"""
        for particle in self.particles[:]:  # Create a copy to safely remove while iterating
            particle['lifetime'] -= dt
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
                continue
            
            # Update position
            particle['pos'][0] += particle['vel'][0] * dt
            particle['pos'][1] += particle['vel'][1] * dt
            
            # Optional: Update size or color based on lifetime
            fade = particle['lifetime'] / particle['max_lifetime']
            particle['color'] = (
                particle['color'][0],
                particle['color'][1],
                particle['color'][2],
                int(255 * fade)
            )
    
    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            pos = (int(particle['pos'][0]), int(particle['pos'][1]))
            color = particle['color']
            size = particle['size']
            
            # Create a surface for the particle with alpha
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color, (size, size), size)
            screen.blit(particle_surface, (pos[0] - size, pos[1] - size))
    
    def clear(self):
        """Clear all particles from the system"""
        self.particles.clear()

class PokemonTextBox:
    """Base class for Pokemon-style text boxes"""
    def __init__(self, screen, font_manager, relative_size=(0.8, 0.3)):
        self.screen = screen
        self.font_manager = font_manager
        
        # Calculate size based on screen dimensions
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.width = int(self.screen_width * relative_size[0])
        self.height = int(self.screen_height * relative_size[1])
        
        # Center position
        self.x = (self.screen_width - self.width) // 2
        self.y = self.screen_height - self.height - 20  # Default bottom position
        
        # Box styling
        self.border_color = (50, 50, 50)  # Dark gray
        self.bg_color = (240, 240, 240, 230)  # Light gray, semi-transparent
        self.border_width = 3
        self.corner_radius = 10
        self.padding = 15
        
        # Text properties
        self.text = ""
        self.visible = False
        self.line_height = 25
        self.max_chars_per_line = 50
        
        # Animation properties
        self.animation_counter = 0
        self.char_index = 0
        self.animation_speed = 2
        self.is_animating = False
    
    def set_text(self, text):
        """Set text and prepare for animation"""
        self.text = text
        self.char_index = 0
        self.is_animating = True
    
    def wrap_text(self, text):
        """Wrap text to fit within box width"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            if current_length + word_length + 1 <= self.max_chars_per_line:
                current_line.append(word)
                current_length += word_length + 1
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length + 1
        
        if current_line:
            lines.append(' '.join(current_line))
        return lines
    
    def draw_pokemon_style_box(self, surface, rect):
        """Draw a Pokemon-style box with border and shadow"""
        # Draw shadow
        shadow_rect = rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(surface, (20, 20, 20, 128), shadow_rect, border_radius=self.corner_radius)
        
        # Draw main box
        pygame.draw.rect(surface, self.bg_color, rect, border_radius=self.corner_radius)
        pygame.draw.rect(surface, self.border_color, rect, self.border_width, border_radius=self.corner_radius)
        
        # Draw inner border
        inner_rect = rect.inflate(-8, -8)
        pygame.draw.rect(surface, self.border_color, inner_rect, 1, border_radius=self.corner_radius-2)
    
    def update(self):
        """Update animation"""
        if self.is_animating:
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.char_index += 1
                if self.char_index >= len(self.text):
                    self.is_animating = False
    
    def draw(self):
        """Draw the text box"""
        if not self.visible:
            return
        
        # Create surface for the box
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        box_rect = pygame.Rect(0, 0, self.width, self.height)
        
        # Draw the styled box
        self.draw_pokemon_style_box(surface, box_rect)
        
        # Wrap and draw text
        display_text = self.text[:self.char_index] if self.is_animating else self.text
        wrapped_lines = self.wrap_text(display_text)
        
        y_offset = self.padding
        for line in wrapped_lines:
            if y_offset + self.line_height > self.height - self.padding:
                break
                
            text_surface = self.font_manager.get_font('normal').render(line, True, (0, 0, 0))
            surface.blit(text_surface, (self.padding, y_offset))
            y_offset += self.line_height
        
        # Draw continue indicator if text is complete
        if not self.is_animating and len(wrapped_lines) > 0:
            indicator = "▼"
            indicator_surface = self.font_manager.get_font('normal').render(indicator, True, (0, 0, 0))
            surface.blit(indicator_surface, (self.width - self.padding - indicator_surface.get_width(),
                                          self.height - self.padding - indicator_surface.get_height()))
        
        # Draw to screen
        self.screen.blit(surface, (self.x, self.y))

class InfoBox:
    def __init__(self, x, y, width, height, title, font=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.visible = False
        self.scroll_offset = 0
        self.max_scroll = 0
        self.line_height = 25
        self.text_lines = []
        self.font = font
        self.font_manager = FontManager()
    
    def set_text(self, text_lines):
        """Set text content with color information"""
        self.text_lines = text_lines
        # Calculate max scroll based on text length
        num_lines = len(text_lines)
        visible_lines = self.height // self.line_height
        self.max_scroll = max(0, (num_lines * self.line_height) - self.height + 60)  # Add padding
        self.scroll_offset = 0
    
    def toggle(self):
        """Toggle visibility of the info box"""
        self.visible = not self.visible
        self.scroll_offset = 0  # Reset scroll position when toggling
    
    def handle_scroll(self, event):
        """Handle mouse wheel scrolling"""
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset = max(0, min(self.max_scroll, 
                                          self.scroll_offset - event.y * self.line_height))
                                          
    def handle_event(self, event):
        """Handle all events for the info box"""
        if not self.visible:
            return False
            
        if event.type == pygame.MOUSEWHEEL:
            self.handle_scroll(event)
            return True
            
        return False
        
    def update(self):
        """Update method for compatibility with slot machine"""
        pass
    
    def draw(self, screen, font_manager=None):
        if not self.visible:
            return
            
        # Use provided font or get default from font manager
        title_font = self.font or self.font_manager.get_font('medium')
        text_font = self.font or self.font_manager.get_font('normal')
        
        # Draw box background
        box_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (240, 240, 240), box_rect)
        pygame.draw.rect(screen, (0, 0, 0), box_rect, 2)
        
        # Draw title
        title = self.font.render(self.title, True, (0, 0, 0))
        title_rect = title.get_rect(centerx=self.x + self.width//2, top=self.y + 10)
        screen.blit(title, title_rect)
        
        # Draw text content
        content_y = self.y + 50 - self.scroll_offset
        for text, color in self.text_lines:
            if content_y + self.line_height > self.y and content_y < self.y + self.height:
                text_surface = text_font.render(text, True, color)
                screen.blit(text_surface, (self.x + 20, content_y))
            content_y += self.line_height

class InputField:
    def __init__(self, x, y, width, height, label, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.text = ''
        self.font = font
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            return True
        return False
        
    def draw(self, screen, active=False):
        color = (200, 200, 255) if active else (255, 255, 255)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        
        label_surface = self.font.render(self.label, True, (0, 0, 0))
        screen.blit(label_surface, (self.rect.x, self.rect.y - 20))
        
        if self.text:
            text_surface = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(midleft=(self.rect.x + 5, self.rect.centery))
            screen.blit(text_surface, text_rect)

class PrizeConfig:
    def __init__(self, x, y, width, height, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.visible = False
        self.active_field = None
        self.scroll_y = 0
        self.max_scroll = 0
        
        # Text input fields
        self.fields = {
            'jackpot': {'text': JACKPOT_PRIZE, 'label': 'Lugia Jackpot:'},
            'main1': {'text': MAIN_PRIZES[0] if MAIN_PRIZES else '', 'label': 'Charizard Preis:'},
            'main2': {'text': MAIN_PRIZES[1] if len(MAIN_PRIZES) > 1 else '', 'label': 'Tyranitar Preis:'},
            'main3': {'text': MAIN_PRIZES[2] if len(MAIN_PRIZES) > 2 else '', 'label': 'Gengar Preis:'},
            'main4': {'text': MAIN_PRIZES[3] if len(MAIN_PRIZES) > 3 else '', 'label': 'Oshawott Preis:'},
            'main5': {'text': MAIN_PRIZES[4] if len(MAIN_PRIZES) > 4 else '', 'label': 'Arcanine Preis:'},
            'double1': {'text': DOUBLE_PRIZES[0] if DOUBLE_PRIZES else '', 'label': '2x Gleiche Preis 1:'},
            'double2': {'text': DOUBLE_PRIZES[1] if len(DOUBLE_PRIZES) > 1 else '', 'label': '2x Gleiche Preis 2:'},
            'double3': {'text': DOUBLE_PRIZES[2] if len(DOUBLE_PRIZES) > 2 else '', 'label': '2x Gleiche Preis 3:'},
            'easy1': {'text': EASY_PRIZES[0] if EASY_PRIZES else '', 'label': 'Kein Match Preis 1:'},
            'easy2': {'text': EASY_PRIZES[1] if len(EASY_PRIZES) > 1 else '', 'label': 'Kein Match Preis 2:'}
        }
        
        # Calculate field positions and max scroll
        y_offset = 80  # Start weiter unten für Labels
        for field in self.fields.values():
            field['rect'] = pygame.Rect(x + 20, y + y_offset, width - 40, 30)
            y_offset += 65  # Mehr Platz zwischen den Feldern für Labels
        
        # Calculate max scroll
        self.max_scroll = max(0, y_offset - height + 60)
        
        # Save button
        self.save_button = Button(
            x + width//4,
            y + height - 60,
            width//2,
            40,
            "SPEICHERN",
            color=(0, 200, 0),
            hover_color=(0, 255, 0),
            font=font
        )
        
    def handle_event(self, event):
        if not self.visible:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Handle scrolling
            if event.button == 4:  # Mouse wheel up
                self.scroll_y = max(0, self.scroll_y - 20)
                return True
            elif event.button == 5:  # Mouse wheel down
                self.scroll_y = min(self.max_scroll, self.scroll_y + 20)
                return True
            
            # Adjust mouse position for scroll
            adjusted_pos = (mouse_pos[0], mouse_pos[1] + self.scroll_y)
            
            # Check save button
            if self.save_button.rect.collidepoint(mouse_pos):
                self.save_prizes()
                self.visible = False
                return True
                
            # Check text fields
            for name, field in self.fields.items():
                scroll_adjusted_rect = field['rect'].copy()
                scroll_adjusted_rect.y -= self.scroll_y
                if scroll_adjusted_rect.collidepoint(mouse_pos):
                    self.active_field = name
                    return True
                    
            # Click outside fields = deactivate
            self.active_field = None
            
        elif event.type == pygame.KEYDOWN and self.active_field:
            if event.key == pygame.K_RETURN:
                self.active_field = None
            elif event.key == pygame.K_BACKSPACE:
                self.fields[self.active_field]['text'] = self.fields[self.active_field]['text'][:-1]
            elif event.key == pygame.K_ESCAPE:
                self.visible = False
            else:
                self.fields[self.active_field]['text'] += event.unicode
            return True
            
        return False
        
    def save_prizes(self):
        """Save the configured prizes to prizes.py"""
        try:
            with open('games/prizes.py', 'w', encoding='utf-8') as f:
                f.write("# Preise für die Slot Machine\n")
                f.write("# Diese Listen können vor dem Stream angepasst werden\n\n")
                
                # Save jackpot prize
                f.write("# Hauptpreis (3x Lugia)\n")
                f.write(f'JACKPOT_PRIZE = "{self.fields["jackpot"]["text"]}"\n\n')
                
                # Save main prizes
                f.write("# Preise für 3 gleiche Symbole (außer Lugia)\n")
                f.write("MAIN_PRIZES = [\n")
                for i in range(1, 6):
                    text = self.fields[f'main{i}']['text']
                    if text:
                        f.write(f'    "{text}",\n')
                f.write("]\n\n")
                
                # Save double prizes (2x gleiche)
                f.write("# Preise für 2 gleiche Symbole\n")
                f.write("DOUBLE_PRIZES = [\n")
                for i in range(1, 4):
                    text = self.fields[f'double{i}']['text']
                    if text:
                        f.write(f'    "{text}",\n')
                f.write("]\n\n")
                
                # Save easy prizes
                f.write("# Preise für keine Übereinstimmungen\n")
                f.write("EASY_PRIZES = [\n")
                for i in range(1, 3):
                    text = self.fields[f'easy{i}']['text']
                    if text:
                        f.write(f'    "{text}",\n')
                f.write("]\n")
                
        except Exception as e:
            print(f"Error saving prizes: {str(e)}")
            
    def get_prizes(self):
        """Get all prizes from input fields"""
        prizes = {
            'jackpot': self.fields['jackpot']['text'],
            'main': [
                self.fields['main1']['text'],
                self.fields['main2']['text'],
                self.fields['main3']['text'],
                self.fields['main4']['text'],
                self.fields['main5']['text']
            ],
            'double': [
                self.fields['double1']['text'],
                self.fields['double2']['text'],
                self.fields['double3']['text']
            ],
            'easy': [
                self.fields['easy1']['text'],
                self.fields['easy2']['text']
            ]
        }
        
        # Filter out empty strings
        prizes['main'] = [p for p in prizes['main'] if p]
        prizes['double'] = [p for p in prizes['double'] if p]
        prizes['easy'] = [p for p in prizes['easy'] if p]
        
        return prizes
        
    def draw(self, screen):
        if not self.visible:
            return
            
        # Draw background
        pygame.draw.rect(screen, (240, 240, 240), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Border
        
        # Draw title
        title = self.font.render("Preise Konfigurieren", True, (0, 0, 0))
        title_rect = title.get_rect(centerx=self.rect.centerx, top=self.rect.top + 20)
        screen.blit(title, title_rect)
        
        # Draw fields
        for name, field in self.fields.items():
            # Only draw if field is visible (accounting for scroll)
            field_rect = field['rect'].copy()
            field_rect.y -= self.scroll_y
            
            if field_rect.bottom > self.rect.top and field_rect.top < self.rect.bottom:
                # Draw label
                label = self.font.render(field['label'], True, (0, 0, 0))
                screen.blit(label, (field_rect.x + 5, field_rect.y - 35))  # Label weiter oben
                
                # Draw input box
                color = (200, 200, 255) if name == self.active_field else (255, 255, 255)
                pygame.draw.rect(screen, color, field_rect)
                pygame.draw.rect(screen, (0, 0, 0), field_rect, 1)
                
                # Draw text
                if field['text']:
                    text = self.font.render(field['text'], True, (0, 0, 0))
                    text_rect = text.get_rect(midleft=(field_rect.x + 5, field_rect.centery))
                    screen.blit(text, text_rect)
        
        # Draw save button
        self.save_button.draw(screen)
        
    def update(self):
        """Update method for compatibility with slot machine"""
        pass

class Slot:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.symbol = 0  # Default symbol index
        
    def update(self):
        pass

class WonPrizesList:
    def __init__(self, x, y, width, height, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.visible = True
        self.scroll_y = 0
        self.max_scroll = 0
        self.line_height = 25
        self.won_prizes = []
        
    def add_prize(self, prize_text):
        """Füge einen neuen gewonnenen Preis zur Liste hinzu"""
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        self.won_prizes.append({
            "prize": prize_text,
            "won_at": current_time,
            "crossed": False
        })
        # Speichere die Liste
        self.save_prizes()
        
    def toggle_cross(self, index):
        """Preis als eingelöst markieren/demarkieren"""
        if 0 <= index < len(self.won_prizes):
            self.won_prizes[index]["crossed"] = not self.won_prizes[index]["crossed"]
            self.save_prizes()
            
    def save_prizes(self):
        """Speichere die Preisliste in die Datei"""
        try:
            with open('games/won_prizes.py', 'w', encoding='utf-8') as f:
                f.write("# Liste der bereits gewonnenen Preise\n")
                f.write("WON_PRIZES = [\n")
                for prize in self.won_prizes:
                    f.write(f'    {{"prize": "{prize["prize"]}", "won_at": "{prize["won_at"]}", "crossed": {prize["crossed"]}}},\n')
                f.write("]\n")
        except Exception as e:
            print(f"Error saving won prizes: {str(e)}")
            
    def load_prizes(self):
        """Lade die Preisliste - immer leer beim Start"""
        self.won_prizes = []
        # Erstelle leere Datei
        try:
            with open('games/won_prizes.py', 'w', encoding='utf-8') as f:
                f.write("# Liste der bereits gewonnenen Preise\n")
                f.write("WON_PRIZES = []\n")
        except Exception as e:
            print(f"Error resetting won prizes file: {str(e)}")
            
    def handle_event(self, event):
        """Handle mouse events"""
        if not self.visible:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle scrolling
            if event.button == 4:  # Mouse wheel up
                self.scroll_y = max(0, self.scroll_y - 20)
                return True
            elif event.button == 5:  # Mouse wheel down
                self.scroll_y = min(self.max_scroll, self.scroll_y + 20)
                return True
            
            # Handle prize clicking (to cross out)
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos):
                    # Calculate which prize was clicked
                    rel_y = mouse_pos[1] - self.rect.y + self.scroll_y
                    clicked_index = rel_y // self.line_height
                    if 0 <= clicked_index < len(self.won_prizes):
                        self.toggle_cross(clicked_index)
                        return True
        
        return False
        
    def draw(self, screen):
        """Draw the won prizes list"""
        if not self.visible:
            return
            
        # Draw background
        pygame.draw.rect(screen, (240, 240, 240), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        
        # Draw title
        title = self.font.render("Gewonnene Preise", True, (0, 0, 0))
        title_rect = title.get_rect(centerx=self.rect.centerx, top=self.rect.top + 10)
        screen.blit(title, title_rect)
        
        # Calculate visible area
        visible_rect = pygame.Rect(
            self.rect.x,
            self.rect.y + 40,  # Space for title
            self.rect.width,
            self.rect.height - 60  # Space for spin counter at bottom
        )
        
        # Draw prizes
        y = visible_rect.y - self.scroll_y
        for prize in self.won_prizes:
            if y + self.line_height > visible_rect.y and y < visible_rect.bottom:
                # Draw time
                time_text = self.font.render(prize["won_at"], True, (100, 100, 100))
                screen.blit(time_text, (visible_rect.x + 5, y))
                
                # Draw prize text with more space for the text
                prize_text = self.font.render(prize["prize"], True, (0, 0, 0))
                text_x = visible_rect.x + 120  # Mehr Platz für die Zeit
                
                if prize["crossed"]:
                    # Draw strikethrough
                    pygame.draw.line(screen, (255, 0, 0),
                        (text_x, y + self.line_height//2),
                        (text_x + prize_text.get_width(), y + self.line_height//2),
                        2
                    )
                
                screen.blit(prize_text, (text_x, y))
            
            y += self.line_height
        
        # Update max scroll
        self.max_scroll = max(0, y - visible_rect.bottom)
        
        # Draw spin counter at bottom
        if hasattr(self, 'slot_machine'):
            spins_text = self.font.render(f"Spins: {self.slot_machine.spin_count}", True, (0, 0, 0))
            spins_rect = spins_text.get_rect(centerx=self.rect.centerx, bottom=self.rect.bottom - 10)
            screen.blit(spins_text, spins_rect)
