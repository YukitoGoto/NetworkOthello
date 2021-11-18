import socket
import pickle
from enum import IntEnum

# ゲーム情報
class PlayerNum(IntEnum):
	PLAYER1 = 1
	PLAYER2 = 2
PlayerColor = {
	PlayerNum.PLAYER1 : 'black',
	PlayerNum.PLAYER2 : 'white'
}
NUM_SQUARE = 8
serverBoard = [[None] * NUM_SQUARE for i in range(NUM_SQUARE)]

# ネットワーク情報
PORT_NUM = 7010
BUFFER_SIZE = 4092

# Socketの作成
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
# IPアドレス・Port番号をソケット割り当てる
s.bind((socket.gethostname(), PORT_NUM))
# Socketの待機状態
s.listen(5)

# クライアントからの要求を待つ
while True:
	# 要求があれば接続を確立して、ソケット・アドレスを代入
	clientSocket, addr = s.accept()
	print(addr)
	# クライアントからデータを受信
	receivedBytes = clientSocket.recv(BUFFER_SIZE)
	data = pickle.loads(receivedBytes)
	print(data)
	serverBoard = data
	# クライアントにデータを送信
	sendBytes = pickle.dumps(serverBoard)
	clientSocket.send(sendBytes)
	# ソケットを閉じて通信を切断
	clientSocket.close()
