from tkinter import *


def onObjectClick(event):
    print('Got object click', event.x, event.y, event.widget)
    item = event.widget.find_closest(event.x, event.y)
    print(event.widget.gettags(item))


root = Tk()
canv = Canvas(root, width=100, height=100)
obj1 = canv.create_text(50, 30, text='Click me one', tags="a")
obj2 = canv.create_text(50, 70, text='Click me two', tags="b")

canv.tag_bind(obj1, '<Button-1>', onObjectClick)
canv.tag_bind(obj2, '<Button-1>', onObjectClick)
canv.pack()
root.mainloop()
