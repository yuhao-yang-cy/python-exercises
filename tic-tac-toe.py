import simpleguitk as simplegui
import random

DIM = 3
GSIZE = 80

board_lines = []
# draw game board
for i in range(1, DIM):
    board_lines.append([(0, i * GSIZE), (DIM * GSIZE, i * GSIZE)])
for j in range(1, DIM):
    board_lines.append([(j * GSIZE, 0), (j * GSIZE, DIM * GSIZE)])

class TTTBoard:
    # class to represent a tic-tac-toe board.
    # empty = 0, player = 1(O), computer = 2(X)
    # True = player's turn, False = computer's turn

    def __init__(self, dim, turn = True, stones = None):
        self.dim = dim
        self.turn = turn
        if stones == None:
            self.stones = [0] * self.dim ** 2
        else:
            self.stones = stones

    def __str__(self):
        type_stone = []
        for j in range(self.dim):
            type_stone.append(self.stones[j:j+DIM])
        return str(type_stone)

    def get_empty_squares(self):
        empty_squares = []
        for index in range(self.dim ** 2):
            if self.stones[index] == 0:
                empty_squares.append(index)
        return empty_squares

    def move(self, index, player):
        if self.stones[index] == 0:
            if self.check_win() not in [0, 1, 2]:
                self.stones[index] = player

    def check_win(self):
        # check horizontal and vertical
        for i in range(self.dim):
            for j in range(self.dim-2):
                if self.stones[i + j*self.dim] != 0:
                    if self.stones[i + j*self.dim] == self.stones[i + (j+1)*self.dim] \
                       and self.stones[i + j*self.dim] == self.stones[i + (j+2)*self.dim]:
                        return self.stones[i + j*self.dim]
                if self.stones[j + i*self.dim] != 0:
                    if self.stones[j + i*self.dim] == self.stones[j + 1 + i*self.dim] \
                       and self.stones[j + i*self.dim] == self.stones[j + 2 + i*self.dim]:
                        return self.stones[j + i*self.dim]
        # check diagonal
        for i in range(self.dim-2):
            for j in range(self.dim-2):
                if self.stones[i + j*self.dim] != 0:
                    if self.stones[i + j*self.dim] == self.stones[i+1 + (j+1)*self.dim] \
                       and self.stones[i + j*self.dim] == self.stones[i+2 + (j+2)*self.dim]:
                        return self.stones[i + j*self.dim]
            for j in range(2, self.dim):
                if self.stones[i + j*self.dim] != 0:
                    if self.stones[i + j*self.dim] == self.stones[i+1 + (j-1)*self.dim] \
                       and self.stones[i + j*self.dim] == self.stones[i+2 + (j-2)*self.dim]:
                        return self.stones[i + j*self.dim]
        # check if game tied
        if len(self.get_empty_squares()) == 0:
            return 0
        
    def clone(self):
        return TTTBoard(int(self.dim), bool(self.turn), list(self.stones))

def mc_trial(board, empty_squares):
    # make a copy of board, run a random game
    # when game is over, simulated board is evaluated
    fboard = board.clone()
    slots = list(empty_squares)
    random.shuffle(slots)
    while len(slots) > 0 and fboard.check_win() not in [0, 1, 2]:
        move = slots.pop()
        if fboard.turn == True:
            fboard.move(move, 2)
            if fboard.check_win() == 2:
                mc_update_scores(fboard, empty_squares, len(slots)+1, 2)
        else:
            fboard.move(move, 1)
            if fboard.check_win() == 1:
                mc_update_scores(fboard, empty_squares, len(slots)+1, 1)
        fboard.turn = not fboard.turn    

def mc_update_scores(board, empty_squares, weight, winner):
    # evaluate multiple possible outcomes
    # if game won, attribute positive values to square, negative otherwise
    # quicker win/loss earns/loses more credits
    global scores
    for index in empty_squares:
        if winner == 2:
            if board.stones[index] == 2:
                scores[index] += 2 * weight
            elif board.stones[index] == 1:
                scores[index] += - weight
        if winner == 1:
            if board.stones[index] == 2:
                scores[index] += - weight
            elif board.stones[index] == 1:
                scores[index] += 2 * weight

def mc_bestmove(board, ntrials):
    # run large number of random games to find best move for AI
    empty_squares = board.get_empty_squares()
    for counter in range(ntrials):
        mc_trial(board, empty_squares)
    best = max(scores)
    best_moves = []
    for index in empty_squares:
        if scores[index] == best:
            best_moves.append(index)
    return random.choice(best_moves)

def draw(canvas):
    for line in board_lines:
        canvas.draw_line(line[0], line[1], 5, 'Black')
    for index in range(ttt.dim ** 2):
        if ttt.stones[index] == 1:
            canvas.draw_circle(((index % DIM + 0.5) * GSIZE, (index // DIM + 0.5)* GSIZE),
                               (GSIZE-20)//2, 5, 'Black')
        if ttt.stones[index] == 2:
            canvas.draw_line(((index % DIM + 0.5) * GSIZE - (GSIZE-20)//2,
                              (index // DIM + 0.5) * GSIZE + (GSIZE-20)//2),
                             ((index % DIM + 0.5) * GSIZE + (GSIZE-20)//2,
                              (index // DIM + 0.5) * GSIZE - (GSIZE-20)//2), 5, 'Black')
            canvas.draw_line(((index % DIM + 0.5) * GSIZE - (GSIZE-20)//2,
                              (index // DIM + 0.5) * GSIZE - (GSIZE-20)//2),
                             ((index % DIM + 0.5) * GSIZE + (GSIZE-20)//2,
                              (index // DIM + 0.5) * GSIZE + (GSIZE-20)//2), 5, 'Black')

def click(pos):
    global scores
    empty_squares = ttt.get_empty_squares()
    x = int(pos[0] / GSIZE)
    y = int(pos[1] / GSIZE)
    player_move = x + y * DIM
    if player_move in empty_squares:
        ttt.move(player_move, 1)
        empty_squares.remove(player_move)
        scores = [0] * ttt.dim ** 2
        if len(empty_squares) > 0:
            computer_move = mc_bestmove(ttt, 20 * len(empty_squares))
            ttt.move(computer_move, 2)
    if ttt.check_win() == 0:
        label.set_text('Game Tied!')
    elif ttt.check_win() == 1:
        label.set_text('Player Wins!')
    elif ttt.check_win() == 2:
        label.set_text('Computer Wins!')

def new_game():
    global ttt
    label.set_text('')
    ttt = TTTBoard(DIM, True)

frame = simplegui.create_frame("Tic-Tac-Toe", DIM * GSIZE, DIM * GSIZE)
frame.set_canvas_background('White')
frame.set_draw_handler(draw)
frame.add_button("New Game", new_game, 100)
label = frame.add_label('')
frame.set_mouseclick_handler(click)

new_game()
frame.start()
