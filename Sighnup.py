from database import Database
from Tkinter import *
import sqlite3
import tkMessageBox
from main_screen import main_screen1
main_screen1.withdraw()
main_screen1.withdraw()

class SighnUp(object):
    def __init__(self):
        try:
            self.User_database = Database("FAKE_DRIVB_DB")
            self.User_database.create_table("Users", "IP string, Authorization string")
            print "DB created"
        except sqlite3.OperationalError:
            print "DB accessed"

        self.root = Toplevel(main_screen1)
        self.root.title('Sign Up')


        self.RO_var = IntVar()
        self.WO_var = IntVar()
        self.ALL_var = IntVar()
        self.NONE_var = IntVar()

        self.imageframe = Frame(self.root)
        self.imageframe.pack(side=TOP)
        self.imgPath = r"hsk.gif"
        self.photo = PhotoImage(file=self.imgPath)
        self.backlabel = Label(self.imageframe, image=self.photo, padx=0, pady=0)
        self.backlabel.pack(side=LEFT)

        self.ErrorFrame = Frame(self.root)
        self.DATAFrame = Frame(self.root)
        self.ErrorFrame.pack(side=RIGHT)
        self.DATAFrame.pack(side=LEFT, fill=BOTH)

        self.IPentry = Entry(self.DATAFrame)
        self.IPlable = Label(self.DATAFrame, text='Enter IP:')
        self.IPlable.grid(column=0, sticky=W)
        self.IPentry.grid(column=1, row=0)

        self.Ro_checlbox = Checkbutton(self.DATAFrame, text='READ_ONLY', variable=self.RO_var)
        self.Wo_checlbox = Checkbutton(self.DATAFrame, text='WRITE_ONLY', variable=self.WO_var)
        self.ALL_checlbox = Checkbutton(self.DATAFrame, text='ALL(READ WRITE AND DELETE)', variable=self.ALL_var)
        self.NONE_checlbox = Checkbutton(self.DATAFrame, text='NONE', variable=self.NONE_var)

        self.Ro_checlbox.grid(row=1, column=0)
        self.Wo_checlbox.grid(row=2, column=0)
        self.ALL_checlbox.grid(row=1, column=1)
        self.NONE_checlbox.grid(row=2, column=1, sticky=W)

        self.SubmitButton = Button(self.DATAFrame, text='submit')
        self.SubmitButton.bind("<Button-1>", self.add_user)
        self.SubmitButton.grid(row=3, column=0, columnspan=2)

    def add_user(self, event):
        on_counter = 0
        on_counter += self.RO_var.get()
        on_counter += self.WO_var.get()
        on_counter += self.ALL_var.get()
        on_counter += self.NONE_var.get()
        if on_counter > 1:
            self.ErrorFrame.destroy()
            self.ErrorFrame = Frame(self.root)
            self.ErrorFrame.pack(side=RIGHT)
            self.ErrorLabel = Label(self.ErrorFrame,
                                    text='ERROR: Only one checkbox can be checked\n User was not added.', fg='black',
                                    justify=LEFT)
            self.ErrorLabel.pack(side=TOP)
            self.new_img = PhotoImage(file='homer.gif')
            self.backlabel.configure(image=self.new_img)
            self.backlabel.image = self.new_img
            self.backlabel.update()
            self.clear_fields()
            return
        elif on_counter == 0:
            self.ErrorFrame.destroy()
            self.ErrorFrame = Frame(self.root)
            self.ErrorFrame.pack(side=RIGHT)
            self.ErrorLabel = Label(self.ErrorFrame, text="ERROR: One checbox must be checked\n User was not added",
                                    fg='black',
                                    justify=LEFT)
            self.ErrorLabel.pack(side=TOP)
            self.new_img = PhotoImage(file='homer.gif')
            self.backlabel.configure(image=self.new_img)
            self.backlabel.image = self.new_img
            self.clear_fields()
            return

        if self.check_ip(self.IPentry.get()):
            self.Handle_request()
        else:
            self.ErrorFrame.destroy()
            self.ErrorFrame = Frame(self.root)
            self.ErrorFrame.pack(side=RIGHT)
            self.ErrorLabel = Label(self.ErrorFrame, text="ERROR: IP incorrect\n User was not added", fg='black',
                                    justify=LEFT)
            self.ErrorLabel.pack(side=TOP)
            self.new_img = PhotoImage(file='homer.gif')
            self.backlabel.configure(image=self.new_img)
            self.backlabel.image = self.new_img
            self.clear_fields()
            return

    def Handle_request(self):
        clearence = 0

        if self.RO_var.get() == 1:
            clearence = 1
        elif self.WO_var.get() == 1:
            clearence = 2
        elif self.ALL_var.get() == 1:
            clearence = 3
        elif self.NONE_var.get() == 1:
            clearence = -1
        print self.User_database.get_by_column("Users", "IP", '\'' + self.IPentry.get() + '\'').fetchall()
        if self.User_database.get_by_column("Users", "IP", '\'' + self.IPentry.get() + '\'').fetchall():
            result = tkMessageBox.askyesno("Duplicate error",
                                           "That user is already in our database\n do you want to override?")
            if result == 'yes':
                self.input_new()

        else:
            self.User_database.insert_data("Users", "IP, Authorization",
                                           "\'" + self.IPentry.get() + "\', \'" + str(clearence) + "\'")

        self.ErrorFrame.destroy()
        self.ErrorFrame = Frame(self.root)
        self.ErrorFrame.pack(side=RIGHT)
        self.SuccessLabel = Label(self.ErrorFrame, text="USER successfully added", fg='black', justify=LEFT)
        self.SuccessLabel.pack(side=TOP)
        self.new_img = PhotoImage(file='hsk.gif')
        self.backlabel.configure(image=self.new_img)
        self.backlabel.image = self.new_img
        self.clear_fields()

    def check_ip(self, ip):
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

    def clear_fields(self):
        self.Ro_checlbox.deselect()
        self.Wo_checlbox.deselect()
        self.ALL_checlbox.deselect()
        self.NONE_checlbox.deselect()
        self.IPentry.delete(0, 'end')

    def input_new(self):
        self.User_database.delete_by_column("Users", "IP", self.IPentry.get())
        self.add_user(event=1)

    def Get_root(self):
        return self.root

    def run(self):
        self.root.resizable(width=False, height=False)
        self.root.mainloop()

x = SighnUp()
x.run()
