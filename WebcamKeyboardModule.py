from pynput.keyboard import Key, Controller
import HandTrackingModule as HTM
import KeyboardModule as KM
import cv2
import numpy as np
import time

class Webcam_keyboard(KM.Keyboard):
    def __init__(self, window_size) :
        super().__init__(window_size)

        self.cap = cv2.VideoCapture(0)
        self.controller = Controller()
        self.detector = HTM.handDetector()

        self.c_key = str()
        self.p_key = str()
        self.base_time = int()
        self.delta_time = int()

        self.Wait_time = 2000000000 # 2s in nano-seconds

        self.key_dict = {
            "backspace"     : Key.backspace,
            "tab"           : Key.tab,
            #"caps_lock"     : Key.caps_lock,
            "enter"         : Key.enter,
            #"shift"         : Key.shift,
            "ctrl"          : Key.ctrl,
            "space"         : Key.space,
            "alt"           : Key.alt,
            "left"          : Key.left,
            "right"         : Key.right,
            "up"            : Key.up,
            "down"          : Key.down
        }

        self.pTime = 0
        self.cTime = 0

        self.isFlipped = True
        self.is_inBoundary = False
        
        self.lmList = []
        self.diag_points = self.get_diag_keyposition()

    def run_keyboard(self, Usingimshow):
        self.Usingimshow = Usingimshow
        if self.cap.isOpened():
            ret, self.img = self.cap.read()
            self.img = cv2.resize(self.img, (self.window_size[1], self.window_size[0]))
            self.img_Flip()
            self.detector.findHands(self.img)
            self.lmList = self.detector.findPosition(
                self.img, realscale=True, 
                windowsize=[self.window_size[1], self.window_size[0]]
            )

            # 클래스 내부에서 작동하기 때문에 이미지 업데이트과정이 불필요
            # self.get_image(self.img) 

            if ret:
                if len(self.lmList) != 0:
                    # --- boundary condition ---
                    self.check_boundary()

                    # --- To measure how long the c_key keeps ---
                    self.check_ckey_Keeps()

                # --- Draw Keyboard ---
                self.drawing_keyboard()

                # --- Draw FPS rate ---
                self.draw_fps_rate()

        #         # --- Run OpenCV window ---
        #         self.run_CV_window(Usingimshow)
        # if Usingimshow:
        #     cv2.destroyAllWindows()

    def run_CV_window(self):
        if self.Usingimshow:
            cv2.imshow("test", self.img)
            if cv2.waitKey(1) != -1:
                return True
            else :
                return False

    def draw_fps_rate(self):
        self.cTime = time.time()
        fps = 1/(self.cTime-self.pTime)
        self.pTime = self.cTime
        cv2.putText(
            self.img, str(int(fps)) + "FPS", (10, 70), 
            cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3 )

    def check_ckey_Keeps(self):
        if self.c_key != self.p_key:
            self.p_key = self.c_key
            self.base_time = 0
            self.delta_time = 0
        
        elif self.is_inBoundary :
            temp = time.time_ns()
            if self.delta_time == 0:
                self.delta_time = temp
            else :
                self.base_time += temp - self.delta_time
            
            if self.base_time > self.Wait_time:
                try:
                    print(f"try block : c_key = {self.c_key}")
                    self.controller.press(self.c_key)
                    self.controller.release(self.c_key)
                except ValueError:
                    if self.c_key in ('Lng', 'shift_l', 'shift_r', 'caps_lock', 'OPT_l', 'OPT_r'):
                        print("Key Changed!")
                        self.change_key(self.c_key)
                        self.diag_points = self.get_diag_keyposition()
                    else :
                        print(f"except block : c_key = {self.c_key}")
                        self.controller.press(self.key_dict[self.c_key])
                        self.controller.release(self.key_dict[self.c_key])
                except:
                    pass

                self.base_time  = 0
                self.delta_time = 0



    def check_boundary(self):
        for key, points in self.diag_points.items():
            if (points[0][0] < self.lmList[8][1]) and (self.lmList[8][1] < points[1][0]) :
                    if (points[0][1] < self.lmList[8][2]) and (self.lmList[8][2] < points[1][1]) :
                            self.c_key = key
                            self.is_inBoundary = True
                            break
                    else:
                        self.is_inBoundary = False
            else:
                self.is_inBoundary = False
        return self.is_inBoundary


    def img_Flip(self):
        if self.isFlipped:
            self.img = cv2.flip(self.img, 1)




def main():
    size_x, size_y, channel_ = 1280, 720, 3
    webcam_keyboard = Webcam_keyboard(window_size=(size_y, size_x, channel_))
    Usingimshow = True

    while True:
        webcam_keyboard.run_keyboard(Usingimshow)
        if webcam_keyboard.run_CV_window():
            break

if __name__ == "__main__":
    main()

