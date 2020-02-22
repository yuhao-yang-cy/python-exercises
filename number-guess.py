import simpleguitk as simplegui
import random
import math

game_range = 0

# helper functions
def find_trial(number):
    return int(math.ceil(math.log(number, 2)))

def reset_counter():
    global counter, trial, win
    counter = 0
    win = False
    trial = find_trial(game_range)

def output_setting():
    print("--------------------")
    print("New Game!")
    print("The mysterious number is between 0 to", game_range)
    print("You have", trial, "chances to make it!")

# event handlers for control panel
def new_game():
    global game_range, number, trial
    if game_range == 0:
        game_range = 100
    number = random.randrange(1, game_range)
    reset_counter()
    output_setting()

def input_range(range):
    global game_range
    game_range = int(range)
    new_game()

def input_guess(guess):
    global player_guess, counter, win
    if not win:
        player_guess = int(guess)
        counter += 1
        if counter <= trial:
            if player_guess == number:
                win = True
                print("Congratulations! You made the correct guess!")
                print("The number is", number)
            else:
                print("Number of trials remaining:", trial - counter)
                if player_guess > number:
                    print("Your guess is", guess, "Try lower!")
                else:
                    print("Your guess is", guess, "Try higher!")
        if trial - counter == 0 and player_guess != number:
            print("Sorry, you lose! The number is", number)

# main frame
frame = simplegui.create_frame('Guessing The Mysterious Number', 300, 200)
frame.add_button('New Game', new_game, 150)
frame.add_input("Enter Range", input_range, 150)
frame.add_input("Enter Guess", input_guess, 150)

frame.start()
new_game()
