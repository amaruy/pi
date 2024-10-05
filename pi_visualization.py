import pygame
import math
import colorsys

# Initialize Pygame
pygame.init()

class Config:
    def __init__(self):
        self.radial1_length = 400
        self.radial2_length = 400
        self.initial_speed = 0.01
        self.zoom_factor = 0.5
        self.color_mode = 'white'

class PiVisualization:
    def __init__(self, config):
        self.config = config
        self.width, self.height = 1600, 900
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pi Visualization with Radial Arms")
        self.clock = pygame.time.Clock()
        self.angle1 = 0
        self.angle2 = 0
        self.speed = config.initial_speed
        self.path = []
        self.surface = pygame.Surface((self.width * 3, self.height * 3))
        self.offset_x, self.offset_y = self.surface.get_width() // 2, self.surface.get_height() // 2
        self.show_menu = True
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)

    def update(self):
        self.angle1 += self.speed
        self.angle2 += self.speed * math.pi

        x1 = self.config.radial1_length * math.cos(self.angle1)
        y1 = self.config.radial1_length * math.sin(self.angle1)
        
        x2 = x1 + self.config.radial2_length * math.cos(self.angle2)
        y2 = y1 + self.config.radial2_length * math.sin(self.angle2)

        self.path.append((x2 + self.offset_x, y2 + self.offset_y))

    def draw(self):
        self.surface.fill((0, 0, 0))
        
        # Draw path with anti-aliasing
        if len(self.path) > 1:
            if self.config.color_mode == 'rainbow':
                for i in range(1, len(self.path)):
                    progress = i / len(self.path)
                    color = [int(c * 255) for c in colorsys.hsv_to_rgb(progress, 1, 1)]
                    pygame.draw.aaline(self.surface, color, self.path[i-1], self.path[i])
            else:
                pygame.draw.aalines(self.surface, (255, 255, 255), False, self.path)

        # Draw radial arms with anti-aliasing
        pygame.draw.aaline(self.surface, (255, 255, 255), 
                         (self.offset_x, self.offset_y), 
                         (self.config.radial1_length * math.cos(self.angle1) + self.offset_x, 
                          self.config.radial1_length * math.sin(self.angle1) + self.offset_y))
        
        pygame.draw.aaline(self.surface, (255, 255, 255),
                         (self.config.radial1_length * math.cos(self.angle1) + self.offset_x, 
                          self.config.radial1_length * math.sin(self.angle1) + self.offset_y),
                         (self.path[-1][0], self.path[-1][1]))

        # Apply zoom and blit to screen
        scaled_surface = pygame.transform.smoothscale(self.surface, 
                                                (int(self.surface.get_width() * self.config.zoom_factor),
                                                 int(self.surface.get_height() * self.config.zoom_factor)))
        self.screen.blit(scaled_surface, 
                         ((self.width - scaled_surface.get_width()) // 2,
                          (self.height - scaled_surface.get_height()) // 2))

        # Draw menu
        if self.show_menu:
            self.draw_menu()

    def draw_menu(self):
        menu_width, menu_height = 800, 600
        menu_surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
        menu_surface.fill((0, 0, 0, 230))

        title = self.font.render("Welcome to the irrational world of π", True, (255, 255, 255))
        menu_surface.blit(title, (menu_width // 2 - title.get_width() // 2, 50))

        explanation1 = self.small_font.render("This visualization demonstrates the fascinating property of π:", True, (255, 255, 255))
        explanation2 = self.small_font.render("its decimal representation never settles into a repeating pattern.", True, (255, 255, 255))
        menu_surface.blit(explanation1, (50, 120))
        menu_surface.blit(explanation2, (50, 160))

        controls_title = self.font.render("Controls:", True, (255, 255, 255))
        menu_surface.blit(controls_title, (50, 220))

        controls = [
            "'+'/'-': Increase/decrease rotation speed",
            "Mouse wheel: Zoom in/out",
            "'c': Toggle color mode (white/rainbow)",
            "'m': Toggle this menu"
        ]

        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, (255, 255, 255))
            menu_surface.blit(control_text, (70, 270 + i * 40))

        # Draw "Show me" button
        button_rect = pygame.Rect(menu_width // 2 - 100, menu_height - 80, 200, 50)
        pygame.draw.rect(menu_surface, (100, 100, 255), button_rect)
        button_text = self.font.render("Show me", True, (255, 255, 255))
        menu_surface.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2))

        self.screen.blit(menu_surface, ((self.width - menu_width) // 2, (self.height - menu_height) // 2))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        self.speed *= 1.1
                    elif event.key == pygame.K_MINUS:
                        self.speed /= 1.1
                    elif event.key == pygame.K_c:
                        self.config.color_mode = 'rainbow' if self.config.color_mode == 'white' else 'white'
                    elif event.key == pygame.K_m:
                        self.show_menu = not self.show_menu
                elif event.type == pygame.MOUSEWHEEL:
                    self.config.zoom_factor *= 1.1 if event.y > 0 else 0.9
                    self.config.zoom_factor = max(0.1, min(10, self.config.zoom_factor))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.show_menu:
                            menu_width, menu_height = 800, 600
                            button_rect = pygame.Rect((self.width - menu_width) // 2 + menu_width // 2 - 100, 
                                                      (self.height - menu_height) // 2 + menu_height - 80, 
                                                      200, 50)
                            if button_rect.collidepoint(event.pos):
                                self.show_menu = False

            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    config = Config()
    visualization = PiVisualization(config)
    visualization.run()
