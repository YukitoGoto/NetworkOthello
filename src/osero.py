"""
ライブラリ
"""
import numpy as np
import random
import sys

"""
定数宣言
"""
# マスの状態
EMPTY = 0 # 空きマス
WHITE = -1 # 白石
BLACK = 1 # 黒石
WALL = 2 # 壁

# ボードのサイズ
BOARD_SIZE = 8

# 方向(2進数)
NONE = 0
LEFT = 2**0 # =1
UPPER_LEFT = 2**1 # =2 
UPPER = 2**2 # =4
UPPER_RIGHT = 2**3 # =8
RIGHT = 2**4 # =16
LOWER_RIGHT = 2**5 # =32
LOWER = 2**6 # =64
LOWER_LEFT = 2**7 # =128

# 手の表現
IN_ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
IN_NUMBER = ['1', '2', '3', '4', '5', '6', '7', '8']

# 手数の上限
MAX_TURNS = 60

# 人間の色
if len(sys.argv) == 2:
    HUMAN_COLOR = sys.argv[1]
else:
    HUMAN_COLOR = ''


"""
ボードの表現
"""
class Board:

    def __init__(self):

        # 全マスを空きマスに設定
        self.RawBoard = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)

        # 壁の設定
        self.RawBoard[0, :] = WALL
        self.RawBoard[:, 0] = WALL
        self.RawBoard[BOARD_SIZE + 1, :] = WALL
        self.RawBoard[:, BOARD_SIZE + 1] = WALL

        # 初期配置
        self.RawBoard[4, 4] = WHITE
        self.RawBoard[5, 5] = WHITE
        self.RawBoard[4, 5] = BLACK
        self.RawBoard[5, 4] = BLACK

        # 手番
        self.Turns = 0

        # 現在の手番の色
        self.CurrentColor = BLACK

        # 置ける場所と石が返る方向
        self.MovablePos = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
        self.MovableDir = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)

        # MovablePosとMovableDirを初期化
        self.initMovable()

        # ユーザの石の色をhumanColorに格納
        if HUMAN_COLOR == 'B':
            self.humanColor = BLACK
        elif HUMAN_COLOR == 'W':
            self.humanColor = WHITE
        else:
            print('引数にBかWを指定してください')
            sys.exit()
        
    """
    どの方向に石が裏返るかをチェック
    """
    def checkMobility(self, x, y, color):

        # 注目しているマスの裏返せる方向の情報が入る
        dir = 0

        # 既に石がある場合はダメ
        if(self.RawBoard[x, y] != EMPTY):
            return dir

        ## 左
        if(self.RawBoard[x - 1, y] == - color): # 直上に相手の石があるか
            
            x_tmp = x - 2
            y_tmp = y

            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
            
            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LEFT

        ## 左上
        if(self.RawBoard[x - 1, y - 1] == - color): # 直上に相手の石があるか
            
            x_tmp = x - 2
            y_tmp = y - 2
            
            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
                y_tmp -= 1
            
            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER_LEFT

        ## 上
        if(self.RawBoard[x, y - 1] == - color): # 直上に相手の石があるか
            
            x_tmp = x
            y_tmp = y - 2
            
            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                y_tmp -= 1
            
            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER

        ## 右上
        if(self.RawBoard[x + 1, y - 1] == - color): # 直上に相手の石があるか
            
            x_tmp = x + 2
            y_tmp = y - 2
            
            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
                y_tmp -= 1
            
            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER_RIGHT

        ## 右
        if(self.RawBoard[x + 1, y] == - color): # 直上に相手の石があるか

            x_tmp = x + 2
            y_tmp = y
            
            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
            
            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | RIGHT

        ## 右下
        if(self.RawBoard[x + 1, y + 1] == - color): # 直上に相手の石があるか
            
            x_tmp = x + 2
            y_tmp = y + 2
            
            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
                y_tmp += 1
            
            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER_RIGHT

        ## 下
        if(self.RawBoard[x, y + 1] == - color): # 直上に相手の石があるか
            
            x_tmp = x
            y_tmp = y + 2
            
            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                y_tmp += 1
            
            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER

        ## 左下
        if(self.RawBoard[x - 1, y + 1] == - color): # 直上に相手の石があるか
            
            x_tmp = x - 2
            y_tmp = y + 2
            
            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
                y_tmp += 1
            
            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER_LEFT

        return dir


    """
    石を置くことによる盤面の変化をボードに反映
    """
    def flipDiscs(self, x, y):

        # 石を置く
        self.RawBoard[x, y] = self.CurrentColor

        # 石を裏返す
        # MovableDirの(y, x)座標をdirに代入
        dir = self.MovableDir[x, y]

        ## 左
        if dir & LEFT: # AND演算子

            x_tmp = x - 1

            # 相手の石がある限りループが回る
            while self.RawBoard[x_tmp, y] == - self.CurrentColor:

                # 相手の石があるマスを自分の石の色に塗り替えている
                self.RawBoard[x_tmp, y] = self.CurrentColor

                # さらに1マス左に進めてループを回す
                x_tmp -= 1

        ## 左上
        if dir & UPPER_LEFT: # AND演算子

            x_tmp = x - 1
            y_tmp = y - 1

            # 相手の石がある限りループが回る
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:

                # 相手の石があるマスを自分の石の色に塗り替えている
                self.RawBoard[x_tmp, y_tmp] = self.CurrentColor
                
                # さらに1マス左上に進めてループを回す
                x_tmp -= 1
                y_tmp -= 1

        ## 上
        if dir & UPPER: # AND演算子

            y_tmp = y - 1

            # 相手の石がある限りループが回る
            while self.RawBoard[x, y_tmp] == - self.CurrentColor:

                # 相手の石があるマスを自分の石の色に塗り替えている
                self.RawBoard[x, y_tmp] = self.CurrentColor

                # さらに1マス上に進めてループを回す
                y_tmp -= 1

        ## 右上
        if dir & UPPER_RIGHT: # AND演算子

            x_tmp = x + 1
            y_tmp = y - 1

            # 相手の石がある限りループが回る
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:

                # 相手の石があるマスを自分の石の色に塗り替えている
                self.RawBoard[x_tmp, y_tmp] = self.CurrentColor

                # さらに1マス右上に進めてループを回す
                x_tmp += 1
                y_tmp -= 1

        ## 右
        if dir & RIGHT: # AND演算子

            x_tmp = x + 1

            # 相手の石がある限りループが回る
            while self.RawBoard[x_tmp, y] == - self.CurrentColor:

                # 相手の石があるマスを自分の石の色に塗り替えている
                self.RawBoard[x_tmp, y] = self.CurrentColor
                
                # さらに1マス右に進めてループを回す
                x_tmp += 1

        ## 右下
        if dir & LOWER_RIGHT: # AND演算子

            x_tmp = x + 1
            y_tmp = y + 1

            # 相手の石がある限りループが回る
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:

                # 相手の石があるマスを自分の石の色に塗り替えている
                self.RawBoard[x_tmp, y_tmp] = self.CurrentColor

                # さらに1マス右下に進めてループを回す
                x_tmp += 1
                y_tmp += 1

        ## 下
        if dir & LOWER: # AND演算子

            y_tmp = y + 1

            # 相手の石がある限りループが回る
            while self.RawBoard[x, y_tmp] == - self.CurrentColor:

                # 相手の石があるマスを自分の石の色に塗り替えている
                self.RawBoard[x, y_tmp] = self.CurrentColor

                # さらに1マス下に進めてループを回す
                y_tmp += 1

        ## 左下
        if dir & LOWER_LEFT: # AND演算子

            x_tmp = x - 1
            y_tmp = y + 1

            # 相手の石がある限りループが回る
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:
                
                # 相手の石があるマスを自分の石の色に塗り替えている
                self.RawBoard[x_tmp, y_tmp] = self.CurrentColor

                # さらに1マス左下に進めてループを回す
                x_tmp -= 1
                y_tmp += 1

        
    """
    石を置く
    """
    def move(self, x, y):

        # 置く位置が正しいかどうかをチェック
        if x < 1 or BOARD_SIZE < x:
            return False
        if y < 1 or BOARD_SIZE < y:
            return False
        if self.MovablePos[x, y] == 0:
            return False

        # 石を裏返す
        self.flipDiscs(x, y)

        # 手番を進める
        self.Turns += 1

        # 手番を交代する
        self.CurrentColor = - self.CurrentColor
        
        # MovablePosとMovableDirの更新
        self.initMovable()

        return True


    """
    MovablePosとMovableDirの更新
    """
    def initMovable(self):

        # MovablePosの初期化（すべてFalseにする）
        self.MovablePos[:, :] = False

        # すべてのマス（壁を除く）に対してループ
        for x in range(1, BOARD_SIZE + 1):
            for y in range(1, BOARD_SIZE + 1):

                # checkMobility関数の実行
                dir = self.checkMobility(x, y, self.CurrentColor)

                # 各マスのMovableDirにそれぞれのdirを代入
                self.MovableDir[x, y] = dir

                # dirが0でないならMovablePosにTrueを代入
                if dir != 0:
                    self.MovablePos[x, y] = True
                

    """
    終局判定
    """
    def isGameOver(self):

        # 60手に達していたらゲーム終了
        if self.Turns >= MAX_TURNS:
            return True

        # (現在の手番)打てる手がある場合はゲームを終了しない
        if self.MovablePos[:, :].any():
            return False

        # (相手の手番)打てる手がある場合はゲームを終了しない
        for x in range(1, BOARD_SIZE + 1):
            for y in range(1, BOARD_SIZE + 1):

                # 置ける場所が1つでもある場合はゲーム終了ではない
                if self.checkMobility(x, y, - self.CurrentColor) != 0:
                    return False

        # ここまでたどり着いたらゲームは終わっている
        return True


    """
    パスの判定
    """
    def skip(self):

        # すべての要素が0のときだけパス(1つでも0以外があるとFalse)
        if any(MovablePos[:, :]):
            return False

        # ゲームが終了しているときはパスできない
        if isGameOver():
            return False

        # ここまで来たらパスなので手番を変える
        self.CurrentColor = - self.CurrentColor

        # MovablePosとMovableDirの更新
        self.initMovable()

        return True

    
    """
    オセロ盤面の表示
    """
    def display(self):

        # 横軸
        print(' abcdefgh')
        # 縦軸方向へのマスのループ
        for y in range(1, 9):

            # 縦軸
            print(y, end="")
            # 横軸方向へのマスのループ
            for x in range(1, 9):

                # マスの種類(数値)をgridに代入
                grid = self.RawBoard[x, y]

                # マスの種類によって表示を変化
                if grid == EMPTY: # 空きマス
                    print(' ', end="")
                elif grid == WHITE: # 白石
                    print('○', end="")
                elif grid == BLACK: # 黒石
                    print('●', end="")

            # 最後に改行
            print()


    """
    入力された手の形式をチェック
    """
    def checkIN(self, IN):

        # INが空でないかをチェック
        if not IN:
            return False

        # INの1文字目と2文字目がそれぞれa~h,1~8の範囲内であるかをチェック
        if IN[0] in IN_ALPHABET:
            if IN[1] in IN_NUMBER:
                return True

        return False


    """
    ランダムに手を打つCPU
    """
    def randomInput(self):

        # マス判定(skip)をして置けるマスが無い場合はFalseを返す
        if board.skip == True:
            return False
        
        # 置けるマス(MovablePos=1)のインデックスをgridsに格納
        grids = np.where(self.MovablePos == 1)

        # 候補からランダムに手を選ぶ
        randam_chosen_index = random.randrange(len(grids[0]))
        x_grid = grids[0][randam_chosen_index]
        y_grid = grids[1][randam_chosen_index]

        # オセロの正式な座標表現で返す
        return IN_ALPHABET[x_grid - 1] + IN_NUMBER[y_grid - 1]


"""
メインコード
"""

# ボートインスタンスの作成
board = Board()

# 手番ループ
while True:

    # 盤面の表示
    board.display()

    # 手番の表示
    if board.CurrentColor == BLACK:
        print('黒の番です:', end = "")
    else:
        print('白の番です:', end = "")

    # CPU or 人間
    if board.CurrentColor == board.humanColor:
        # 人間の手を入力
        IN = input()
    else: # ランダムAI
        IN = board.randomInput()
        print(IN)
    print()

    # 対戦を終了
    if IN == "e":
        print('おつかれ')
        break

    # 入力手をチェック
    if board.checkIN(IN):
        x = IN_ALPHABET.index(IN[0]) + 1
        y = IN_NUMBER.index(IN[1]) + 1
    else:
        print('正しい形式(例：f5)で入力してください')
        continue

    # 手を打つ
    if not board.move(x, y):
        print('そこには置けません')
        continue

    # 終局判定
    if board.isGameOver():
        board.display()
        print('おわり')
        break

    # パス
    if not board.MovablePos[:, :].any():
        board.CurrentColor = - board.CurrentColor
        board.initMovable()
        print('パスしました')
        print()
        continue

    
# ゲーム終了後の表示
print()
    
## 各色の数
count_black = np.count_nonzero(board.RawBoard[:, :] == BLACK)
count_white = np.count_nonzero(board.RawBoard[:, :] == WHITE)
    
print('黒:', count_black)
print('白:', count_white)

## 勝敗
dif = count_black - count_white
if dif > 0:
    print('黒の勝ち')
elif dif < 0:
    print('白の勝ち')
else:
    print('引き分け')
