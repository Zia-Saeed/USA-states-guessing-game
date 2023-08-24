import turtle
import pandas as pd
from turtle import Turtle

# Screen object
screen = turtle.Screen()
screen.title("U.S States Game.")

# State object
state = turtle.Turtle()

# Image path
image = "./blank_states_img.gif"

# Argument for the write function in turtle
Font = ("Arial", 8, "normal")
ALIGNMENT = "center"
SCORE_POSITION = (0, 250)
LIFE_POSITION = (-90, 250)

# Adding map picture to the screen_obj
screen.addshape(image)

# Displaying map picture
turtle.shape(image)

# Reading Data from 50_states.csv
data = pd.read_csv("50_states.csv")

#  List of Sates of America
states_list = data.state.to_list()


# Writing States Name on the map
def state_writing(position, state_name):
    state.hideturtle()
    state.penup()
    state.goto(position)
    state.write(state_name, font=Font, align=ALIGNMENT)


# Function to Show GAME OVER
def game_over():
    state.hideturtle()
    state.penup()
    state.goto(0, 0)
    state.write("GAME OVER!", font=Font, align=ALIGNMENT)


# Score object
score_obj = Turtle()
life_obj = Turtle()


# Function to display Scores
def score(position, u_score):
    score_obj.hideturtle()
    score_obj.penup()
    score_obj.goto(position)
    score_obj.write(f"Score={u_score}", align=ALIGNMENT, font=Font)


# Function to display lives
def user_life(position, u_life):
    # life_obj.clear()
    life_obj.hideturtle()
    life_obj.penup()
    life_obj.goto(position)
    life_obj.write(f"Chances remaining={u_life}", align=ALIGNMENT, font=Font)


life = 3
user_score = 0
correct_user_guess = []
try:
    while len(correct_user_guess) < 50:

        score(position=SCORE_POSITION, u_score=user_score)
        user_life(LIFE_POSITION, life)

        if life == 0:
            print("You ran out of chances")
            game_over()
            break
        user_guess = screen.textinput(f"States Guessing,{user_score}/50", prompt="Enter the state name:").title()
        if user_guess == "Exit":
            break
        # condition if the user guess in correct
        if user_guess in states_list:
            if user_guess not in correct_user_guess:
                correct_user_guess.append(user_guess)

                # Getting row of that record that is equal to user_guess
                state_data = data[data.state == user_guess]
                # x and y cor for the states in the map
                x_cor = int(state_data.x)
                y_cor = int(state_data.y)
                state_writing((x_cor, y_cor), user_guess)

                # state.goto(x_cor, y_cor)
                score_obj.clear()
                user_score += 1

        # checking for repeated Guess
        elif user_guess in correct_user_guess:
            print("You have already guessed this State.")
        # decrease the life by -1 whenever user_guess is wrong
        elif user_guess not in states_list:
            life -= 1
            life_obj.clear()

        # User guess in not correct
        else:
            game_over()
            print("Better Luck Next Time.")
            break

    states_list = set(states_list)
    # putting states that are missed by user in new csv file name misses_states

    missed_states = [state for state in states_list if state not in correct_user_guess]


    dict_user_missed_states = {
        "misses_states": missed_states,
                            }

    missed_states_data = pd.DataFrame(dict_user_missed_states)
    missed_states_file = missed_states_data.to_csv("missed_states")


    screen.mainloop()
except Exception:
    game_over()
    screen.mainloop()