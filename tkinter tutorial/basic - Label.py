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

    label = tk.Label(window, text="Python", width=10, height=5, fg="red", relief="solid")
    label.pack()

    # Label Parameter을 통해서 다음과 같은 속성을 설정.
    # 문자열, 형태, 형식, 상태, 하이라이트
    # 

    # 생성된 윈도우 이름의 윈도우를 종료될때까지 실행
    window.mainloop() 


if __name__ == "__main__":
    main()