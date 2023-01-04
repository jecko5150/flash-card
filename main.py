from random import choice
from tkinter import *

import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    d = pd.read_csv("data/words_to_learn.csv")

except FileNotFoundError:
    original_data = pd.read_csv('data/french_words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = d.to_dict(orient='records')


def next_card():
    global current_card, flip_timer, current_card
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(card_title, text='French', fill='black')
    canvas.itemconfig(card_word, text=(current_card['French']), fill='black')
    canvas.itemconfig(flash_card, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    t_word = current_card['English']
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=t_word, fill='white')
    canvas.itemconfig(flash_card, image=card_back)


def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


##################################################################


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)

card_back = PhotoImage(file="images/card_back.png", height=526, width=800)
card_front = PhotoImage(file="images/card_front.png", height=526, width=800)
right_answer = PhotoImage(file='images/right.png')
wrong_answer = PhotoImage(file='images/wrong.png')
# -------------------------------------------------------------------
flash_card = canvas.create_image(400, 263, image=card_front)

card_title = language_label = canvas.create_text(400, 150, text="Title", font=('Arial', 40, 'italic'))
card_word = word_label = canvas.create_text(400, 263, text='french', font=('Arial', 60, 'bold'))

right_button = Button(image=right_answer, highlightthickness=0, activeforeground=BACKGROUND_COLOR, command=is_known)
wrong_button = Button(image=wrong_answer, highlightthickness=0, activeforeground=BACKGROUND_COLOR, command=next_card)

canvas.grid(columnspan=2, column=0, row=0)
right_button.grid(column=1, row=1)
wrong_button.grid(column=0, row=1)

next_card()

window.mainloop()
