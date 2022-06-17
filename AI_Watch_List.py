import copy
from tkinter import messagebox
import sys

from board_object import BoardObject

# 定数
# GUI用
NUMBER_OF_SQUARE = 8  # マスの数
# マスのステート
OUT_OF_BOARD = -2
DARK = -1
GREEN = 0
LIGHT = 1
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


# 優先順位型
class AIWatchList:
    def __init__(self):
        # 優先順位のリスト作る
        self.priority_list = [[0, 0], [0, 7], [7, 7], [7, 0]]
        for i in range(2, 6):
            self.priority_list.append([0, i])
        for i in range(2, 6):
            self.priority_list.append([7, i])
        for i in range(2, 6):
            self.priority_list.append([i, 0])
        for i in range(2, 6):
            self.priority_list.append([i, 7])
        for i in range(2, 6):
            for j in range(2, 6):
                self.priority_list.append([i, j])
        for i in range(2, 6):
            self.priority_list.append([1, i])
        for i in range(2, 6):
            self.priority_list.append([6, i])
        for i in range(2, 6):
            self.priority_list.append([i, 1])
        for i in range(2, 6):
            self.priority_list.append([i, 6])
        self.priority_list.append([0, 1])
        self.priority_list.append([1, 1])
        self.priority_list.append([1, 0])
        self.priority_list.append([6, 0])
        self.priority_list.append([6, 1])
        self.priority_list.append([7, 1])
        self.priority_list.append([7, 6])
        self.priority_list.append([6, 6])
        self.priority_list.append([6, 7])
        self.priority_list.append([1, 7])
        self.priority_list.append([1, 6])
        self.priority_list.append([0, 6])
        print(self.priority_list)
        print(len(self.priority_list))

    def calculate_place_point(self, board_object: BoardObject):
        for i in range(len(self.priority_list)):
            point_vec = copy.deepcopy(self.priority_list[i])
            if board_object.get_placeable_or_not_board(point_vec[X_AXIS], point_vec[Y_AXIS]) == PLACEABLE:
                break
        else:
            messagebox.showerror("error", "AILookPriorityはおける場所を見つけられませんでした。強制終了します。")
            sys.exit(1)
        return point_vec

    def __del__(self):
        print("AIオブジェクト破棄")
