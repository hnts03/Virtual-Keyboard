import tkinter as tk



def main():
    window = tk.Tk() 
    window.title("test1")
    window.geometry("640x400+100+100")
    window.resizable(True, True)

    count = 0    

    # --- Label ---
    label = tk.Label(window, text="0")
    label.pack()

    def countUP():
        nonlocal count
        count += 1
        label.config(text=str(count))


    # --- Button ---
    button = tk.Button(window, overrelief="solid", width=15, command=countUP, repeatdelay=1000, repeatinterval=100)
    button.pack()


    window.mainloop() 


if __name__ == "__main__":
    main()