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
turn = 0 # 0:black 1:white

# フラグ情報
game_start_flag = 0
read_flag = 0

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
    # ゲーム開始前の処理
    while game_start_flag == 0:
        res = s.recv(5)
        if res == b'START':
            print("Welcome Othello Game! please wait ...")
        elif res == b'PLAY0':
            print("Your color is \'black\'")
            player = 0
        elif res == b'PLAY1':
            print("Your color is \'white\'")
            player = 1
        elif res == b'MATCH':
            print("Matching success! Game start!")
            game_start_flag = 1
            time.sleep(0.5)

    # ボードの受信
    while read_flag == 0:
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
                    turn = player
                    read_flag = 1
                    break
                
        elif res == b'WAITN':
            print("Waiting others...")
            break
    
    # ボードの更新
    if turn == player:
        # テスト用
        if player == 0:
            clientBoard[1][1] = PlayerColor[PlayerNum.PLAYER1]
        if player == 1:
            clientBoard[1][1] = PlayerColor[PlayerNum.PLAYER2]
    
    # ボードの送信
    if turn == player:
        # サーバーへボードを送信
        sendBytes = pickle.dumps(clientBoard)
        s.send(sendBytes)

    # フラグを元に戻す
    read_flag = 0
    time.sleep(10)