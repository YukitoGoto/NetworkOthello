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
turn_end_flag = 0
gameoverflag = 0

# 実験用
cnt = 0

# threading
def main_thread(clientSocket, PlayerNo):
	global game_start_flag
	global turn_end_flag
	global gameoverflag
	global Turn
	global serverBoard
	global cnt # 実験用
	try:
		while gameoverflag == 0:
			# ゲーム開始前の処理
			while game_start_flag == 0:
				clientSocket.send("START".encode("utf-8"))
				time.sleep(1)
				if PlayerNo == 0:
					clientSocket.send("PLAY0".encode("utf-8"))
					time.sleep(0.5)
				if PlayerNo == 1:
					clientSocket.send("PLAY1".encode("utf-8"))
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

			# ターンかどうかの情報を送る,5byte
			if Turn == PlayerNo:
				clientSocket.send("TURNN".encode("utf-8"))
			else:
				clientSocket.send("WAITN".encode("utf-8"))  
			
			# ボードの送信
			if Turn == PlayerNo:
				sendBytes = pickle.dumps(serverBoard)
				clientSocket.send(sendBytes)
			
			# ボードの受信,更新
			while turn_end_flag == 0:
				if Turn == PlayerNo:
					while True:
						# クライアントからボードを受信
						receivedBytes = clientSocket.recv(BUFFER_SIZE)
						# 空でない場合は、ボードが送信されてきているので読み込む
						if isNotNULL(receivedBytes) == True:
							data = pickle.loads(receivedBytes)
							serverBoard = data
							print(*serverBoard, sep = '\n')
							turn_end_flag = 1
							break
			# 実験用
			if cnt >= 3:
				gameoverflag = 1
			else:
				# ターンを更新
				Turn = not Turn
				# フラグを初期化
				turn_end_flag = 0
				# 実験用
				cnt += 1
				
	except Exception as e:
		print(e)
	
	finally:
		clientSocket.close()

# 中身が空かどうか判別する
def isNotNULL(data):
	if len(data) != 0:
		return True
	else:
		return False

#メイン#

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
