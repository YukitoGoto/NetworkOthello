import socket
import pickle
from enum import IntEnum
import time

from ServerExample import Turn

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
clientBoard[3][3] = PlayerColor[PlayerNum.PLAYER1]
clientBoard[3][4] = PlayerColor[PlayerNum.PLAYER2]
clientBoard[4][3] = PlayerColor[PlayerNum.PLAYER2]
clientBoard[4][4] = PlayerColor[PlayerNum.PLAYER1]

# ネットワーク情報
PORT_NUM = 7010
BUFFER_SIZE = 4092
player = 0 # 0:black 1:white
Turn # 0:black 1:white

# フラグ情報
game_start_flag = 0
check_flag = 0

# Socketの作成
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# サーバーに接続を要求
s.connect((socket.gethostname(), PORT_NUM))

# メインループ
while True:
    # ゲーム開始フラグが立つまで、サーバーから応答メッセージ(5byteの固定長)を受信
    while game_start_flag == 0:
        res = s.recv(5)
        if res == b'START':
            print("Welcome Othello Game! please wait ...")
        elif res == b'PLAY1':
            print("Your color is \'black\'")
            player = 0
        elif res == b'PLAY2':
            print("Your color is \'white\'")
            player = 1
        elif res == b'MATCH':
            print("Matching success! Game start!")
            game_start_flag = 1
            time.sleep(0.5)

    while check_flag == 0:
        # サーバーからターン情報(5byte)を受信
        res = s.recv(5)
        # black_turn
        if res == b'TURNB':
            Turn = 0
        # white_turn
        if res == b'TURNW':
            Turn = 1
        # 受信対象のクライアントは受信準備完了をサーバーに知らせる
        if Turn == player:
            s.send("CHECK".encode("utf-8"))
            check_flag = 1
        elif Turn != player:
            print("Waiting others...")
            break
    
    # ターンが来ているクライアントはボードの送受信をする
    if Turn == player:
        # ボード受信
        receivedBytes = s.recv(BUFFER_SIZE)
        data = pickle.loads(receivedBytes)
        print(*data, sep = '\n')
        clientBoard = data
        # テスト用(ボード更新)
        if player == 0:
            clientBoard[1][1] = PlayerColor[PlayerNum.PLAYER1]
        elif player == 1:
            clientBoard[1][1] = PlayerColor[PlayerNum.PLAYER2]
        
        # ボード送信
        sendBytes = pickle.dumps(clientBoard)
        s.send(sendBytes)

        # フラグを元に戻す
        check_flag = 0
        time.sleep(3)