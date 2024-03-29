from modules.gpio_handler import unlock
from modules.whatsapp_handler import *
from sem_tocar import *
from tkinter import *


def gui():
    window = Tk()
    window.geometry("200x150")
    routineButton = Button(
        window, text="Routine", bg="grey", command=lambda: routine()
    ).pack()
    refreshButton = Button(
        window, text="Refresh", bg="grey", command=lambda: request_calendars()
    ).pack()
    doormanButton = Button(
        window, text="Doorman", bg="grey", command=lambda: doorman()
    ).pack()
    setupButton = Button(
        window, text="Setup", bg="grey", command=lambda: setup()
    ).pack()
    doorButton = Button(
        window, text="QR found", bg="grey", command=lambda: qr_found_warn()
    ).pack()
    #wappButton = Button(
    #    window, text="Whatsapp", bg="grey", command=lambda: test_whatsapp()
    #).pack()

    window.mainloop()


if __name__ == "__main__":
    gui()
