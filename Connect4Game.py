import numpy as np
import math
import random
import pygame
import sys
import time

YELLOW = (254, 245, 231)
purple=(195, 155, 211)
white=(23, 32, 42)
blue=(174, 214, 241)
white2=(255,255,255)


# Main board class
class Connect4_board:
    def __init__(self, rowCount=6, columnCount=7, player1=1, player2=2):
        self.rowCount = rowCount
        self.columnCount = columnCount
        self.player1 = player1
        self.player2 = player2
        self.frame = 60
        self.width = self.columnCount * self.frame
        self.height = (self.rowCount + 1) * self.frame
        self.size = (self.width, self.height)
        self.rad = int(self.frame / 2 - 3)
        self.screen = pygame.display.set_mode((420,520))
    # Creating the initialization state of board
    def createBoard(self):
        board = np.zeros((self.rowCount, self.columnCount))
        return board

    # Dropping the disk into the specified row and column
    def dropDisk(self, board, row, column, disk):
        board[row][column] = disk

    # Checking if tile fits in column or not
    def isValidLocation(self, board, column):
        return board[self.rowCount - 1][column] == 0

    # Checking if board is in winning state or not

    def winningMove(self, board, disk):

        # Check horizantaly
        for column in range(self.columnCount - 3):
            for row in range(self.rowCount):
                if board[row][column] == disk and board[row][column + 1] == disk and board[row][column + 2] == disk and \
                        board[row][column + 3] == disk:
                    return True

        # Check verticaly
        for column in range(self.columnCount):
            for row in range(self.rowCount - 3):
                if board[row][column] == disk and board[row + 1][column] == disk and board[row + 2][column] == disk and \
                        board[row + 3][column] == disk:
                    return True

        # Check diagonally(positive)
        for column in range(self.columnCount - 3):
            for row in range(self.rowCount - 3):
                if board[row][column] == disk and board[row + 1][column + 1] == disk and board[row + 2][
                    column + 2] == disk and board[row + 3][column + 3] == disk:
                    return True

        # Check diagonally(negative)
        for column in range(self.columnCount - 3):
            for row in range(3, self.rowCount):
                if board[row][column] == disk and board[row - 1][column + 1] == disk and board[row - 2][
                    column + 2] == disk and board[row - 3][column + 3] == disk:
                    return True

    # Get the empty row in this specific column
    def getNextAvailableRow(self, board, column):
        for row in range(self.rowCount):
            if board[row][column] == 0:
                return row

    def available_tiles(self, board):
        all_available_tiles = []
        for each_column in range(self.columnCount):
            if self.isValidLocation(board, each_column):
                all_available_tiles.append(each_column)
        return all_available_tiles

    def end_node(self, board):  ##checking if the node we have is at the end of the tree or not
        return self.winningMove(board, self.player1) or self.winningMove(board, self.player2) or len(
            self.available_tiles(board)) == 0

    def minimax(self, board, depth, max_player, heu):
        available_tiles = self.available_tiles(board)
        is_end = self.end_node(board)

        ##The base cases for iterative minimax
        if depth == 0 or is_end:
            if is_end:
                if self.winningMove(board, self.player2):
                    return (None, math.inf)
                elif self.winningMove(board, self.player1):
                    return (None, -math.inf)
                else:
                    return (None, 0)
            else:
                if heu==1:
                    return (None, self.scoring_heuristic_1(board, self.player2))
                elif heu==2:
                    return (None, self.scoring_heuristic_2(board, self.player2))
                elif heu==3:
                    return (None, self.scoring_heuristic_3(board,5, self.player2))

        if max_player:
            value = -math.inf
            column = random.choice(available_tiles)
            for col in available_tiles:
                row = self.getNextAvailableRow(board, col)
                b_copy = board.copy()
                self.dropDisk(b_copy, row, col, self.player2)
                c, new_score = self.minimax(b_copy, depth - 1, False,heu)  # false to change from max_player to min_player
                if new_score > value:
                    value = new_score
                    column = col
                return column, value


        else:
            value = math.inf
            column = random.choice(available_tiles)
            for col in available_tiles:
                row = self.getNextAvailableRow(board, col)
                b_copy = board.copy()
                self.dropDisk(b_copy, row, col, self.player1)
                c, new_score = self.minimax(b_copy, depth - 1, False,heu)  # false to change from max_player to min_player
                if new_score < value:
                    value = new_score
                    column = col
                return column, value

    def scoring_heuristic_1(self, board, turn):
        ###Heuristic one searches for 4 executives tiles horizontaly, verticaly, positive_diagonaly and negative_diagonally
        ##and scores upon how many tiles each 4-executives have!

        score = 0  # Starting with score =0

        ## Scoring with Horizontal
        for r in range(self.rowCount):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.columnCount - 3):
                sub_row = row_array[c:c + 4]
                if sub_row.count(turn) == 4:  # if a subrow is filled horizontally in 4 same number(winning)
                    score += 10
                elif sub_row.count(turn) == 3 and sub_row.count(0) == 1:
                    score += 8
                elif sub_row.count(turn) == 2 and sub_row.count(0) == 2:
                    score += 5

        for col in range(self.columnCount):
            column_array = [int(i) for i in list(board[:, col])]
            for r in range(self.rowCount - 3):
                sub_col = column_array[r:r + 4]
                if sub_col.count(turn) == 4:  # if a subrow is filled vertically in 4 same number(winning)
                    score += 10
                elif sub_col.count(turn) == 3 and sub_col.count(0) == 1:
                    score += 8
                elif sub_col.count(turn) == 2 and sub_col.count(0) == 2:
                    score += 5

        for r in range(self.rowCount - 3):
            for c in range(self.columnCount - 3):
                sub_diagonal = [board[r + i][c + i] for i in range(4)]
                if sub_diagonal.count(turn) == 4:
                    score += 10
                elif sub_diagonal.count(turn) == 3 and sub_diagonal.count(0) == 1:
                    score += 8
                elif sub_diagonal.count(turn) == 2 and sub_diagonal.count(0) == 2:
                    score += 5

        for r in range(self.rowCount - 3):
            for c in range(self.columnCount - 3):
                sub_diagonal = [board[r + i][c - i] for i in range(4)]
                if sub_diagonal.count(turn) == 4:
                    score += 10
                elif sub_diagonal.count(turn) == 3 and sub_diagonal.count(0) == 1:
                    score += 8
                elif sub_diagonal.count(turn) == 2 and sub_diagonal.count(0) == 2:
                    score += 5
        return score

    def scoring_heuristic_2(self, board, turn):  ##keeping the ai in center
        if turn == self.player2:
            other_turn = self.player1
        else:
            other_turn = self.player2
        score = 0
        for r in range(self.rowCount):
            row_array = [int(i) for i in list(board[r, :])]
            indexes = [0, -1]
            row_array_sides = [row_array[x] for x in indexes]
            row_array_center = row_array[1:6]
            if row_array_center.count(turn) >= 2:
                score += 10
            elif row_array_center.count(other_turn) >= 2:
                score -= 10
            elif row_array_sides.count(turn) >= 1:
                score -= 10
            elif row_array_sides.count(other_turn) >= 1:
                score += 10

        for c in range(self.columnCount):
            column_array = [int(i) for i in list(board[:, c])]
            indexes = [0, -1]
            column_array_sides = [column_array[x] for x in indexes]
            column_array_center = column_array[1:5]
            if column_array_center.count(turn) >= 2:
                score += 10
            elif column_array_center.count(other_turn) >= 2:
                score -= 10
            elif column_array_sides.count(turn) >= 1:
                score -= 10
            elif column_array_sides.count(other_turn) >= 1:
                score += 10
        return score

    def scoring_heuristic_3(self, board, depth, turn):
        # If leaf is a win: positive score resulting from 22 - number of moves played
        # If leaf is a loss: negative score resulting from 22 - number of moves played by opponent
        # If leaf is a draw: score is 0
        if turn == self.player2:
            other_turn = self.player1
        else:
            other_turn = self.player2
        score = 0
        if self.winningMove(board, turn):
            score = 21 - (depth / 2)
        elif self.winningMove(board, other_turn):
            score = -1 * (21 - (depth / 2))
        elif len(self.available_tiles(board)) == 0:  ##moves finished
            score = 0
        elif depth % 2 == 0:
            # MAX node returns
            score = math.inf
        else:
            # MIN node returns
            score = -math.inf
        return score
    def draw_board(self,board):
        for c in range(self.columnCount):
            for r in range(self.rowCount):
                pygame.draw.rect(self.screen, purple, (c * self.frame, r * self.frame + self.frame, self.frame, self.frame))
                pygame.draw.circle(self.screen, white, (
                    int(c * self.frame + self.frame / 2), int(r * self.frame + self.frame + self.frame / 2)), self.rad)

        for c in range(self.columnCount):
            for r in range(self.rowCount):
                if board[r][c] == 1:
                    pygame.draw.circle(self.screen, blue, (
                        int(c * self.frame + self.frame / 2), self.height - int(r * self.frame + self.frame / 2)), self.rad)
                elif board[r][c] == 2:
                    pygame.draw.circle(self.screen, YELLOW, (
                        int(c * self.frame + self.frame / 2), self.height - int(r * self.frame + self.frame / 2)), self.rad)
        pygame.display.update()


#PLAYING HUMAN VS. HUMAN
class HumantoHuman(Connect4_board):
    def playgame(self):
        pygame.init()
        pygame.display.update()

        myfont = pygame.font.SysFont("bold", 25)
        myfont2 = pygame.font.SysFont("bold", 30)
        label = myfont2.render("Human VS. Human", 1, white2)
        self.screen.blit(label, (10, 430))

        turn = self.player1
        gameOver = False

        while not gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, white, (0,0, game.width, game.frame))
                    posx = event.pos[0]

                    if turn == 0:
                        pygame.draw.circle(self.screen, blue, (posx, int(game.
                                                                        frame/2)), game.rad)
                    else:
                        pygame.draw.circle(self.screen, YELLOW, (posx, int(game.
                                                                           frame/2)), game.rad)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, white, (0,0, game.width, game.frame))
                    if turn == 0:
                        posx = event.pos[0]
                        col = int(math.floor(posx/game.frame))

                        if game.isValidLocation(board, col):
                            row = game.getNextAvailableRow(board, col)
                            game.dropDisk(board, row, col, 1)

                            if game.winningMove(board, 1):
                                label = myfont.render("!!!! Nice job PLAYER 1 ,you WON !!!!", True, white2)
                                self.screen.blit(label, (10, 450))
                                gameOver = True

                    # # Ask for Player 2 Input
                    else:
                        posx = event.pos[0]
                        col = int(math.floor(posx/game.frame))

                        if game.isValidLocation(board, col):
                            row = game.getNextAvailableRow(board, col)
                            game.dropDisk(board, row, col, 2)
                            if game.winningMove(board, 2):
                                label = myfont.render("!!!! Nice job PLAYER 2 ,you WON !!!!", True, white2)
                                self.screen.blit(label, (10, 450))
                                gameOver = True

                    game.draw_board(board)

                    turn += 1
                    turn = turn % 2

        if gameOver:
            pygame.time.wait(4000)

class AItoAI(Connect4_board):

    def playgame(self):
        pygame.init()

        AI_1 = 0
        AI_2 = 1

        pygame.display.update()

        myfont = pygame.font.SysFont("bold", 25)
        myfont2 = pygame.font.SysFont("bold", 30)


        label = myfont2.render("Computer 1 (h1) vs Computer 2 (h3)", 1, white2)
        self.screen.blit(label, (10,20))
        turn = random.randint(self.player1, self.player2)
        gameOver = False
        times_for_ai1=[]
        times_for_ai2=[]
        max_turns=21
        while not gameOver:
            if max_turns>0:
                # # Ask for Player 2 Input
                if turn == AI_1 and not gameOver:
                    start= time.time()
                    col, minimax_score = self.minimax(board, 5, self.player1,1)
                    end= time.time()
                    times_for_ai1.append(end-start)
                    if self.isValidLocation(board, col):
                        pygame.time.wait(500)
                        row = self.getNextAvailableRow(board, col)
                        self.dropDisk(board, row, col, self.player1)

                        if self.winningMove(board, self.player1):
                            label = myfont.render("!!!! Nice job COMPUTER 1 ,you WON !!!!", True, white2)
                            self.screen.blit(label, (10, 430))

                            label2 = myfont.render("The maximum depth:", 1, white2)
                            self.screen.blit(label2, (10, 450))
                            label3 = myfont.render("5", 1, white2)
                            self.screen.blit(label3, (200, 450))
                            label5 = myfont.render("The maximum time for best move:", 1, white2)
                            self.screen.blit(label5, (10, 470))
                            time_taken = max(times_for_ai1)
                            label4 = myfont.render(str(time_taken), 1, white2)
                            self.screen.blit(label4, (10, 500))
                            gameOver = True
                        self.draw_board(board)
                        turn += 1
                        turn = turn % 2
                else:
                    start= time.time()
                    col, minimax_score = self.minimax(board, 5, self.player2,3)
                    end= time.time()

                    times_for_ai2.append(end-start)

                    if self.isValidLocation(board, col):
                        pygame.time.wait(500)
                        row = self.getNextAvailableRow(board, col)
                        self.dropDisk(board, row, col, self.player2)

                        if self.winningMove(board, self.player2):
                            label = myfont.render("!!!! Nice job COMPUTER 2 ,you WON !!!!", True, white2)
                            self.screen.blit(label, (10, 430))
                            label2 = myfont.render("The maximum depth:", 1, white2)
                            self.screen.blit(label2, (10, 450))
                            label3 = myfont.render("5", 1, white2)
                            self.screen.blit(label3, (200, 450))
                            label5 = myfont.render("The maximum time for best move:", 1, white2)

                            self.screen.blit(label5, (10, 470))
                            time_taken = max(times_for_ai2)

                            label4 = myfont.render(str(time_taken), 1, white2)
                            self.screen.blit(label4, (10, 500))
                            gameOver = True
                        self.draw_board(board)
                        turn += 1
                        turn = turn % 2
                        max_turns-=1
        if gameOver:
            pygame.time.wait(10000)


# PLAYING HUMAN VS AI
class HumantoAI(Connect4_board):

    def playgame(self):
        pygame.init()
        PLAYER = 0
        AI = 1
        times_for_ai = []
        pygame.display.update()
        myfont = pygame.font.SysFont("bold", 25)
        myfont2 = pygame.font.SysFont("bold", 30)
        label = myfont2.render("Human vs Computer(heuristic 3)", 1, white2)
        self.screen.blit(label, (0, 430))
        turn = 1
        gameOver = False

        while not gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, white, (0, 0, self.width, self.frame))
                    posx = event.pos[0]

                    if turn == PLAYER:
                        pygame.draw.circle(self.screen, blue, (posx, int(self.frame / 2)), self.rad)

                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen,
                    white, (0, 0, self.width, self.frame))
                    if turn == PLAYER:
                        posx = event.pos[0]
                        col = int(math.floor(posx / self.
                                             frame))

                        if self.isValidLocation(board, col):
                            row = self.getNextAvailableRow(board, col)
                            self.dropDisk(board, row, col, self.player1)

                            if self.winningMove(board, self.player1):
                                label = myfont.render("!!!! Nice job, Player 1 WON !!!!", True, white2)
                                self.screen.blit(label, (10, 450))
                                gameOver = True

                            turn += 1
                            turn = turn % 2
                            self.draw_board(board)

            if turn == AI and not gameOver:
                start=time.time()
                col, minimax_score = self.minimax(board, 5, self.player2,3)
                end=time.time()
                times_for_ai.append(end-start)
                if self.isValidLocation(board, col):
                    pygame.time.wait(500)
                    row = self.getNextAvailableRow(board, col)
                    self.dropDisk(board, row, col, self.player2)
                    if self.winningMove(board, self.player2):
                        label = myfont.render("!!!! Nice job, COMPUTER WON !!!!", True, white2)
                        self.screen.blit(label, (10, 460))
                        label2 = myfont.render("The maximum depth:", 1, white2)
                        self.screen.blit(label2, (10, 480))
                        label3 = myfont.render("5", 1, white2)
                        self.screen.blit(label3, (200, 480))
                        label5 = myfont.render("The maximum time for best move:", 1, white2)
                        self.screen.blit(label5, (10, 500))
                        time_taken = max(times_for_ai)
                        label4 = myfont.render(str(time_taken), 1, white2)
                        self.screen.blit(label4, (300, 500))
                        gameOver = True
                    self.draw_board(board)
                    turn += 1
                    turn = turn % 2

        if gameOver:
            pygame.time.wait(4000)

if __name__ == '__main__':
    game = HumantoAI()
    board = game.createBoard()
    play = game.playgame()