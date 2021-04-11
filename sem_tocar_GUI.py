from sem_tocar import *
from tkinter import *


def main():
    window = Tk()
    window.geometry("200x150")
    routineButton = Button(
        window, text="Routine", bg="grey", command=lambda: routine()
    ).pack()
    doormanButton = Button(
        window, text="Doorman", bg="grey", command=lambda: doorman()
    ).pack()

    window.mainloop()


if __name__ == "__main__":
    main()
