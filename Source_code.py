import tkinter as tk
from tkinter import messagebox
import tkSimpleDialog

#***********global variables*********
TIMER_START_MIN=25
TIMER_START_SEC=TIMER_START_MIN*60
min,sec=divmod(TIMER_START_SEC,60)
banner_text1="{:02d}:{:02d}".format(min,sec)
switch=False
time_remaining=0

'''
    When customer selects Set time in minutes,
    following function kicks in
'''

def global_variable_readjust(t):
    global TIMER_START_MIN
    global TIMER_START_SEC
    global min
    global sec
    global banner_text1

    if(t>0):
        TIMER_START_MIN=t
        TIMER_START_SEC = TIMER_START_MIN * 60
        min, sec = divmod(TIMER_START_SEC, 60)
        banner_text1 = "{:02d}:{:02d}".format(min, sec)

    else:
        TIMER_START_MIN = 25
        TIMER_START_SEC = TIMER_START_MIN * 60
        min, sec = divmod(TIMER_START_SEC, 60)
        banner_text1 = "{:02d}:{:02d}".format(min, sec)


#*************Class and functions related to Menubar*********

'''
    In the following link, the code of tkSimpledialog can be found:
    http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
    To create dialogbox, it is suggested to create a class that inherits the Dialog class and
    overwrite the body and apply method to suit the specific need

'''

class MyDialog(tkSimpleDialog.Dialog):

    def body(self,root):
        tk.Label(root,text="Set minutes\n(only integer, no negative or fraction)").grid(row=0,column=0)

        self.e1=tk.Entry(root)
        self.e1.grid(row=0,column=1)

        return self.e1

    def apply(self):
        '''
        self.e1 is an Entry object; first we need to convert it to string,
        then float, then absolute value and eventually int.
        If the customer enters something like -0.89,
        the default 25 minutes will be used to start the timer.
        '''
        result=int(abs(float(str((self.e1.get())))))
        if(result==0):
            tk.messagebox.showinfo("Warning!", "Only positive whole numbers please.\nIf the input is less than 1,\nthe counter will start countdown from 25 minutes.")
            global_variable_readjust(result)
        else:
            global_variable_readjust(result)


def take_input():

    d=MyDialog(root)


def about_this_app():

    tk.messagebox.showinfo("About this app","This is a 2-in-1 app.\nYou can use it as a timer by choosing number of minutes from \nFile>Set time in minutes\nOr,\nUse the standard 25 minutes Pmodoro chunk.")


def Pmodoro_history():

    tk.messagebox.showinfo("About Pomodoro Technique", "From wikipedia:\n\nThe Pomodoro Technique is a time management method developed by Francesco Cirillo in the late 1980s that uses a timer to break down work into intervals, traditionally 25 minutes in length, separated by short breaks. \nLink:\nhttps://en.wikipedia.org/wiki/Pomodoro_Technique")

def command_the_creator_of_this_app():

    tk.messagebox.showinfo("Contact the Creator","Asif Choudhury\n\nEmail:\tasifikchoudhury@gmail.com\nLocation:\tVictoria, BC, Canada\n\nPlease contact the creator of the app, if you have any feedback.")


#***********functions related to buttons***********
def timer_func():

    global time_remaining,TIMER_START_SEC
    time_remaining=TIMER_START_SEC
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    flip_switch_false_to_true()
    update_regularly()

def flip_switch_false_to_true():
    global switch
    switch = True

def flip_switch_true_to_false():
    global switch
    switch=False
    stop_button.config(state=tk.DISABLED)
    reset_button.config(state=tk.NORMAL)
    resume_button.config(state=tk.NORMAL)

def update_regularly():

    global time_remaining

    global switch

    if (time_remaining>0 and switch==True):

        min, sec = divmod(time_remaining, 60)
        banner_text2 = "{:02d}:{:02d}".format(min, sec)
        lbl.config(text=banner_text2)
        time_remaining-=1
        if (time_remaining==0):
            banner_text3="00:00"
            lbl.config(text=banner_text3)
            stop_button.config(state=tk.DISABLED)
            reset_button.config(state=tk.NORMAL)

        root.after(1000,update_regularly)

def resume_action():

    resume_button.config(state=tk.DISABLED)
    reset_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    flip_switch_false_to_true()
    update_regularly()

def reset_action():

    lbl.config(text=banner_text1)
    resume_button.config(state=tk.DISABLED)
    reset_button.config(state=tk.DISABLED)
    start_button.config(state=tk.NORMAL)

root=tk.Tk()

#*******Menubar*********************
menubar=tk.Menu(root)
root.config(menu=menubar)

filemenu=tk.Menu(menubar,tearoff=0)
filemenu.add_cascade(label="Set time in minutes", command=take_input)

filemenu.add_separator()

filemenu.add_cascade(label="Exit",command=root.quit)

helpmenu=tk.Menu(menubar,tearoff=0)
helpmenu.add_cascade(label="About this app",command=about_this_app)
helpmenu.add_cascade(label="About Pomodoro Technique",command=Pmodoro_history)
helpmenu.add_separator()
helpmenu.add_cascade(label="Contact the creator",command=command_the_creator_of_this_app)


menubar.add_cascade(label="File",menu=filemenu)
menubar.add_cascade(label="Help",menu=helpmenu)

#*******Timer display and buttons***************
top_frame=tk.Frame(root)

top_frame.pack(side=tk.TOP)

bottom_frame=tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM)

lbl=tk.Label(top_frame,text=banner_text1,font=('Helvetica', 36), fg='black')

lbl.grid(row=0,columnspan=4)

start_button=tk.Button(bottom_frame,text="START",font=("Helvetica",24),command=timer_func)
start_button.grid(row=1,column=0)
start_button.config(state=tk.NORMAL)

stop_button=tk.Button(bottom_frame,text="STOP",font=("Helvetica",24),command=flip_switch_true_to_false)
stop_button.grid(row=1,column=1)
stop_button.config(state=tk.DISABLED)

resume_button=tk.Button(bottom_frame,text="RESUME",font=("Helvetica",24),command=resume_action)
resume_button.grid(row=1,column=2)
resume_button.config(state=tk.DISABLED)

reset_button=tk.Button(bottom_frame,text="RESET",font=("Helvetica",24),command=reset_action)
reset_button.grid(row=1,column=3)
reset_button.config(state=tk.DISABLED)


#******************Window Title Bar**************
root.title("Pomodoro Technique 2.1.2")

#******************Window Title Bar Icon*********
# root.call('wm', 'iconbitmap', root._w, '-default', 'POMODOROICON.ico')



root.mainloop()