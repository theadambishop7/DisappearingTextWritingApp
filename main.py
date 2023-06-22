from tkinter import *
import time
import math

MASTER_TIMER_LENGTH = 300
SEGMENT_TIMER_LENGTH = 5

BIG_FONT = ("Arial", 24, "normal")
SMALL_FONT = ("Arial", 14, "normal")

current_timer = None
current_segment_timer = None


def key_press(event):
    global current_segment_timer
    if current_segment_timer is not None:  # Add this check
        window.after_cancel(current_segment_timer)
        segment_timer.config(text="00", fg="black")
        segment_timer_label.config(fg="black")
        current_segment_timer = None  # Set to None after canceling


def key_released(event):
    global current_segment_timer
    if current_segment_timer is not None:  # Add this check
        window.after_cancel(current_segment_timer)
    current_segment_timer = window.after(1000, kill_count_down, SEGMENT_TIMER_LENGTH)  # Start a new timer


def kill_count_down(count):
    global current_segment_timer
    if count == 0:  # Stop the count when it reaches zero
        if current_timer is not None:
            window.after_cancel(current_timer)
        segment_timer.config(text="00")
        typing_window.delete("1.0", END)
        typing_window.insert(END, "TIMES UP")
        typing_window.config(state=DISABLED, fg="red")
        return
    if count < 10:
        count = f"0{count}"
    segment_timer.config(text=count, fg="red")
    segment_timer_label.config(fg="red")
    current_segment_timer = window.after(1000, kill_count_down, int(count) - 1)  # Schedule the next call

def count_down(count):
    global current_timer
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    clock_count = f"{count_min}:{count_sec}"
    master_timer.config(text=clock_count)
    current_timer = window.after(1000, count_down, int(count) - 1)


def start_timer():
    global current_timer
    if current_timer is not None:
        window.after_cancel(current_timer)
    key_released("event")
    current_timer = MASTER_TIMER_LENGTH
    typing_window.config(state=NORMAL, fg="black")
    typing_window.delete("1.0", END)
    count_down(MASTER_TIMER_LENGTH)
    typing_window.focus_set()


window = Tk()
window.title("Disappearing Text App")
window.config(padx=100, pady=100)

title_label = Label(text="Writer's Block Breaker", font=BIG_FONT, pady=2)
title_label.grid(row=0, column=1, columnspan=3)

instructions = Label(text="Click to start a 5 minute challenge\n"
                          "If you stop typing for more than 5 seconds, your work will be LOST!\n",
                     font=SMALL_FONT, pady=4)
instructions.grid(row=1, column=1, columnspan=3)

typing_window = Text(window, wrap=WORD, width=40, height=5, font=("", 14), padx=5, pady=5)
typing_window.insert(END, "Type here, but be warned!")
typing_window.config(state=DISABLED, bd=2, relief="solid")
typing_window.grid(row=2, column=1, columnspan=3)

start_button = Button(text="Start", command=start_timer)
start_button.grid(row=4, column=1, columnspan=3)

segment_timer_label = Label(text="Delete Timer", font=SMALL_FONT)
segment_timer_label.grid(row=5, column=1, columnspan=1)

segment_timer = Label(text="00", font=("Arial", 14))
segment_timer.grid(row=6, column=1, columnspan=1)

master_timer_label = Label(text="Challenge Timer", font=SMALL_FONT)
master_timer_label.grid(row=5, column=3)

master_timer = Label(text="00", font=("Arial", 14))
master_timer.grid(row=6, column=3, columnspan=1)

window.bind('<KeyPress>', key_press)
window.bind('<KeyRelease>', func=key_released)

window.mainloop()
