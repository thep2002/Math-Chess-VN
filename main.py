"""
Main driver file.
Handling user input.
Displaying current GameStatus object.
"""

import pygame
import time
from Engine.GameState import GameState
from Engine.Move import Move
from AI.Negamax import Negamax
from AI.Negascout import Negascout
from AI.Minimax import Minimax
from AI.Greedy import Greedy
from UI.UI import *
from UI.CAL import *
WIDTH = 832
HEIGHT = 704
C_DIMENSION = 9
R_DIMENSION = 11
SQ_SIZE = HEIGHT // R_DIMENSION
MAX_FPS = 10
IMAGES = {}
WIDTH_CAL = 256
HEIGHT_CAL = 256
scenes = {
        'TITLE': SimpleScene('Cờ toán Việt Nam'),
        'CHOOSE_MODE': ChooseScene('Chọn chế độ chơi','Người Vs Người','Người Vs Máy','Máy Vs Máy'),
        'CHOOSE_BOT': ChooseBot('Chọn Bot','Negamax','Negascout','Minimax','Greedy'),
        'CHOOSE_DEPTH': ChooseDepth('Chọn độ sâu','Độ sâu: ')
    }
botai = {
    'Negamax': Negamax(),
    'Negascout': Negascout(),
    'Minimax': Minimax(),
    'Greedy': Greedy()
}

def loadImages():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ["b0", "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9",
              "r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("image/" + piece + ".png"),
                                               (SQ_SIZE - 10, SQ_SIZE - 10))


def scoreMaterial(gs):
    score_1 = 0
    score_2 = 0
    for row in gs.board:
        for square in row:
            if square[0] == "r":
                if int(square[1]) == 0:
                    score_1 += 1000000
                else:
                    score_1 += int(square[1])
            elif square[0] == "b":
                if int(square[1]) == 0:
                    score_2 += 1000000
                else:
                    score_2 += int(square[1])
    score_3 = 1000045 - score_2
    score_4 = 1000045 - score_1
    return score_3, score_4
def CalTime(gs):
    time1 = 600
    time2 = 600
    if gs.red_to_move:
        time1 -= 1/MAX_FPS
    else:
        time2 -= 1/MAX_FPS
    if time1 < 0 or time2 < 0:
        time1 = time2 = 600
    return time1, time2



def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    gs = GameState()
    valid_moves = gs.getAllPossibleMoves()
    move_made = False  # flag variable for when a move is made
    loadImages()
    running = True
    sq_selected = ()  # no square is selected, keep track of the last click of the user (tuple: (row, col))
    player_clicks = []  # keep track of the player clicks
    game_over = False
    # AI = Negascout()  # Greedy / Minimax / Negamax / Negascout
    player_time = 1200
    player1_time = 600
    player2_time = 600
    player1_timeint = 600
    player2_timeint = 600
    red_score = 0
    blue_score = 0
    start_time = pygame.time.get_ticks()
    AI_BLUE = None
    DEPTH_AI_BLUE = None
    DEPTH_AI_RED = None
    AI_RED = None
    red_score = 0
    blue_score = 0
    end_UI = True
    scene = scenes['TITLE']
    CAL = CACULATION()
    while running:
        if end_UI == True:
            screen = pygame.display.set_mode((640, 480))
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    return
            result = scene.update(events)
            ele = scene.element(events)
            if result or ele:
                if ele or ele == 0 :
                    if ele == (True, True):
                        player_one = True  # if a human playing red, then this will be True. If an AI is playing, then false
                        player_two = True  # same as above but for blue
                        end_UI = False
                        result = 'CHOOSE_MODE'
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    if ele == (True, False):
                        player_one = True
                        player_two = False
                        result = 'CHOOSE_BOT'
                    if ele == (False, False):
                        player_one = False
                        player_two = False
                        result = 'CHOOSE_BOT'
                    if ele == 'Negamax' and  AI_BLUE:
                        AI_RED = botai['Negamax']
                        result = 'CHOOSE_DEPTH'
                    if ele == 'Negamax' and not AI_BLUE:
                        AI_BLUE = botai['Negamax']
                        result = 'CHOOSE_DEPTH'
                    if ele == 'Negascout' and  AI_BLUE:
                        AI_RED = botai['Negamax']
                        result = 'CHOOSE_DEPTH'
                    if ele == 'Negascout' and not AI_BLUE:
                        AI_BLUE = botai['Negascout']
                        result = 'CHOOSE_DEPTH'
                    if ele == 'Minimax' and AI_BLUE:
                        AI_RED = botai['Negamax']
                        result = 'CHOOSE_DEPTH'
                    if ele == 'Minimax' and not AI_BLUE:
                        AI_BLUE = botai['Minimax']
                        result = 'CHOOSE_DEPTH'
                    if ele == 'Greedy' and  AI_BLUE:
                        AI_RED = botai['Greedy']
                        DEPTH_AI_RED = True
                    if ele == 'Greedy' and not AI_BLUE:
                        AI_BLUE = botai['Greedy']
                        DEPTH_AI_BLUE = True
                    if isinstance(ele, int) and  DEPTH_AI_BLUE :
                        if ele >= 0:
                            DEPTH_AI_RED = ele
                        else:
                            AI_RED = None
                    if isinstance(ele, int) and not DEPTH_AI_BLUE:
                        if ele >= 0:
                            DEPTH_AI_BLUE = ele
                        else:
                            AI_BLUE = None
                    if not player_one and not AI_RED and (DEPTH_AI_BLUE or DEPTH_AI_BLUE == 0):
                        result = 'CHOOSE_BOT'

                    if (player_one and not player_two and AI_BLUE and (DEPTH_AI_BLUE or DEPTH_AI_BLUE == 0)) or (not player_one and not player_two and AI_BLUE and AI_RED and (DEPTH_AI_BLUE or DEPTH_AI_BLUE == 0) and (DEPTH_AI_RED or DEPTH_AI_RED == 0)):

                        result = 'CHOOSE_MODE'
                        end_UI = False
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))

                scene = scenes[result]
            scene.draw(screen)
            pygame.display.flip()
        else:
            drawGameState(screen, gs, valid_moves, sq_selected,events)
            game_over = gs.check()
            if game_over:
                if gs.red_to_move:
                    loser("Blue win", screen)
                    running = False
                else:
                    loser("Red win", screen)
                    running = False
            human_turn = (gs.red_to_move and player_one) or (not gs.red_to_move and player_two)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    if not game_over and human_turn and location[0] <= WIDTH-WIDTH_CAL:
                        col = location[0] // SQ_SIZE
                        row = location[1] // SQ_SIZE
                        if sq_selected == (row, col):  # the user clicked the same square twice
                            sq_selected = ()  # deselect
                            player_clicks = []  # clear player clicks
                        else:
                            sq_selected = (row, col)
                            player_clicks.append(sq_selected)  # append for both 1st and 2nd clicks
                        if len(player_clicks) == 2:  # after 2 click
                            move = Move(player_clicks[0], player_clicks[1], gs.board)
                            if move in valid_moves:
                                gs.makeMove(move)
                                move_made = True
                                sq_selected = ()  # reset user clicks
                                player_clicks = []
                            else:
                                player_clicks = [sq_selected]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:  # undo when 'z' is pressed
                        gs.undoMove()
                        gs.undoMove()
                        move_made = True

            player1_time = CalTime(gs)[0]
            player1_timeint = int(player1_time)
            player1_minutes = player1_timeint // 60
            player1_minutes1 = player1_minutes // 10
            player1_minutes2 = player1_minutes % 10
            player1_second = player1_timeint % 60
            player1_second1 = player1_second // 10
            player1_second2 = player1_second % 10
            player2_time = CalTime(gs)[1]
            player2_timeint = int(player2_time)
            player2_minutes = player2_timeint // 60
            player2_minutes1 = player2_minutes // 10
            player2_minutes2 = player2_minutes % 10
            player2_second = player2_timeint % 60
            player2_second1 = player2_second // 10
            player2_second2 = player2_second % 10

                # Check for time expiration
            if player1_time <= 0:
                print("Player 1 has run out of time!")
                break
            if player2_time <= 0:
                print("Player 2 has run out of time!")
                break
            font = pygame.font.Font(None, 36)
            sub_screen1 = pygame.Surface((256, 176))
            sub_screen1.fill((255, 0, 0))
            # Write some text on the sub-screen
            font = pygame.font.Font(None, 36)
            text = font.render("Red time: " + str(player1_minutes1) + str(player1_minutes2) + ':' + str(player1_second1) + str(player1_second2), True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.centerx = sub_screen1.get_rect().centerx
            text_rect.centery = sub_screen1.get_rect().centery+70
            sub_screen1.blit(text, text_rect)
            # Blit the sub-screen onto the main screen
            screen.blit(sub_screen1, (576, 352))

            sub_screen4 = pygame.Surface((256, 176))
            sub_screen4.fill((0, 0, 255))
            # Write some text on the sub-screen
            font = pygame.font.Font(None, 36)
            text = font.render("Blue time: " + str(player2_minutes1) + str(player2_minutes2) + ':' + str(player2_second1) + str(player2_second2), True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.centerx = sub_screen4.get_rect().centerx
            text_rect.centery = sub_screen4.get_rect().centery-70
            sub_screen4.blit(text, text_rect)
            # Blit the sub-screen onto the main screen
            screen.blit(sub_screen4, (576, 176))

            # Calculate red score
            red_score = scoreMaterial(gs)[0]
            blue_score = scoreMaterial(gs)[1]
            if red_score >= 15:
                loser("Red win", screen)
                running = False
            elif blue_score >= 15:
                loser("Blue win", screen)
                running = False

            sub_screen3 = pygame.Surface((256, 176))
            sub_screen3.fill((255, 0, 0))
            # Write some text on the sub-screen
            font = pygame.font.Font(None, 36)
            text = font.render("Red score: " + str(red_score), True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.centerx = sub_screen3.get_rect().centerx
            text_rect.centery = sub_screen3.get_rect().centery+50
            sub_screen3.blit(text, text_rect)
            # Blit the sub-screen onto the main screen
            screen.blit(sub_screen3, (576, 528))

            sub_screen2 = pygame.Surface((256, 176))
            sub_screen2.fill((0, 0, 255))
            # Write some text on the sub-screen
            font = pygame.font.Font(None, 36)
            text = font.render("Blue score: " + str(blue_score), True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.centerx = sub_screen2.get_rect().centerx
            text_rect.centery = sub_screen2.get_rect().centery-50
            sub_screen2.blit(text, text_rect)
            # Blit the sub-screen onto the main screen
            screen.blit(sub_screen2, (576, 0))
            # Update the display

            # AI move finder
            if not game_over and not human_turn  and not gs.red_to_move:
                ################################
                AIMove = AI_BLUE.findMove(gs, valid_moves,DEPTH_AI_BLUE)
                gs.makeMove(AIMove)
                move_made = True
                ################################

            elif not game_over and not human_turn and AI_RED and gs.red_to_move:
                ################################
                AIMove = AI_BLUE.findMove(gs, valid_moves,DEPTH_AI_RED)
                gs.makeMove(AIMove)
                move_made = True
                ################################
            if move_made:
                valid_moves = gs.getAllPossibleMoves()
                move_made = False
            drawGameState(screen, gs, valid_moves, sq_selected,events)

            CAL.draw_caltable(screen, events,IMAGES)
            clock.tick(MAX_FPS)
            pygame.display.flip()


'''
Highlight square selected and moves for piece selected
'''


def highlightSquares(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ('r' if gs.red_to_move else 'b'):  # sq_selected is a piece that can be moved
            # highlight selected square
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value -> 0 transparent; 255 opaque
            s.fill(pygame.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(pygame.Color('yellow'))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))


def drawGameState(screen, gs, valid_moves, sq_selected,events):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)
    highlightSquares(screen, gs, valid_moves, sq_selected)
    drawPieces(screen, gs.board)

    # CAL.__init__().cal_num_1 = 1

def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    colors = [pygame.Color("white"), pygame.Color("bisque3")]
    for r in range(R_DIMENSION):
        for c in range(C_DIMENSION):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for r in range(R_DIMENSION):
        for c in range(C_DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c * SQ_SIZE + 5, r * SQ_SIZE + 5, SQ_SIZE, SQ_SIZE))
def loser(message, screen):
    time.sleep(0.5)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(message, True, pygame.Color('green'))
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2)
    screen.fill(pygame.Color('white'))
    screen.blit(text, textRect)
    pygame.display.update()
    time.sleep(5)




if __name__ == '__main__':
    main()
