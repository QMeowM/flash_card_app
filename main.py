from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"

#------------------------------------------CREATE NEW FLASH CARDS-------------------------------------#
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")

french_to_english_list = data.to_dict(orient="records")
current_card = {}

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(french_to_english_list)
    canvas.itemconfig(card_side, image=card_front_image)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)

#using iterrows returns a list of dictionaries as
# {French_word:English_word}, making it hard to pull out key separately

#------------------------------------------FLIP THE CARD-------------------------------------#
def flip_card():
    canvas.itemconfig(card_side, image=card_back_image)
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")

#------------------------------------------REMOVE KNOWN WORD-------------------------------------#

def remove_word():
    french_to_english_list.remove(current_card)
#------------------------------------------UI-------------------------------------#
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)
# The above line must be before the first next_card()

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_side = canvas.create_image(400, 263, image=card_front_image)
language = canvas.create_text(400, 150, text="", fill="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", fill="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
unknown_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=unknown_image, command=next_card, highlightbackground=BACKGROUND_COLOR)
unknown_button.grid(row=1, column=0)

known_image = PhotoImage(file="images/right.png")
known_button = Button(image=known_image, command=lambda:[next_card(),remove_word()], highlightbackground=BACKGROUND_COLOR)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()

#------------------------------------------SAVING PROGRESS-------------------------------------#
words_to_learn = pandas.DataFrame.from_dict(french_to_english_list)
words_to_learn.to_csv("data/words_to_learn.csv", index=False)
