import numpy as np
import cv2

# TODO :
# 1. drawing_keyboard 함수의 간소화 (완료)
# 2. 특정 키의 좌표 리턴용 함수 추가 (완료)

# class COLOR():
#     def __init__():
        

class Keyboard():
    def __init__(self, img=np.zeros((720,1280,3), np.uint8)):
        #모두 0으로 되어 있는 빈 canvas(검정색) - 크기는 현재 (720,1280,3)으로 설정해둠
        self.img = img   # 바탕 이미지 변수
        self.s = int(self.img.shape[0] * 0.0764)
        self.x = int(self.img.shape[1] * 0.172)
        self.y = self.img.shape[0] - int(self.img.shape[0] * 0.118) - (self.s * 5)
        self.key_list = ['`','1','2','3','4','5','6','7','8','9','0','-','=','backspace','\n',
                    'tab', 'Q','W','E','R','T','Y','U','I','O','P','[',']','\\','\n',
                    'caps_lock','A','S','D','F','G','H','J','K','L',';','\'','enter', '\n',
                    'shift','Z','X','C','V','B','N','M',',','.','/','shift', '\n',
                    'FN','ctrl','OPT','alt','space','Lng','OPT','left', 'up','down','right'
                    ]
        
    def get_image(self, img): # 이미지 업데이트 함수
        self.img = img
    
    def draw_key(self, key:str, bias_scaler:int=1.0, text_position_scaler:tuple=(0.5, 0.1), 
                boundary_color=(255,0,0), text_color=(255,0,0)):
        key_p = np.array([[self.x, self.y], [self.x + bias_scaler * self.s, self.y], [self.x + bias_scaler * self.s, self.y + self.s], [self.x, self.y + self.s]], np.int32)
        self.img = cv2.polylines(self.img, [key_p], True, boundary_color, 1) 
        point = int(self.x + (text_position_scaler[1] * self.s)), int(self.y + (text_position_scaler[0] * self.s))
        cv2.putText(self.img, str(key), point, cv2.FONT_HERSHEY_PLAIN, 1, text_color, 1, cv2.LINE_AA)
        self.x += (bias_scaler * self.s) + 2

    def get_keyposition(self, in_key:str):
        is_key_exist = False
        x = self.x
        y = self.y

        for key in self.key_list:
            scaler, diag_scaler = 1.0, 1.0
            if key != in_key:
                if key in ('\n','backspace','tab','caps_lock','enter','shift','space'): # if key in ('\n','BACK','TAP','CAPS','ENTER','SHIFT','SPACE'):
                    if key == '\n':
                        y += self.s + 2
                        x = self.x
                    elif key == 'backspace' or key == 'tab':
                        scaler = 1.5
                    elif key == 'caps_lock':
                        scaler = 1.75
                    elif key == 'enter':
                        scaler = 1.8
                    elif key == 'shift':
                        scaler = 2.31
                    elif key == 'space':
                        scaler = 4.7
                
                x += int(scaler * self.s) + 2

            else:
                is_key_exist = True
                if key in ('backspace','tab','caps_lock','enter','shift','space'):
                    if key == 'backspace' or key == 'tab':
                        diag_scaler = 1.5
                    elif key == 'caps_lock':
                        diag_scaler = 1.75
                    elif key == 'enter':
                        diag_scaler = 1.8
                    elif key == 'shift':
                        diag_scaler = 2.31
                    elif key == 'space':
                        diag_scaler = 4.7
                return is_key_exist, [[x, y], [x + int(diag_scaler * self.s), y + self.s]]

        return is_key_exist, [[0, 0], [0, 0]]


    def drawing_keyboard(self):
        #color 설정 
        blue_color= (255,0,0)
        
        #작성할 key 리스트로 작성
        

        #키보드가 시작할 위치 설정 (변경 시 27번 줄의 x 값도 같이 변경해야 줄바뀜 시 같이 바뀜)
        #x=220
        #y=350
        #키보드의 가로 세로 길이 size 설정
        #s=55

        #key_list의 key를 하나씩 불러와서 드로잉
        for key in self.key_list:
            bias_scaler = 1.0
            text_position_scaler = (0.5, 0.1)

            if key in ('\n','backspace','tab','caps_lock','enter','shift','space'):  #특수키 크기 조절
                if key == '\n':  #\n이면 줄바꿈
                    self.y += self.s+2
                    self.x = int(self.img.shape[1] * 0.172)
                
                elif key == 'backspace' or key == 'tab': #back, tap키, bias_scaler=1.5, text_position_scaler=(0.5, 0.1)
                    bias_scaler=1.5

                elif key == 'caps_lock': #caps키, bias_scaler=1.75, text_position_scaler=(0.5, 0.1)
                    bias_scaler=1.75

                elif key == 'enter': #enter키, bias_scaler=1.8, text_position_scaler=(0.5, 0.1)
                    bias_scaler=1.8

                elif key == 'shift': #shift키, bias_scaler=2.31, text_position_scaler=(0.5, 0.1)
                    bias_scaler=2.31

                elif key == 'space': #SPACE키, bias_scaler=4.7, text_position_scaler=(0.5, 1.9)
                    bias_scaler=4.7
                    text_position_scaler=(0.5, 1.9)

            #일반 사이즈 키 드로잉
            else:
                if len(key) <= 1:
                    text_position_scaler = (0.5, 0.5)

            if key != '\n':    
                self.draw_key(key=key, bias_scaler=bias_scaler, text_position_scaler=text_position_scaler)

        self.s = int(self.img.shape[0] * 0.0764)
        self.x = int(self.img.shape[1] * 0.172)
        self.y = self.img.shape[0] - int(self.img.shape[0] * 0.118) - (self.s * 5)

        return self.img

    def get_all_keyposition(self):
        points = dict()
        for key in self.key_list:
            if key != '\n':
                _, ret = self.get_keyposition(key)
                points[key] = ret

        return points

def main():
    kb = Keyboard()             # 키보드 클래스 가져오기
    kb.drawing_keyboard()       # 키보드 클래스의 drawing_keyboard 함수 사용
    # print(f"BACK : {kb.get_keyposition('BACK')}")
    # print(f"1 : {kb.get_keyposition('1')}")
    # print(f"M : {kb.get_keyposition('M')}")
    # print(f"BAC : {kb.get_keyposition('BAC')}")
    # print(kb.get_all_keyposition())

    cv2.imshow("1234", kb.img)  # 클래스 내부 이미지 변수를 이용하여 이미지 출력
    cv2.waitKey()               # 키 입력들어올때까지 대기
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

