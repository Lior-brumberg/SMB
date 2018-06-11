from database import Database
from Tkinter import *
import sqlite3


def yes_click(event):
    global screen
    from smb_database import User_database as DataB, IPentry
    from smb_database import add_user
    DataB.delete_by_column("Users", "IP", IPentry.get())
    add_user()
    screen.quit()


def no_click(event):
    from smb_database import clear_fields
    global screen
    clear_fields()
    screen.quit()


screen = Tk()

Ask_label = Label(screen, text="That user is already in our database\n do you want to override?")
yes_button = Button(screen, text='Yes', fg='black')
no_button = Button(screen, text='No', fg='black')

Ask_label.pack(side=TOP)
no_button.bind("<Button-1>", yes_click())
no_button.pack(side=BOTTOM)
yes_button.bind("<Button-1>", no_button)
yes_button.pack(side=BOTTOM)

screen.resizable(width=False, height=False)
screen.mainloop()
