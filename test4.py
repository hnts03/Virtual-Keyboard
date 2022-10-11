# This file is test file for operating test3.py on tkinter

# TODO
# 1. tkinter과 threading 모듈을 활용하여 tkinter 화면에 넣기(완료)
# 2. tkinter window에 entry 삽입


import WebcamKeyboardModule as WKM
import cv2
import tkinter as tk
import threading
from PIL import Image, ImageTk
import time
import numpy as np

class tk_window():
    def __init__(self, window:tk.Tk):
        self.window = window
        self.window.title("test1")
        self.window.geometry("1300x800+300+300")
        self.window.resizable(False, False)

        self.imgtk = None

        button1 = tk.Button(self.window, text="close", overrelief="solid", width=15, command=self.window_close, repeatdelay=1000, repeatinterval=100)
        button1.pack()

        self.label = tk.Label(self.window, image=self.imgtk)
        self.label.pack()

        self.entry = tk.Entry(self.window)
        self.entry.pack()

    def window_close(self):
        print("close")
        self.window.quit()

    # def toggle_image(self):

    def convert_tkimage(self, cv_image):
        RGB = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(RGB)
        self.imgtk = ImageTk.PhotoImage(image=img)

        self.label.config(image=self.imgtk)
        self.label.image = self.imgtk


class Cam_Thread(WKM.Webcam_keyboard):
    def __init__(self, tk_win:tk_window, window_size, Usingimshow):
        super().__init__(window_size)
        self.tkimg = []
        self.tk_window = tk_win
        self.Usingimshow = Usingimshow
    
    def run_thread(self):
        while True:
            self.run_keyboard(self.Usingimshow)
            # time.sleep(0.0000001)
            self.tk_window.convert_tkimage(self.img)


def main():
    root = tk.Tk()
    tk_win = tk_window(root)

    size_x, size_y, channel = 1280, 720, 3
    window_size = (size_y, size_x, channel)
    Usingimshow = True
    cam_thread = Cam_Thread(tk_win, window_size=window_size, Usingimshow=Usingimshow)

    thread_img = threading.Thread(target=cam_thread.run_thread, args=())
    thread_img.daemon = True
    thread_img.start()

    root.mainloop()

if __name__ == "__main__":
    main()