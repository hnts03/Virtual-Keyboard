from pynput.keyboard import Key, Controller
import HandTrackingModule as HTM
import KeyboardModule as KM
import cv2
import numpy as np
import time

# Changes (10.25)
# 1. Single handed -> Multi Handed
# 2. New function added
#       * Webcam_keyboard.check_ckey_Keeps_base()
#           -> module function for Webcam_keyboard.check_ckey_Keeps()
#       * Webcam_keyboard.check_boundary_base()
#           -> module function for Webcam_keyboard.check_boundary()
# 3. Existing function changes
#       * Webcam_keyboard.run_keyboard()
#           -> Working condition added <- number of hands
#       * Webcam_keyboard.check_ckey_Keeps()
#           -> simplified with module function
#       * Webcam_keyboard.check_boundary()
#           -> simplified with module function



class Webcam_keyboard(KM.Keyboard):
    def __init__(self, window_size) :
        super().__init__(window_size)

        self.cap = cv2.VideoCapture(0)
        self.controller = Controller()
        self.detector = HTM.handDetector()

        self.c_key = [str(), str()]
        self.p_key = [str(), str()]
        self.base_time = [int(), int()]
        self.delta_time = [int(), int()]

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
        self.is_inBoundary = [False, False]
        
        self.lmList = []
        self.diag_points = self.get_diag_keyposition()

    def run_keyboard(self, Usingimshow):
        self.Usingimshow = Usingimshow
        if self.cap.isOpened():
            ret, self.img = self.cap.read()
            self.img = cv2.resize(self.img, (self.window_size[1], self.window_size[0]))
            self.img_Flip()

            ###########################################
            ## Code Position for gesture recognition ##
            ###########################################

            self.detector.findHands(self.img)
            self.lmList = self.detector.findPosition(
                self.img, realscale=True, 
                windowsize=[self.window_size[1], self.window_size[0]]
            )
            
            # 클래스 내부에서 작동하기 때문에 이미지 업데이트과정이 불필요
            # self.get_image(self.img) 

            if ret:
            # 손이 두개인 경우와 한개인 경우 분기
                # 손이 1개인 경우
                if len(self.lmList) == 1:
                    hand_num = 1
                
                # 손이 2개인 경우
                elif len(self.lmList) == 2:
                    hand_num = 2
                
                # 손이 0개 혹은 3개 이상 나오는 경우
                else :
                    pass

                if len(self.lmList) != 0:
                    # --- boundary condition ---
                    self.check_boundary(hand_num=hand_num)

                    # --- To measure how long the c_key keeps ---
                    self.check_ckey_Keeps(hand_num=hand_num)

                # --- Draw Keyboard ---
                self.drawing_keyboard()

                # --- Draw FPS rate ---
                self.draw_fps_rate()



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

    def check_ckey_Keeps_base(self, iter):
        if self.c_key[iter] != self.p_key[iter]:
                self.p_key[iter] = self.c_key[iter]
                self.base_time[iter] = 0
                self.delta_time[iter] = 0

        elif self.is_inBoundary[iter] :
            temp = time.time_ns()
            if self.delta_time[iter] == 0:
                self.delta_time[iter] = temp

            else :
                self.base_time[iter] += temp - self.delta_time[iter]
            
            if self.base_time[iter] > self.Wait_time:
                print(f'iter = {iter}, base_time = {self.base_time[iter]}')
                try:
                    print(f"try block : c_key = {self.c_key[iter]}")
                    self.controller.press(self.c_key[iter])
                    self.controller.release(self.c_key[iter])
                except ValueError:
                    if self.c_key in ('Lng', 'shift_l', 'shift_r', 'caps_lock', 'OPT_l', 'OPT_r'):
                        print("Key Changed!")
                        self.change_key(self.c_key[iter])
                        self.diag_points = self.get_diag_keyposition()
                    else :
                        print(f"except block : c_key = {self.c_key[iter]}")
                        self.controller.press(self.key_dict[self.c_key[iter]])
                        self.controller.release(self.key_dict[self.c_key[iter]])
                except:
                    pass

                self.base_time[iter]  = 0
                self.delta_time[iter] = 0

    def check_ckey_Keeps(self, hand_num=1):
        if hand_num == 1:
            self.check_ckey_Keeps_base(iter=hand_num-1)

        elif hand_num == 2:
            for i in range(hand_num):
                self.check_ckey_Keeps_base(iter=i)
        else :
            pass


    def check_boundary_base(self, iter=1):
        for key, points in self.diag_points.items():
                if (points[0][0] < self.lmList[iter][8][1]) and (self.lmList[iter][8][1] < points[1][0]) :
                        if (points[0][1] < self.lmList[iter][8][2]) and (self.lmList[iter][8][2] < points[1][1]) :
                                self.c_key[iter] = key
                                self.is_inBoundary[iter] = True
                                break
                        else:
                            self.is_inBoundary[iter] = False
                else:
                    self.is_inBoundary[iter] = False

    def check_boundary(self, hand_num=1):
        if hand_num == 1:
            self.check_boundary_base(iter=hand_num-1)
            return self.is_inBoundary

        elif hand_num == 2 :
            for i in range(hand_num):
                self.check_boundary_base(iter=i)
            return self.is_inBoundary

        else :
            pass

    def img_Flip(self):
        if self.isFlipped:
            self.img = cv2.flip(self.img, 1)




def __main():
    size_x, size_y, channel_ = 1280, 720, 3
    webcam_keyboard = Webcam_keyboard(window_size=(size_y, size_x, channel_))
    Usingimshow = True

    while True:
        webcam_keyboard.run_keyboard(Usingimshow)
        if webcam_keyboard.run_CV_window():
            break

if __name__ == "__main__":
    __main()

