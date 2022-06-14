import random

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


# ランダム
class AIRandom:
    def __init__(self):
        pass

    @classmethod
    def calculate_place_point(cls, board_object: BoardObject):
        placeable_points_num = 0
        for i in range(NUMBER_OF_SQUARE):
            for j in range(NUMBER_OF_SQUARE):
                if board_object.get_placeable_or_not_board(i, j) == PLACEABLE:
                    placeable_points_num += 1
        the_decision = random.randrange(placeable_points_num)
        k = 0
        point_vec = [0, 0]
        for i in range(NUMBER_OF_SQUARE):  # 暫定9二重ループをブレークしたい
            for j in range(NUMBER_OF_SQUARE):
                if board_object.get_placeable_or_not_board(i, j) == PLACEABLE:
                    if k == the_decision:
                        point_vec = [i, j]
                    k += 1
        return point_vec
