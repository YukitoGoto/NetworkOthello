import tkinter
from tkinter.constants import S, Y
import socket
import pickle
from enum import IntEnum
import time

# ゲーム情報
class PlayerNum(IntEnum):
	PLAYER1 = 1
	PLAYER2 = 2
PlayerColor = {
	PlayerNum.PLAYER1 : 'black',
	PlayerNum.PLAYER2 : 'white'
}
NUM_SQUARE = 8
clientBoard = [[None] * NUM_SQUARE for i in range(NUM_SQUARE)]

# ネットワーク情報
PORT_NUM = 7010
BUFFER_SIZE = 4092
player = 0 # 0:black 1:white

# フラグ情報
game_start_flag = False
read_flag = False
turn_flag = False
pass_flag = False


# 中身が空かどうか判別する
def isNotNULL(data):
	if len(data) != 0:
		return True
	else:
		return False

def start_call():
    global player
    global game_start_flag
    global s
    # Socketの作成
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # サーバーに接続を要求
    s.connect((socket.gethostname(), PORT_NUM))

    # ゲーム開始前の処理
    while game_start_flag == 0:
        res = s.recv(5)
        if res == b'START':
            print("Welcome Othello Game! please wait ...")
        elif res == b'BLACK':
            print("Your color is \'black\'")
            player = 0
            your_color = "black"
            enemy_color = "white"

        elif res == b'WHITE':
            print("Your color is \'white\'")
            player = 1
            your_color = "white"
            enemy_color = "black"
        elif res == b'MATCH':
            print("Matching success! Game start!")
            game_start_flag = 1
            time.sleep(0.5)
        # サーバーにプレイヤー情報を伝える
    if player == 0:
        s.send("BLACK".encode("utf-8"))
    elif player == 1:
        s.send("WHITE".encode("utf-8"))

    return your_color,enemy_color

def turn_call():

    global s
    global read_flag
    global clientBoard
    global turn_flag

    if player == 0:
        s.send("BLACK".encode("utf-8"))
    elif player == 1:
        s.send("WHITE".encode("utf-8"))
    # ボードの受信
    while read_flag == False:
        # サーバーからターン情報(5byte)を受信
        res = s.recv(5)
        if res == b'TURNN':
                while True:
                    # サーバーからボードを受信
                    receivedBytes = s.recv(BUFFER_SIZE)
                    # 空でない場合は、ボードが送信されてきているので読み込む
                    if isNotNULL(receivedBytes) == True:
                        data = pickle.loads(receivedBytes)
                        clientBoard = data

                        turn_flag = True
                        read_flag = True
                        break
        elif res == b'WAITN':
            print("Waiting Others...")
            turn_flag = False
            break

    return clientBoard,turn_flag

def board_send(board):
    # ボードの更新
    clientBoard=board
    # パスかどうかの情報をサーバーに送る
    if turn_flag == True:
        if pass_flag == True:
            s.send("PASS".encode("utf-8"))
        else:
            s.send("DONE".encode("utf-8"))
    # ボードの送信
    if turn_flag == True:
        sendBytes = pickle.dumps(clientBoard)
        s.send(sendBytes)

def turn_end():

    global read_flag
    global pass_flag

    # フラグを元に戻す
    read_flag = False
    pass_flag = False
    time.sleep(1)
    while True:
        res = s.recv(8)
        if res == b'GAMEOVER':
            print("GAMEOVER")
            time.sleep(5)
            exit()
        elif res == b'NEXTTURN':
            break
