# server_multi_thread.py
import socket
import pickle
import sys
import threading


'''
[from server]
turn("white"-"black")
gameoverflag(ture-false)
board(list)
[from client1]
passflag(true-false)
board(list)
[fomr client2]
passflag(true-false)
board(list)
'''

# ゲーム情報
NUM_SQUARE = 8
PLAYER_COLOR_LIST = ['black', 'white']
serverBoard = [[None] * NUM_SQUARE for i in range(NUM_SQUARE)]
clientSocketList = list()

# ネットワーク情報
PORT_NUMBER = 8888
BUFFER_SIZE = 512

def main():
    serverSocket = create_server_socket()
    entry_accept(serverSocket)
    othello_server_main(serverBoard)

def create_server_socket():
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((socket.gethostname(), PORT_NUMBER))
        serverSocket.listen(socket.SOMAXCONN)
        return serverSocket
    except Exception as e:
        print(e)
        sys.exit(1)

def send_to_client(clientSocket, data):
    try:
        sendBytes = pickle.dumps(data)
        clientSocket.send(sendBytes)
    except Exception as e:
        print(e)

def receive_from_client(clientSocket):
    try:
        receivedBytes = clientSocket.recv(BUFFER_SIZE)
        data = pickle.loads(receivedBytes)
        return data
    except Exception as e:
        print(e)

def entry_accept(serverSocket):
    playerNumber = 0
    while True:
        try:
            clientSocket, addr = serverSocket.accept()
            serverThread = threading.Thread(target = entry_thread, args = (clientSocket, playerNumber))
            serverThread.start()
            playerNumber += 1
            if(len(PLAYER_COLOR_LIST) == playerNumber):
                print('Done enrty.')
                break
        except Exception as e:
            print(e)
            sys.exit(1)

def entry_thread(clientSocket, playerNumber):
    receiveData = receive_from_client(clientSocket)
    if(receiveData == 'entry_to_server'):
        send_to_client(clientSocket, PLAYER_COLOR_LIST[playerNumber])
        clientSocketList.append(clientSocket)

def othello_server_main(board):
    board[4][4] = 'black'
    board[4][5] = 'white'
    board[5][4] = 'white'
    board[5][5] = 'black'
    turnFlag = True
    gameoverFlag = False
    passFlagList = [False, False]
    while True:
        send_to_client(clientSocketList[turnFlag], True)
        send_to_client(clientSocketList[not turnFlag], False)
        send_to_client(clientSocketList[0], gameoverFlag)
        send_to_client(clientSocketList[1], gameoverFlag)
        send_to_client(clientSocketList[0], board)
        send_to_client(clientSocketList[1], board)
        if(not passFlagList[turnFlag] == receive_from_client(clientSocketList[turnFlag])):
            board = receive_from_client(clientSocketList[turnFlag])
        gameoverFlag = check_gameover()
        turnFlag = not turnFlag

def check_gameover(passFlagList):
    if(passFlagList[0] & passFlagList[1]):
        return True

if __name__ == '__main__':
    main()
