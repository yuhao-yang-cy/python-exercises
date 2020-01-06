import simpleguitk as simplegui
import random

COL, ROW = 4, 4
BORDER = 5
TILE_WIDTH, TILE_HEIGHT = 80, 80

CANVAS_WIDTH = COL * (BORDER + TILE_WIDTH) + BORDER
CANVAS_HEIGHT = ROW * (BORDER + TILE_HEIGHT) + BORDER

tile = {}

def merge(data):
    temp = []		# store non-zero values from data
    for item in data:
        if item != 0:
            temp.append(item)
    newdata = []	# store merged data
    i = 0
    while i < len(temp):
        if i == len(temp) - 1:
            newdata.append(temp[i])
            i += 1
        else:
            if temp[i] == temp[i+1]:
                newdata.append(2 * temp[i])
                i += 2
            else:
                newdata.append(temp[i])
                i += 1
    zeros = len(data) - len(newdata)
    newdata.extend([0] * zeros)
    return newdata
	
def x_coord(col):
    return (col+1) * BORDER + (col+0.5) * TILE_WIDTH

def y_coord(row):
    return (row+1) * BORDER + (row+0.5) * TILE_HEIGHT
	
class ErLingSiBa:
    def __init__(self, x, y):
        self.col = x
        self.row = y
        self.reset()
	
    def reset(self):
        for i in range(0, self.col):
            for j in range(0, self.row):
                tile[(i,j)] = [x_coord(i), y_coord(j), 0]
        self.new_tile()
	
    def new_tile(self):
        empty_index = []
        for i in range(0, self.col):
            for j in range(0, self.row):
                if tile[(i,j)][2] == 0:
                    empty_index.append(i + j * ROW)
        if len(empty_index) > 0:
            index = random.choice(empty_index)
            value = random.choice([2, 4])
            tile[index%ROW, index//ROW][2] = value
	
    def move(self, key):
        new = False
        if key==simplegui.KEY_MAP['left'] or key==simplegui.KEY_MAP['right']:
            for j in range(0, self.row):
                temp = []
                for i in range(0, self.col):
                    temp.append(tile[(i,j)][2])
                if key==simplegui.KEY_MAP['left']:
                    merged = merge(temp)
                    if merged != temp:
                        new = True
                elif key==simplegui.KEY_MAP['right']:
                    temp.reverse()
                    merged = merge(temp)
                    if merged != temp:
                        new = True
                    merged.reverse()
                for i in range(0, self.col):
                    tile[(i,j)][2] = merged[i]
        elif key==simplegui.KEY_MAP['up'] or key==simplegui.KEY_MAP['down']:
            for i in range(0, self.col):
                temp = []
                for j in range(0, self.row):
                    temp.append(tile[(i,j)][2])
                if key==simplegui.KEY_MAP['up']:
                    merged = merge(temp)
                    if merged != temp:
                        new = True
                elif key==simplegui.KEY_MAP['down']:
                    temp.reverse()
                    merged = merge(temp)
                    if merged != temp:
                        new = True
                    merged.reverse()
                for j in range(0, self.row):
                    tile[(i,j)][2] = merged[j]
        if new:
            self.new_tile()
	
    def check_dead(self):
        for i in range(0, self.col):
            for j in range(0, self.row):
                if tile[(i,j)][2] == 0:
                    return False
                if i < self.col - 1:
                    if tile[(i,j)][2] == tile[(i+1,j)][2]:
                        return False
                if j < self.row - 1:
                    if tile[(i,j)][2] == tile[(i,j+1)][2]:
                        return False
        return True		

def draw(canvas):
    for i in range(0, COL):
        for j in range(0, ROW):
            canvas.draw_line((tile[(i,j)][0] - TILE_WIDTH // 2, tile[(i,j)][1]),
                             (tile[(i,j)][0] + TILE_WIDTH // 2, tile[(i,j)][1]), TILE_HEIGHT, 'Yellow')
            if tile[(i,j)][2] > 0:
                canvas.draw_text(str(tile[(i,j)][2]), (tile[(i,j)][0] - len(str(tile[(i,j)][2]))*10, tile[(i,j)][1] + 20), 30, 'Blue')
    if game.check_dead():
        canvas.draw_text('Game Over', (CANVAS_WIDTH//2 - 150, CANVAS_HEIGHT//2 + 20), 50, 'Red')

game = ErLingSiBa(COL, ROW)

frame = simplegui.create_frame("2048", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background("White")
frame.add_button("New Game", game.reset, 100)
frame.set_keydown_handler(game.move)
frame.set_draw_handler(draw)

frame.start()
