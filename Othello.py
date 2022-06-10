import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import numpy as np
from time import sleep
import copy
import random
import sys

# 定数
# GUI用
SQUARE_SIZE = 50  # マスの大きさ
NUMBER_OF_SQUARE = 8  # マスの数
GAP_SIZE = 50  # 隙間の広さ
BOARD_SIZE = SQUARE_SIZE * NUMBER_OF_SQUARE  # ボードの広さ
OPTIONS_HEIGHT = 50  # オプションの縦の幅
# マスのステート
OUT_OF_BOARD = -2
DARK = -1
GREEN = 0
LIGHT = 1
# ターンが先行か後攻か
TURN_OF_DARK = -1
TURN_OF_WHITE = 1
TURN_OF_OTHER = 3
# 配列の要素用の先行か後攻か
T_DARK = 0
T_LIGHT = 1
T_OTHER = 2
# 人かAIか
HUMAN = 0
AI_PLAYER = 1
# ゲームモード
PLAY_GAME_MODE = 0
LEARNING_MODE = 1
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


# 暫定9
# aaa=AIRandom()

# クラス群
# ランダム
class AIRandom:
    def __init__(self):
        pass

    def playprocess(self, aiboadsurface, aiputablepoint, aifirstornot, aiturnnumber):
        puttablecount = np.count_nonzero(aiputablepoint == PLACEABLE)
        thedecision = random.randrange(puttablecount)
        k = 0
        pointreturn = [0, 0]
        for i in range(NUMBER_OF_SQUARE):  # 暫定9二重ループをブレークしたい
            for j in range(NUMBER_OF_SQUARE):
                if aiputablepoint[i][j] == PLACEABLE:
                    if k == thedecision:
                        pointreturn = [i, j]
                    k += 1
        return pointreturn

    def getgamerecord(self, airecord):
        pass

    def passprocess(self):
        pass

    def save(self):
        pass

    def endprocess(self):
        pass

    def __del__(self):
        print("AIオブジェクト破棄")


# 優先順位型
class AILookPriority:
    def __init__(self):
        # 優先順位のリスト作る
        self.prioritylist = [[0, 0], [0, 7], [7, 7], [7, 0]]
        for i in range(2, 6):
            self.prioritylist.append([0, i])
        for i in range(2, 6):
            self.prioritylist.append([7, i])
        for i in range(2, 6):
            self.prioritylist.append([i, 0])
        for i in range(2, 6):
            self.prioritylist.append([i, 7])
        for i in range(2, 6):
            for j in range(2, 6):
                self.prioritylist.append([i, j])
        for i in range(2, 6):
            self.prioritylist.append([1, i])
        for i in range(2, 6):
            self.prioritylist.append([6, i])
        for i in range(2, 6):
            self.prioritylist.append([i, 1])
        for i in range(2, 6):
            self.prioritylist.append([i, 6])
        self.prioritylist.append([0, 1])
        self.prioritylist.append([1, 1])
        self.prioritylist.append([1, 0])
        self.prioritylist.append([6, 0])
        self.prioritylist.append([6, 1])
        self.prioritylist.append([7, 1])
        self.prioritylist.append([7, 6])
        self.prioritylist.append([6, 6])
        self.prioritylist.append([6, 7])
        self.prioritylist.append([1, 7])
        self.prioritylist.append([1, 6])
        self.prioritylist.append([0, 6])
        print(self.prioritylist)
        print(len(self.prioritylist))

    def playprocess(self, aiboadsurface, aiputablepoint, aifirstornot, aiturnnumber):
        for i in range(len(self.prioritylist)):
            aipoint = copy.copy(self.prioritylist[i])
            if aiputablepoint[aipoint[X_AXIS], aipoint[Y_AXIS]] == PLACEABLE:
                break
        else:
            messagebox.showerror("error／(^o^)＼", "AILookPriorityはおける場所を見つけられませんでした。強制終了します。")
            sys.exit(1)
        return aipoint

    def getgamerecord(self, airecord):
        pass

    def passprocess(self):
        pass

    def save(self):
        pass

    def endprocess(self):
        pass

    def __del__(self):
        print("AIオブジェクト破棄")


# 先読み型
class AIReadAhead:

    def __init__(self):
        self.firstornotT2 = None
        self.ChangeMoveTurnNumber = 26
        self.Deeplevel = 5

    def playprocess(self, aiboadsurface, aiputablepoint, aifirstornot, aiturnnumber):
        alpha = None
        beta = None
        if aifirstornot == T_DARK:
            self.firstornotT2 = TURN_OF_DARK
        elif aifirstornot == T_LIGHT:
            self.firstornotT2 = TURN_OF_WHITE
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(firstornot)。強制終了します。")
            sys.exit(1)
        firstornotT = self.firstornotT2
        moveableornot, putableplace, trunplacelist = CalculateBoard.Search2(aiboadsurface, firstornotT=firstornotT)
        if moveableornot != STATE_PLACE:
            messagebox.showerror("error／(^o^)＼", "不正な値(moveableornot)。強制終了します。")
            sys.exit(1)
        if aiturnnumber >= 26:
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
                        score = self.selectminscore(nextboadsurface, self.Deeplevel - 1, alpha, beta, firstornotT * -1)
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

    def getgamerecord(self, airecord):
        pass

    def passprocess(self):
        pass

    def save(self):
        pass

    def endprocess(self):
        pass

    def __del__(self):
        print("AIオブジェクト破棄")

    def makescore(self, boadsurface2, firstornotT):
        moveableornot, puttableplace = CalculateBoard.calculate_where_placeable(boadsurface2, the_turn=firstornotT)
        if moveableornot == PLACEABLE:
            puttablecount = np.count_nonzero(puttableplace == PLACEABLE)
        else:
            puttablecount = 0
        A = puttablecount * firstornotT * self.firstornotT2
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
            messagebox.showerror("error／(^o^)＼", "不正な値(moveableornot)。強制終了します。")
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
            messagebox.showerror("error／(^o^)＼", "不正な値(moveableornot)。強制終了します。")
            sys.exit(1)

    def countmypiece(self, boadsurface2):
        return np.count_nonzero(boadsurface2 == self.firstornotT2)

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
            messagebox.showerror("error／(^o^)＼", "不正な値(moveableornot)。強制終了します。")
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
            messagebox.showerror("error／(^o^)＼", "不正な値(moveableornot)。強制終了します。")
            sys.exit(1)


# 強化学習
class AIReinforcementLearning:
    def __init__(self, learnornot):
        pass

    def playprocess(self, aiboadsurface, aiputablepoint, aifirstornot, aiturnnumber):
        pass

    def getgamerecord(self, airecord):
        pass

    def passprocess(self):
        pass

    def save(self):
        pass

    def endprocess(self):
        pass

    def __del__(self):
        print("AIオブジェクト破棄")


# 進化学習
class AIGA:
    def __init__(self, learnornot):
        pass

    def playprocess(self, aiboadsurface, aiputablepoint, aifirstornot, aiturnnumber):
        pass

    def getgamerecord(self, airecord):
        pass

    def passprocess(self):
        pass

    def save(self):
        pass

    def endprocess(self):
        pass

    def __del__(self):
        print("AIオブジェクト破棄")


# スキャンするオブジェクト
class CalculateBoard:
    def __init__(self):
        pass

    # そこにおいたときどこがひっくり返るか、ひっくり返った盤面をしめしてくれる
    @classmethod
    def calculate_where_reverse(cls, x5, y5, the_turn, board_state):
        # board_surfaceに合うように+1する
        point_vec = (x5 + 1, y5 + 1)
        # 最初置けないに設定して、あとから置けるに設定しなおす
        placeable_or_not = NOT_PLACEABLE
        # 配列宣言
        reverse_point = np.zeros((NUMBER_OF_SQUARE, NUMBER_OF_SQUARE))

        # その場所がgreenの場合のみおける
        if board_state[point_vec] == DARK or board_state[point_vec] == LIGHT:
            pass
        elif board_state[point_vec] == GREEN:
            # ひっくり返す場所検索
            # 8方向繰り返し
            for delta in DIRECTION_LIST:
                # 位置検索用
                t_point = copy.copy(point_vec)
                while True:
                    # 位置ずらす
                    t_point = (t_point[X_AXIS] + delta[X_AXIS], t_point[Y_AXIS] + delta[Y_AXIS])
                    # 値を評価
                    z1 = board_state[t_point] * the_turn
                    if z1 == -1:
                        # 違う色なので続ける
                        pass
                    elif z1 == 1:
                        # 挟んでることが確認できたのでひっくり返しへ(ひっくり返しonにする)
                        flag_of_reverse = True
                        break
                    elif z1 == -2 or z1 == 0 or z1 == 2:
                        # 自分の色がないまま空白のマス又は盤外になったので何もせず終わる
                        flag_of_reverse = False
                        break
                    else:
                        messagebox.showerror("error", "不正な値。強制終了します。")
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
                        reverse_point[t_point[X_AXIS] - 1, t_point[Y_AXIS] - 1] = True
                        # ひっくり返す場所あるにする
                        placeable_or_not = PLACEABLE
        else:
            messagebox.showerror("error", "不正な値。強制終了します。")
            sys.exit(1)
        return placeable_or_not, reverse_point

    # おけるかどうかのみ示すようにする予定 暫定9
    @classmethod
    def Scan2(cls, x5, y5, the_turn, board_state):
        # board_stateに合うように+1する
        point_vec = [x5 + 1, y5 + 1]
        # 最初置けないに設定して、あとから置けるに設定しなおす
        placeable_or_not = NOT_PLACEABLE
        # 配列宣言
        reverse_point = np.zeros((NUMBER_OF_SQUARE, NUMBER_OF_SQUARE))
        # その場所がgreenの場合のみおける
        if board_state[point_vec] == DARK or board_state[point_vec] == LIGHT:
            pass
        elif board_state[point_vec] == GREEN:
            # ひっくり返す場所検索
            # 8方向繰り返し
            for delta in DIRECTION_LIST:
                # 位置検索用
                t_point = copy.copy(point_vec)
                while True:
                    # 位置ずらす
                    t_point = t_point + delta
                    # 値を評価
                    z1 = board_state[t_point] * the_turn
                    if z1 == -1:
                        # 続ける
                        pass
                    elif z1 == 1:
                        # 挟んでることが確認できたのでひっくり返しへ(ひっくり返しonにする)
                        reverse_flag = True
                        break
                    elif z1 == -2 or z1 == 0 or z1 == 2:
                        # 自分の色がないまま空白のマス又は盤外になったので何もせず終わる
                        reverse_flag = False
                        break
                    else:
                        messagebox.showerror("error", "不正な値。強制終了します。")
                        sys.exit(1)
                # ひっくり返しonのとき
                if reverse_flag:
                    while True:
                        # 位置逆にずらす
                        t_point = t_point - delta
                        # もとの位置に戻ったら終了
                        if t_point == point_vec:
                            break
                        # そこの位置をひっくり返すに
                        reverse_point[t_point[X_AXIS] - 1, t_point[Y_AXIS] - 1] = True
                        # ひっくり返す場所あるにする
                        placeable_or_not = PLACEABLE
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(pointC又はboadsurface2)。強制終了します。")
            sys.exit(1)
        return placeable_or_not, reverse_point

    # おける場所のみ示す
    @classmethod
    def calculate_where_placeable(cls, board_state, idx_turn=T_OTHER, the_turn=TURN_OF_OTHER):
        pass_or_not = STATE_PASS
        placeable_point = np.zeros((NUMBER_OF_SQUARE, NUMBER_OF_SQUARE))
        tempfirstornotA = 0
        # 先行後攻を変換
        if not the_turn == TURN_OF_OTHER:
            tempfirstornotA = the_turn
        else:
            if idx_turn == T_DARK:
                tempfirstornotA = TURN_OF_DARK
            elif idx_turn == T_LIGHT:
                tempfirstornotA = TURN_OF_WHITE
            else:
                messagebox.showerror("error／(^o^)＼", "不正な値(firstornot)。強制終了します。")
                sys.exit(1)
        # 一マスごとにおける場所を調べておける場所があるかをおける場所を記録した配列に記録、これを全マスやり、一マスでもおける場所があるか調べる
        for i in range(NUMBER_OF_SQUARE):
            for j in range(NUMBER_OF_SQUARE):
                putableornotA, temp = cls.calculate_where_reverse(i, j, tempfirstornotA, board_state)  # 暫定9ベクトル化
                if putableornotA == PLACEABLE:
                    pass_or_not = STATE_PLACE
                    placeable_point[i, j] = PLACEABLE
                else:
                    placeable_point[i, j] = NOT_PLACEABLE
        # 置けないなら次ターンも調べる 両方パスに設定して　全マス調べておける場所があるなら片パスに設定する
        if pass_or_not == NOT_PLACEABLE:
            pass_or_not = STATE_GAME_END
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    putableornotA, temp = cls.calculate_where_reverse(i, j, tempfirstornotA * -1,
                                                                      board_state)  # 暫定9ベクトル化
                    if putableornotA == PLACEABLE:
                        pass_or_not = NOT_PLACEABLE
        return (pass_or_not, placeable_point)

    # おける場所とともにおいたときの挙動も示す
    @classmethod
    def Search2(cls, boadsurface2, firstornotP=T_OTHER, firstornotT=TURN_OF_OTHER):
        moveableornotB = STATE_PASS
        putablepointB = np.zeros((NUMBER_OF_SQUARE, NUMBER_OF_SQUARE))
        tempfirstornotA = 0
        trunplacelist = np.zeros((NUMBER_OF_SQUARE, NUMBER_OF_SQUARE, NUMBER_OF_SQUARE, NUMBER_OF_SQUARE))
        # 先行後攻を変換
        if not firstornotT == TURN_OF_OTHER:
            tempfirstornotA = firstornotT
        else:
            if firstornotP == T_DARK:
                tempfirstornotA = TURN_OF_DARK
            elif firstornotP == T_LIGHT:
                tempfirstornotA = TURN_OF_WHITE
            else:
                messagebox.showerror("error／(^o^)＼", "不正な値(firstornot)。強制終了します。")
                sys.exit(1)
        # 一マスごとにおける場所を調べておける場所があるかをおける場所を記録した配列に記録、これを全マスやり、一マスでもおける場所があるか調べる
        for i in range(NUMBER_OF_SQUARE):
            for j in range(NUMBER_OF_SQUARE):
                putableornotA, turnplaceC = cls.Scan2(i, j, tempfirstornotA, boadsurface2)  # 暫定9ベクトル化
                if putableornotA == PLACEABLE:
                    moveableornotB = STATE_PLACE
                    putablepointB[i, j] = PLACEABLE
                    trunplacelist[i][j] = copy.copy(turnplaceC)
                else:
                    putablepointB[i, j] = NOT_PLACEABLE
        # 置けないなら次ターンも調べる 両方パスに設定して　全マス調べておける場所があるなら片パスに設定する
        if moveableornotB == NOT_PLACEABLE:
            moveableornotB = STATE_GAME_END
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    putableornotA, turnplaceC = cls.Scan2(i, j, tempfirstornotA * -1, boadsurface2)  # 暫定9ベクトル化
                    if putableornotA == PLACEABLE:
                        moveableornotB = NOT_PLACEABLE
        return (moveableornotB, putablepointB, trunplacelist)


# メインクラス
class mainclass():

    def __init__(self):

        # 核となるもの？
        self.root = Tk()
        self.root.title('othello')

        # ウィンドウ作成
        self.mainframe = ttk.Frame(
            self.root,
            height=GAP_SIZE * 2 + BOARD_SIZE + OPTIONS_HEIGHT,
            width=GAP_SIZE + BOARD_SIZE + GAP_SIZE + 200 + GAP_SIZE,
            relief='sunken',
            borderwidth=5)
        self.mainframe.grid()

        # ゲーム画面用
        self.mainpanel = ttk.Frame(
            self.mainframe,
            relief='sunken',
            borderwidth=5)
        self.mainpanel.place(x=GAP_SIZE, y=GAP_SIZE)

        # ゲーム画面にボード用キャンバス作成
        self.gamecanvas = tk.Canvas(
            self.mainpanel,
            height=BOARD_SIZE,
            width=BOARD_SIZE)
        self.gamecanvas.create_rectangle(0, 0, BOARD_SIZE, BOARD_SIZE, fill='green')  # 塗りつぶし
        for i in range(NUMBER_OF_SQUARE - 1):
            tempx = (i + 1) * SQUARE_SIZE
            self.gamecanvas.create_line(tempx, 0, tempx, BOARD_SIZE)
            self.gamecanvas.create_line(0, tempx, BOARD_SIZE, tempx)
        self.gamecanvas.bind("<1>", self.boadclick)
        self.gamecanvas.grid()

        # メッセージ用のラベル
        self.messagelabel = ttk.Label(
            self.mainframe,
            text='a',
            background='#0000aa',
            foreground='#ffffff')
        self.messagelabel.place(x=GAP_SIZE, y=GAP_SIZE + BOARD_SIZE + GAP_SIZE)

        # 一回戦う為のボタン
        self.gamestartbutton = ttk.Button(
            self.mainframe,
            text='game')
        self.gamestartbutton.bind("<1>", self.gamestartbuttonclick)
        self.gamestartbutton.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE, y=GAP_SIZE)

        # 何回も試行するためのボタン
        self.runningstartbutton = ttk.Button(
            self.mainframe,
            text='run')
        self.runningstartbutton.bind("<1>", self.runningstartbuttonclick)
        self.runningstartbutton.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE + 100, y=GAP_SIZE)

        # 先行のAI決める
        self.labelforfirst = ttk.Label(
            self.mainframe,
            text="先行"
        )
        self.labelforfirst.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE, y=GAP_SIZE + OPTIONS_HEIGHT)
        self.comboforfirstvalue = StringVar()
        self.comboforfirst = ttk.Combobox(
            self.mainframe,
            state="readonly",
            textvariable=self.comboforfirstvalue
        )
        self.comboforfirst['values'] = ["人間", "ランダム", "優先順位型", "先読み型", "強化学習", "進化学習"]
        self.comboforfirst.set("人間")
        self.comboforfirst.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE + 50, y=GAP_SIZE + OPTIONS_HEIGHT)

        # 後攻のAI決める
        self.labelforsecond = ttk.Label(
            self.mainframe,
            text="後攻"
        )
        self.labelforsecond.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE, y=GAP_SIZE + OPTIONS_HEIGHT * 2)
        self.comboforsecondvalue = StringVar()
        self.comboforsecond = ttk.Combobox(
            self.mainframe,
            state="readonly",
            textvariable=self.comboforsecondvalue
        )
        self.comboforsecond['values'] = ["人間", "ランダム", "優先順位型", "先読み型", "強化学習", "進化学習"]
        self.comboforsecond.set("人間")
        self.comboforsecond.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE + 50, y=GAP_SIZE + OPTIONS_HEIGHT * 2)

        # 学習するか否か設定用
        self.checkbuttonforlearnornotvalue = BooleanVar()
        self.checkbuttonforlearnornot = ttk.Checkbutton(
            self.mainframe,
            text="学習する",
            onvalue=True,
            offvalue=False,
            variable=self.checkbuttonforlearnornotvalue
        )
        self.checkbuttonforlearnornot.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE + 20,
                                            y=GAP_SIZE + OPTIONS_HEIGHT * 3 + GAP_SIZE)

        # 試合試行回数設定用
        self.labelforentry = ttk.Label(
            self.mainframe,
            text="試合回数"
        )
        self.labelforentry.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE + 20,
                                 y=GAP_SIZE + OPTIONS_HEIGHT * 3 + GAP_SIZE + OPTIONS_HEIGHT)
        self.entryforrunnningtimevalue = StringVar()
        self.entryforrunnningtime = ttk.Entry(
            self.mainframe,
            textvariable=self.entryforrunnningtimevalue
        )
        self.entryforrunnningtime.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE + 80,
                                        y=GAP_SIZE + OPTIONS_HEIGHT * 3 + GAP_SIZE + OPTIONS_HEIGHT)

        # 試合止めるよう
        self.stopbutton = ttk.Button(
            self.mainframe,
            text="stop"
        )
        self.stopbutton.bind("<1>", self.stopbuttonclick)
        self.stopbutton.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE,
                              y=GAP_SIZE + OPTIONS_HEIGHT * 3 + GAP_SIZE + OPTIONS_HEIGHT * 2)

        # 自己学習を始めるボタン
        self.selflearnbutton = ttk.Button(
            self.mainframe,
            text="selflern"
        )
        self.selflearnbutton.bind("<1>", self.selflearnbuttonclick)
        self.selflearnbutton.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE,
                                   y=GAP_SIZE + OPTIONS_HEIGHT * 3 + GAP_SIZE + OPTIONS_HEIGHT * 4)

        # 自己学習回数設定用
        self.labelforentry2 = ttk.Label(
            self.mainframe,
            text="自己学習回数"
        )
        self.labelforentry2.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE,
                                  y=GAP_SIZE + OPTIONS_HEIGHT * 3 + GAP_SIZE + OPTIONS_HEIGHT * 5)
        self.entryforselflearntimevalue = StringVar()
        self.entryforselflearntime = ttk.Entry(
            self.mainframe,
            textvariable=self.entryforselflearntimevalue
        )
        self.entryforselflearntime.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE + 80,
                                         y=GAP_SIZE + OPTIONS_HEIGHT * 3 + GAP_SIZE + OPTIONS_HEIGHT * 5)

        # 変数宣言
        self.boadsurface = np.zeros((NUMBER_OF_SQUARE + 2, NUMBER_OF_SQUARE + 2), dtype=int)
        self.player = [0, 0]
        self.playerAI = [0, 0]
        self.turnnumber = 0
        self.firstornot = 0
        self.gameorrun = 0
        self.stoptrigger = False
        self.record = []

        # ボタン押せるかの管理
        self.gamestartbuttonclickable = True
        self.runningstartbuttonclickable = False  # 暫定5
        self.runningstartbutton.config(state="disable")  # 暫定5
        self.boadclickable = False
        self.stopbuttonclickable = False
        self.stopbutton.config(state="disable")
        self.entryforrunnningtime.config(state="disable")  # 暫定5
        self.checkbuttonforlearnornot.config(state="disable")  # 暫定5
        self.selflearnbuttonclickable = False  # 暫定5
        self.selflearnbutton.config(state="disable")  # 暫定5
        self.entryforselflearntime.config(state="disable")  # 暫定5

    def selflearnbuttonclick(self, event):
        pass

    def runningstartbuttonclick(self, event):

        if self.runningstartbuttonclickable == True:
            self.gamestartbuttonclickable = False
            self.gamestartbutton.config(state="disable")
            self.runningstartbuttonclickable = False
            self.runningstartbutton.config(state="disable")
            self.boadclickable = False
            self.stopbuttonclickable = False
            self.stopbutton.config(state="disable")
            self.comboforfirst.config(state="disable")
            self.comboforsecond.config(state="disable")
            self.entryforrunnningtime.config(state="disable")
            self.checkbuttonforlearnornot.config(state="disable")
            self.selflearnbuttonclickable = False  # 暫定5
            self.selflearnbutton.config(state="disable")  # 暫定5
            self.entryforrunnningtime.config(state="disable")  # 暫定5

            messagebox.showwarning("error／(^o^)＼", "そのボタンは現在準備中です。")  # 暫定5
            self.gameorrun = LEARNING_MODE
        else:
            self.messagelabel.config(text="そのボタンは押せません")

    def OverTurn(self, x1, y1, option1, color=0):
        x2 = x1 + 1
        y2 = y1 + 1
        if option1 == True:
            color = self.boadsurface[x2][y2] * -1
        # 色変更
        self.boadsurface[x2][y2] = color
        if color == OUT_OF_BOARD:
            pass
        elif color == DARK:
            self.gamecanvas.create_oval(x1 * SQUARE_SIZE + 2, y1 * SQUARE_SIZE + 2, (x1 + 1) * SQUARE_SIZE - 2,
                                        (y1 + 1) * SQUARE_SIZE - 2, fill="black")
        elif color == GREEN:
            self.gamecanvas.create_oval(x1 * SQUARE_SIZE + 2, y1 * SQUARE_SIZE + 2, (x1 + 1) * SQUARE_SIZE - 2,
                                        (y1 + 1) * SQUARE_SIZE - 2, fill="green", outline="green")
        elif color == LIGHT:
            self.gamecanvas.create_oval(x1 * SQUARE_SIZE + 2, y1 * SQUARE_SIZE + 2, (x1 + 1) * SQUARE_SIZE - 2,
                                        (y1 + 1) * SQUARE_SIZE - 2, fill="white")
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(color)。強制終了します。")
            sys.exit(1)

    def stopbuttonclick(self, event):
        messagebox.showwarning("error／(^o^)＼", "stopボタンは現在準備中です。")  # 暫定3

    def GameEnd1(self):

        print(self.record)
        # 勝敗
        gameendmessage = 0
        blackcount = np.count_nonzero(self.boadsurface == DARK)
        whitecount = np.count_nonzero(self.boadsurface == LIGHT)
        if blackcount > whitecount:
            gameendmessage = str(blackcount) + "対" + str(whitecount) + "で黒の勝ち"
            messagebox.showinfo("勝敗", gameendmessage)
        elif blackcount < whitecount:
            gameendmessage = str(blackcount) + "対" + str(whitecount) + "で白の勝ち"
            messagebox.showinfo("勝敗", gameendmessage)
        else:
            gameendmessage = str(blackcount) + "対" + str(whitecount) + "で引き分け"
            messagebox.showinfo("勝敗", gameendmessage)
        # 全部green
        for i in range(NUMBER_OF_SQUARE):
            for j in range(NUMBER_OF_SQUARE):
                self.OverTurn(i, j, False, GREEN)
        # AIにゲームの終わりを伝える
        if self.player[T_DARK] == AI_PLAYER:
            self.playerAI[T_DARK].endprocess()
        if self.player[T_LIGHT] == AI_PLAYER:
            self.playerAI[T_LIGHT].endprocess()
        # AI破壊先行から消してしまうとずれて後攻が先行になってしまうのでわかりやすく後攻から消す
        if self.player[T_LIGHT] == AI_PLAYER:
            del self.playerAI[T_LIGHT]
        if self.player[T_DARK] == AI_PLAYER:
            del self.playerAI[T_DARK]
        # 枠確保
        self.playerAI = [0, 0]
        # ボードクリック不可stop不可その他可
        self.gamestartbuttonclickable = True
        self.gamestartbutton.config(state="nomal")
        self.runningstartbuttonclickable = False  # 暫定5
        self.runningstartbutton.config(state="disable")  # 暫定5
        self.boadclickable = False
        self.stopbuttonclickable = False
        self.stopbutton.config(state="disable")
        self.comboforfirst.config(state="nomal")
        self.comboforsecond.config(state="nomal")
        self.entryforrunnningtime.config(state="disable")  # 暫定5
        self.checkbuttonforlearnornot.config(state="disable")  # 暫定5
        self.selflearnbuttonclickable = False  # 暫定5
        self.selflearnbutton.config(state="disable")  # 暫定5
        self.entryforrunnningtime.config(state="disable")  # 暫定5

    def Standby(self):
        # 駒を初期配置にする
        for i in range(NUMBER_OF_SQUARE):
            for j in range(NUMBER_OF_SQUARE):
                self.OverTurn(i, j, False, GREEN)
        self.OverTurn(3, 3, False, LIGHT)
        self.OverTurn(3, 4, False, DARK)
        self.OverTurn(4, 4, False, LIGHT)
        self.OverTurn(4, 3, False, DARK)
        for i in range(NUMBER_OF_SQUARE + 2):
            self.OverTurn(i - 1, -1, False, OUT_OF_BOARD)
            self.OverTurn(NUMBER_OF_SQUARE, i - 1, False, OUT_OF_BOARD)
            self.OverTurn(i - 1, NUMBER_OF_SQUARE, False, OUT_OF_BOARD)
            self.OverTurn(-1, i - 1, False, OUT_OF_BOARD)

    def PassTheTurn(self):
        self.Turn1()

    def Turn2(self):

        # ターン進める
        if self.turnnumber == 0:
            self.turnnumber = 1
            self.firstornot = T_DARK
        else:
            if self.firstornot == T_DARK:
                self.firstornot = T_LIGHT
            elif self.firstornot == T_LIGHT:
                self.turnnumber += 1
                self.firstornot = T_DARK
            else:
                messagebox.showerror("error／(^o^)＼", "不正な値(firstornot)。強制終了します。")
                sys.exit(1)
        # おける場所確認
        moveableornotA, putablepointA = CalculateBoard.calculate_where_placeable(self.boadsurface, self.firstornot)
        if moveableornotA == STATE_GAME_END:  # お互いパスなら
            # ゲーム終わり
            nextmoving = [STATE_GAME_END, [0, 0]]
        elif moveableornotA == STATE_PASS:  # 置けないならパス
            if self.player[self.firstornot] == HUMAN:
                messagebox.showinfo("パス", "おける場所がありません,ターンをパスします")
            else:
                self.playerAI[self.firstornot].passprocess()
            nextmoving = [STATE_PASS, [0, 0]]
        elif moveableornotA == STATE_PLACE:  # おける場合
            if self.player[self.firstornot] == HUMAN:
                messagebox.showerror("error／(^o^)＼", "不正な値(player[firstornot])。強制終了します。")
                sys.exit(1)
            else:
                # AIに情報渡す
                putpoint = self.playerAI[self.firstornot].playprocess(copy.copy(self.boadsurface), putablepointA,
                                                                      self.firstornot, self.turnnumber)
                # 次へ
                nextmoving = [STATE_PLACE, putpoint]
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(moveableornotA)。強制終了します。")
            sys.exit(1)
        return nextmoving

    def move2(self, pointB):

        tempfirstornotC = 0
        # 手を表記
        gamemessage = str(pointB[X_AXIS] + 1) + "," + str(pointB[Y_AXIS] + 1)
        self.messagelabel.config(text=gamemessage)
        # 先行後攻を変換
        if self.firstornot == T_DARK:
            tempfirstornotC = TURN_OF_DARK
        elif self.firstornot == T_LIGHT:
            tempfirstornotC = TURN_OF_WHITE
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(firstornot)。強制終了します。")
            sys.exit(1)
        # ひっくり返す場所をもらう
        putableornotC, turnplaceB = CalculateBoard.calculate_where_reverse(pointB[X_AXIS], pointB[Y_AXIS],
                                                                           tempfirstornotC, self.boadsurface)
        # おけるか否か
        if putableornotC == NOT_PLACEABLE:
            if self.player[self.firstornot] == HUMAN:
                messagebox.showerror("error／(^o^)＼", "不正な値(player[firstornot])。強制終了します。")
                sys.exit(1)
            else:
                messagebox.showerror("error／(^o^)＼", "AIが不正な場所に駒がおこうとしました。強制終了します。")
                sys.exit(1)
        else:
            # 押せる場所表示を消す
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    self.gamecanvas.create_rectangle(i * SQUARE_SIZE + 1, j * SQUARE_SIZE + 1,
                                                     (i + 1) * SQUARE_SIZE - 1,
                                                     (j + 1) * SQUARE_SIZE - 1, outline="green")
            # 押した場所表示をする
            self.gamecanvas.create_rectangle(pointB[X_AXIS] * SQUARE_SIZE + 1, pointB[Y_AXIS] * SQUARE_SIZE + 1,
                                             (pointB[X_AXIS] + 1) * SQUARE_SIZE - 1,
                                             (pointB[Y_AXIS] + 1) * SQUARE_SIZE - 1,
                                             outline="yellow")
            # 画面を更新して0.01秒待つ
            self.gamecanvas.update()
            sleep(0.01)
            # 押した場所表示を消す
            self.gamecanvas.create_rectangle(pointB[X_AXIS] * SQUARE_SIZE + 1, pointB[Y_AXIS] * SQUARE_SIZE + 1,
                                             (pointB[X_AXIS] + 1) * SQUARE_SIZE - 1,
                                             (pointB[Y_AXIS] + 1) * SQUARE_SIZE - 1,
                                             outline="green")
            # 全マス調べてひっくり返る場所表示をする
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if turnplaceB[i][j]:
                        self.gamecanvas.create_rectangle(i * SQUARE_SIZE + 1, j * SQUARE_SIZE + 1,
                                                         (i + 1) * SQUARE_SIZE - 1, (j + 1) * SQUARE_SIZE - 1,
                                                         outline="yellow")
            # 画面を更新して0.01秒待つ
            self.gamecanvas.update()
            sleep(0.01)
            # 全マス調べてひっくり返す
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if turnplaceB[i][j]:
                        self.OverTurn(x1=i, y1=j, option1=True)
            # 押した場所に駒をおく
            self.OverTurn(pointB[X_AXIS], pointB[Y_AXIS], False, tempfirstornotC)
            # 画面を更新して0.01秒待つ
            self.gamecanvas.update()
            sleep(0.01)
            # 全マス調べてひっくり返る場所表示を消す
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if turnplaceB[i][j]:
                        self.gamecanvas.create_rectangle(i * SQUARE_SIZE + 1, j * SQUARE_SIZE + 1,
                                                         (i + 1) * SQUARE_SIZE - 1, (j + 1) * SQUARE_SIZE - 1,
                                                         outline="green")
            # 相手AIに伝える為のデータ
            self.record.append(copy.copy(pointB))
            # 次へ

    def GameAIvsAI(self):
        while True:
            moveableornotC, putpointB = self.Turn2()
            if moveableornotC == PLACEABLE:
                self.move2(putpointB)
            elif moveableornotC == NOT_PLACEABLE:
                pass
            elif moveableornotC == STATE_GAME_END:
                break
            else:
                messagebox.showerror("error／(^o^)＼", "不正な値(moveableornotC)。強制終了します。")
                sys.exit(1)
        self.GameEnd1()

    def move1(self, pointB):

        tempfirstornotC = 0
        # 手を表記
        gamemessage = str(pointB[X_AXIS] + 1) + "," + str(pointB[Y_AXIS] + 1)
        self.messagelabel.config(text=gamemessage)
        # 先行後攻を変換
        if self.firstornot == T_DARK:
            tempfirstornotC = TURN_OF_DARK
        elif self.firstornot == T_LIGHT:
            tempfirstornotC = TURN_OF_WHITE
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(firstornot)。強制終了します。")
            sys.exit(1)
        # ひっくり返す場所をもらう
        putableornotC, turnplaceB = CalculateBoard.calculate_where_reverse(pointB[X_AXIS], pointB[Y_AXIS],
                                                                           tempfirstornotC, self.boadsurface)
        # おけるか否か
        if putableornotC == NOT_PLACEABLE:
            if self.player[self.firstornot] == HUMAN:
                self.messagelabel.config(text="そこにはおけません")
                # boadclickで押せなくなっていたボードを押せるようにする
                self.boadclickable = True
            else:
                messagebox.showerror("error／(^o^)＼", "AIが不正な場所に駒がおこうとしました。強制終了します。")
                sys.exit(1)
        else:
            # 押せる場所表示を消す
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    self.gamecanvas.create_rectangle(i * SQUARE_SIZE + 1, j * SQUARE_SIZE + 1,
                                                     (i + 1) * SQUARE_SIZE - 1,
                                                     (j + 1) * SQUARE_SIZE - 1, outline="green")
            # 押した場所表示をする
            self.gamecanvas.create_rectangle(pointB[X_AXIS] * SQUARE_SIZE + 1, pointB[Y_AXIS] * SQUARE_SIZE + 1,
                                             (pointB[X_AXIS] + 1) * SQUARE_SIZE - 1,
                                             (pointB[Y_AXIS] + 1) * SQUARE_SIZE - 1,
                                             outline="yellow")
            # 画面を更新して0.01秒待つ
            self.gamecanvas.update()
            sleep(0.01)
            # 押した場所表示を消す
            self.gamecanvas.create_rectangle(pointB[X_AXIS] * SQUARE_SIZE + 1, pointB[Y_AXIS] * SQUARE_SIZE + 1,
                                             (pointB[X_AXIS] + 1) * SQUARE_SIZE - 1,
                                             (pointB[Y_AXIS] + 1) * SQUARE_SIZE - 1,
                                             outline="green")
            # 全マス調べてひっくり返る場所表示をする
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if turnplaceB[i][j]:
                        self.gamecanvas.create_rectangle(i * SQUARE_SIZE + 1, j * SQUARE_SIZE + 1,
                                                         (i + 1) * SQUARE_SIZE - 1, (j + 1) * SQUARE_SIZE - 1,
                                                         outline="yellow")
            # 画面を更新して0.01秒待つ
            self.gamecanvas.update()
            sleep(0.01)
            # 全マス調べてひっくり返す
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if turnplaceB[i][j]:
                        self.OverTurn(x1=i, y1=j, option1=True)
            # 押した場所に駒をおく
            self.OverTurn(pointB[X_AXIS], pointB[Y_AXIS], False, tempfirstornotC)
            # 画面を更新して0.01秒待つ
            self.gamecanvas.update()
            sleep(0.01)
            # 全マス調べてひっくり返る場所表示を消す
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    if turnplaceB[i][j]:
                        self.gamecanvas.create_rectangle(i * SQUARE_SIZE + 1, j * SQUARE_SIZE + 1,
                                                         (i + 1) * SQUARE_SIZE - 1, (j + 1) * SQUARE_SIZE - 1,
                                                         outline="green")
            # 相手AIに伝える為のデータ
            self.record.append(copy.copy(pointB))
            # 次へ
            self.Turn1()

    def boadclick(self, event):
        # クリック個所を調べて次につなげる
        x3 = self.gamecanvas.canvasx(event.x)
        y3 = self.gamecanvas.canvasx(event.y)
        x4 = int(x3 // SQUARE_SIZE)
        y4 = int(y3 // SQUARE_SIZE)
        pointA = [x4, y4]
        if not self.boadclickable:
            self.messagelabel.config(text="現在ボードクリック不可です")
        else:
            # ボード押せないようにする
            self.boadclickable = False
            self.move1(pointA)

    def Turn1(self):

        # ターン進める
        if self.turnnumber == 0:
            self.turnnumber = 1
            self.firstornot = T_DARK
        else:
            if self.firstornot == T_DARK:
                self.firstornot = T_LIGHT
            elif self.firstornot == T_LIGHT:
                self.turnnumber += 1
                self.firstornot = T_DARK
            else:
                messagebox.showerror("error／(^o^)＼", "不正な値(firstornot)。強制終了します。")
                sys.exit(1)
        # おける場所確認
        moveableornotA, putablepointA = CalculateBoard.calculate_where_placeable(self.boadsurface, self.firstornot)
        if moveableornotA == STATE_GAME_END:  # お互いパスなら
            # ゲーム終わり
            self.GameEnd1()
        elif moveableornotA == STATE_PASS:  # 置けないならパス
            if self.player[self.firstornot] == HUMAN:
                messagebox.showinfo("パス", "おける場所がありません,ターンをパスします")
            else:
                self.playerAI[self.firstornot].passprocess()
            self.PassTheTurn()
        elif moveableornotA == STATE_PLACE:  # おける場合
            if self.player[self.firstornot] == HUMAN:
                # おける場所を色で伝える
                for i in range(NUMBER_OF_SQUARE):
                    for j in range(NUMBER_OF_SQUARE):
                        if putablepointA[i][j] == PLACEABLE:
                            self.gamecanvas.create_rectangle(i * SQUARE_SIZE + 1, j * SQUARE_SIZE + 1,
                                                             (i + 1) * SQUARE_SIZE - 1, (j + 1) * SQUARE_SIZE - 1,
                                                             outline="yellow")
                # ボードクリック可
                self.boadclickable = True
            else:
                # AIに情報渡す
                putpoint = self.playerAI[self.firstornot].playprocess(copy.copy(self.boadsurface), putablepointA,
                                                                      self.firstornot, self.turnnumber)
                # 次へ
                self.move1(putpoint)
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(moveableornotA)。強制終了します。")
            sys.exit(1)

    def Gamestart(self):

        # モードを読み込みAIを作る
        playerAI = [0, 0]
        if self.comboforfirstvalue.get() == "人間":
            self.player[T_DARK] = HUMAN
            self.playerAI[T_DARK] = 0
        elif self.comboforfirstvalue.get() == "ランダム":
            self.player[T_DARK] = AI_PLAYER
            self.playerAI[T_DARK] = AIRandom()
        elif self.comboforfirstvalue.get() == "優先順位型":
            self.player[T_DARK] = AI_PLAYER
            self.playerAI[T_DARK] = AILookPriority()
        elif self.comboforfirstvalue.get() == "先読み型":
            self.player[T_DARK] = AI_PLAYER
            self.playerAI[T_DARK] = AIReadAhead()
        elif self.comboforfirstvalue.get() == "強化学習":
            self.player[T_DARK] = AI_PLAYER
            self.playerAI[T_DARK] = AIReinforcementLearning(self.entryforrunnningtimevalue.get())
            messagebox.showerror("error／(^o^)＼", "指定された先行のAIがまだ実装されていません。強制終了します")  # 暫定2
            sys.exit(1)  # 暫定2
        elif self.comboforfirstvalue.get() == "進化学習":
            self.player[T_DARK] = AI_PLAYER
            self.playerAI[T_DARK] = AIGA(self.entryforrunnningtimevalue.get())
            messagebox.showerror("error／(^o^)＼", "指定された先行のAIがまだ実装されていません。強制終了します")  # 暫定2
            sys.exit(1)  # 暫定2
        else:
            messagebox.showerror("error／(^o^)＼", "先行のAI指定が不正です。強制終了します")
            sys.exit(1)

        if self.comboforsecondvalue.get() == "人間":
            self.player[T_LIGHT] = HUMAN
            self.playerAI[T_LIGHT] = 0
        elif self.comboforsecondvalue.get() == "ランダム":
            self.player[T_LIGHT] = AI_PLAYER
            self.playerAI[T_LIGHT] = AIRandom()
        elif self.comboforsecondvalue.get() == "優先順位型":
            self.player[T_LIGHT] = AI_PLAYER
            self.playerAI[T_LIGHT] = AILookPriority()
        elif self.comboforsecondvalue.get() == "先読み型":
            self.player[T_LIGHT] = AI_PLAYER
            self.playerAI[T_LIGHT] = AIReadAhead()
        elif self.comboforsecondvalue.get() == "強化学習":
            self.player[T_LIGHT] = AI_PLAYER
            if self.comboforfirstvalue.get() == "強化学習":
                self.playerAI[T_LIGHT] = playerAI[T_DARK]
            else:
                self.playerAI[T_LIGHT] = AIReinforcementLearning(self.entryforrunnningtimevalue.get())
            messagebox.showerror("error／(^o^)＼", "指定された先行のAIがまだ実装されていません。強制終了します")  # 暫定2
            sys.exit(1)  # 暫定2
        elif self.comboforsecondvalue.get() == "進化学習":
            self.player[T_LIGHT] = AI_PLAYER
            if self.comboforfirstvalue.get() == "進化学習":
                self.playerAI[T_LIGHT] = playerAI[T_DARK]
            else:
                self.playerAI[T_LIGHT] = AIGA(self.entryforrunnningtimevalue.get())
            messagebox.showerror("error／(^o^)＼", "指定された先行のAIがまだ実装されていません。強制終了します")  # 暫定2
            sys.exit(1)  # 暫定2
        else:
            messagebox.showerror("error／(^o^)＼", "後攻のAI指定が不正です。強制終了します")
            sys.exit(1)
        # 初期準備
        self.Standby()
        # ストップボタン可　　暫定で不可3
        self.stopbuttonclickable = False  # 暫定3
        self.stopbutton.config(state="disable")  # 暫定3
        # ターン数初期化
        self.turnnumber = 0
        self.firstornot = T_DARK
        # 人間がいるかどうかで分岐
        if self.player[T_DARK] == HUMAN:
            self.Turn1()
        elif self.player[T_LIGHT] == HUMAN:
            self.Turn1()
        else:
            self.GameAIvsAI()

    def gamestartbuttonclick(self, event):

        if self.gamestartbuttonclickable:
            # 全ボタン不可
            self.gamestartbuttonclickable = False
            self.gamestartbutton.config(state="disable")
            self.runningstartbuttonclickable = False
            self.runningstartbutton.config(state="disable")
            self.boadclickable = False
            self.stopbuttonclickable = False
            self.stopbutton.config(state="disable")
            self.comboforfirst.config(state="disable")
            self.comboforsecond.config(state="disable")
            self.entryforrunnningtime.config(state="disable")
            self.checkbuttonforlearnornot.config(state="disable")
            self.selflearnbuttonclickable = False
            self.selflearnbutton.config(state="disable")
            self.entryforrunnningtime.config(state="disable")
            # ゲームをスタートさせる
            self.gameorrun = PLAY_GAME_MODE
            self.Gamestart()
        else:
            self.messagelabel.config(text="そのボタンは押せません")

    def Start(self):
        # 開始
        self.root.mainloop()


myothello = mainclass()
myothello.Start()
