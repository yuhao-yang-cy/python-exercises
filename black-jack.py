import simpleguitk as simplegui
import random

# define globals
SUITS = ('H', 'D', 'C', 'S')
RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# load card image and define dimensions
card_image = simplegui.load_image('http://ww2.sinaimg.cn/large/578b564fgw1eh4lhgzs43j21950p5qax.jpg')
CARD_SIZE = (125.0, 181.0)
SCALE = 0.6
CARD_DISPLAY_SIZE = (CARD_SIZE[0] * SCALE, CARD_SIZE[1] * SCALE)
CARD_BACK_CENTER = (.5 * CARD_SIZE[0], 4.5 * CARD_SIZE[1])

# coordinate parameters to define start position of messages
MSGX = CARD_DISPLAY_SIZE[0] * 0.6    
MSGY = CARD_DISPLAY_SIZE[1]

class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)
        
    def __str__(self):
        return self.suit + self.rank
        
    def card_name(self):
        if self.suit == 'S':
            return 'Spade ' + self.rank
        elif self.suit == 'H':
            return 'Heart ' + self.rank
        elif self.suit == 'D':
            return 'Diamond ' + self.rank
        elif self.suit == 'C':
            return 'Club ' + self.rank
    
    def draw(self, canvas, canvas_pos):
        i = RANKS.index(self.rank)
        j = SUITS.index(self.suit)
        card_pos = [(i + .5) * CARD_SIZE[0], (j + .5) * CARD_SIZE[1]]
        canvas.draw_image(card_image, card_pos, CARD_SIZE, canvas_pos, CARD_DISPLAY_SIZE)
    
    def draw_back(self, canvas, canvas_pos):
        canvas.draw_image(card_image, CARD_BACK_CENTER, CARD_SIZE, canvas_pos, CARD_DISPLAY_SIZE)

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.bust = False
        
    def __str__(self):
        card_list = ''
        for card in self.cards:
            card_list += card.card_name() + ' '
        return 'Cards in Hand: ' + card_list

    def get_value(self):
        value = 0
        count_ace = 0
        for card in self.cards:
            value += VALUES[card.rank]
            if card.rank == 'A':
                count_ace +=1
        if count_ace == 0 or value > 11:
            return value
        else:
            return value + 10    
            
    def add_card(self, new_card):
        self.cards.append(new_card)
        self.value = self.get_value()
        if self.value > 21:
            self.bust = True
        
class Deck:
    def __init__(self):
        self.cards = []
        self.shuffle()
    
    def __str__(self):
        card_list = ''
        for card in self.cards:
            card_list += card.card_name() + ' '
        return 'Cards on Deck: ' + card_list
    
    def shuffle(self):
        number_list = [x for x in range(0, 52)]
        random.shuffle(number_list)
        while len(number_list) > 0:
            index = number_list.pop()
            self.cards.append(Card(SUITS[index // 13], RANKS[index % 13]))
        
    def pick_card(self):
        return self.cards.pop()

def new_round():
    global player, dealer, in_play
    player = Hand()
    dealer = Hand()
    in_play = True
    board.shuffle()
    
    player.add_card(board.pick_card())
    player.add_card(board.pick_card())
    dealer.add_card(board.pick_card())
    dealer.add_card(board.pick_card())
    
def hit():
    global score
    if in_play:
        player.add_card(board.pick_card())
    if player.bust:
        score += -1

def stand():
    global in_play, score
    if in_play:
        in_play = False
        while dealer.value < 17:
            dealer.add_card(board.pick_card())
    if dealer.bust or player.value > dealer.value:
        score += 1
    elif player.value < dealer.value and not dealer.bust:
        score += -1

def draw(canvas):
    global in_play
    canvas.draw_text('Score: ' + str(score), (MSGX * 8, MSGY * 0.5), 20, 'Black')
    canvas.draw_text('Player: ' + str(player.value), (MSGX, MSGY * 2.1), 20, 'Black')
    
    # draw dealer's cards
    for card in dealer.cards:
        x_coord = (dealer.cards.index(card) + 1 )* CARD_DISPLAY_SIZE[0]
        if in_play:
            if dealer.cards.index(card) == 0:
                card.draw_back(canvas, (x_coord, MSGY * 1.2))
            else:
                card.draw(canvas, (x_coord, MSGY * 1.2))
            canvas.draw_text('Dealer: ?', (MSGX, MSGY * 0.5), 20, 'Black')
        else:
            card.draw(canvas, (x_coord, MSGY * 1.2))
            canvas.draw_text('Dealer: ' + str(dealer.value), (MSGX, MSGY * 0.5), 20, 'Black')
            
    # draw player's cards
    for card in player.cards:
        x_coord = (player.cards.index(card) + 1 )* CARD_DISPLAY_SIZE[0]
        card.draw(canvas, (x_coord, MSGY * 2.8))
    
    # find winner
    if player.bust:
        in_play = False
        canvas.draw_text('You go bust! You lose!', (MSGX, MSGY * 3.7), 20, 'Black')
    elif dealer.bust:
        in_play = False
        canvas.draw_text('Dealer goes bust! You win!', (MSGX, MSGY * 3.7), 20, 'Black')
    elif in_play == False:
        if player.value > dealer.value:
            canvas.draw_text('You win!', (MSGX, MSGY * 3.7), 20, 'Black')
        elif player.value < dealer.value:
            canvas.draw_text('You lose!', (MSGX, MSGY * 3.7), 20, 'Black')
        else:
            canvas.draw_text('Tie!', (MSGX, MSGY * 3.7), 20, 'Black')

score = 0
board = Deck()
new_round()
    
frame = simplegui.create_frame('Black Jack', CARD_DISPLAY_SIZE[0] * 7, CARD_DISPLAY_SIZE[1] * 4)
frame.set_canvas_background('White')
frame.set_draw_handler(draw)
frame.add_button('Deal', new_round, 80)
frame.add_button('Hit', hit, 80)
frame.add_button('Stand', stand, 80)
frame.start()
