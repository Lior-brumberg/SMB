# -*- coding: utf-8 -*-
from Tkinter import *


def ADD(event):
    execfile("C:\Users\user\Desktop\SMB-master\smb_database.py")


def main():
    main_screen = Tk()
    main_screen.title("Drive protector")
    main_screen.geometry('500x500')

    start_button = Button(main_screen, text='start', fg='black')
    add_user_button = Button(main_screen, text='Add User', fg='black')

    #start_button.bind("<Button-1>", )
    add_user_button.bind("<Button-1>", ADD)

    start_button.pack(side=TOP, fill=X)
    add_user_button.pack(side=TOP, fill=X)

    main_screen.resizable(width=False, height=False)
    main_screen.mainloop()


if __name__ == '__main__':
    main()