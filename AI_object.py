from board_object import BoardObject
from AI_Random import AIRandom
from AI_Watch_List import AIWatchList
from AI_Count_placeable_point_num import AICounting

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


# AIクラス群
class AIObject:
    ai_list = ["人間", "ランダム", "優先順位型"]  # ,"先読み型", "強化学習", "進化学習"]

    def __init__(self, ai_type):
        self.ai_type = ai_type
        if self.ai_type == "優先順位型":
            self.priority_ai = AIWatchList()
        elif self.ai_type == "先読み型":
            self.counting_ai = AICounting()

    def calculate_place_point(self, board_object: BoardObject, turn_d_or_l, turn_number):
        point_vec = [0, 0]
        if self.ai_type == "ランダム":
            point_vec = AIRandom.calculate_place_point(board_object)
        elif self.ai_type == "優先順位型":
            point_vec = self.priority_ai.calculate_place_point(board_object)
        elif self.ai_type == "先読み型":
            point_vec = self.counting_ai.calculate_place_point(board_object, turn_d_or_l, turn_number)
        return point_vec

    def pass_process(self):
        pass

    def record(self, record):
        pass

    def end_process(self):
        pass

    def __del__(self):
        print("AIオブジェクト破棄")
        if self.ai_type == "優先順位型":
            del self.priority_ai
        elif self.ai_type == "先読み型":
            del self.counting_ai
