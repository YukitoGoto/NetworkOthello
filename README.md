# NetworkOthello
## About
Server-Client間でオセロを対戦できる。
## Execute
### Server
~~~
$ python src/OthelloServer.py
('192.168.0.12', 59197)
('192.168.0.12', 59198)
~~~
### Client1
~~~
$ python src/OthelloMain.py
Welcome Othello Game! please wait ...
Your color is 'black'
Matching success! Game start!
~~~
### Client2
~~~
$ python src/OthelloMain.py
Welcome Othello Game! please wait ...
Your color is 'white'
Matching success! Game start!
Waiting Others...
~~~
## Reference
### GUI
- [【Python/tkinter】オセロ（リバーシ）ゲームの作り方](https://daeudaeu.com/tkinter-othello/#i-5)
- [Tkinterの使い方：メインウィンドウを作成する](https://daeudaeu.com/main_window/)
### Socket
- [【Python】サーバーとクライアント間でのデータ送信・受信方法（socketモジュール）](https://office54.net/python/app/python-data-socket#section3-3)
- [【Python3】Pythonでソケット通信を試してみた](https://dev.classmethod.jp/articles/python3socketserver/)
- [socket --- 低水準ネットワークインターフェース](https://docs.python.org/ja/3/library/socket.html#module-socket)
### Thread
- [bjgame](https://github.com/ttgk5/bjgame)
- [サーバーソケットの多重化](https://engineeringnote.hateblo.jp/entry/python/network-programming/server-multi-thread)
- [threading --- スレッドベースの並列処理](https://docs.python.org/ja/3.7/library/threading.html)
