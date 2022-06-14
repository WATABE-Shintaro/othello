from tkinter import messagebox
import numpy as np
import copy
import sys

# 定数
# GUI用
NUMBER_OF_SQUARE = 8  # マスの数
# マスのステート
OUT_OF_BOARD = -2
DARK = -1
GREEN = 0
LIGHT = 1
# ターンが先行か後攻か
TURN_OF_DARK = -1
TURN_OF_LIGHT = 1
TURN_OF_OTHER = 3
# 配列の要素用の先行か後攻か
T_DARK = 0
T_LIGHT = 1
T_OTHER = 2
# 座標
X_AXIS = 0
Y_AXIS = 1
# そこにおけるかどうか
NOT_PLACEABLE = 0
PLACEABLE = 1
# おける場所があるか
STATE_GAME_END = -1
STATE_PASS = 0
STATE_PLACE = 1
# 8方向のリスト
DIRECTION_LIST = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]


class BoardObject:
    def __init__(self):
        self.board_state = np.zeros((NUMBER_OF_SQUARE + 2, NUMBER_OF_SQUARE + 2), dtype=int)
        self.placeable_or_not_board = np.zeros((NUMBER_OF_SQUARE + 2, NUMBER_OF_SQUARE + 2), dtype=int)
        self.placeable_or_pass = STATE_PASS
        # 駒を初期配置にする
        self.board_state[4, 4] = LIGHT
        self.board_state[4, 5] = DARK
        self.board_state[5, 5] = LIGHT
        self.board_state[5, 4] = DARK
        for i in range(NUMBER_OF_SQUARE + 2):
            self.board_state[0, i] = OUT_OF_BOARD
            self.board_state[NUMBER_OF_SQUARE+1, i] = OUT_OF_BOARD
            self.board_state[i, 0] = OUT_OF_BOARD
            self.board_state[i, NUMBER_OF_SQUARE+1] = OUT_OF_BOARD
        self.calculate_where_placeable(-1)

    def place_piece(self, x, y, idx_turn):
        # インデックス用の先攻後攻の値から計算用に変換
        if idx_turn == T_DARK:
            the_turn = TURN_OF_DARK
        elif idx_turn == T_LIGHT:
            the_turn = TURN_OF_LIGHT
        else:
            messagebox.showerror("error", "不正な値。468.idx_turn。強制終了します。")
            sys.exit(1)
        # board_surfaceに合うように+1する
        point_vec = (x + 1, y + 1)
        # おけない場所におかれたとき。
        if self.placeable_or_not_board[point_vec] == NOT_PLACEABLE:
            return False
        # おかれた場所にコマを置く
        if the_turn == TURN_OF_DARK:
            color = DARK
        elif the_turn == TURN_OF_LIGHT:
            color = LIGHT
        else:
            messagebox.showerror("error", "不正な値。481.強制終了します。")
            sys.exit(1)
        self.board_state[point_vec] = color
        # 配列宣言
        reverse_point = np.zeros((NUMBER_OF_SQUARE + 2, NUMBER_OF_SQUARE + 2))
        # ひっくり返す場所検索
        # 8方向繰り返し
        for delta in DIRECTION_LIST:
            # 位置検索用
            t_point = copy.copy(point_vec)
            counter = 0
            while True:
                # 位置ずらす
                t_point = (t_point[X_AXIS] + delta[X_AXIS], t_point[Y_AXIS] + delta[Y_AXIS])
                counter += 1
                # 値を評価
                z1 = self.board_state[t_point] * the_turn
                if z1 == -1:
                    # 違う色なので続ける
                    pass
                elif z1 == 1:
                    if counter > 1:
                        # 挟んでることが確認できたのでひっくり返しへ(ひっくり返しonにする)
                        flag_of_reverse = True
                    else:
                        # 自分の色と隣り合っていたので、終える。
                        flag_of_reverse = False
                    break
                elif z1 == -2 or z1 == 0 or z1 == 2:
                    # 自分の色がないまま空白のマス又は盤外になったので何もせず終わる
                    flag_of_reverse = False
                    break
                else:
                    messagebox.showerror("error", "不正な値。508.強制終了します。")
                    sys.exit(1)
            # ひっくり返しonのとき
            if flag_of_reverse:
                while True:
                    # 位置逆にずらす
                    t_point = (t_point[X_AXIS] - delta[X_AXIS], t_point[Y_AXIS] - delta[Y_AXIS])
                    # もとの位置に戻ったら終了
                    if t_point == point_vec:
                        break
                    # そこの位置をひっくり返すに
                    reverse_point[t_point[X_AXIS], t_point[Y_AXIS]] = True
        for i in range(1, NUMBER_OF_SQUARE + 1):
            for j in range(1, NUMBER_OF_SQUARE + 1):
                if reverse_point[i, j]:
                    color = self.board_state[i, j] * -1
                    # 色変更
                    self.board_state[i, j] = color
        self.calculate_where_placeable(the_turn*-1)
        return True

    def pass_the_turn(self, idx_turn):
        # インデックス用の先攻後攻の値から計算用に変換
        if idx_turn == T_DARK:
            the_turn = TURN_OF_DARK
        elif idx_turn == T_LIGHT:
            the_turn = TURN_OF_LIGHT
        else:
            messagebox.showerror("error", "不正な値。468.idx_turn。強制終了します。")
            sys.exit(1)
        self.calculate_where_placeable(the_turn * -1)

    def calculate_where_placeable(self, the_turn):
        # 一マスごとにおける場所を調べておける場所があるかをおける場所を記録した配列に記録、これを全マスやり、一マスでもおける場所があるか調べる
        self.placeable_or_pass = STATE_PASS
        for i in range(1, NUMBER_OF_SQUARE + 1):
            for j in range(1, NUMBER_OF_SQUARE + 1):
                self.placeable_or_not_board[i, j] = self.calculate_is_placeable(i, j, the_turn)  # 暫定9ベクトル化
                if self.placeable_or_not_board[i, j] == PLACEABLE:
                    self.placeable_or_pass = STATE_PLACE
        # 置けないなら次ターンも調べる 両方パスに設定して　全マス調べておける場所があるなら片パスに設定する
        if self.placeable_or_pass == STATE_PASS:
            self.placeable_or_pass = STATE_GAME_END
            for i in range(1, NUMBER_OF_SQUARE + 1):
                for j in range(1, NUMBER_OF_SQUARE + 1):
                    temp_placeable_or_not = self.calculate_is_placeable(i, j, the_turn * -1)  # 暫定9ベクトル化
                    if temp_placeable_or_not == PLACEABLE:
                        self.placeable_or_pass = STATE_PASS

    def calculate_is_placeable(self, x, y, the_turn):
        point_vec = (x, y)
        # 最初置けないに設定して、あとから置けるに設定しなおす
        placeable_or_not = NOT_PLACEABLE
        # 配列宣言
        # その場所がgreenの場合のみおける
        if self.board_state[point_vec] == DARK or self.board_state[point_vec] == LIGHT:
            pass
        elif self.board_state[point_vec] == GREEN:
            # ひっくり返す場所検索
            # 8方向繰り返し
            for delta in DIRECTION_LIST:
                # 位置検索用
                t_point = copy.copy(point_vec)
                counter = 0
                while True:
                    # 位置ずらす
                    t_point = (t_point[X_AXIS] + delta[X_AXIS], t_point[Y_AXIS] + delta[Y_AXIS])
                    counter += 1
                    # 値を評価
                    z1 = self.board_state[t_point] * the_turn
                    if z1 == -1:
                        # 続ける
                        pass
                    elif z1 == 1:
                        if counter > 1:
                            # 挟んでることが確認できたのでひっくり返しへ(ひっくり返しonにする)
                            reverse_flag = True
                        else:
                            # 自分の色と隣り合っていたので、終える。
                            reverse_flag = False
                        break
                    elif z1 == -2 or z1 == 0 or z1 == 2:
                        # 自分の色がないまま空白のマス又は盤外になったので何もせず終わる
                        reverse_flag = False
                        break
                    else:
                        messagebox.showerror("error", "578.。強制終了します。")
                        sys.exit(1)
                if reverse_flag:
                    placeable_or_not = PLACEABLE
                    break
        else:
            messagebox.showerror("error", str(point_vec[0]) + str(point_vec[1]) + "不正な値584。強制終了します。")
            sys.exit(1)
        return placeable_or_not

    def get_board_state(self, x, y):
        return self.board_state[x + 1, y + 1]

    def get_placeable_or_pass(self):
        return self.placeable_or_pass

    def get_placeable_or_not_board(self, x, y):
        return self.placeable_or_not_board[x + 1, y + 1]
