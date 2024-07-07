import pygame
from maze import kruskals, recursive_backtracker, hunt_and_kill, ellers, astar
import svgwrite

class Button:
    def __init__(self, screen, text, position, size, font, function):
        self.screen = screen
        self.text = text
        self.position = position
        self.size = size
        self.font = font
        self.rect = pygame.Rect(position, size)
        self.onclick = function

        # Redefine colors so python doesn't have to search out of the class scope to find them
        self.white = (255, 255, 255)
        self.gray = (190, 190, 190)
        self.black = (0, 0, 0)

    def draw(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.gray, self.rect, border_radius=8)
        else:
            pygame.draw.rect(self.screen, self.white, self.rect, border_radius=8)
        text_surface = self.font.render(self.text, True, self.black)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.onclick()

class AlgorithmSelectButton:
    def __init__(self, screen, text, position, size, font, algorithm):
        self.screen = screen
        self.text = text
        self.position = position
        self.size = size
        self.font = font
        self.algorithm = algorithm
        self.rect = pygame.Rect(position, size)
        self.inner_rect = pygame.Rect((position[0]+2, position[1]+2), (size[0]-4, size[1]-4))

        self.white = (255, 255, 255)
        self.gray = (190, 190, 190)
        self.black = (0, 0, 0)
        self.lightblue = (2, 60, 254)

    def draw(self, mouse_pos):
        global selected_algorithm

        pygame.draw.rect(self.screen, self.white, self.rect, border_radius=8)
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.gray, self.rect, border_radius=8)
        else:
            pygame.draw.rect(self.screen, self.white, self.rect, border_radius=8)
        if selected_algorithm == self.algorithm:
            pygame.draw.rect(self.screen, self.lightblue, self.inner_rect, 5, border_radius=8)
        
        text_surface = self.font.render(self.text, True, self.black)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_click(self, event):
        global selected_algorithm
        if self.rect.collidepoint(event.pos):
            selected_algorithm = self.algorithm

def gen_maze():
    global display_maze, maze, maze_start, maze_end, display_solution, solution_path, selected_algorithm
    display_solution = False # Remove solution so it doesn't overlap the new maze
    display_maze = True

    if selected_algorithm == "Kruskal's":
        maze_start, maze_end, maze = kruskals(39, 39)
    elif selected_algorithm == "DFS":
        maze_start, maze_end, maze = recursive_backtracker(79, 79)
    elif selected_algorithm == "Hunt And Kill":
        maze_start, maze_end, maze = hunt_and_kill(79, 79)
    else: # Selected algorithm is Eller's
        maze_start, maze_end, maze = ellers(79, 79)
    
    solution_path = astar(maze, maze_start, maze_end)

def toggle_solution():
    global maze, display_solution
    if display_maze:
        display_solution = not display_solution

def clear_maze():
    global display_maze, maze, display_solution, solution_path
    display_maze = False
    display_solution = False
    maze = []
    solution_path = []

def save_svg():
    global display_maze, maze, display_solution, solution_path

    if display_maze:
        filename = 'maze_solved.svg' if display_solution else 'maze.svg'
        dwg = svgwrite.Drawing(filename, profile='tiny', size=(800, 800))
    
        border_path_string = ""
        for y, row in enumerate(maze):
            for x, value in enumerate(row):
                if value == 1:
                    x1 = x * 10 + 5
                    y1 = y * 10 + 5
                    border_path_string += f'M{x1},{y1} h10 v10 h-10 z '
        border_path_string.strip()
    
        dwg.add(dwg.rect(insert=(0, 0), size=(800, 800), fill=svgwrite.rgb(255, 255, 255)))
        dwg.add(dwg.path(d=border_path_string, fill=svgwrite.rgb(0, 0, 255)))
    
        if display_solution:
            solution_path_string = ""
            for y, x in solution_path:
                x1 = x * 10 + 5
                y1 = y * 10 + 5
                solution_path_string += f'M{x1},{y1} h10 v10 h-10 z '
            solution_path_string.strip()
            dwg.add(dwg.path(d=solution_path_string, fill=svgwrite.rgb(255, 0, 0)))
    
        dwg.save()

def save_png(screen):
    global display_maze
    if display_maze:
        filename = 'maze_solved.png' if display_solution else 'maze.png'
        capture_surface = screen.subsurface(pygame.Rect(200, 0, 800, 800))
        pygame.image.save(capture_surface, filename)

def save_jpg(screen):
    global display_maze
    if display_maze:
        filename = 'maze_solved.jpg' if display_solution else 'maze.jpg'
        capture_surface = screen.subsurface(pygame.Rect(200, 0, 800, 800))
        pygame.image.save(capture_surface, 'maze.jpg')

def main():
    global display_maze, maze, maze_start, maze_end, display_solution, solution_path, selected_algorithm
    
    pygame.init()

    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption('Maze Generation and Solving')
    fps_controller = pygame.time.Clock()

    white = (255, 255, 255)
    black = (0, 0, 0)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    button_default = (255, 255, 255)
    button_hover = (190, 190, 190)

    title_font = pygame.font.Font(None, 32)
    font = pygame.font.Font(None, 25)

    maze_controls_text = title_font.render('Maze Controls', True, black)
    maze_algorithm_text = title_font.render('Maze Algorithm', True, black)
    save_as_text = title_font.render('Save Maze', True, black)

    display_maze = False
    display_solution = False

    selected_algorithm = "Kruskal's"

    buttons = [
        Button(screen, 'Generate Maze', (20, 70), (140, 40), font, gen_maze),
        Button(screen, 'Toggle Solution', (20, 130), (140, 40), font, toggle_solution),
        Button(screen, 'Clear Maze', (30, 190), (120, 40), font, clear_maze),
        AlgorithmSelectButton(screen, "Kruskal's", (25, 310), (130, 40), font, "Kruskal's"),
        AlgorithmSelectButton(screen, "DFS", (25, 370), (130, 40), font, "DFS"),
        AlgorithmSelectButton(screen, "Hunt And Kill", (25, 430), (130, 40), font, "Hunt And Kill"),
        AlgorithmSelectButton(screen, "Eller's", (25, 490), (130, 40), font, "Eller's"),
        Button(screen, 'SVG', (50, 610), (80, 40), font, save_svg),
        Button(screen, 'PNG', (50, 670), (80, 40), font, lambda: save_png(screen)),
        Button(screen, 'JPG', (50, 730), (80, 40), font, lambda: save_jpg(screen))
    ]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.handle_click(event)

        screen.fill(white)
        pygame.draw.rect(screen, blue, pygame.Rect(0, 0, 180, 800))
        pygame.draw.rect(screen, black, pygame.Rect(180, 0, 20, 800))

        text_rect = maze_controls_text.get_rect(center=(90, 40))
        screen.blit(maze_controls_text, text_rect.topleft)
        pygame.draw.line(screen, black, (text_rect.left, text_rect.bottom), (text_rect.right, text_rect.bottom), 2)

        text_rect = maze_algorithm_text.get_rect(center=(90, 280))
        screen.blit(maze_algorithm_text, text_rect.topleft)
        pygame.draw.line(screen, black, (text_rect.left, text_rect.bottom), (text_rect.right, text_rect.bottom), 2)

        text_rect = save_as_text.get_rect(center=(90, 580))
        screen.blit(save_as_text, text_rect.topleft)
        pygame.draw.line(screen, black, (text_rect.left, text_rect.bottom), (text_rect.right, text_rect.bottom), 2)

        for button in buttons:
            button.draw(mouse_pos) # Pass mouse position to tell if it is being hovered over

        if display_maze:
            for y, row in enumerate(maze):
                for x, block in enumerate(row):
                    if block == 1: # Draw walls
                        pygame.draw.rect(screen, blue, pygame.Rect(x*10+205, y*10+5, 10, 10))

        if display_solution:
            for y, x in solution_path:
                pygame.draw.rect(screen, red, pygame.Rect(x*10+205, y*10+5, 10, 10))

        pygame.display.update()
        fps_controller.tick(30)

if __name__ == '__main__':
    main()
