import tkinter
from tkinter.constants import S

board= [[None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,"black","white",None,None,None],
        [None,None,None,"white","black",None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None]]

def leftClick(event):
    cliy=event.x//50
    clix=event.y//50
    board_rename(clix,cliy)
    cirdrow()

def board_rename(x,y):
    board[x][y]="white"

def cirdrow():
    for i in range(len(board)):
        for j in range(len(board[i])):
            xs=j*50+5
            ys=i*50+5
            xe=j*50+45
            ye=i*50+45
            if(board[i][j]=="white"):
                canvas.create_oval(xs,ys,xe,ye,width=1.0,fill="white")
            if(board[i][j]=="black"): 
                canvas.create_oval(xs,ys,xe,ye,width=1.0,fill="black")



###【基本】ウィンドウ名とウィンドウのサイズを決定可能###

r=tkinter.Tk()
r.title(u"Othello")
r.geometry("400x400")

###【キャンバス】ウィンドウ上に線、円、塗りつぶしなどを描画###
#以下コメントアウトを外すとオセロの盤面みたいなのが描画される

canvas=tkinter.Canvas(r,width=400,height=400)                                 #キャンバスの大きさを決定 
canvas.create_rectangle(0,0,400,400,fill="green")                             #塗りつぶし 引数は前から(塗りつぶしスタート地点のx座標,y座標,塗りつぶし終わり地点のx座標,y座標,fill=に入れた色に塗りつぶし)
for i in range(8):
   canvas.create_line(50*i,0,50*i,400,fill="black",width=2.0)                 #線の描画 引数は前から(線のスタート地点のx座標...で塗りつぶしと同じ感じ)
   canvas.create_line(0,50*i,400,50*i,fill="black",width=2.0)
canvas.place(x=0,y=0)
cirdrow()
canvas.bind("<ButtonPress-1>",leftClick)
r.mainloop()