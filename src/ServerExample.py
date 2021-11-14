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

# ネットワーク情報
PORT_NUM = 7010
BUFFER_SIZE = 4092
PlayerNo = 0 #クライアントの番号

# フラグ関連
game_start_flag = 0
turn_flag = 1
board_update_flag = 0
ack_flag = 0

def main_thread(clientSocket, PlayerNo):
	global game_start_flag
	global turn_flag
	global board_update_flag
	global ack_flag
	global serverBoard

	# ゲーム開始前の処理
	try:
		while game_start_flag == 0:
			clientSocket.send("START".encode("utf-8"))
			time.sleep(1)
			if PlayerNo == 1:
				clientSocket.send("PLAY1".encode("utf-8"))
				time.sleep(0.5)
			if PlayerNo == 2:
				clientSocket.send("PLAY2".encode("utf-8"))
				time.sleep(0.5)
			if PlayerNo == MAX_PLAYER:
				game_start_flag = 1

			# 人数が集まるまで待機
			while True:
				# 人数が集まったら定型文を送り、ゲーム開始
				if game_start_flag == 1:
					clientSocket.send("MATCH".encode("utf-8"))
					time.sleep(1.0)
					break
		# ターン情報を送る,5byte
		if turn_flag == PlayerNo:
			clientSocket.send("TURNN".encode("utf-8"))
			receivedBytes = clientSocket.recv(BUFFER_SIZE)
			data = pickle.loads(receivedBytes)
			print(*data, sep = '\n')
			serverBoard = data # 盤面更新
			board_update_flag = 1 #フラグを立てる
		else:
			clientSocket.send("WAITN".encode("utf-8"))
		
		# 盤面更新まで待機
		while True:
			# 更新終了の合図を次のターンのクライアントに送信
			if board_update_flag == 1:
				clientSocket.send("CHECK".encode("utf-8"))
				break

		# 次のターンのクライアントに盤面を送信
		if turn_flag != PlayerNo:
			sendBytes = pickle.dumps(serverBoard)
			clientSocket.send(sendBytes)
	
		# ターンを切り替える
		if turn_flag == 1:
			turn_flag = 2
		elif turn_flag == 2:
			turn_flag = 1

		#フラグを元に戻す
		board_update_flag = 0
		ack_flag = 0
	finally:
    		clientSocket.close()

# Socketの作成
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# IPアドレス・Port番号をソケット割り当てる
s.bind((socket.gethostname(), PORT_NUM))
# Socketの待機状態
s.listen(MAX_PLAYER)

# クライアントからの要求を待つ
while True:
	try:
		# クライアント番号を更新
		PlayerNo += 1
		# 要求があれば接続を確立して、ソケット・アドレスを代入
		clientSocket, addr = s.accept()
		print(addr)
	except KeyboardInterrupt:
		clientSocket.close()
		exit()
	# スレッド処理
	p = threading.Thread(target = main_thread, args = (clientSocket, PlayerNo))
	p.start()
