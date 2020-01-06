import simpleguitk as simplegui
import random
# define globals
WIDTH = 800
HEIGHT = 600
BALL_RADIUS = 10.0
PAD_WIDTH = 8.0
PAD_HEIGHT = 250.0
HALF_PAD_WIDTH = PAD_WIDTH/2.0
HALF_PAD_HEIGHT = PAD_HEIGHT/2.0
PAD_VEL = 12.0
BALL_VEL_INC = 1.1
LEFT_BOUND = 0
# define parameters
left_paddle, right_paddle = HEIGHT/2.0, HEIGHT/2.0
score1, score2 = 0, 0
ball_pos = [(WIDTH + LEFT_BOUND)/2.0, HEIGHT/2.0]
ball_vel = [0.0, 0.0]
score_winner = True

# helper functions
def auto_serve():
	ball_pos[0] = (WIDTH + LEFT_BOUND)/2.0
	ball_pos[1] = HEIGHT/2.0
	ball_vel[0] = random.random() * 5 + 2
	ball_vel[1] = (random.random() * 5 + 2) * random.choice([-1, 1])
	if not score_winner:
		ball_vel[0] = -ball_vel[0]

def hit_paddle():
	ball_vel[0] *= -BALL_VEL_INC
	ball_vel[1] *= BALL_VEL_INC

# event handlers
def start_game():
	global left_paddle, right_paddle, score1, score2
	left_paddle, right_paddle = HEIGHT/2.0, HEIGHT/2.0
	score1, score2 = 0, 0
	auto_serve()

def draw(canvas):
	global score1, score2, score_winner
	ball_pos[0] += ball_vel[0]
	ball_pos[1] += ball_vel[1]
	if ball_pos[0] <= PAD_WIDTH + LEFT_BOUND + BALL_RADIUS:
		if ball_pos[1] > left_paddle + HALF_PAD_HEIGHT or ball_pos[1] < left_paddle - HALF_PAD_HEIGHT:
			score2 += 1
			score_winner = True
			auto_serve()
		else:
			hit_paddle()
	if ball_pos[0] >= WIDTH - 1 - PAD_WIDTH - BALL_RADIUS:
		if ball_pos[1] > right_paddle + HALF_PAD_HEIGHT or ball_pos[1] < right_paddle - HALF_PAD_HEIGHT:
			score1 += 1
			score_winner = False
			auto_serve()
		else:
			hit_paddle()
	if ball_pos[1] <= BALL_RADIUS:
		ball_vel[1] = -ball_vel[1]
	if ball_pos[1] >= HEIGHT - 1 - BALL_RADIUS:
		ball_vel[1] = -ball_vel[1]

	canvas.draw_line([HALF_PAD_WIDTH + LEFT_BOUND, left_paddle - HALF_PAD_HEIGHT], [HALF_PAD_WIDTH + LEFT_BOUND, left_paddle + HALF_PAD_HEIGHT], PAD_WIDTH, 'Blue')
	canvas.draw_line([WIDTH - 1 - HALF_PAD_WIDTH, right_paddle - HALF_PAD_HEIGHT], [WIDTH - 1 - HALF_PAD_WIDTH, right_paddle + HALF_PAD_HEIGHT], PAD_WIDTH, 'Blue')
	canvas.draw_line([(WIDTH + LEFT_BOUND)/2.0, 0], [(WIDTH + LEFT_BOUND)/2.0, HEIGHT], 3, 'White')
	canvas.draw_text(str(score1), [WIDTH/4 - 16, HEIGHT/2 + 32], 50, 'White')
	canvas.draw_text(str(score2), [3*WIDTH/4 - 16, HEIGHT/2 + 32], 50, 'White')
	canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "Yellow")

def move_paddle(key):
	global left_paddle, right_paddle
	if key==simplegui.KEY_MAP["s"] and left_paddle + HALF_PAD_HEIGHT < HEIGHT - 1:
		left_paddle += PAD_VEL
	if key==simplegui.KEY_MAP["w"] and left_paddle - HALF_PAD_HEIGHT > 0:
		left_paddle += - PAD_VEL
	if key==simplegui.KEY_MAP["down"] and right_paddle + HALF_PAD_HEIGHT < HEIGHT - 1:
		right_paddle += PAD_VEL
	if key==simplegui.KEY_MAP["up"] and right_paddle - HALF_PAD_HEIGHT  > 0:
		right_paddle += -PAD_VEL

# main frame
frame = simplegui.create_frame("Arcade Pong", WIDTH, HEIGHT)
frame.set_keydown_handler(move_paddle)
frame.set_draw_handler(draw)
frame.add_button("Game Start", start_game, 60)

frame.start()
