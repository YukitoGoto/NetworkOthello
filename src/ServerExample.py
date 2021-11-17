import socket
import pickle
import threading
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
MAX_PLAYER = 2
NUM_SQUARE = 8
serverBoard = [[None] * NUM_SQUARE for i in range(NUM_SQUARE)]
Turn = 0 # 0:black 1:white

# ネットワーク情報
PORT_NUM = 7010
BUFFER_SIZE = 4092
PlayerNo = 0 # 0:black 1:white

# フラグ関連
game_start_flag = 0
send_flag = 0

def main_thread(clientSocket, PlayerNo):
	global game_start_flag
	global send_flag
	global Turn
	global serverBoard

	# ゲーム開始前の処理
	while game_start_flag == 0:
		clientSocket.send("START".encode("utf-8"))
		time.sleep(1)
		if PlayerNo == 0:
			clientSocket.send("PLAY1".encode("utf-8"))
			time.sleep(0.5)
		if PlayerNo == 1:
			clientSocket.send("PLAY2".encode("utf-8"))
			time.sleep(0.5)
		if PlayerNo == MAX_PLAYER - 1:
			game_start_flag = 1
		# 人数が集まるまで待機
		while True:
			# 人数が集まったら定型文を送り、ゲーム開始
			if game_start_flag == 1:
				clientSocket.send("MATCH".encode("utf-8"))
				time.sleep(1.0)
				break

	# ターン情報を送る,5byte
	if Turn == 0:
		clientSocket.send("TURNB".encode("utf-8"))
	elif Turn == 1:
		clientSocket.send("TURNW".encode("utf-8"))  
	
	# クライアントの受信準備確認が取れるまで待機
	while send_flag == 0:
		# ターンが来ていないクライアントはループを抜ける
		if Turn != PlayerNo:
			break
		else:
			res = clientSocket.recv(5)
			# 確認が取れればターンが来ているクライアントにボードを送信する
			if res == b'CHECK':
				sendBytes = pickle.dumps(serverBoard)
				clientSocket.send(sendBytes)
				send_flag = 1

	# ターンが来ているクライアントから受信,ボードを更新
	if Turn == PlayerNo:
		receivedBytes = clientSocket.recv(BUFFER_SIZE)
		data = pickle.loads(receivedBytes)
		print(*data, sep = '\n')
		serverBoard = data # 盤面更新

	# ターンを更新
	Turn = not Turn
	# フラグを元に戻す
	send_flag = 0

# Socketの作成
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# IPアドレス・Port番号をソケット割り当てる
s.bind((socket.gethostname(), PORT_NUM))

# Socketの待機状態
s.listen(MAX_PLAYER)

# クライアントからの要求を待つ
while True:
	try:
		# 要求があれば接続を確立して、ソケット・アドレスを代入
		clientSocket, addr = s.accept()
		print(addr)
	except KeyboardInterrupt:
		clientSocket.close()
		exit()
	# スレッド処理
	p = threading.Thread(target = main_thread, args = (clientSocket, PlayerNo))
	p.start()
	# クライアント番号を更新
	PlayerNo += 1
