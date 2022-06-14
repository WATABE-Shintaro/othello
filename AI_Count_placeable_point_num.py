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
        self.deep_level = 5

    def calculate_place_point(self, board_object: BoardObject, idx_d_or_l, turn_num):
        alpha = None
        beta = None
        if idx_d_or_l == T_DARK:
            self.turn_d_or_l = TURN_OF_DARK
        elif idx_d_or_l == T_LIGHT:
            self.turn_d_or_l = TURN_OF_LIGHT
        else:
            messagebox.showerror("error", "不正な値(idx_d_or_l)。強制終了します。")
            sys.exit(1)
        firstornotT = self.turn_d_or_l
        moveableornot, putableplace, trunplacelist = CalculateBoard.Search2(aiboadsurface, firstornotT=firstornotT)
        if moveableornot != STATE_PLACE:
            messagebox.showerror("error", "不正な値(moveableornot)。強制終了します。")
            sys.exit(1)
        if turn_num >= 26:
            scoremax = None
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if putableplace[i, j] == PLACEABLE:
                        nextboadsurface = copy.copy(aiboadsurface)
                        nextboadsurface[i + 1][j + 1] = firstornotT
                        for k in range(NUMBER_OF_SQUARE):
                            for l in range(NUMBER_OF_SQUARE):
                                if trunplacelist[i][j][k][l]:
                                    nextboadsurface[k + 1][l + 1] = nextboadsurface[k + 1][l + 1] * -1
                        score = self.selectminpiece(nextboadsurface, alpha, beta, firstornotT * -1)
                        if scoremax is not None and score > scoremax:
                            scoremax = score
                            if alpha is None:
                                alpha = scoremax
                            else:
                                alpha = max([scoremax, alpha])
                            point = [i, j]
                        elif scoremax is None:
                            scoremax = score
                            point = [i, j]
            return point
        else:
            scoremax = None
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if putableplace[i, j] == PLACEABLE:
                        nextboadsurface = copy.copy(aiboadsurface)
                        nextboadsurface[i + 1][j + 1] = firstornotT
                        for k in range(NUMBER_OF_SQUARE):
                            for l in range(NUMBER_OF_SQUARE):
                                if trunplacelist[i][j][k][l]:
                                    nextboadsurface[k + 1][l + 1] = nextboadsurface[k + 1][l + 1] * -1
                        score = self.selectminscore(nextboadsurface, self.deep_level - 1, alpha, beta, firstornotT * -1)
                        if scoremax is not None and score > scoremax:
                            scoremax = score
                            if alpha is None:
                                alpha = scoremax
                            else:
                                alpha = max([scoremax, alpha])
                            point = [i, j]
                        elif scoremax is None:
                            scoremax = score
                            point = [i, j]
            return point

    def makescore(self, boadsurface2, firstornotT):
        moveableornot, puttableplace = CalculateBoard.calculate_where_placeable(boadsurface2, the_turn=firstornotT)
        if moveableornot == PLACEABLE:
            puttablecount = np.count_nonzero(puttableplace == PLACEABLE)
        else:
            puttablecount = 0
        A = puttablecount * firstornotT * self.turn_d_or_l
        templist = [boadsurface2[1][1], boadsurface2[1][8], boadsurface2[8][8], boadsurface2[8][1]]
        B = templist.count(firstornotT) - templist.count(firstornotT * -1)
        return A + B * 5

    def selectmaxscore(self, boadsurface2, depth, alpha, beta, firstornotT):
        if depth == 0:
            return self.makescore(boadsurface2, firstornotT)
        moveableornot, putableplace, trunplacelist = CalculateBoard.Search2(boadsurface2, firstornotT=firstornotT)
        depth -= 1
        if moveableornot == STATE_PLACE:
            scoremax = None
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if putableplace[i, j] == PLACEABLE:
                        nextboadsurface = copy.copy(boadsurface2)
                        nextboadsurface[i + 1][j + 1] = firstornotT
                        for k in range(NUMBER_OF_SQUARE):
                            for l in range(NUMBER_OF_SQUARE):
                                if trunplacelist[i][j][k][l]:
                                    nextboadsurface[k + 1][l + 1] = nextboadsurface[k + 1][l + 1] * -1
                        score = self.selectminscore(nextboadsurface, depth, alpha, beta, firstornotT * -1)
                        if beta is not None and score >= beta:
                            return score
                        if scoremax is not None and score > scoremax:
                            scoremax = score
                            if alpha is None:
                                alpha = scoremax
                            else:
                                alpha = max([scoremax, alpha])
                        elif scoremax is None:
                            scoremax = score
            return scoremax
        elif moveableornot == STATE_PASS:
            score = self.selectminscore(boadsurface2, depth, alpha, beta, firstornotT * -1)
            return score
        else:
            messagebox.showerror("error", "不正な値(moveableornot)。強制終了します。")
            sys.exit(1)

    def selectminscore(self, boadsurface2, depth, alpha, beta, firstornotT):
        if depth == 0:
            return self.makescore(boadsurface2, firstornotT)
        moveableornot, putableplace, trunplacelist = CalculateBoard.Search2(boadsurface2, firstornotT=firstornotT)
        depth -= 1
        if moveableornot == STATE_PLACE:
            scoremin = None
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if putableplace[i, j] == PLACEABLE:
                        nextboadsurface = copy.copy(boadsurface2)
                        nextboadsurface[i + 1][j + 1] = firstornotT
                        for k in range(NUMBER_OF_SQUARE):
                            for l in range(NUMBER_OF_SQUARE):
                                if trunplacelist[i][j][k][l]:
                                    nextboadsurface[k + 1][l + 1] = nextboadsurface[k + 1][l + 1] * -1
                        score = self.selectmaxscore(nextboadsurface, depth, alpha, beta, firstornotT * -1)
                        if alpha is not None and score <= alpha:
                            return score
                        if scoremin is not None and score < scoremin:
                            scoremin = score
                            if beta is None:
                                beta = scoremin
                            else:
                                beta = min([scoremin, beta])
                        elif scoremin is None:
                            scoremin = score
            return scoremin
        elif moveableornot == STATE_PASS:
            score = self.selectmaxscore(boadsurface2, depth, alpha, beta, firstornotT * -1)
            return score
        else:
            messagebox.showerror("error", "不正な値(moveableornot)。強制終了します。")
            sys.exit(1)

    def countmypiece(self, boadsurface2):
        return np.count_nonzero(boadsurface2 == self.turn_d_or_l)

    def selectmaxpiece(self, boadsurface2, alpha, beta, firstornotT):
        moveableornot, putableplace, trunplacelist = CalculateBoard.Search2(boadsurface2, firstornotT=firstornotT)
        if moveableornot == STATE_GAME_END:
            return self.countmypiece(boadsurface2)
        elif moveableornot == STATE_PASS:
            score = self.selectminpiece(boadsurface2, alpha, beta, firstornotT * -1)
            return score
        elif moveableornot == PLACEABLE:
            scoremax = None
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if putableplace[i, j] == PLACEABLE:
                        nextboadsurface = copy.copy(boadsurface2)
                        nextboadsurface[i + 1][j + 1] = firstornotT
                        for k in range(NUMBER_OF_SQUARE):
                            for l in range(NUMBER_OF_SQUARE):
                                if trunplacelist[i][j][k][l]:
                                    nextboadsurface[k + 1][l + 1] = nextboadsurface[k + 1][l + 1] * -1
                        score = self.selectminpiece(nextboadsurface, alpha, beta, firstornotT * -1)
                        if beta is not None and score >= beta:
                            return score
                        if scoremax is not None and score > scoremax:
                            scoremax = score
                            if alpha is None:
                                alpha = scoremax
                            else:
                                alpha = max([scoremax, alpha])
                        elif scoremax is None:
                            scoremax = score
            return scoremax
        else:
            messagebox.showerror("error", "不正な値(moveableornot)。強制終了します。")
            sys.exit(1)

    def selectminpiece(self, boadsurface2, alpha, beta, firstornotT):
        moveableornot, putableplace, trunplacelist = CalculateBoard.Search2(boadsurface2, firstornotT=firstornotT)
        if moveableornot == STATE_GAME_END:
            return self.countmypiece(boadsurface2)
        elif moveableornot == STATE_PASS:
            score = self.selectmaxpiece(boadsurface2, alpha, beta, firstornotT * -1)
            return score
        elif moveableornot == PLACEABLE:
            scoremin = None
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if putableplace[i, j] == PLACEABLE:
                        nextboadsurface = copy.copy(boadsurface2)
                        nextboadsurface[i + 1][j + 1] = firstornotT
                        for k in range(NUMBER_OF_SQUARE):
                            for l in range(NUMBER_OF_SQUARE):
                                if trunplacelist[i][j][k][l]:
                                    nextboadsurface[k + 1][l + 1] = nextboadsurface[k + 1][l + 1] * -1
                        self.selectmaxpiece(nextboadsurface, alpha, beta, firstornotT * -1)
                        if alpha is not None and score <= alpha:
                            return score
                        if scoremin is not None and score < scoremin:
                            scoremin = score
                            if beta is None:
                                beta = scoremin
                            else:
                                beta = min([scoremin, beta])
                        elif scoremin is None:
                            scoremin = score
            return scoremin
        else:
            messagebox.showerror("error", "不正な値(moveableornot)。強制終了します。")
            sys.exit(1)

    def __del__(self):
        print("AIオブジェクト破棄")
