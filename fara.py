from tkinter import *
import sys
import os
root = Tk()
def close_window():
	pass

def take(event):
	os.system('python3 farming.py')
	os.system('sudo poweroff')


bu_1=Button(root,text="AUTOFARM")
bu_1.bind("<Button-1>",take)
bu_1.pack()
bu_2=Button(root, text = "Good-bye.", command = close_window)
bu_2.bind("<Button-2>",close_window)
bu_2.pack()

root.mainloop()
