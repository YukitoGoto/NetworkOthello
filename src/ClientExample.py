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
clientBoard[3][3] = PlayerColor[PlayerNum.PLAYER1]
clientBoard[3][4] = PlayerColor[PlayerNum.PLAYER2]
clientBoard[4][3] = PlayerColor[PlayerNum.PLAYER2]
clientBoard[4][4] = PlayerColor[PlayerNum.PLAYER1]

# ネットワーク情報
PORT_NUM = 7010
BUFFER_SIZE = 4092
player = 0 # 0:black 1:white

# フラグ情報
game_start_flag = 0
check_flag = 0
board_update_flag = 0

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
            # 盤面変更(テスト用)
            if player == 0:
                clientBoard[0][0] = PlayerColor[PlayerNum.PLAYER1]
            if player == 1:
                clientBoard[0][0] = PlayerColor[PlayerNum.PLAYER2]
            # 盤面送信
            sendBytes = pickle.dumps(clientBoard)
            s.send(sendBytes)
        # white_turn
        if res == b'TURNW':
            # 盤面変更(テスト用)
            if player == 0:
                clientBoard[0][0] = PlayerColor[PlayerNum.PLAYER1]
            if player == 1:
                clientBoard[0][0] = PlayerColor[PlayerNum.PLAYER2]
            # 盤面送信
            sendBytes = pickle.dumps(clientBoard)
            s.send(sendBytes)
        # 盤面更新が終わるまで待機
        while True:
            res = s.recv(5)
            # ターンが終了し、盤面更新が終わった場合
            if res == b'CHECK':
                # 次のターンのクライアントは盤面を受信する
                if turn_flag == 0:
                    receivedBytes = s.recv(BUFFER_SIZE)
                    data = pickle.loads(receivedBytes)
                    print(*data, sep = '\n')
                board_update_flag = 1
                # ループを抜ける
                break

        # クライアントのタイミングを同期させる
        if board_update_flag == 1:
            break

    # フラグを元に戻す
    check_flag = 0
    time.sleep(3)