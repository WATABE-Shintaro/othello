from tkinter import messagebox
import numpy as np
import copy
import sys

# 定数
# GUI用
cdef int NUMBER_OF_SQUARE = 8  # マスの数
# マスのステート
cdef int OUT_OF_BOARD = -2
cdef int DARK = -1
cdef int GREEN = 0
cdef int LIGHT = 1
# ターンが先行か後攻か
cdef int TURN_OF_DARK = -1
cdef int TURN_OF_LIGHT = 1
cdef int TURN_OF_OTHER = 3
# 配列の要素用の先行か後攻か
cdef int T_DARK = 0
cdef int T_LIGHT = 1
cdef int T_OTHER = 2
# 座標
cdef int X_AXIS = 0
cdef int Y_AXIS = 1
# そこにおけるかどうか
cdef int NOT_PLACEABLE = 0
cdef int PLACEABLE = 1
# おける場所があるか
cdef int STATE_GAME_END = -1
cdef int STATE_PASS = 0
cdef int STATE_PLACE = 1
#True,False
cdef int NUM_TRUE = 1
cdef int NUM_FALSE = 0
# 8方向のリスト
cdef int[8][2] DIRECTION_LIST
DIRECTION_LIST[0][X_AXIS] = 0
DIRECTION_LIST[0][Y_AXIS] = 1

DIRECTION_LIST[1][X_AXIS] = 1
DIRECTION_LIST[1][Y_AXIS] = 1

DIRECTION_LIST[2][X_AXIS] = 1
DIRECTION_LIST[2][Y_AXIS] = 0

DIRECTION_LIST[3][X_AXIS] = 1
DIRECTION_LIST[3][Y_AXIS] = -1

DIRECTION_LIST[4][X_AXIS] = 0
DIRECTION_LIST[4][Y_AXIS] = -1

DIRECTION_LIST[5][X_AXIS] = -1
DIRECTION_LIST[5][Y_AXIS] = -1

DIRECTION_LIST[6][X_AXIS] = -1
DIRECTION_LIST[6][Y_AXIS] = 0

DIRECTION_LIST[7][X_AXIS] = -1
DIRECTION_LIST[7][Y_AXIS] = 1

cdef class BoardObject:
    cdef int[10][10] board_state
    cdef int[10][10] placeable_or_not_board
    cdef int placeable_or_pass
    def __init__(self):
        cdef int i
        cdef int j
        for i in range(10):
            for j in range(10):
                self.board_state[i][j] = 0
                self.placeable_or_not_board[i][j] = 0
        self.placeable_or_pass = STATE_PASS
        # 駒を初期配置にする
        self.board_state[4][4] = LIGHT
        self.board_state[4][5] = DARK
        self.board_state[5][5] = LIGHT
        self.board_state[5][4] = DARK
        for i in range(NUMBER_OF_SQUARE + 2):
            self.board_state[0][i] = OUT_OF_BOARD
            self.board_state[NUMBER_OF_SQUARE + 1][i] = OUT_OF_BOARD
            self.board_state[i][0] = OUT_OF_BOARD
            self.board_state[i][NUMBER_OF_SQUARE + 1] = OUT_OF_BOARD
        self.calculate_where_placeable(-1)

    def place_piece(self, int x, int y, int idx_turn):
        # インデックス用の先攻後攻の値から計算用に変換
        cdef int the_turn
        cdef int color 
        cdef int[2] point_vec
        cdef int[2] t_point
        cdef int[10][10] reverse_point
        cdef int[2] delta
        cdef int counter
        cdef int z1
        cdef int flag_of_reverse
        cdef int i
        cdef int j
        if idx_turn == T_DARK:
            the_turn = TURN_OF_DARK
        elif idx_turn == T_LIGHT:
            the_turn = TURN_OF_LIGHT
        else:
            messagebox.showerror("error", "不正な値。468.idx_turn。強制終了します。")
            sys.exit(1)
        # board_surfaceに合うように+1する
        point_vec[X_AXIS] = x + 1
        point_vec[Y_AXIS] = y + 1
        # おけない場所におかれたとき。
        if self.placeable_or_not_board[point_vec[X_AXIS]][point_vec[Y_AXIS]] == NOT_PLACEABLE:
            return False
        # おかれた場所にコマを置く
        if the_turn == TURN_OF_DARK:
            color = DARK
        elif the_turn == TURN_OF_LIGHT:
            color = LIGHT
        else:
            messagebox.showerror("error", "不正な値。481.強制終了します。")
            sys.exit(1)
        self.board_state[point_vec[X_AXIS]][point_vec[Y_AXIS]] = color
        # 配列宣言
        for i in range(10):
            for j in range(10):
                reverse_point[i][j] = 0
        # ひっくり返す場所検索
        # 8方向繰り返し
        for i in range(8):
            delta[X_AXIS] = DIRECTION_LIST[i][X_AXIS]
            delta[Y_AXIS] = DIRECTION_LIST[i][Y_AXIS]
            # 位置検索用
            t_point[X_AXIS] = point_vec[X_AXIS]
            t_point[Y_AXIS] = point_vec[Y_AXIS]
            counter = 0
            while True:
                # 位置ずらす
                t_point[X_AXIS] = t_point[X_AXIS] + delta[X_AXIS]
                t_point[Y_AXIS] = t_point[Y_AXIS] + delta[Y_AXIS]
                counter += 1
                # 値を評価
                z1 = self.board_state[t_point[X_AXIS]][t_point[Y_AXIS]] * the_turn
                if z1 == -1:
                    # 違う色なので続ける
                    pass
                elif z1 == 1:
                    if counter > 1:
                        # 挟んでることが確認できたのでひっくり返しへ(ひっくり返しonにする)
                        flag_of_reverse = NUM_TRUE
                    else:
                        # 自分の色と隣り合っていたので、終える。
                        flag_of_reverse = NUM_FALSE
                    break
                elif z1 == -2 or z1 == 0 or z1 == 2:
                    # 自分の色がないまま空白のマス又は盤外になったので何もせず終わる
                    flag_of_reverse = NUM_FALSE
                    break
                else:
                    messagebox.showerror("error", "不正な値。508.強制終了します。")
                    sys.exit(1)
            # ひっくり返しonのとき
            if flag_of_reverse == NUM_TRUE:
                while True:
                    # 位置逆にずらす
                    t_point[X_AXIS] = t_point[X_AXIS] - delta[X_AXIS]
                    t_point[Y_AXIS] = t_point[Y_AXIS] - delta[Y_AXIS]
                    # もとの位置に戻ったら終了
                    if t_point[X_AXIS] == point_vec[X_AXIS] and t_point[Y_AXIS] == point_vec[Y_AXIS]:
                        break
                    # そこの位置をひっくり返すに
                    reverse_point[t_point[X_AXIS]][t_point[Y_AXIS]] = NUM_TRUE
        for i in range(1, NUMBER_OF_SQUARE + 1):
            for j in range(1, NUMBER_OF_SQUARE + 1):
                if reverse_point[i][j]:
                    color = self.board_state[i][j] * -1
                    # 色変更
                    self.board_state[i][j] = color
        self.calculate_where_placeable(the_turn * -1)
        return True

    def pass_the_turn(self, int idx_turn):
        # インデックス用の先攻後攻の値から計算用に変換
        cdef int the_turn
        if idx_turn == T_DARK:
            the_turn = TURN_OF_DARK
        elif idx_turn == T_LIGHT:
            the_turn = TURN_OF_LIGHT
        else:
            messagebox.showerror("error", "不正な値。468.idx_turn。強制終了します。")
            sys.exit(1)
        self.calculate_where_placeable(the_turn * -1)

    cdef int calculate_where_placeable(self, int the_turn):
        cdef int i
        cdef int j
        # 一マスごとにおける場所を調べておける場所があるかをおける場所を記録した配列に記録、これを全マスやり、一マスでもおける場所があるか調べる
        self.placeable_or_pass = STATE_PASS
        for i in range(1, NUMBER_OF_SQUARE + 1):
            for j in range(1, NUMBER_OF_SQUARE + 1):
                self.placeable_or_not_board[i][j] = self.calculate_is_placeable(i, j, the_turn)  # 暫定9ベクトル化
                if self.placeable_or_not_board[i][j] == PLACEABLE:
                    self.placeable_or_pass = STATE_PLACE
        # 置けないなら次ターンも調べる 両方パスに設定して　全マス調べておける場所があるなら片パスに設定する
        if self.placeable_or_pass == STATE_PASS:
            self.placeable_or_pass = STATE_GAME_END
            for i in range(1, NUMBER_OF_SQUARE + 1):
                for j in range(1, NUMBER_OF_SQUARE + 1):
                    temp_placeable_or_not = self.calculate_is_placeable(i, j, the_turn * -1)  # 暫定9ベクトル化
                    if temp_placeable_or_not == PLACEABLE:
                        self.placeable_or_pass = STATE_PASS
        return 0

    cdef int calculate_is_placeable(self, int x, int y, int the_turn):
        cdef int[2] point_vec
        point_vec[X_AXIS] = x
        point_vec[Y_AXIS] = y
        cdef int[2] t_point
        # 最初置けないに設定して、あとから置けるに設定しなおす
        cdef int placeable_or_not = NOT_PLACEABLE
        cdef int counter
        cdef int z1
        cdef int reverse_flag
        cdef int i
        cdef int[2] delta
        # 配列宣言
        # その場所がgreenの場合のみおける
        if self.board_state[point_vec[X_AXIS]][point_vec[Y_AXIS]] == DARK or self.board_state[point_vec[X_AXIS]][point_vec[Y_AXIS]] == LIGHT:
            pass
        elif self.board_state[point_vec[X_AXIS]][point_vec[Y_AXIS]] == GREEN:
            # ひっくり返す場所検索
            # 8方向繰り返し
            for i in range(8):
                delta[X_AXIS] = DIRECTION_LIST[i][X_AXIS]
                delta[Y_AXIS] = DIRECTION_LIST[i][Y_AXIS]
                # 位置検索用
                t_point[X_AXIS] = point_vec[X_AXIS]
                t_point[Y_AXIS] = point_vec[Y_AXIS]
                counter = 0
                while True:
                    # 位置ずらす
                    t_point[X_AXIS] = t_point[X_AXIS] + delta[X_AXIS]
                    t_point[Y_AXIS] = t_point[Y_AXIS] + delta[Y_AXIS]
                    counter += 1
                    # 値を評価
                    z1 = self.board_state[t_point[X_AXIS]][t_point[Y_AXIS]] * the_turn
                    if z1 == -1:
                        # 続ける
                        pass
                    elif z1 == 1:
                        if counter > 1:
                            # 挟んでることが確認できたのでひっくり返しへ(ひっくり返しonにする)
                            reverse_flag = NUM_TRUE
                        else:
                            # 自分の色と隣り合っていたので、終える。
                            reverse_flag = NUM_FALSE
                        break
                    elif z1 == -2 or z1 == 0 or z1 == 2:
                        # 自分の色がないまま空白のマス又は盤外になったので何もせず終わる
                        reverse_flag = NUM_FALSE
                        break
                    else:
                        messagebox.showerror("error", "578.。強制終了します。")
                        sys.exit(1)
                if reverse_flag == NUM_TRUE:
                    placeable_or_not = PLACEABLE
                    break
        else:
            messagebox.showerror("error", str(point_vec[0]) + str(point_vec[1]) + "不正な値584。強制終了します。")
            sys.exit(1)
        return placeable_or_not

    def get_board_state(self, x, y):
        return self.board_state[x + 1][y + 1]

    def get_placeable_or_pass(self):
        return self.placeable_or_pass

    def get_placeable_or_not_board(self, x, y):
        return self.placeable_or_not_board[x + 1][y + 1]

    def __deepcopy__(self, memo):
        new_object = BoardObject()
        cdef int i
        cdef int j
        for i in range(10):
            for j in range(10):
                new_object.board_state[i][j] = self.board_state[i][j]
                new_object.placeable_or_not_board[i][j] = self.placeable_or_not_board[i][j]
        new_object.placeable_or_pass = self.placeable_or_pass
        return new_object
