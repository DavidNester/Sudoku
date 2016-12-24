import pygame, sys
from pygame import constants as c
from sudokuBoard import Board
import copy

class Tile(object):
    def __init__(self, image, x1, y1, x2, y2, step=5):
        self.image = image
        # if x1 > x2:
        #     xstep = -1
        # ...
        self.x = x1
        self.y = y1
        self.x2 = x2
        self.y2 = y2
        self.step = step
    def blit(self, screen):
        screen.blit(self.image, (self.x, self.y))


def main():
    board = Board([[0,3,0,9,0,0,0,2,0],[8,0,0,0,0,2,0,0,7],[0,0,1,4,0,0,6,0,0],[0,9,0,0,4,0,5,0,2],[0,0,0,6,0,3,0,0,0],[7,0,6,0,1,0,0,8,0],[0,0,9,0,0,4,1,0,0],[2,0,0,8,0,0,0,0,3],[0,7,0,0,0,9,0,5,0]])
    screen = pygame.display.set_mode((1000, 675))
    pygame.font.init()
    myfont = pygame.font.SysFont("Comic Sans MS", 30)
    clock = pygame.time.Clock()
    tiles = list()
    tile_images = {}
    
    reaction = None
    
    move = None
    
    selected = (0,0)
    
    squareSize = 75
    
    done = False
    
    for number in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
        filename = 'static/{}.jpeg'.format(number)
        image = pygame.image.load(filename)
        image = image.convert_alpha()
        image = pygame.transform.smoothscale(image, (squareSize-5, squareSize-5))
        tile_images[number] = image
        
    screen.fill((255, 255, 255))
    check = False
    while True:
        old_board = copy.deepcopy(board)
        
        for event in pygame.event.get():
            if event.type == c.KEYDOWN:
                if event.key == c.K_ESCAPE:
                    sys.exit(0)

                # NEW:
                elif event.key == c.K_RIGHT:
                    if selected[0] < 8:
                        selected = (selected[0]+1,selected[1])
                elif event.key == c.K_LEFT:
                    if selected[0] > 0:
                        selected = (selected[0]-1,selected[1])
                elif event.key == c.K_UP:
                    if selected[1] > 0:
                        selected = (selected[0],selected[1]-1)
                elif event.key == c.K_DOWN:
                    if selected[1] < 8:
                        selected = (selected[0],selected[1]+1)
                
                elif event.key == c.K_r:
                    board = Board([[0,3,0,9,0,0,0,2,0],[8,0,0,0,0,2,0,0,7],[0,0,1,4,0,0,6,0,0],[0,9,0,0,4,0,5,0,2],[0,0,0,6,0,3,0,0,0],[7,0,6,0,1,0,0,8,0],[0,0,9,0,0,4,1,0,0],[2,0,0,8,0,0,0,0,3],[0,7,0,0,0,9,0,5,0]])
                
                elif event.key == c.K_1:
                    board.add(selected[1],selected[0],1)
                    check = True
                elif event.key == c.K_2:
                    board.add(selected[1],selected[0],2)
                    check = True
                elif event.key == c.K_3:
                    board.add(selected[1],selected[0],3)
                    check = True
                elif event.key == c.K_4:
                    board.add(selected[1],selected[0],4)
                    check = True
                elif event.key == c.K_5:
                    board.add(selected[1],selected[0],5)
                    check = True
                elif event.key == c.K_6:
                    board.add(selected[1],selected[0],6)
                    check = True
                elif event.key == c.K_7:
                    board.add(selected[1],selected[0],7)
                    check = True
                elif event.key == c.K_8:
                    board.add(selected[1],selected[0],8)
                    check = True
                elif event.key == c.K_9:
                    board.add(selected[1],selected[0],9)
                    check = True
                    
                elif event.key == c.K_DELETE or event.key == c.K_BACKSPACE:
                    board.add(selected[1],selected[0],0)
                    
                if check:
                    if not board.check(selected[1],selected[0]):
                        board.add(selected[1],selected[0],0)
                        reaction = "No"
                    check = False

        screen.fill((255, 255, 255))
        
        #draws squares on screen
        for a in range(9):
            for b in range(9):
                e = squareSize * a
                f = squareSize * b
                pygame.draw.rect(screen, (0,0,0), (e,f,squareSize,squareSize), 1)
        for a in range(3):
            for b in range(3):
                e = squareSize * a * 3
                f = squareSize * b * 3
                pygame.draw.rect(screen, (0,0,0), (e,f,squareSize*3,squareSize*3), 3)
               
        rows = board.rows()
        #inserts numbers
        for i in range(9):
            j = 0
            for number in rows[i]:
                x = squareSize * j + 2
                y = squareSize * i + 2
                j += 1
                number = '%s' % number
                screen.blit(tile_images[number], (x, y))
                
        pygame.draw.rect(screen, (255,0,0), (squareSize*selected[0],squareSize*selected[1],squareSize,squareSize), 3)
        
        if reaction:
            screen.blit(myfont.render(reaction, 4, (255,0,0)),(squareSize*10,squareSize))
        
        if not done and board.isFull():
            board.printBoard()
            print board.rows()
            if board.check():
                done = True
        if done:
            screen.blit(myfont.render("Success", 4, (0,255,0)),(squareSize*10,squareSize))
        move = None
        reaction = None
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
