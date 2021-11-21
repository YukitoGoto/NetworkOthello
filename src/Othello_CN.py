import tkinter

import ClientExample

BOARD_SIZE=8


board= [[None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,"black","white",None,None,None],
        [None,None,None,"white","black",None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None]]

your_color,enemy_color=ClientExample.start_call()

turnflg=False
passflg=False
isGameover=False

def leftClick(event):

    global your_color
    global enemy_color
    global placeableflg
    global gameover_cnt
    global turnflg
    
    if(isGameover==False):
        if(turnflg==True):

            clix=event.x//50
            cliy=event.y//50
            putflg=False
            placeableflg=True
            gameover_cnt=0

            if(board[clix][cliy]==None):
                putflg=reverse_check(clix,cliy)

            if(putflg):
                board_rename(clix,cliy)
                turnflg=False
                r.after(100,r_quit)
                othello_board_draw()
                circle_draw()

def reverse_check(clix,cliy):
    putflg=False
    for i in range(-1,2):
        for j in range(-1,2):
            check_x=clix+j
            check_y=cliy+i
            cnt=1
            if(i==0 and j==0):
                pass
            elif(outrange_check(check_x,check_y)==False):
                pass
            elif(board[check_x][check_y]==enemy_color):
                while(outrange_check(check_x+j,check_y+i) and board[check_x+j][check_y+i]==enemy_color):
                    check_x+=j
                    check_y+=i
                    cnt+=1
                if(outrange_check(check_x+j,check_y+i)==False):
                    pass
                elif(board[check_x+j][check_y+i]==your_color):
                    putflg=True
                    if(placeableflg):
                        for rev in range(0,cnt):
                            board_rename(check_x,check_y)
                            check_x-=j
                            check_y-=i
    return putflg

def outrange_check(x,y):
    orflg=True
    if(x>=BOARD_SIZE or x<0 or y>=BOARD_SIZE or y<0):
        orflg=False
    return orflg

def board_rename(x,y):
    board[x][y]=your_color

def othello_board_draw():
    canvas.create_rectangle(0,0,400,400,fill="green")                             #塗りつぶし 引数は前から(塗りつぶしスタート地点のx座標,y座標,塗りつぶし終わり地点のx座標,y座標,fill=に入れた色に塗りつぶし)
    for i in range(8):
        canvas.create_line(50*i,0,50*i,400,fill="black",width=2.0)                 #線の描画 引数は前から(線のスタート地点のx座標...で塗りつぶしと同じ感じ)
        canvas.create_line(0,50*i,400,50*i,fill="black",width=2.0)

def circle_draw():
    for i in range(len(board)):
        for j in range(len(board[i])):
            xs=j*50+5
            ys=i*50+5
            xe=j*50+45
            ye=i*50+45
            if(board[j][i]=="white"):
                canvas.create_oval(xs,ys,xe,ye,width=1.0,fill="white")
            if(board[j][i]=="black"):
                canvas.create_oval(xs,ys,xe,ye,width=1.0,fill="black")

def putablecheck():
    global gameover_cnt
    global passflg
    passflg=True
    for putable_y in range(len(board)):
        for putable_x in range(len(board[putable_y])):
            if(board[putable_x][putable_y]==None):
                putable=reverse_check(putable_x,putable_y)
                if(putable):
                    passflg=False
                    xs=putable_x*50
                    ys=putable_y*50
                    xe=(putable_x+1)*50
                    ye=(putable_y+1)*50
                    canvas.create_rectangle(xs,ys,xe,ye,fill="yellow")
    if(passflg):
        global your_color
        global enemy_color
        global Static2

        Static2=tkinter.Label(text=str(your_color)+" pass...",foreground="black",background="white")   #ラベルの基本設定 引数は前から(表示したいテキスト,文字色,文字の背景)
        Static2.pack()                                                                                 #表示
        Static2.place(x=500,y=100)

        r.after(1000,passdel)

def passdel():
    Static2.place_forget()
    r.quit()

def yourturn_draw():
    Static1=tkinter.Label(text="your_turn",foreground="black",background="white")   #ラベルの基本設定 引数は前から(表示したいテキスト,文字色,文字の背景)
    Static1.pack()                                                                  #表示
    Static1.place(x=500,y=100)
    

def r_quit():
    r.quit()
###【基本】ウィンドウ名とウィンドウのサイズを決定可能###
r=tkinter.Tk()
r.title(u"Othello"+str(your_color)) 
r.geometry("600x400")

while isGameover==False:

###【キャンバス】ウィンドウ上に線、円、塗りつぶしなどを描画###
    
    canvas=tkinter.Canvas(r,width=400,height=400)                                 #キャンバスの大きさを決定 
    canvas.place(x=0,y=0)
    
    othello_board_draw()
    # yourturn_draw()
    board,turnflg=ClientExample.turn_call()
    print(turnflg)
    if turnflg:
        placeableflg=False
        putablecheck()
        circle_draw()
        canvas.bind("<ButtonPress-1>",leftClick)
        r.mainloop()

    ClientExample.board_send(board,passflg)
    ClientExample.turn_end()