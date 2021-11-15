# server_multi_thread.py
import socket
import sys
import errno
import threading
import pickle

PORT_NUMBER 8000
BUFFER_SIZE 512
 
def create_server_socket(portNumber):
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except OSError as e:
        print("socket:{}".format(e))
        sys.exit(1)
    try:
        serverSocket.bind((socket.gethostname(), portNumber))
    except OSError as e:
        print("bind:{}".format(e))
        serverSocket.close()
        sys.exit(1)
    try:
        serverSocket.listen(socket.SOMAXCONN)
    except OSError as e:
        print("listen:{}".format(e))
        serverScoket.close()
        sys.exit(1)
    return serverSocket

def accept_loop(serverSocket, bufferSize):
    while True:
        try:
            clientSocket, addr = soc.accept()
            t = threading.Thread(target=send_recieve, args=(clientSocket, bufferSize))
            t.start()             
        except InterruptedError as e:
            if e.errno != errno.EINTR:
                print("accept:{}".format(e))
        except RuntimeError as e:
            print("thread:{}".format(e))
 
def send_recieve(clientSocket, bufferSize):
    id = threading.get_ident()
    while True:
        try:
            receivedBytes = clientSocket.recv(bufferSize)
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
	        print(boardData)
	        sendBytes = pickle.dumps(boardData)
	        clientSocket.send(sendBytes)
        except:
            print("pickle:{}", pickle.PicklingError)
            break
        try:
            clientSocket.send(sendBytes)
        except InterruptedError as e:
            print("send:{}".format(e))
            break
    clientSocket.close()
 
if __name__ == '__main__':
    serverSocket = create_server_socket(PORT_NUM)
    try:
        accept_loop(serverSocket, BUFFER_SIZE)
        soc.close()
    except KeyboardInterrupt:
        soc.close()
        sys.exit(1)
