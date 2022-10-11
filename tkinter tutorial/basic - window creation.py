import tkinter as tk



def main():
    # 최상위 레벨의 윈도우 생성
    window = tk.Tk() 

    # 윈도우 타이틀
    window.title("test1")

    # 윈도우 너비, 높이, 초기위치
    # window.geometry("widthxheight+x+y")
    window.geometry("640x400+100+100")

    # 윈도우 창 크기조절 가능여부
    # window.resizable(vertical_bool, horizontal_bool)
    # window.resizable(False, False)
    window.resizable(True, True)


    # --- widget :: Lable ---

    # tkinter.label(위치할 윈도우, 입력할 텍스트)
    label = tk.Label(window, text="Hello world!")

    # tkinter.Label().pack() 위젯 배치
    # 별도 설정 안할 시 "기본 속성"으로 설정
    label.pack()



    # 생성된 윈도우 이름의 윈도우를 종료될때까지 실행
    window.mainloop() 


if __name__ == "__main__":
    main()