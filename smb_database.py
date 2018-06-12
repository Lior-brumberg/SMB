from database import Database
from Tkinter import *
import sqlite3
import tkMessageBox
from main_screen import main_screen1


def RUN(self):
    self.root.resizable(width=False, height=False)
    self.root.mainloop()


try:
    User_database = Database("FAKE_DRIVB_DB")
    User_database.create_table("Users", "IP string, Authorization string")
except sqlite3.OperationalError:
    pass


def input_new(self):
    User_database.delete_by_column("Users", "IP", IPentry.get())
    self.add_user(event=1)


def check_ip(ip):
    x = True
    if '.' in ip:
        ip = ip.split(".")
        if len(ip) != 4:
            return False
        try:
            for byte in ip:
                x = x and (0 <= int(byte) <= 255)
        except ValueError:
            x = False
    else:
        x = False
    return x


def clear_fields():
    global IPentry
    global Ro_checlbox
    global Wo_checlbox
    global ALL_checlbox
    global NONE_checlbox

    Ro_checlbox.deselect()
    Wo_checlbox.deselect()
    ALL_checlbox.deselect()
    NONE_checlbox.deselect()
    IPentry.delete(0, 'end')


def Handle_request():
    global ErrorFrame
    global IPentry
    global RO_var
    global WO_var
    global ALL_var
    global NONE_var
    global User_database
    clearence = 0

    if RO_var.get() == 1:
        clearence = 1
    elif WO_var.get() == 1:
        clearence = 2
    elif ALL_var.get() == 1:
        clearence = 3
    elif NONE_var.get() == 1:
        clearence = -1
    print User_database.get_by_column("Users", "IP", '\'' + IPentry.get() + '\'').fetchall()
    if User_database.get_by_column("Users", "IP", '\'' + IPentry.get() + '\'').fetchall():
        result = tkMessageBox.askyesno("Duplicate error",
                                       "That user is already in our database\n do you want to override?")
        if result == 'yes':
            input_new()
    else:
        User_database.insert_data("Users", "IP, Authorization", "\'" + IPentry.get() + "\', \'" + str(clearence) + "\'")

    ErrorFrame.destroy()
    ErrorFrame = Frame(root)
    ErrorFrame.pack(side=RIGHT)
    SuccessLabel = Label(ErrorFrame, text="USER successfully added", fg='black', justify=LEFT)
    SuccessLabel.pack(side=TOP)
    new_img = PhotoImage(file='hsk.gif')
    backlabel.configure(image=new_img)
    backlabel.image = new_img
    clear_fields()


def add_user(event):
    global root
    global ErrorFrame
    global IPentry
    global RO_var
    global WO_var
    global ALL_var
    global NONE_var
    global photo
    global backlabel

    on_counter = 0
    on_counter += RO_var.get()
    on_counter += WO_var.get()
    on_counter += ALL_var.get()
    on_counter += NONE_var.get()
    if on_counter > 1:
        ErrorFrame.destroy()
        ErrorFrame = Frame(root)
        ErrorFrame.pack(side=RIGHT)
        ErrorLabel = Label(ErrorFrame, text='ERROR: Only one checkbox can be checked\n User was not added.', fg='black',
                           justify=LEFT)
        ErrorLabel.pack(side=TOP)
        new_img = PhotoImage(file='homer.gif')
        backlabel.configure(image=new_img)
        backlabel.image = new_img
        backlabel.update()
        clear_fields()
        return
    elif on_counter == 0:
        ErrorFrame.destroy()
        ErrorFrame = Frame(root)
        ErrorFrame.pack(side=RIGHT)
        ErrorLabel = Label(ErrorFrame, text="ERROR: One checbox must be checked\n User was not added", fg='black',
                           justify=LEFT)
        ErrorLabel.pack(side=TOP)
        new_img = PhotoImage(file='homer.gif')
        backlabel.configure(image=new_img)
        backlabel.image = new_img
        clear_fields()
        return

    if check_ip(IPentry.get()):
        Handle_request()
    else:
        ErrorFrame.destroy()
        ErrorFrame = Frame(root)
        ErrorFrame.pack(side=RIGHT)
        ErrorLabel = Label(ErrorFrame, text="ERROR: IP incorrect\n User was not added", fg='black', justify=LEFT)
        ErrorLabel.pack(side=TOP)
        new_img = PhotoImage(file='homer.gif')
        backlabel.configure(image=new_img)
        backlabel.image = new_img
        clear_fields()
        return


root = Toplevel(main_screen1)
imageframe = Frame(root)
imageframe.pack(side=TOP)
imgPath = r"hsk.gif"
photo = PhotoImage(file=imgPath)
backlabel = Label(imageframe, image=photo, padx=0, pady=0)
backlabel.pack(side=LEFT)

ErrorFrame = Frame(root)
ErrorFrame.pack(side=RIGHT)
DATAFrame = Frame(root)
DATAFrame.pack(side=LEFT, fill=BOTH)

RO_var = IntVar()
WO_var = IntVar()
ALL_var = IntVar()
NONE_var = IntVar()

IPentry = Entry(DATAFrame)
IPlable = Label(DATAFrame, text='Enter IP:')

IPlable.grid(column=0, sticky=W)
IPentry.grid(column=1, row=0)

Ro_checlbox = Checkbutton(DATAFrame, text='READ_ONLY', variable=RO_var)
Wo_checlbox = Checkbutton(DATAFrame, text='WRITE_ONLY', variable=WO_var)
ALL_checlbox = Checkbutton(DATAFrame, text='ALL(READ WRITE AND DELETE)', variable=ALL_var)
NONE_checlbox = Checkbutton(DATAFrame, text='NONE', variable=NONE_var)

Ro_checlbox.grid(row=1, column=0)
Wo_checlbox.grid(row=2, column=0)
ALL_checlbox.grid(row=1, column=1)
NONE_checlbox.grid(row=2, column=1, sticky=W)

SubmitButton = Button(DATAFrame, text='submit')
SubmitButton.bind("<Button-1>", add_user)
SubmitButton.grid(row=3, column=0, columnspan=2)

root.resizable(width=False, height=False)