# test file for interlocking threading and tkinter module

# TODO
# run test3.py on tkinter window (미해결)


from pynput.keyboard import Key, Controller
import HandTrackingModule as HTM
import KeyboardModule as KM
import cv2
import numpy as np
import time


size_x, size_y = 1280, 720

cap = cv2.VideoCapture(0)
kb_layout = KM.Keyboard(window_size=(size_y, size_x, 3))
controller = Controller()
detector = HTM.handDetector()

c_key = str()
p_key = str()
base_time = int()
delta_time = int()

Wait_time = 2000000000 # 2s in ns


key_dict = {
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

pTime = 0                       # previous time
cTime = 0                       # current time



isFlipped = True
all_key_points = kb_layout.get_diag_keyposition()
is_in_boundary = False

# print(points)
if cap.isOpened():
    while True:
        success, img = cap.read()
        img = cv2.resize(img, (size_x, size_y))

        if isFlipped:
            img = cv2.flip(img, 1)

        detector.findHands(img)
        lmList = detector.findPosition(img, realscale=True, windowsize=[size_x, size_y])

        kb_layout.get_image(img)

        
        if len(lmList) != 0:
            # --- boundary condition ---
            for key, points in all_key_points.items():
                if (points[0][0] < lmList[8][1]) and (lmList[8][1] < points[1][0]) :
                    if (points[0][1] < lmList[8][2]) and (lmList[8][2] < points[1][1]) :
                        try :
                            c_key = key
                            is_in_boundary = True
                            break
                            # controller.press(key)
                            # controller.release(key)
                            
                        except ValueError :
                            print(f"special key : {key}")
                            # controller.press(key_dict[key])
                            # controller.release(key_dict[key])
                        
                else:
                    is_in_boundary = False

            # --- To measure how long the c_key keeps ---
            if c_key != p_key: #손가락이 계속 움직이는 경우 초기화 하며 basetime 초기화
                p_key = c_key
                base_time = 0
                delta_time = 0
                
            elif is_in_boundary: #손가락이 계속 한키에 머물러 있을경우
                temp = time.time_ns()
                if delta_time == 0:
                    delta_time = temp
                else :
                    base_time += temp - delta_time

                
                if base_time > Wait_time:
                    try:
                        print(f"try block : c_key = {c_key}")
                        controller.press(c_key)
                        controller.release(c_key)

                    except ValueError:
                        if c_key in ('Lng', 'shift_l', 'shift_r', 'caps_lock', 'OPT_l', 'OPT_r'):
                            print("changed key!")
                            kb_layout.change_key(c_key)
                            all_key_points = kb_layout.get_diag_keyposition()
                        else :
                            print(f"except block : c_key = {c_key}")
                            controller.press(key_dict[c_key])
                            controller.release(key_dict[c_key])
                    except :
                        pass
                    
                    base_time = 0
                    delta_time = 0

        
        # --- Draw keyboard ---
        img = kb_layout.drawing_keyboard()

        # --- Draw FPS rate ---
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)) + "FPS", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3 )

        # --- Run OpenCV window ---
        cv2.imshow("test3", img)
        if cv2.waitKey(1) != -1:
            break

cv2.destroyAllWindows()

