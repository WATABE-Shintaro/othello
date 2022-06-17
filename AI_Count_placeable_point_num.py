from tkinter import messagebox
import sys
import copy

from cy_board_object import BoardObject


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


# 先読み型
class AICounting:

    def __init__(self):
        self.turn_d_or_l = TURN_OF_OTHER
        self.change_move_turn_num = 26
        self.deep_level = 2

    def calculate_place_point(self, board_object: BoardObject, turn_d_or_l, turn_num):
        alpha = -1000
        beta = 1000
        if turn_d_or_l == T_DARK:
            self.turn_d_or_l = TURN_OF_DARK
        elif turn_d_or_l == T_LIGHT:
            self.turn_d_or_l = TURN_OF_LIGHT
        else:
            messagebox.showerror("error", "不正な値(idx_d_or_l)。強制終了します。")
            sys.exit(1)
        if board_object.get_placeable_or_pass() != STATE_PLACE:
            messagebox.showerror("error", "動けないのに手を求められた。強制終了します。")
            sys.exit(1)
        if turn_num >= self.change_move_turn_num:
            max_score = None
            point = [0, 0]
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if board_object.get_placeable_or_not_board(i, j) == PLACEABLE:
                        # コピーして、i,jに置いた時のボードを生成する。
                        next_board_object = copy.deepcopy(board_object)
                        next_board_object.place_piece(i, j, turn_d_or_l)
                        score = self.select_min_piece(next_board_object, alpha, beta, self.change_turn(turn_d_or_l))
                        # メモリ解放
                        del next_board_object
                        # 一段上での暫定的な最小値ベータを上回った場合、もはや採択されることはないので、適当に返す。
                        if score >= beta:
                            messagebox.showerror("error", "。強制終了します。")
                            sys.exit(1)
                        # 最大値を記録する。暫定的な最大値アルファを設定する。
                        if max_score is not None and score > max_score:
                            max_score = score
                            if alpha is None:
                                alpha = max_score
                            else:
                                alpha = max([max_score, alpha])
                            point = [i, j]
                        elif max_score is None:
                            max_score = score
                            point = [i, j]
            return point
        else:
            max_score = None
            point = [0, 0]
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if board_object.get_placeable_or_not_board(i, j) == PLACEABLE:
                        # コピーして、i,jに置いた時のボードを生成する。
                        next_board_object = copy.deepcopy(board_object)
                        next_board_object.place_piece(i, j, turn_d_or_l)
                        score = self.select_min_score(next_board_object, self.deep_level, alpha, beta,
                                                      self.change_turn(turn_d_or_l))
                        # メモリ解放
                        del next_board_object
                        # 一段上での暫定的な最小値ベータを上回った場合、もはや採択されることはないので、適当に返す。
                        if score >= beta:
                            messagebox.showerror("error", "。強制終了します。")
                            sys.exit(1)
                        # 最大値を記録する。暫定的な最大値アルファを設定する。
                        if max_score is not None and score > max_score:
                            max_score = score
                            if alpha is None:
                                alpha = max_score
                            else:
                                alpha = max([max_score, alpha])
                            point = [i, j]
                        elif max_score is None:
                            max_score = score
                            point = [i, j]
            return point

    def make_score(self, board_object: BoardObject, turn_d_or_l):
        if turn_d_or_l == T_DARK and self.turn_d_or_l == TURN_OF_LIGHT:
            messagebox.showerror("error", "不正な値。強制終了します。")
            sys.exit(1)
        elif turn_d_or_l == T_LIGHT and self.turn_d_or_l == TURN_OF_DARK:
            messagebox.showerror("error", "不正な値。強制終了します。")
            sys.exit(1)
        # 自分の置ける場所のカウント
        a = self.caliculate_score(board_object)
        # 相手の置ける場所のカウントの最小値
        b = 100
        for i in range(NUMBER_OF_SQUARE):
            for j in range(NUMBER_OF_SQUARE):
                if board_object.get_placeable_or_not_board(i, j) == PLACEABLE:
                    # コピーして、i,jに置いた時のボードを生成する。
                    next_board_object = copy.deepcopy(board_object)
                    next_board_object.place_piece(i, j, turn_d_or_l)
                    temp = self.caliculate_score(next_board_object)
                    b = min([b, temp])
        return a-b

    def caliculate_score(self, board_object: BoardObject):
        if board_object.get_placeable_or_pass() == STATE_PLACE:
            count_of_placeable = 0
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if board_object.get_placeable_or_not_board(i, j) == PLACEABLE:
                        count_of_placeable += 1
        else:
            count_of_placeable = 0
        return count_of_placeable

    def select_max_score(self, board_object: BoardObject, depth, alpha, beta, turn_d_or_l):
        # 再起的にminとmaxで関数を回していく。depthを減らしていき、0になったらその時のスコアを出す。
        depth -= 1
        if depth == 0:
            return self.make_score(board_object, turn_d_or_l)
            # ターンをパスせずにすむとき
        if board_object.get_placeable_or_pass() == STATE_PLACE:
            max_score = None
            # 全マスを調べて、置けるときにそこに置いた時のボードオブジェクトを生成し、スコアを計算する。
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if board_object.get_placeable_or_not_board(i, j) == PLACEABLE:
                        # コピーして、i,jに置いた時のボードを生成する。
                        next_board_object = copy.deepcopy(board_object)
                        next_board_object.place_piece(i, j, turn_d_or_l)
                        score = self.select_min_score(next_board_object, depth, alpha, beta,
                                                      self.change_turn(turn_d_or_l))
                        # メモリ解放
                        del next_board_object
                        # 一段上での暫定的な最小値ベータを上回った場合、もはや採択されることはないので、適当に返す。
                        if score >= beta:
                            return score
                        # 最大値を記録する。暫定的な最大値アルファを設定する。
                        if max_score is not None and score > max_score:
                            max_score = score
                            if alpha is None:
                                alpha = max_score
                            else:
                                alpha = max([alpha, max_score])
                        elif max_score is None:
                            max_score = score
            return max_score
        elif board_object.get_placeable_or_pass() == STATE_PASS:
            next_board_object = copy.deepcopy(board_object)
            next_board_object.pass_the_turn(turn_d_or_l)
            score = self.select_min_score(next_board_object, depth, alpha, beta, self.change_turn(turn_d_or_l))
            return score
        else:
            messagebox.showerror("error", "不正な値。強制終了します。")
            sys.exit(1)

    def select_min_score(self, board_object: BoardObject, depth, alpha, beta, turn_d_or_l):
        # 再起的にminとmaxで関数を回していく。depthを減らしていき、0になったらその時のスコアを出す
        if board_object.get_placeable_or_pass() == STATE_PLACE:
            min_score = None
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if board_object.get_placeable_or_not_board(i, j) == PLACEABLE:
                        # コピーして、i,jに置いた時のボードを生成する。
                        next_board_object = copy.deepcopy(board_object)
                        next_board_object.place_piece(i, j, turn_d_or_l)
                        score = self.select_max_score(next_board_object, depth, alpha, beta,
                                                      self.change_turn(turn_d_or_l))
                        # メモリ解放
                        del next_board_object
                        # 一段上での暫定的な最大値アルファを上回った場合、もはや採択されることはないので、適当に返す。
                        if score <= alpha:
                            return score
                        # 最小値を記録する。暫定的な最小値ベータを設定する。
                        if min_score is not None and score < min_score:
                            min_score = score
                            if beta is None:
                                beta = min_score
                            else:
                                beta = min([min_score, beta])
                        elif min_score is None:
                            min_score = score
            return min_score
        if board_object.get_placeable_or_pass() == STATE_PASS:
            next_board_object = copy.deepcopy(board_object)
            next_board_object.pass_the_turn(turn_d_or_l)
            score = self.select_max_score(board_object, depth, alpha, beta, self.change_turn(turn_d_or_l))
            return score
        else:
            messagebox.showerror("error", "不正な値。強制終了します。")
            sys.exit(1)

    def count_piece(self, board_object: BoardObject):
        count = 0
        for i in range(NUMBER_OF_SQUARE):
            for j in range(NUMBER_OF_SQUARE):
                if board_object.get_board_state(i, j) == self.turn_d_or_l:
                    count += 1
        return count

    def select_max_piece(self, board_object: BoardObject, alpha, beta, turn_d_or_l):
        # 再起的にminとmaxで関数を回していく。ゲームが終わったら底
        if board_object.get_placeable_or_pass() == STATE_GAME_END:
            return self.count_piece(board_object)
        elif board_object.get_placeable_or_pass() == PLACEABLE:
            max_score = None
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if board_object.get_placeable_or_not_board(i, j) == PLACEABLE:
                        # コピーして、i,jに置いた時のボードを生成する。
                        next_board_object = copy.deepcopy(board_object)
                        next_board_object.place_piece(i, j, turn_d_or_l)
                        score = self.select_min_piece(next_board_object, alpha, beta, self.change_turn(turn_d_or_l))
                        # メモリ解放
                        del next_board_object
                        # 一段上での暫定的な最小値ベータを上回った場合、もはや採択されることはないので、適当に返す。
                        if score >= beta:
                            return score
                        # 最大値を記録する。暫定的な最大値アルファを設定する。
                        if max_score is not None and score > max_score:
                            max_score = score
                            if alpha is None:
                                alpha = max_score
                            else:
                                alpha = max([max_score, alpha])
                        elif max_score is None:
                            max_score = score
            return max_score
        elif board_object.get_placeable_or_pass() == STATE_PASS:
            next_board_object = copy.deepcopy(board_object)
            next_board_object.pass_the_turn(turn_d_or_l)
            score = self.select_min_piece(next_board_object, alpha, beta, self.change_turn(turn_d_or_l))
            return score
        else:
            messagebox.showerror("error", "不正な値。強制終了します。")
            sys.exit(1)

    def select_min_piece(self, board_object: BoardObject, alpha, beta, turn_d_or_l):
        # 再起的にminとmaxで関数を回していく。ゲームが終わったら底
        if board_object.get_placeable_or_pass() == STATE_GAME_END:
            return self.count_piece(board_object)
        elif board_object.get_placeable_or_pass() == PLACEABLE:
            min_score = None
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if board_object.get_placeable_or_not_board(i, j) == PLACEABLE:
                        # コピーして、i,jに置いた時のボードを生成する。
                        next_board_object = copy.deepcopy(board_object)
                        next_board_object.place_piece(i, j, turn_d_or_l)
                        score = self.select_max_piece(next_board_object, alpha, beta, self.change_turn(turn_d_or_l))
                        # メモリ解放
                        del next_board_object
                        # 一段上での暫定的な最大値アルファを上回った場合、もはや採択されることはないので、適当に返す。
                        if alpha is not None and score <= alpha:
                            return score
                        # 最小値を記録する。暫定的な最小値ベータを設定する。
                        if min_score is not None and score < min_score:
                            min_score = score
                            if beta is None:
                                beta = min_score
                            else:
                                beta = min([min_score, beta])
                        elif min_score is None:
                            min_score = score
            return min_score
        elif board_object.get_placeable_or_pass() == STATE_PASS:
            next_board_object = copy.deepcopy(board_object)
            next_board_object.pass_the_turn(turn_d_or_l)
            score = self.select_max_piece(next_board_object, alpha, beta, self.change_turn(turn_d_or_l))
            return score
        else:
            messagebox.showerror("error", "不正な値。強制終了します。")
            sys.exit(1)

    def change_turn(self, turn_d_or_l):
        if turn_d_or_l == T_DARK:
            return T_LIGHT
        if turn_d_or_l == T_LIGHT:
            return T_DARK

    def __del__(self):
        print("AIオブジェクト破棄")

if __name__ == '__main__':
    import time
    start = time.time()
    aaa = AICounting()
    bbb = BoardObject()
    for i in range(1,4):
        ccc=aaa.calculate_place_point(bbb,T_DARK,i)
        print(ccc)
        bbb.place_piece(ccc[X_AXIS], ccc[Y_AXIS], T_DARK)

        ccc=aaa.calculate_place_point(bbb,T_LIGHT,i)
        print(ccc)
        bbb.place_piece(ccc[X_AXIS], ccc[Y_AXIS], T_LIGHT)
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")