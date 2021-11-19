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
game_start_flag = False
gameoverflag = False
p0connect_flag = False
p1connect_flag = False
p0turnend_flag = False
p1turnend_flag = False

# threading
def main_thread(clientSocket, PlayerNo):
	global game_start_flag
	global gameoverflag
	global Turn
	global serverBoard
	global p0turnend_flag
	global p1turnend_flag
	global p0connect_flag
	global p1connect_flag
	try:
		while True:
			# クライアントからプレイヤー情報を受け取る
			if game_start_flag == True:
				while True:
					res = clientSocket.recv(5)
					if res == b'BLACK':
						PlayerNo = 0
						# ターン終了時のフラグを初期化
						p0turnend_flag = False
						p0connect_flag = True
						break
					elif res == b'WHITE':
						PlayerNo = 1
						# ターン終了時のフラグを初期化
						p1turnend_flag = False
						p1connect_flag = True
						break

				# 両方の接続が確認できるまで待機
				while True:
					if p0connect_flag == True & p1connect_flag == True:
						break

			# ゲーム開始前の処理
			while game_start_flag == False:
				clientSocket.send("START".encode("utf-8"))
				time.sleep(1)
				if PlayerNo == 0:
					clientSocket.send("BLACK".encode("utf-8"))
					time.sleep(0.5)
				if PlayerNo == 1:
					clientSocket.send("WHITE".encode("utf-8"))
					time.sleep(0.5)
				if PlayerNo == MAX_PLAYER - 1:
					game_start_flag = True
				# 人数が集まるまで待機
				while True:
					# 人数が集まったら定型文を送り、ゲーム開始
					if game_start_flag == True:
						clientSocket.send("MATCH".encode("utf-8"))
						time.sleep(1.0)
						break

			# ターンかどうかの情報を送る,5byte
			if Turn == PlayerNo:
				clientSocket.send("TURNN".encode("utf-8"))
			elif Turn != PlayerNo:
				clientSocket.send("WAITN".encode("utf-8"))

			# ターンが来ているプレイヤーとボードの送受信
			if Turn == PlayerNo:
				# ボードの送信
				sendBytes = pickle.dumps(serverBoard)
				clientSocket.send(sendBytes)
				# ボードの受信
				while True:
						receivedBytes = clientSocket.recv(BUFFER_SIZE)
						# 空でない場合は、ボードが送信されてきているので読み込む
						if isNotNULL(receivedBytes) == True:
							data = pickle.loads(receivedBytes)
							serverBoard = data
							print(*serverBoard, sep = '\n')
							# ターンを経過させる
							if Turn == 0:
								Turn = 1
							elif Turn == 1:
								Turn = 0
							p0turnend_flag = True 
							break
			else:
				p1turnend_flag = True

			# ターン終了後の処理
			while True:
				if p0turnend_flag == True & p1turnend_flag == True:
					# ターン開始時のフラグを初期化
					if PlayerNo == 0:
						p0connect_flag = False
					elif PlayerNo == 1:
						p1connect_flag = False
					# ゲームオーバー処理
					if gameoverflag == True:
						clientSocket.send("GAMEOVER".encode("utf-8"))
						while True:
							res = clientSocket.recv(5)
							if res ==b'CHECK':
								sendBytes = pickle.dumps(serverBoard)
								clientSocket.send(sendBytes)
								time.sleep(10)
								clientSocket.close()
								exit()
					else:
						clientSocket.send("NEXTTURN".encode("utf-8"))
						break

	except Exception as e:
		print(e)

	finally:
		clientSocket.close()
		exit()

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
	# 要求があれば接続を確立して、ソケット・アドレスを代入
	clientSocket, addr = s.accept()
	print(addr)
	# スレッド処理
	p = threading.Thread(target = main_thread, args = (clientSocket, PlayerNo))
	p.start()
	if PlayerNo == 1:
		PlayerNo = 0
	else:
		PlayerNo = 1