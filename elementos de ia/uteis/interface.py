import pygame
import sys
import os
import numpy as np
from board import create_board, print_board
from check_win import check_win
from movimentos import move_piece, select_piece, possible_moves


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from algoritmos.a_star import *

# Initialize pygame
pygame.init()

# Screen dimensions
largura, altura = 1900, 900
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Sport Sort")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
BRIGHT_RED = (255, 0, 0)
vermelho_tijolo = (236, 127, 110)
vermelho_tijolo_escuro = (131, 37, 17)
dark_blue = (93, 90, 136)
light_blue = (162, 159, 230)
really_light_blue = (185, 183, 217)
YELLOW = (255, 255, 0)

# Load backgrounds
fundo = pygame.image.load("fundos/fundo.jpeg") 
fundo = pygame.transform.scale(fundo, (largura, altura))  # Scale to fit screen
fundo_final = pygame.image.load("fundos/fundo_final.jpg")
fundo_final = pygame.transform.scale(fundo_final, (largura, altura))

# Fonts
title_font = pygame.font.SysFont("Showcard Gothic", 250)
button_font = pygame.font.SysFont("comicsansms", 50)
button_font2 = pygame.font.SysFont("comicsans", 35)
title_in_rules = pygame.font.SysFont("Showcard Gothic", 175)
subtitles = pygame.font.SysFont("comicsansms", 70)
message_font = pygame.font.SysFont("comicsansms", 40)

# Create ball constants
BASKETBOL = 1
FUTEBOL = 2
VOLEIBOL = 3
BASEBOL = 4
TENIS = 5
RUGBY = 6

# Load ball images
ball_images = {}
ball_types = {
    BASKETBOL: "basketbol",
    FUTEBOL: "futebol",
    VOLEIBOL: "voleibol",
    BASEBOL: "basebol", 
    TENIS: "tenis",
    RUGBY: "rugby"
}

for ball_value, ball_name in ball_types.items():
    image_path = f"bolas/{ball_name}.png"
    try:
        img = pygame.image.load(image_path)
        # Scale the balls to an appropriate size
        img = pygame.transform.scale(img, (80, 80))
        ball_images[ball_value] = img
    except pygame.error:
        print(f"Could not load image {image_path}")


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = font if font else button_font  # Use custom font if provided, else default
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        text_color = WHITE if self.is_hovered else BLACK
        border_color = WHITE if self.is_hovered else BLACK
        
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=10)  # Border
        
        text_surf = self.font.render(self.text, True, text_color)  # Use instance font
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False
    
class Shelf:
    def __init__(self, x, y, width, height, index):
        self.rect = pygame.Rect(x, y, width, height)
        self.index = index
        self.selected = False
        self.ball_rects = []  # To track individual ball positions
        
    def draw(self, surface, balls=None):
        # Draw shelf (brown rectangle)
        shelf_color = (139, 69, 19)  # Brown for wooden shelf
        pygame.draw.rect(surface, shelf_color, self.rect)
        
        # Add a border (yellow if selected)
        border_color = BLACK if self.selected else BLACK
        border_width = 3 if self.selected else 1
        pygame.draw.rect(surface, border_color, self.rect, border_width)
        
        # Draw balls if provided
        self.ball_rects = []  # Reset ball rects
        if balls is not None:
            for i, ball in enumerate(balls):
                if ball != 0:  # Only draw non-zero (existing) balls
                    # Calculate position on shelf
                    ball_x = self.rect.x + 10 + i * 90
                    ball_y = self.rect.y - 90
                    ball_rect = pygame.Rect(ball_x, ball_y, 80, 80)
                    self.ball_rects.append(ball_rect)
                    
                    # Draw the ball image
                    if ball in ball_images:
                        surface.blit(ball_images[ball], (ball_x, ball_y))
                    else:
                        pygame.draw.circle(surface, WHITE, (ball_x + 40, ball_y + 40), 40)

    def is_clicked(self, pos, event):
        return self.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN
    
    def get_clicked_ball(self, pos):
        # Check if any ball was clicked (starting from rightmost)
        for i in range(len(self.ball_rects)-1, -1, -1):
            if self.ball_rects[i].collidepoint(pos):
                return i  # Return ball index
        return None

# Create buttons
play_button = Button(largura//2 - 150, altura//2, 300, 100, "JOGAR", dark_blue, light_blue)
rules_button = Button(largura//2 - 150, altura//2 + 150, 300, 100, "REGRAS", dark_blue, light_blue)
jogar_button1 = Button(largura//2 - 150, altura//4 + 100, 300, 100, "NÍVEL 1", dark_blue, light_blue)
jogar_button2 = Button(largura//2 - 150, altura//4 + 220, 300, 100, "NÍVEL 2", dark_blue, light_blue)
jogar_button3 = Button(largura//2 - 150, altura//4 + 340, 300, 100, "NÍVEL 3", dark_blue, light_blue)
back_button = Button(50, altura - 150, 200, 80, "VOLTAR", dark_blue, light_blue)
humano_button = Button(largura//2 - 150, altura//4 + 100, 300, 100, "HUMANO", dark_blue, light_blue)
computador_button = Button(largura//2 - 150, altura//4 + 220, 300, 100, "COMPUTADOR", dark_blue, light_blue, button_font2)
next_button = Button(largura//2 + 200, altura - 150, 200, 80, "PRÓXIMO", dark_blue, light_blue, button_font2)

##################

def draw_main_menu():
    tela.blit(fundo, (0, 0))
    
    # Draw game title
    title_text = title_font.render("SPORT SORT", True, WHITE)
    title_shadow = title_font.render("SPORT SORT", True, vermelho_tijolo_escuro)
    
    # Position the title with a shadow effect
    title_rect = title_text.get_rect(center=(largura//2, altura//4))
    tela.blit(title_shadow, (title_rect.x+10, title_rect.y+10))
    tela.blit(title_text, title_rect)
    
    # Draw buttons
    play_button.draw(tela)
    rules_button.draw(tela)
    
    pygame.display.update()

def show_rules():
    rules_running = True
    
    rules_text = [
        "Regras:",
        "",
        "Como se ganha este jogo?",  # Line 2
        "Para ganhar, organize todas as bolas,",  # Line 3
        "com uma prateleira para cada desporto.",
        "",
        "Quais os possíveis movimentos?",  # Line 6
        "Só pode mover a bola da direita de cada prateleira para uma vazia",  # Line 8
        "ou quando a última bola é igual à que está a ser movida.",
        "Para jogar, clique na bola e depois na prateleira para onde a quer mover",
        "(tem de clicar mesmo na madeira da prateleira, não no espaço em cima desta!)"
        "",
        "(Clique em qualquer lugar para voltar)"
    ]
    
    # Pre-render everything once before the loop
    overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    
    # Create a complete rules surface with just the background
    rules_surface = pygame.Surface((largura, altura))
    rules_surface.blit(fundo, (0, 0))
    rules_surface.blit(overlay, (0, 0))
    
    # Starting y position
    y_offset = (altura // 4 )- 50
    
    # Define spacing values
    TITLE_SPACING = 80
    TITLE_TO_CONTENT_SPACING = 80  # New: Extra space between title and first content
    HEADER_SPACING = 70  # After question lines (3 and 7)
    NORMAL_SPACING = 55
    PARAGRAPH_SPACING = 50  # After empty lines
    
    for i, line in enumerate(rules_text):
        if i == 0:  # Title
            text = title_in_rules.render(line, True, really_light_blue)
            spacing = TITLE_SPACING
        elif i == 2 or i == 6:  # Question lines (3 and 7)
            text = subtitles.render(line, True, really_light_blue)
            spacing = HEADER_SPACING
        elif i == 11:
            text = button_font.render(line, True, really_light_blue)
        else:
            text = button_font.render(line, True, WHITE)
            spacing = NORMAL_SPACING
        
        text_rect = text.get_rect(center=(largura//2, y_offset))
        rules_surface.blit(text, text_rect)
        
        # Add extra space after specific lines
        if i == 2 or i == 6:  # After question lines (3 and 7)
            y_offset += HEADER_SPACING
        elif i == 1 or i == 5:  # After empty lines
            y_offset += PARAGRAPH_SPACING
        else:
            y_offset += NORMAL_SPACING
    
    clock = pygame.time.Clock()
    
    while rules_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                rules_running = False
        
        tela.blit(rules_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def create_shelves(level):
    shelves = []
    shelf_width = 400
    shelf_height = 20
    shelf_gap = 200  # Horizontal gap between columns
    vertical_gap = 120  # Vertical gap between shelves
    
    if level == 1:
        # Level 1: 3 shelves on each side (total 6)
        left_positions = 3
        right_positions = 3
    elif level == 2:
        # Level 2: 3 on left, 4 on right (total 7)
        left_positions = 3
        right_positions = 4
    else:  # level 3
        # Level 3: 4 on each side (total 8)
        left_positions = 4
        right_positions = 4
    
    # Calculate starting y position to center vertically
    total_shelves = max(left_positions, right_positions)
    start_y = (altura - (total_shelves * vertical_gap)) // 2
    
    # Create left column shelves (indices 0, 2, 4, etc.)
    for i in range(left_positions):
        x = (largura // 2) - shelf_width - shelf_gap // 2
        y = start_y + i * vertical_gap
        shelves.append(Shelf(x, y, shelf_width, shelf_height, i*2))
    
    # Create right column shelves (indices 1, 3, 5, etc.)
    for i in range(right_positions):
        x = (largura // 2) + shelf_gap // 2
        y = start_y + i * vertical_gap
        shelves.append(Shelf(x, y, shelf_width, shelf_height, i*2 + 1))
    
    # Sort shelves by index to ensure proper ordering
    shelves.sort(key=lambda shelf: shelf.index)
    return shelves

def draw_game_screen(board, shelves, level, message="", selected_shelf=None, selected_ball=None, possible_moves_list=None):
    background = fundo_final
    tela.blit(background, (0, 0))
    
    # Draw each shelf with its balls
    for i, shelf in enumerate(shelves):
        shelf.selected = (selected_shelf == i)
        shelf.draw(tela, board[i])
        
        # Highlight selected ball if any
        if selected_shelf == i and selected_ball is not None:
            if selected_ball < len(shelf.ball_rects):
                ball_rect = shelf.ball_rects[selected_ball]
                pygame.draw.rect(tela, YELLOW, ball_rect, 3)
    
    # Draw message if any
    if message:
        message_surf = message_font.render(message, True, WHITE)
        message_rect = message_surf.get_rect(center=(largura//2, 100))
        # Draw semi-transparent background for message
        msg_bg = pygame.Rect(message_rect.x - 10, message_rect.y - 5, 
                           message_rect.width + 20, message_rect.height + 10)
        msg_surface = pygame.Surface((msg_bg.width, msg_bg.height), pygame.SRCALPHA)
        msg_surface.fill((0, 0, 0, 180))
        tela.blit(msg_surface, (msg_bg.x, msg_bg.y))
        tela.blit(message_surf, message_rect)
    
    # Note: Buttons are now drawn in the main game loop
    pygame.display.flip()

def start_game(level, player_type="HUMANO"):
    board = create_board(level)
    shelves = create_shelves(level)
    
    selected_shelf = None
    selected_ball = None
    possible_moves_list = []
    message = ""
    game_won = False
    
    # Computer move variables
    computer_moves = []
    current_move = 0
    solving = False
    solution_found = False
    
    if player_type == "COMPUTADOR":
        # Calculate solution when computer player starts
        computer_moves, time_dict, move_count = a_star_solution(board, level)
  
        if computer_moves:
            message = f"Solução encontrada em {move_count} movimentos"
            solution_found = True
            solving = True
        else:
            message = "Computador não encontrou solução"
            solution_found = False
    
    level_running = True
    clock = pygame.time.Clock()

    while level_running:
        mouse_pos = pygame.mouse.get_pos()
   
        if check_win(board, level):
            message = "PARABÉNS! GANHASTE!" if player_type == "HUMANO" else "COMPUTADOR RESOLVEU!"
            game_won = True
            solving = False
        
        # Draw the game screen WITHOUT flipping the display
        background = fundo_final
        tela.blit(background, (0, 0))
        
        # Draw each shelf with its balls
        for i, shelf in enumerate(shelves):
            shelf.selected = (selected_shelf == i)
            shelf.draw(tela, board[i])
            
            # Highlight selected ball if any
            if selected_shelf == i and selected_ball is not None:
                if selected_ball < len(shelf.ball_rects):
                    ball_rect = shelf.ball_rects[selected_ball]
                    pygame.draw.rect(tela, YELLOW, ball_rect, 3)
        
        # Draw message if any
        if message:
            message_surf = message_font.render(message, True, WHITE)
            message_rect = message_surf.get_rect(center=(largura//2, 100))
            # Draw semi-transparent background for message
            msg_bg = pygame.Rect(message_rect.x - 10, message_rect.y - 5, 
                               message_rect.width + 20, message_rect.height + 10)
            msg_surface = pygame.Surface((msg_bg.width, msg_bg.height), pygame.SRCALPHA)
            msg_surface.fill((0, 0, 0, 180))
            tela.blit(msg_surface, (msg_bg.x, msg_bg.y))
            tela.blit(message_surf, message_rect)
        
        # Draw buttons after checking hover states
        back_button.check_hover(mouse_pos)
        back_button.draw(tela)
        
        # Draw next button if computer is solving and solution was found
        if player_type == "COMPUTADOR" and not game_won and solution_found:
            next_button.check_hover(mouse_pos)
            next_button.draw(tela)
        
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if back_button.is_clicked(mouse_pos, event):
                level_running = False
                break
            
            # Handle next button click for computer moves
            if (player_type == "COMPUTADOR" and not game_won and solution_found and 
                next_button.is_clicked(mouse_pos, event)):
                if current_move < len(computer_moves):
                    from_shelf, to_shelf = computer_moves[current_move]
                    if move_piece(board, from_shelf, to_shelf):
                        current_move += 1
                        message = f"Movimento {current_move}/{len(computer_moves)}"
                        if current_move == len(computer_moves):
                            solving = False
                    else:
                        message = "Erro ao executar movimento"
            
            # Only allow human moves if human player
            if player_type == "HUMANO" and event.type == pygame.MOUSEBUTTONDOWN and not game_won:
                clicked_on_ball = False
                
                # First check for destination selection
                if selected_shelf is not None:
                    for shelf_idx, shelf in enumerate(shelves):
                        if shelf.is_clicked(mouse_pos, event):
                            clicked_on_ball = True
                            if shelf_idx in possible_moves_list:
                                if move_piece(board, selected_shelf, shelf_idx):
                                    message = ""
                                else:
                                    message = "Movimento inválido"
                            else:
                                message = "Destino inválido"
                            
                            selected_shelf = None
                            selected_ball = None
                            possible_moves_list = []
                            break
                
                # Then check for new ball selection
                if not clicked_on_ball:
                    for shelf_idx, shelf in enumerate(shelves):
                        current_shelf = board[shelf_idx]
                        
                        # Find the rightmost actual ball (non-zero) position
                        rightmost_pos = -1
                        for i in range(len(current_shelf)-1, -1, -1):
                            if current_shelf[i] != 0:
                                rightmost_pos = i
                                break
                        
                        if rightmost_pos == -1:  # Skip empty shelves
                            continue
                            
                        ball_idx = shelf.get_clicked_ball(mouse_pos)
                        
                        if ball_idx is not None and ball_idx == rightmost_pos:
                            clicked_on_ball = True
                            selected_shelf = shelf_idx
                            selected_ball = ball_idx
                            ball = current_shelf[ball_idx]
                            possible_moves_list = possible_moves(board, shelf_idx, ball, level)
                            message = ""
                            break
                
                if not clicked_on_ball and selected_shelf is not None:
                    selected_shelf = None
                    selected_ball = None
                    possible_moves_list = []
                    message = ""
        
        # Update the display once per frame
        pygame.display.flip()
        clock.tick(60)  # Increased frame rate for smoother animations


def show_jogar():
    # First show the player type selection
    player_type_running = True
    
    # Create overlay surface
    overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    
    while player_type_running:
        mouse_pos = pygame.mouse.get_pos()

        # Draw background with overlay
        tela.blit(fundo, (0, 0))
        tela.blit(overlay, (0, 0))
        
        # Draw title
        title_text = title_in_rules.render("ESCOLHA O JOGADOR", True, really_light_blue)
        title_rect = title_text.get_rect(center=(largura//2, altura//6))
        tela.blit(title_text, title_rect)

        # Check hovers and draw buttons
        humano_button.check_hover(mouse_pos)
        computador_button.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)
        
        humano_button.draw(tela)
        computador_button.draw(tela)
        back_button.draw(tela)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(mouse_pos, event):
                    player_type_running = False
                elif humano_button.is_clicked(mouse_pos, event):
                    show_level_selection("HUMANO")
                    player_type_running = False
                elif computador_button.is_clicked(mouse_pos, event):
                    show_level_selection("COMPUTADOR")
                    player_type_running = False
        
        pygame.display.flip()
        pygame.time.delay(30)

def show_level_selection(player_type):
    level_running = True

    # Create overlay surface
    overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    
    while level_running:
        mouse_pos = pygame.mouse.get_pos()

        # Draw background with overlay
        tela.blit(fundo, (0, 0))
        tela.blit(overlay, (0, 0))
        
        # Draw title 
        title_text = title_in_rules.render("NÍVEL", True, really_light_blue)
        title_rect = title_text.get_rect(center=(largura//2, altura//6))
        tela.blit(title_text, title_rect)

        # Check hovers and draw buttons
        jogar_button1.check_hover(mouse_pos)
        jogar_button2.check_hover(mouse_pos)
        jogar_button3.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)
        
        jogar_button1.draw(tela)
        jogar_button2.draw(tela)
        jogar_button3.draw(tela)
        back_button.draw(tela)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(mouse_pos, event):
                    level_running = False
                elif jogar_button1.is_clicked(mouse_pos, event):
                    start_game(1, player_type)
                elif jogar_button2.is_clicked(mouse_pos, event):
                    start_game(2, player_type)
                elif jogar_button3.is_clicked(mouse_pos, event):
                    start_game(3, player_type)
        
        pygame.display.flip()
        pygame.time.delay(30)

def main():
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        draw_main_menu()
        
        play_button.check_hover(mouse_pos)
        rules_button.check_hover(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(mouse_pos, event):
                    show_jogar()
                elif rules_button.is_clicked(mouse_pos, event):
                    show_rules()
        
        pygame.display.flip()
        pygame.time.delay(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()