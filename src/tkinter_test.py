import tkinter
from tkinter.constants import S

###(【ボタン】のところで使う関数)###
def osuna(event):
    Static2=tkinter.Label(text="押すなって言ったのに！",foreground="red")
    Static2.pack()
    Static2.place(x=20,y=110)


###【基本】ウィンドウ名とウィンドウのサイズを決定可能###

r=tkinter.Tk()
r.title(u"Othello")
r.geometry("400x400")

###【ラベル】任意の場所に文字列を表示できる###
Static1=tkinter.Label(text=u"test",foreground="#ff00ff",background="#00ff00")   #ラベルの基本設定 引数は前から(表示したいテキスト,文字色,文字の背景)
Static1.pack()                                                                  #表示
Static1.place(x=0,y=0)                                                          #表示する座標の設定

###【一行入力ボックス】改行のできない入力ボックスを作成できる###
Editbox=tkinter.Entry(width=50)                                                 #一行入力ボックスの基本設定 引数は(幅)
Editbox.insert(tkinter.END,"はじめから")                                        #はじめから文字を入れておく方法
Editbox.pack()
Editbox.place(x=0,y=40)                                                         #表示
value=Editbox.get()                                                             #入力した文字列の取得

###【ボタン】押されると何らかの動きを起こせる###
Button=tkinter.Button(text=u"押すな",width=30)                                  #ボタンの基本設定 引数は前から(ボタンに表示したいテキスト,幅)
Button.pack()                                                                   #表示
Button.place(x=0,y=80)
Button.bind("<Button-1>",osuna)                                                 #押されたら反応する関数を呼び出し "<Button-1>"は左クリック、"<Button-2>"にするとホイールクリック、"<Button-3>"にすると右クリックに反応する                                                
