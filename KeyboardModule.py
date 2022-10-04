import numpy as np
import cv2

# TODO :
# 1. drawing_keyboard 함수의 간소화
# 2. 특정 키의 좌표 리턴용 함수 추가


class Keyboard():
    def __init__(self, img=np.zeros((720,1280,3), np.uint8)):
        #모두 0으로 되어 있는 빈 canvas(검정색) - 크기는 현재 (720,1280,3)으로 설정해둠
        self.img = img   # 바탕 이미지 변수
        self.s = int(self.img.shape[0] * 0.0764)
        self.x = int(self.img.shape[1] * 0.172)
        self.y = self.img.shape[0] - int(self.img.shape[0] * 0.118) - (self.s * 5)
        

    def get_image(self, img): # 이미지 업데이트 함수
        self.img = img

    def drawing_keyboard(self):
        #color 설정 
        blue_color= (255,0,0)
        
        #작성할 key 리스트로 작성
        key_list = ['`','1','2','3','4','5','6','7','8','9','0','-','=','BACK','\n',
                    'TAP', 'Q','W','E','R','T','Y','U','I','O','P','[',']','\\','\n',
                    'CAPS','A','S','D','F','G','H','J','K','L',';','\'','ENTER', '\n',
                    'SHIFT','Z','X','C','V','B','N','M',',','.','/','SHIFT', '\n',
                    'FN','CTR','OPT','ALT','SPACE','Lng','OPT','<', '^','v','>'
                    ]

        #키보드가 시작할 위치 설정 (변경 시 27번 줄의 x 값도 같이 변경해야 줄바뀜 시 같이 바뀜)
        #x=220
        #y=350
        #키보드의 가로 세로 길이 size 설정
        #s=55

        #key_list의 key를 하나씩 불러와서 드로잉
        for key in key_list:
            if key in ('\n','BACK','TAP','CAPS','ENTER','SHIFT','SPACE'):  #특수키 크기 조절
                if key == '\n':  #\n이면 줄바꿈
                    self.y += self.s+2
                    self.x = 220
                
                elif key == 'BACK': #back키 길이 1.5배
                    key_p = np.array([[self.x,self.y], [self.x+1.5*self.s, self.y], [self.x+1.5*self.s, self.y+self.s], [self.x, self.y+self.s]], np.int32)
                    self.img = cv2.polylines(self.img,[key_p], True, blue_color, 1) 
                    point = int(self.x + (0.1*self.s)), int(self.y + (0.5*self.s))
                    cv2.putText(self.img, str(key), point, cv2.FONT_HERSHEY_PLAIN, 1, blue_color, 1 ,cv2.LINE_AA)
                    self.x += (1.5*self.s)+2
                
                elif key == 'TAP': #tap키 길이 1.5배
                    key_p = np.array([[self.x,self.y], [self.x+1.5*self.s, self.y], [self.x+1.5*self.s, self.y+self.s], [self.x, self.y+self.s]], np.int32)
                    self.img = cv2.polylines(self.img,[key_p], True, blue_color, 1) 
                    point = int(self.x + (0.1*self.s)), int(self.y + (0.5*self.s))
                    cv2.putText(self.img, str(key), point, cv2.FONT_HERSHEY_PLAIN, 1, blue_color, 1,cv2.LINE_AA)
                    self.x += (1.5*self.s)+2

                elif key == 'CAPS': #caps키 길이 1.75배
                    key_p = np.array([[self.x,self.y], [self.x+1.75*self.s, self.y], [self.x+1.75*self.s, self.y+self.s], [self.x, self.y+self.s]], np.int32)
                    self.img = cv2.polylines(self.img,[key_p], True, blue_color, 1) 
                    point = int(self.x + (0.1*self.s)), int(self.y + (0.5*self.s))
                    cv2.putText(self.img, str(key), point, cv2.FONT_HERSHEY_PLAIN, 1, blue_color, 1 ,cv2.LINE_AA)
                    self.x += (1.75*self.s)+2

                elif key == 'ENTER': #enter키 길이 1.8배
                    key_p = np.array([[self.x,self.y], [self.x+1.8*self.s, self.y], [self.x+1.8*self.s, self.y+self.s], [self.x, self.y+self.s]], np.int32)
                    self.img = cv2.polylines(self.img,[key_p], True, blue_color, 1) 
                    point = int(self.x + (0.1*self.s)), int(self.y + (0.5*self.s))
                    cv2.putText(self.img, str(key), point, cv2.FONT_HERSHEY_PLAIN, 1, blue_color, 1 ,cv2.LINE_AA)
                    self.x += (1.8*self.s)+2

                elif key == 'SHIFT': #shift키 길이 2.31배
                    key_p = np.array([[self.x,self.y], [self.x+2.31*self.s, self.y], [self.x+2.31*self.s, self.y+self.s], [self.x, self.y+self.s]], np.int32)
                    self.img = cv2.polylines(self.img,[key_p], True, blue_color, 1) 
                    point = int(self.x + (0.1*self.s)), int(self.y + (0.5*self.s))
                    cv2.putText(self.img, str(key), point, cv2.FONT_HERSHEY_PLAIN, 1, blue_color, 1 ,cv2.LINE_AA)
                    self.x += (2.31*self.s)+2

                elif key == 'SPACE': #SPACE키 길이 4.7배
                    key_p = np.array([[self.x,self.y], [self.x+4.7*self.s, self.y], [self.x+4.7*self.s, self.y+self.s], [self.x, self.y+self.s]], np.int32)
                    self.img = cv2.polylines(self.img,[key_p], True, blue_color, 1) 
                    point = int(self.x + (1.9*self.s)), int(self.y + (0.5*self.s))
                    cv2.putText(self.img, str(key), point, cv2.FONT_HERSHEY_PLAIN, 1, blue_color, 1 ,cv2.LINE_AA)
                    self.x += (4.7*self.s)+2

            #일반 사이즈 키 드로잉
            else:
                #키 좌표 point 설정
                key_p = np.array([[self.x,self.y], [self.x+self.s, self.y], [self.x+self.s, self.y+self.s], [self.x, self.y+self.s]], np.int32)
                #img1위에 그리기 polylines(이미지, [좌표], 닫힌(true), 색상, 두께)
                self.img = cv2.polylines(self.img,[key_p], True, blue_color, 1)

                #key텍스트 넣을 좌표 설정(각 사각형의 가운데 좌표)
                if len(key) > 1:
                    point = int(self.x + (0.1*self.s)), int(self.y + (0.5*self.s))
                else:
                    point = int(self.x + (0.5*self.s)), int(self.y + (0.5*self.s))

                #텍스트 넣기 putText(이미지, 텍스트 내용, 좌표, 폰트 종류 설정, 크기, 색상, 두께, 선종류)
                cv2.putText(self.img, str(key), point, cv2.FONT_HERSHEY_PLAIN, 1, blue_color, 1 ,cv2.LINE_AA)

                #x 값 업데이트해서 다음 키 작성할 x 위치 업데이트 - 현재 2 정도 띄어서 키보드 작성하도록 함
                self.x += self.s+2


         


def main():
    kb = Keyboard()             # 키보드 클래스 가져오기
    kb.drawing_keyboard()       # 키보드 클래스의 drawing_keyboard 함수 사용

    cv2.imshow("1234", kb.img)  # 클래스 내부 이미지 변수를 이용하여 이미지 출력
    cv2.waitKey()               # 키 입력들어올때까지 대기
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

