import pygame
from GUIControl.GameGlobal import GameGlobal
from GUIControl.MovingState import MovingState
from GUIControl.PlacingState import PlacingState
from GUIControl.RemovingState import RemovingState
from NineMensMorrisGame.Game import Game
from NineMensMorrisGame.utils import GamePhase

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 560
FPS = 20

pygame.init()
pygame.display.set_caption("Nine Men's Morris")
icon = pygame.image.load('static/GameLogo.png')
game_board = pygame.image.load('static/GameBoard.png')
pygame.display.set_icon(icon)

font = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 26)
text_surface = font.render("Nine Men's Morris", True, BLACK)

coords = {
	0: (45, 140, 95, 190),
	1: (373, 140, 423, 190),
	2: (701, 140, 751, 190),
	3: (45, 468, 95, 518),
	4: (701, 468, 751, 518),
    5: (45, 796, 95, 846),
    6: (373, 796, 423, 846),
    7: (701, 796, 751, 846),
    8: (148, 246, 198, 296),
    9: (373, 246, 423, 296),
    10: (600, 246, 650, 296),
    11: (148, 468, 198, 518),
    12: (600, 468, 650, 518),
    13: (148, 695, 198, 745),
    14: (373, 695, 423, 745),
    15: (600, 695, 650, 745),
    16: (235, 337, 285, 387),
    17: (373, 337, 423, 387),
    18: (511, 337, 561, 387),
    19: (235, 468, 285, 518),
    20: (511, 468, 561, 518),
    21: (235, 610, 285, 660),
    22: (373, 610, 423, 660),
    23: (511, 610, 561, 660)
}
scaling_factor = 500/843
clickables = [pygame.Rect(scaling_factor*c[0], scaling_factor*c[1], 60, 60) for c in coords.values()]
clock = pygame.time.Clock()
pieces = [(int(area.x + area.width / 2), int(area.y + area.height / 2)) for area in clickables]

def drawBoard(board: list[str]):
    for i in range(len(pieces)):
        if board[i] == '2':
            pygame.draw.circle(screen, BLACK, pieces[i], 15)
        elif board[i] == '1':
            pygame.draw.circle(screen, BLACK, pieces[i], 16)
            pygame.draw.circle(screen, WHITE, pieces[i], 15)

def detect_button_click(event) -> int | None:
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for i, area in enumerate(clickables):
            if area.collidepoint(event.pos):
                return i
    return None

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
running = True
winner = None

placing_state = PlacingState() 
removing_state = RemovingState()
moving_state = MovingState()
current_state = None

game = Game()
state = GameGlobal()

while running:
    screen.fill((255, 255, 255))
    screen.blit(game_board, (50, 110))
    screen.blit(text_surface, (50, 20))
    text = font_small.render(state.text_command, True, BLACK)
    screen.blit(text, (50, 60))
    drawBoard(game.get_board())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if winner is None:
            if not state.mill_tested and state.placed:
                if game.is_mill_formed(state.global_player,state.placed_index):
                    state.text_command = f"PLAYER {state.global_player}: Choose piece of opponent you would like to remove: "
                    current_state = removing_state
                else:
                    state.global_player = 2 if state.global_player == 1 else 1
                    state.placed = False
                    state.placed_index = None
                    state.mill_tested = True
            else:
                current_phase = game.get_current_phase(state.global_player)
                if current_phase == GamePhase.PLACING and not state.placed:
                    state.text_command = f"PLAYER {state.global_player}: Choose position where to place your piece: "
                    current_state = placing_state
                    
                elif current_phase == GamePhase.MOVING or current_phase == GamePhase.FLYING and not state.placed:
                    if state.start is None and state.target is None:
                        state.text_command = f"PLAYER {state.global_player}: Choose position of piece you want to move: "
                    elif state.start is not None and state.target is None:
                        state.text_command = f"PLAYER {state.global_player}: Choose target position to which you want to move your piece"
                    current_state = moving_state

            colidepoint_index = detect_button_click(event)
            if colidepoint_index is not None and current_state is not None:
                current_state.handle_events(game, state, colidepoint_index)
                current_state = None
                    
        pygame.display.update()
        drawBoard(game.get_board())
        clock.tick(FPS)

    if winner is None:
        winner = game.is_winner()
        if winner is not None:
            state.text_command =f"The winner is Player: {winner}"