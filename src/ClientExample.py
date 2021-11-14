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
clientBoard[1][5] = PlayerColor[PlayerNum.PLAYER1]
clientBoard[2][5] = PlayerColor[PlayerNum.PLAYER2]

# ネットワーク情報
PORT_NUM = 8888
BUFFER_SIZE = 4092


while True:
    # Socketの作成
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # サーバーに接続を要求
    s.connect((socket.gethostname(), PORT_NUM))
    # サーバーにデータを送信
    sendBytes = pickle.dumps(clientBoard)
    s.send(sendBytes)
    # サーバーからのデータを受信
    receivedBytes = s.recv(BUFFER_SIZE)
    data = pickle.loads(receivedBytes)
    print(data)
    time.sleep(3)
