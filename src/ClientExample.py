import socket
import pickle

ip_address = '172.16.30.168'
port = 7010
buffer_size = 4092

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# サーバーに接続を要求する
s.connect((socket.gethostname(), port))
# サーバーからのデータを受信
msg = s.recv(buffer_size)
data = pickle.loads(msg)
print(data)

