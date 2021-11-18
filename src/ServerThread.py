# server_multi_thread.py
import socket
import pickle
import sys
import errno
import threading


# ゲーム情報
NUM_SQUARE = 8
PLAYER_COLOR_LIST = ['black', 'white']
myPlayerColor = None
clientBoard = [[None] * NUM_SQUARE for i in range(NUM_SQUARE)]

# ネットワーク情報
PORT_NUMBER = 8888
BUFFER_SIZE = 512

'''
[from server]
turn("white"-"black")
gameoverflag(ture-false)
board(list)
[from client1]
myPlayerColor("white"-"black")
passflag(true-false)
board(list)
[fomr client2]
myPlayerColor("white"-"black")
passflag(true-false)
board(list)
'''

def main():
    serverSocket = create_server_socket()
    entry_accept(serverSocket)

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
        except Exception as e:
            print(e)
            sys.exit(1)

def entry_thread(clientSocket, playerNumber, clientSocketList = list()):
    receiveData = receive_from_client(clientSocket)
    if(receiveData == 'entry_to_server'):
        send_to_client(clientSocket, PLAYER_COLOR_LIST[playerNumber])
        clientSocketList.append(clientSocket)
        if(len(PLAYER_COLOR_LIST) - 1 == playerNumber):
            send_to_client(clientSocketList[0], 'black')
            send_to_client(clientSocketList[1], 'white')
        else:
            None

if __name__ == '__main__':
    main()
