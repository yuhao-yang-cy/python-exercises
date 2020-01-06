import simpleguitk as simplegui
import math

message = "Timer Game"
clock, minute, second, decimal = 0, 0, 0, 0
hit_time = 5
uncertainty = 1
score1, score2 = 0, 0

# Handlers
def start_pause():
	if timer.is_running():
		timer.stop()
	else:
		timer.start()
    
def draw(canvas):
	canvas.draw_text(message, [50,80], 28, "Red")
	canvas.draw_text("Colin: " + str(score1), [50,160], 24, "Blue", "sans-serif")
	canvas.draw_text("Elizabeth: " + str(score2), [50,240], 24, "Blue", "sans-serif")

def inc_timer():
	global clock, message, whole, minute, second, decimal
	clock += 1
	minute = clock / 600
	second = (clock % 600) / 10
	decimal = clock % 10
	message = time_string(minute, second, decimal)

def time_string(minute, second, decimal):
    if second < 10:
        second_string = "0" + str(second)
    else:
        second_string = str(second)
    return str(minute) + ":" + second_string + "." + str(decimal)
	
def player1():
	global score1
	if second % hit_time == 0 and decimal <= uncertainty:
		score1 +=3
	elif second % hit_time == hit_time - 1 and decimal >= 10 - uncertainty:
		score1 +=3
	else:
		score1 -=1
		
def player2(key):
	global score2
	if second % hit_time == 0 and decimal <= uncertainty:
		score2 +=3
	elif second % hit_time == hit_time - 1 and decimal >= 10 - uncertainty:
		score2 +=3
	else:
		score2 -=1

def reset():
	global score1, score2, clock, message
	score1, score2, clock = 0, 0, 0
	timer.stop()
	message = time_string(0, 0, 0)
		
# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", 300, 300)
frame.add_button("Start/Pause", start_pause, 120)
frame.add_button("Click", player1, 120)
frame.add_button("Reset", reset, 120)
frame.set_keydown_handler(player2)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, inc_timer)

# Start the frame animation
frame.start()