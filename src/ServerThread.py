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
    try:
        accept_loop(serverSocket)
        serverSocket.close()
    except KeyboardInterrupt:
        serverSocket.close()
        sys.exit(1)

def create_server_socket():
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((socket.gethostname(), PORT_NUMBER))
        serverSocket.listen(socket.SOMAXCONN)
    except OSError as e:
        print("create_server_socket:{}".format(e))
        serverSocket.close()
        sys.exit(1)
    return serverSocket

def send_to_client(clientSocket, data):
    sendBytes = pickle.dumps(data)
    clientSocket.send(sendBytes)

def receive_from_client(clientSocket):
    receivedBytes = clientSocket.recv(BUFFER_SIZE)
    data = pickle.loads(receivedBytes)
    return data

def accept_loop(serverSocket):
    while True:
        try:
            clientSocket, addr = serverSocket.accept()
            t = threading.Thread(target=send_recieve, args=(clientSocket, BUFFER_SIZE))
            t.start()             
        except InterruptedError as e:
            if e.errno != errno.EINTR:
                print("accept:{}".format(e))
        except RuntimeError as e:
            print("thread:{}".format(e))
 
def send_recieve(clientSocket, BUFFER_SIZE):
    id = threading.get_ident()
    while True:
        try:
            receivedBytes = clientSocket.recv(BUFFER_SIZE)
        except InterruptedError as e:
            print("recieve:{}".format(e))
            break 
        if (len(receivedBytes) == 0):
            # EOF
            print("[{}]recieve:EOF".format(id))
            break
        try:
            receivedBytes = receivedBytes.rstrip()
            boardData = pickle.loads(receivedBytes)
            if(boardData == 'Please myPlayerColor'):
                boardData = 'black'
            else:
                boardData = None
            sendBytes = pickle.dumps(boardData)
        except:
            print("pickle:{}", pickle.PicklingError)
        try:
            clientSocket.send(sendBytes)
        except InterruptedError as e:
            print("send:{}".format(e))
            break
    clientSocket.close()

if __name__ == '__main__':
    main()
