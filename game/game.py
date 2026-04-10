import pygame as pg
import time
import sys
import os

pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()
pg.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

music_path = os.path.join(BASE_DIR, "background_music.mp3")
x_path = os.path.join(BASE_DIR, "x.jpg")
o_path = os.path.join(BASE_DIR, "o.jpg")

try:
    pg.mixer.music.load(music_path)
    pg.mixer.music.set_volume(0.5)
    pg.mixer.music.play(-1)
except:
    print("Music not found")

board = [[None,None,None],[None,None,None],[None,None,None]]
game_over = False
turn = 'X'
winner = None
draw = False

WIDTH = 600
HEIGHT = 700
LINE_WIDTH = 10
CELL_SIZE = WIDTH // 3

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GRAY = (180,180,180)

try:
    x_img = pg.image.load(x_path)
    o_img = pg.image.load(o_path)
except:
    x_img = pg.Surface((CELL_SIZE-40,CELL_SIZE-40))
    x_img.fill((200,0,0))
    o_img = pg.Surface((CELL_SIZE-40,CELL_SIZE-40))
    o_img.fill((0,0,200))

x_img = pg.transform.scale(x_img,(CELL_SIZE-40,CELL_SIZE-40))
o_img = pg.transform.scale(o_img,(CELL_SIZE-40,CELL_SIZE-40))

screen = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Tic Tac Toe - Jack vs Oggy")

font = pg.font.SysFont(None,35)

new_game_btn = pg.Rect(80,640,180,40)
restart_btn = pg.Rect(340,640,180,40)

def game_initiating_window():
    screen.fill(WHITE)

    pg.draw.line(screen,BLACK,(CELL_SIZE,0),(CELL_SIZE,HEIGHT-120),LINE_WIDTH)
    pg.draw.line(screen,BLACK,(WIDTH-CELL_SIZE,0),(WIDTH-CELL_SIZE,HEIGHT-120),LINE_WIDTH)
    pg.draw.line(screen,BLACK,(0,CELL_SIZE),(WIDTH,CELL_SIZE),LINE_WIDTH)
    pg.draw.line(screen,BLACK,(0,HEIGHT-CELL_SIZE-120),(WIDTH,HEIGHT-CELL_SIZE-120),LINE_WIDTH)

    draw_status()
    draw_buttons()
    pg.display.update()

def draw_buttons():
    pg.draw.rect(screen,GRAY,new_game_btn)
    pg.draw.rect(screen,GRAY,restart_btn)

    screen.blit(font.render("New Game",True,BLACK),(110,650))
    screen.blit(font.render("Restart",True,BLACK),(380,650))

def draw_status():
    status_font = pg.font.SysFont(None,40)

    if game_over:
        if winner == 'X':
            text = "Jack Wins!"
        elif winner == 'O':
            text = "Oggy Wins!"
        elif draw:
            text = "Match Draw!"
        else:
            text = "Click New Game"
    else:
        if turn == 'X':
            text = "Jack's Turn"
        else:
            text = "Oggy's Turn"

    pg.draw.rect(screen,BLUE,(0,580,WIDTH,50))

    status = status_font.render(text,True,WHITE)
    rect = status.get_rect(center=(WIDTH//2,605))
    screen.blit(status,rect)

def check_win():
    global winner, game_over

    for i in range(3):
        if board[i][0]==board[i][1]==board[i][2] and board[i][0]!=None:
            winner = board[i][0]
            game_over = True
            return True

        if board[0][i]==board[1][i]==board[2][i] and board[0][i]!=None:
            winner = board[0][i]
            game_over = True
            return True

    if board[0][0]==board[1][1]==board[2][2] and board[0][0]!=None:
        winner = board[0][0]
        game_over = True
        return True

    if board[0][2]==board[1][1]==board[2][0] and board[0][2]!=None:
        winner = board[0][2]
        game_over = True
        return True

    return False

def check_draw():
    global draw, game_over

    for row in board:
        for cell in row:
            if cell is None:
                return False

    if not winner:
        draw = True
        game_over = True

    return draw

def drawXO(row,col):
    x = col*CELL_SIZE + CELL_SIZE//2
    y = row*CELL_SIZE + CELL_SIZE//2

    if turn == 'X':
        offset =30
        pg.draw.line(screen, (255,0,0),
                     (x - offset, y - offset),
                     (x + offset, y + offset), 8)

        pg.draw.line(screen, (255,0,0),
                     (x - offset, y + offset),
                     (x + offset, y - offset), 8)

        
    else:
        rect = o_img.get_rect(cener=(x,y))
        pg.draw.circle(screen,(0,0,255),(x,y),35,8)    
        
        
        

def user_click():
    global turn

    x,y = pg.mouse.get_pos()

    if y < 580:
        row = y // CELL_SIZE
        col = x // CELL_SIZE

        if board[row][col] is None and not game_over:
            board[row][col] = turn
            drawXO(row,col)

            if check_win():
                draw_status()
                return

            if check_draw():
                draw_status()
                return

            turn = 'O' if turn=='X' else 'X'
            draw_status()

def reset_game():
    global board, game_over, turn, winner, draw

    board = [[None,None,None],[None,None,None],[None,None,None]]
    game_over = False
    turn = 'X'
    winner = None
    draw = False

    game_initiating_window()

def main():
    game_initiating_window()

    while True:
        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()

                if new_game_btn.collidepoint(mouse):
                    reset_game()

                elif restart_btn.collidepoint(mouse):
                    reset_game()

                else:
                    user_click()

        pg.display.update()
        time.sleep(0.01)

if __name__ == "__main__":
    main()