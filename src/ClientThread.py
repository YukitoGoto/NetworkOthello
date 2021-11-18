# server_multi_thread.py
import socket
import pickle
import sys
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
    clientSocket = connect_to_server()
    myPlayerColor = entry_to_server(clientSocket)
    print('myPlayerColor is ' + myPlayerColor + '.')
    print(receive_from_server(clientSocket))

def connect_to_server():
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((socket.gethostname(), PORT_NUM))
        return clientSocket
    except Exception as e:
        print(e)
        sys.exit(1)

def entry_to_server(clientSocket):
    print('Entry to the server.')
    try:
        while True:
            send_to_server(clientSocket, 'entry_to_server')
            myPlayerColor = receive_from_server(clientSocket)
            if(myPlayerColor in PLAYER_COLOR_LIST):
                print('Done.')
                return myPlayerColor
            print('Getting myPlayerColor...')
            time.sleep(1)
    except Exception as e:
        print(e)
        clientSocket.close()
        sys.exit(1)

'''
def check_my_turn(clientSocket):
    try:
        while True:
            receive_from_server(clientSocket)
'''

def send_to_server(clientSocket, data):
    try:    
        sendBytes = pickle.dumps(data)
        clientSocket.send(sendBytes)
    except Exception as e:
        print(e)

def receive_from_server(clientSocket):
    try:
        receivedBytes = clientSocket.recv(BUFFER_SIZE)
        data = pickle.loads(receivedBytes)
        return data
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
