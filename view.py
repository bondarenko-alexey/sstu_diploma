from tkinter import *
from parser import parse

root = Tk()

root['bg'] = '#fafafa'
root.title('Информационный поиск')
root.geometry('500x400')
root.resizable(width=False, height=False)

canvas = Canvas(root, height=350, width=450)
canvas.pack()

frame = Frame(root, bg="#e314f2")
frame.place()

def Hello(event):
    print("Yet another hello world")

btn = Button(root,                 
             text="Click me",         
             bg="white",fg="black"
            )
btn.bind("<Button-1>", parse)       
btn.pack()  
                       
root.mainloop()