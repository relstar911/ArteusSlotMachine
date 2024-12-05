import pygame
from utils.font_manager import FontManager

class Button:
    def __init__(self, x, y, width, height, text='', color=(170, 170, 170), hover_color=(200, 200, 200), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font_manager = FontManager()
        self.font = self.font_manager.get_font('normal')  # Use normal size for buttons
        self.is_hovered = False
        self.disabled = False
        self.disabled_color = (100, 100, 100)
        self.disabled_text_color = (160, 160, 160)
        
    def draw(self, screen):
        if self.disabled:
            color = self.disabled_color
            text_color = self.disabled_text_color
        else:
            color = self.hover_color if self.is_hovered else self.color
            text_color = self.text_color
            
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=12)  # Border
        
        if self.text:
            text_surface = self.font.render(self.text, True, text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if self.disabled:
            return False
            
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

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
    def __init__(self, x, y, width, height, title):
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
    
    def update(self):
        """Update method for compatibility with slot machine"""
        pass
    
    def draw(self, screen, font_manager):
        """Draw the info box with title and colored text"""
        if not self.visible:
            return
        
        # Create semi-transparent surface
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, (0, 0, 0, 230), surface.get_rect(), border_radius=15)
        
        # Draw title
        title_font = font_manager.get_font('title')
        title_surface = title_font.render(self.title, True, (255, 215, 0))  # Gold color
        title_rect = title_surface.get_rect(centerx=self.width//2, top=10)
        surface.blit(title_surface, title_rect)
        
        # Draw text lines
        y_offset = 50 - self.scroll_offset  # Start below title
        for line, color in self.text_lines:
            if y_offset + self.line_height > 0 and y_offset < self.height:
                if line:  # Only render non-empty lines
                    font = font_manager.get_font('normal')
                    text_surface = font.render(line, True, color)
                    surface.blit(text_surface, (20, y_offset))
            y_offset += self.line_height
        
        # Draw scroll indicators if needed
        if self.scroll_offset > 0:
            pygame.draw.polygon(surface, (255, 255, 255, 128), 
                              [(self.width - 20, 20), (self.width - 10, 30), (self.width - 30, 30)])
        if self.scroll_offset < self.max_scroll:
            pygame.draw.polygon(surface, (255, 255, 255, 128), 
                              [(self.width - 20, self.height - 20), 
                               (self.width - 30, self.height - 30), 
                               (self.width - 10, self.height - 30)])
        
        # Draw to screen
        screen.blit(surface, (self.x, self.y))
