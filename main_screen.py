# -*- coding: utf-8 -*-
from Tkinter import *
from database import Database
from Tkinter import *
import sqlite3
import tkMessageBox
main_screen1 = Tk()

def ADD(event):
    execfile('Sighnup.py')


def main():
    main_screen1.title("Drive protector")
    main_screen1.geometry('300x400')

    start_button = Button(main_screen1, text='start', fg='black')
    add_user_button = Button(main_screen1, text='Add User', fg='black')

    # start_button.bind("<Button-1>", )
    add_user_button.bind("<Button-1>", ADD)

    path = r'main.gif'
    photo = PhotoImage(file=path)
    photolabel = Label(main_screen1, image=photo)
    photolabel.image = photo
    photolabel.pack(side=TOP)

    add_user_button.pack(side=BOTTOM, fill=X)
    start_button.pack(side=BOTTOM, fill=X)

    main_screen1.resizable(width=False, height=False)
    main_screen1.mainloop()


if __name__ == '__main__':
    main()
