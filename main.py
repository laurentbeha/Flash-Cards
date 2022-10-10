from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/top_1000_german_words.csv")

data_dict = data.to_dict(orient="records")
current_card = {}
# --------------------------------Creating Flash Cards------------------------------------


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(data_dict)
    canvas.itemconfig(title, text="German", fill="black")
    canvas.itemconfig(word, text=current_card["German"], fill="black")
    canvas.itemconfig(canvas_img, image=card_front_img)
    flip_timer = window.after(5000, func=flip_card)


def flip_card():
    canvas.itemconfig(canvas_img, image=card_back_img)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")


def remove_word():
    data_dict.remove(current_card)
    print(len(data_dict))
    next_card()


# ------------------------------------UI config-------------------------------------------
# window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(5000, func=flip_card)

# canvas
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas_img = canvas.create_image(400, 263, image=card_front_img)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong_img = PhotoImage(file="images/wrong.png")
right_img = PhotoImage(file="images/right.png")

unknown_button = Button(image=wrong_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
unknown_button.grid(row=1, column=0)

known_button = Button(image=right_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=remove_word)
known_button.grid(row=1, column=1)


next_card()
window.mainloop()

new_data = pandas.DataFrame(data_dict)

new_data.to_csv("data/words_to_learn.csv", index=False)
