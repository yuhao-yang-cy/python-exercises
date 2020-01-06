# memory game - finding matching card pairs
# use dictionary cards[(x,y)] to index card information, each entry contains 6 pieces of information
# cards[(x,y)][-1] card state: 0-not flipped, 1-flipped, 2-match found
# cards[(x,y)][0] x-label of card
# cards[(x,y)][1] y-label of card
# cards[(x,y)][2] value of card
# cards[(x,y)][3] rectangle colour: blue, red, Gray
# cards[(x,y)][4] text colour: blue, white, white
			
import simpleguitk as simplegui
import random

GRID_SIZEX, GRID_SIZEY = 4, 4
CARD_NUMBER = GRID_SIZEX * GRID_SIZEY
BORDER = 10
CARD_WIDTH, CARD_HEIGHT = 100, 120
HALF_CARD_WIDTH = CARD_WIDTH // 2
HALF_CARD_HEIGHT = CARD_HEIGHT // 2

CANVAS_WIDTH = GRID_SIZEX * (BORDER + CARD_WIDTH) + BORDER
CANVAS_HEIGHT = GRID_SIZEY * (BORDER + CARD_HEIGHT) + BORDER

cards = {}

# helper functions
def x_coord(card_x_label):
    return (card_x_label+1) * BORDER + card_x_label * CARD_WIDTH + HALF_CARD_WIDTH

def y_coord(card_y_label):
    return (card_y_label+1) * BORDER + card_y_label * CARD_HEIGHT + HALF_CARD_HEIGHT

def trial_inc():
    global trial
    trial += 1
    label.set_text("Trials Attempted: " + str(trial))
	
# Event Handlers
def new_game():
    global trial, matched
    trial, matched = 0, 0
    number_list = list(range(1, CARD_NUMBER//2 + 1)) * 2
    random.shuffle(number_list)
    for x in range(0, GRID_SIZEX):
        for y in range(0, GRID_SIZEY):
            cards[(x,y)] = [x_coord(x), y_coord(y), number_list.pop(), 'Blue', 'Blue', 0]
    cards[(99,99)] = [-1]*6

def dummy_init():
    global compare, temp, flipped, match_fail
    compare, temp = (99,99), (99,99)
    flipped, match_fail = False, False
	
def click(pos):
    global compare, flipped, match_fail, temp, matched
    if match_fail:
        cards[compare][3:6] = 'Blue', 'Blue', 0
        cards[temp][3:6] = 'Blue', 'Blue', 0
        dummy_init()
    else:
        for x in range(0, GRID_SIZEX):
            for y in range(0, GRID_SIZEY):
                if abs(x_coord(x) - pos[0]) < HALF_CARD_WIDTH and abs(y_coord(y) - pos[1]) < HALF_CARD_HEIGHT:
                    if cards[(x,y)][-1] == 0 and flipped:
                        if cards[(x,y)][2] == cards[compare][2]:
                            cards[(x,y)][3:6] = 'Gray', 'White', 2
                            cards[compare][3:6] = 'Gray', 'White', 2
                            matched += 1
                            dummy_init()
                        else:
                            cards[(x,y)][3:6] = 'Red', 'White', 1
                            temp, match_fail = (x,y), True
                    elif cards[(x,y)][-1] == 0 and not flipped:
                            compare, flipped = (x,y), True
                            cards[(x,y)][3:6] = 'Red', 'White', 1
                            trial_inc()						

def draw(canvas):
    for x in range(0, GRID_SIZEX):
        for y in range(0, GRID_SIZEY):
            canvas.draw_line((cards[(x,y)][0] - HALF_CARD_WIDTH, cards[(x,y)][1]), (cards[(x,y)][0] + HALF_CARD_WIDTH, cards[(x,y)][1]), CARD_HEIGHT, cards[(x,y)][3])
            if cards[(x,y)][2] < 10:
                canvas.draw_text(str(cards[(x,y)][2]), (cards[(x,y)][0] - 16, cards[(x,y)][1] + 32), 50, cards[(x,y)][4])
            else:
                canvas.draw_text(str(cards[(x,y)][2]), (cards[(x,y)][0] - 36, cards[(x,y)][1] + 32), 50, cards[(x,y)][4])
    if matched * 2 == CARD_NUMBER:
        canvas.draw_text('Win!', (CANVAS_WIDTH//2 - 100, CANVAS_HEIGHT//2 + 40), 80, 'Red')

# main frame
frame = simplegui.create_frame("Memory Game", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background("White")
frame.add_button("New Game", new_game, 100)
label = frame.add_label('')
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
dummy_init()
new_game()

frame.start()
