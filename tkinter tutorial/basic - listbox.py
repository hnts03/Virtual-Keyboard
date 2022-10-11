import tkinter as tk
from math import *

def main():
    window = tk.Tk() 
    window.title("test1")
    window.geometry("640x400+100+100")
    window.resizable(True, True)

    # --- List box ---
    listbox = tk.Listbox(window, selectmode='extended', height=0)
    listbox.insert(0, "1st")
    listbox.insert(1, "2nd")
    listbox.insert(2, "2nd")
    listbox.insert(3, "2nd")
    listbox.insert(4, "3rd")
    listbox.delete(1, 2)
    listbox.pack()


    window.mainloop() 


if __name__ == "__main__":
    main()