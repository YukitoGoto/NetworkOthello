import socket
import pickle

# 横方向・縦方向のマスの数
NUM_SQUARE = 8

ip_address = '172.16.30.168'
port = 7010
buffer_size = 4092

PLAYER1 = 1
PLAYER2 = 2

color = {
	PLAYER1 : 'black',
	PLAYER2 : 'white'
}

board = [[None] * NUM_SQUARE for i in range(NUM_SQUARE)]

# Socketの作成
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
# IP Adress とPort番号をソケット割り当てる
s.bind((socket.gethostname(), port))
# Socketの待機状態
s.listen(5)

board[4][5] = color[PLAYER1]

# while Trueでクライアントからの要求を待つ
while True:
	# 要求があれば接続の確立とソケット、アドレスを代入
	clientSocket, addr = s.accept()
	msg = pickle.dumps(board)
	# データを送信する
	clientSocket.send(msg)
	clientSocket.close()
