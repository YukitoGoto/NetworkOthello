# server_multi_thread.py
import socket
import pickle
import sys
import errno
import time

# ゲーム情報
NUM_SQUARE = 8
PLAYER_COLOR_LIST = ['black', 'white']
myPlayerColor = None
clientBoard = [[None] * NUM_SQUARE for i in range(NUM_SQUARE)]

# ネットワーク情報
PORT_NUM = 8888
BUFFER_SIZE = 512

def main():
    clientSocket = create_client_socket()
    myPlayerColor = initialize_client(clientSocket)
    print('myPlayerColor is ' + myPlayerColor + '.')

def create_client_socket():
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except OSError as e:
        print("create_client_socket:{}".format(e))
        sys.exit(1)
    return clientSocket

def send_to_server(clientSocket, data):
    sendBytes = pickle.dumps(data)
    clientSocket.send(sendBytes)

def receive_from_server(clientSocket):
    receivedBytes = clientSocket.recv(BUFFER_SIZE)
    data = pickle.loads(receivedBytes)
    return data

def initialize_client(clientSocket):
    print('Entry to the server.')
    try:
        while True:
            clientSocket.connect((socket.gethostname(), PORT_NUM))
            send_to_server(clientSocket, 'Please myPlayerColor')
            myPlayerColor = receive_from_server(clientSocket)
            if(myPlayerColor in PLAYER_COLOR_LIST):
                print('Done.')
                return myPlayerColor
            print('Getting myPlayerColor...')
            time.sleep(1)
    except OSError as e:
        print("initialize_client:{}".format(e))
        clientSocket.close()
        sys.exit(1)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        sys.exit(1)

if __name__ == '__main__':
    main()
