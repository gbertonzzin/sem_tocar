from modules.door_handler import unlock
from sem_tocar import *
from tkinter import *


def gui():
    window = Tk()
    window.geometry("200x150")
    routineButton = Button(
        window, text="Routine", bg="grey", command=lambda: main()
    ).pack()
    doormanButton = Button(
        window, text="Doorman", bg="grey", command=lambda: doorman()
    ).pack()
    setupButton = Button(
        window, text="Setup", bg="grey", command=lambda: setup()
    ).pack()
    doorButton = Button(
        window, text="OPEN DOOR", bg="grey", command=lambda: unlock()
    ).pack()

    window.mainloop()


if __name__ == "__main__":
    gui()
