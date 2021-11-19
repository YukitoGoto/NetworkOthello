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

# 中身が空かどうか判別する
def isNotNULL(data):
	if len(data) != 0:
		return True
	else:
		return False

# メインループ
while True:
    # Socketの作成
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # サーバーに接続を要求
    s.connect((socket.gethostname(), PORT_NUM))

    # サーバーにプレイヤー情報を伝える
    if game_start_flag == 1:
        if player == 0:
            s.send("BLACK".encode("utf-8"))
        elif player == 1:
            s.send("WHITE".encode("utf-8"))

    # ゲーム開始前の処理
    while game_start_flag == 0:
        res = s.recv(5)
        if res == b'START':
            print("Welcome Othello Game! please wait ...")
        elif res == b'BLACK':
            print("Your color is \'black\'")
            player = 0
        elif res == b'WHITE':
            print("Your color is \'white\'")
            player = 1
        elif res == b'MATCH':
            print("Matching success! Game start!")
            game_start_flag = 1
            time.sleep(0.5)

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
                        print(*clientBoard, sep = '\n')
                        turn_flag = True
                        read_flag = True
                        break
        elif res == b'WAITN':
            print("Waiting Others...")
            turn_flag = False
            break
    
    # ボードの更新
    if turn_flag == True:
        if player == 0:
            # ここから黒のオセロ処理
            clientBoard[1][1] = PlayerColor[PlayerNum.PLAYER1] #テスト用


        if player == 1:
            # ここから白のオセロ処理
            clientBoard[1][1] = PlayerColor[PlayerNum.PLAYER2] #テスト用

    # ボードの送信
    if turn_flag == True:
        sendBytes = pickle.dumps(clientBoard)
        s.send(sendBytes)

    # フラグを元に戻す
    read_flag = False
    time.sleep(0.5)

    # ターン終了の処理
    while True:
        res = s.recv(8)
        if res == b'GAMEOVER':
            s.send("CHECK".encode("utf-8"))
            while True:
                receivedBytes = s.recv(BUFFER_SIZE)
                if isNotNULL(receivedBytes) == True:
                        data = pickle.loads(receivedBytes)
                        clientBoard = data
                        print(*clientBoard, sep = '\n')
                        print("GAMEOVER")
                        time.sleep(5)
                        exit()
        elif res == b'NEXTTURN':
            break