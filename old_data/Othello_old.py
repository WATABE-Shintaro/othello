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
SquareSize = 50  # マスの大きさ
TheNumberOfSquare = 8  # マスの数
GapSize = 50  # 隙間の広さ
BoadSize = SquareSize * TheNumberOfSquare  # ボードの広さ
OptionsHight = 50  # オプションの縦の幅
# マスのステート
OutBoad = -2
Black = -1
Green = 0
White = 1
# ターンが先行か後攻か
FirstT = -1
SecondT = 1
OtherT = 3
# 配列用の先行か後攻か
FirstP = 0
SecondP = 1
OtherP = 2
# 人かAIか
Human = 0
AIPlayer = 1
# ゲームモード
GameMode = 0
RunMode = 1
# 座標
cX = 0
cY = 1
# そこにおけるかどうか
NotPuttable = 0
Puttable = 1
# おける場所があるか
DoublePass = -1
NotMoveable = 0
Moveable = 1


# 暫定9
# aaa=AIRandom()

# クラス群
# ランダム
class AIRandom():
    def __init__(self):
        pass

    def playprocess(self, aiboadsurface, aiputablepoint, aifirstornot, aiturnnumber):
        puttablecount = np.count_nonzero(aiputablepoint == Puttable)
        thedecision = random.randrange(puttablecount)
        k = 0
        pointreturn = [0, 0]
        for i in range(TheNumberOfSquare):  # 暫定9二重ループをブレークしたい
            for j in range(TheNumberOfSquare):
                if aiputablepoint[i][j] == Puttable:
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
class AILookPriority():
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
            if aiputablepoint[aipoint[cX], aipoint[cY]] == Puttable:
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
class AIReadAhead():

    def __init__(self):
        self.ChangeMoveTurnNumber = 26
        self.Deeplevel = 5

    def playprocess(self, aiboadsurface, aiputablepoint, aifirstornot, aiturnnumber):
        alpha = None
        beta = None
        if aifirstornot == FirstP:
            self.firstornotT2 = FirstT
        elif aifirstornot == SecondP:
            self.firstornotT2 = SecondT
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(firstornot)。強制終了します。")
            sys.exit(1)
        firstornotT = self.firstornotT2
        moveableornot, putableplace, trunplacelist = searchandscan.Search2(aiboadsurface, firstornotT=firstornotT)
        if moveableornot != Moveable:
            messagebox.showerror("error／(^o^)＼", "不正な値(moveableornot)。強制終了します。")
            sys.exit(1)
        if aiturnnumber >= 26:
            scoremax = None
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    if putableplace[i, j] == Puttable:
                        nextboadsurface = copy.copy(aiboadsurface)
                        nextboadsurface[i + 1][j + 1] = firstornotT
                        for k in range(TheNumberOfSquare):
                            for l in range(TheNumberOfSquare):
                                if trunplacelist[i][j][k][l] == True:
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
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    if putableplace[i, j] == Puttable:
                        nextboadsurface = copy.copy(aiboadsurface)
                        nextboadsurface[i + 1][j + 1] = firstornotT
                        for k in range(TheNumberOfSquare):
                            for l in range(TheNumberOfSquare):
                                if trunplacelist[i][j][k][l] == True:
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
        moveableornot, puttableplace = searchandscan.Search(boadsurface2, firstornotT=firstornotT)
        if moveableornot == Puttable:
            puttablecount = np.count_nonzero(puttableplace == Puttable)
        else:
            puttablecount = 0
        A = puttablecount * firstornotT * self.firstornotT2
        templist = [boadsurface2[1][1], boadsurface2[1][8], boadsurface2[8][8], boadsurface2[8][1]]
        B = templist.count(firstornotT) - templist.count(firstornotT * -1)
        return A + B * 5

    def selectmaxscore(self, boadsurface2, depth, alpha, beta, firstornotT):
        if depth == 0:
            return self.makescore(boadsurface2, firstornotT)
        moveableornot, putableplace, trunplacelist = searchandscan.Search2(boadsurface2, firstornotT=firstornotT)
        depth -= 1
        if moveableornot == Moveable:
            scoremax = None
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    if putableplace[i, j] == Puttable:
                        nextboadsurface = copy.copy(boadsurface2)
                        nextboadsurface[i + 1][j + 1] = firstornotT
                        for k in range(TheNumberOfSquare):
                            for l in range(TheNumberOfSquare):
                                if trunplacelist[i][j][k][l] == True:
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
        elif moveableornot == NotMoveable:
            score = self.selectminscore(boadsurface2, depth, alpha, beta, firstornotT * -1)
            return score
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(moveableornot)。強制終了します。")
            sys.exit(1)

    def selectminscore(self, boadsurface2, depth, alpha, beta, firstornotT):
        if depth == 0:
            return self.makescore(boadsurface2, firstornotT)
        moveableornot, putableplace, trunplacelist = searchandscan.Search2(boadsurface2, firstornotT=firstornotT)
        depth -= 1
        if moveableornot == Moveable:
            scoremin = None
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    if putableplace[i, j] == Puttable:
                        nextboadsurface = copy.copy(boadsurface2)
                        nextboadsurface[i + 1][j + 1] = firstornotT
                        for k in range(TheNumberOfSquare):
                            for l in range(TheNumberOfSquare):
                                if trunplacelist[i][j][k][l] == True:
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
        elif moveableornot == NotMoveable:
            score = self.selectmaxscore(boadsurface2, depth, alpha, beta, firstornotT * -1)
            return score
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(moveableornot)。強制終了します。")
            sys.exit(1)

    def countmypiece(self, boadsurface2):
        return np.count_nonzero(boadsurface2 == self.firstornotT2)

    def selectmaxpiece(self, boadsurface2, alpha, beta, firstornotT):
        moveableornot, putableplace, trunplacelist = searchandscan.Search2(boadsurface2, firstornotT=firstornotT)
        if moveableornot == DoublePass:
            return self.countmypiece(boadsurface2)
        elif moveableornot == NotMoveable:
            score = self.selectminpiece(boadsurface2, alpha, beta, firstornotT * -1)
            return score
        elif moveableornot == Puttable:
            scoremax = None
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    if putableplace[i, j] == Puttable:
                        nextboadsurface = copy.copy(boadsurface2)
                        nextboadsurface[i + 1][j + 1] = firstornotT
                        for k in range(TheNumberOfSquare):
                            for l in range(TheNumberOfSquare):
                                if trunplacelist[i][j][k][l] == True:
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
        moveableornot, putableplace, trunplacelist = searchandscan.Search2(boadsurface2, firstornotT=firstornotT)
        if moveableornot == DoublePass:
            return self.countmypiece(boadsurface2)
        elif moveableornot == NotMoveable:
            score = self.selectmaxpiece(boadsurface2, alpha, beta, firstornotT * -1)
            return score
        elif moveableornot == Puttable:
            scoremin = None
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    if putableplace[i, j] == Puttable:
                        nextboadsurface = copy.copy(boadsurface2)
                        nextboadsurface[i + 1][j + 1] = firstornotT
                        for k in range(TheNumberOfSquare):
                            for l in range(TheNumberOfSquare):
                                if trunplacelist[i][j][k][l] == True:
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
class AIReinforcementLearning():
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
class AIGA():
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
class searchandscan():
    def __init__(self):
        pass

    # そこにおいたときの挙動をしめしてくれる
    @classmethod
    def Scan(cls, x5, y5, tempfirstornotB, boadsurface2):
        # boadsurface2に合うように+1する
        pointC = [x5 + 1, y5 + 1]
        # 最初置けないに設定して、あとから置けるに設定しなおす
        putableornotB = NotPuttable
        # 配列宣言
        turnplaceA = np.zeros((TheNumberOfSquare, TheNumberOfSquare))
        # その場所がgreenの場合のみおける
        if boadsurface2[pointC[cX], pointC[cY]] == Black or boadsurface2[pointC[cX], pointC[cY]] == White:
            pass
        elif boadsurface2[pointC[cX], pointC[cY]] == Green:
            # ひっくり返す場所検索
            # 8方向
            l = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
            # 8方向繰り返し
            for delta in l:
                # 位置検索用
                temppoint = copy.copy(pointC)
                while True:
                    # 位置ずらす
                    temppoint[cX] = temppoint[cX] + delta[cX]
                    temppoint[cY] = temppoint[cY] + delta[cY]
                    # 値を評価
                    z1 = boadsurface2[temppoint[cX], temppoint[cY]] * tempfirstornotB
                    if z1 == -1:
                        # 続ける
                        pass
                    elif z1 == 1:
                        # ひっくり返しへ(ひっくり返しonにする)
                        flag = True
                        break
                    elif z1 == -2 or z1 == 0 or z1 == 2:
                        # 何もせず終わる
                        flag = False
                        break
                    else:
                        messagebox.showerror("error／(^o^)＼", "不正な値(color)。強制終了します。")
                        sys.exit(1)
                # ひっくり返しonのとき
                if flag == True:
                    while True:
                        # 位置逆にずらす
                        temppoint[cX] = temppoint[cX] - delta[cX]
                        temppoint[cY] = temppoint[cY] - delta[cY]
                        # もとの位置に戻ったら終了
                        if temppoint == pointC:
                            break
                        # そこの位置をひっくり返すに
                        turnplaceA[temppoint[cX] - 1, temppoint[cY] - 1] = True
                        # ひっくり返す場所あるにする
                        putableornotB = Puttable
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(pointC又はboadsurface2)。強制終了します。")
            sys.exit(1)
        return (putableornotB, turnplaceA)

    # おけるかどうかのみ示すようにする予定 暫定9
    @classmethod
    def Scan2(cls, x5, y5, tempfirstornotB, boadsurface2):
        # boadsurfaceに合うように+1する
        pointC = [x5 + 1, y5 + 1]
        # 最初置けないに設定して、あとから置けるに設定しなおす
        putableornotB = NotPuttable
        # 配列宣言
        turnplaceA = np.zeros((TheNumberOfSquare, TheNumberOfSquare))
        # その場所がgreenの場合のみおける
        if boadsurface2[pointC[cX], pointC[cY]] == Black or boadsurface2[pointC[cX], pointC[cY]] == White:
            pass
        elif boadsurface2[pointC[cX], pointC[cY]] == Green:
            # ひっくり返す場所検索
            # 8方向
            l = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
            # 8方向繰り返し
            for delta in l:
                # 位置検索用
                temppoint = copy.copy(pointC)
                while True:
                    # 位置ずらす
                    temppoint[cX] = temppoint[cX] + delta[cX]
                    temppoint[cY] = temppoint[cY] + delta[cY]
                    # 値を評価
                    z1 = boadsurface2[temppoint[cX], temppoint[cY]] * tempfirstornotB
                    if z1 == -1:
                        # 続ける
                        pass
                    elif z1 == 1:
                        # ひっくり返しへ(ひっくり返しonにする)
                        flag = True
                        break
                    elif z1 == -2 or z1 == 0 or z1 == 2:
                        # 何もせず終わる
                        flag = False
                        break
                    else:
                        messagebox.showerror("error／(^o^)＼", "不正な値(color)。強制終了します。")
                        sys.exit(1)
                # ひっくり返しonのとき
                if flag == True:
                    while True:
                        # 位置逆にずらす
                        temppoint[cX] = temppoint[cX] - delta[cX]
                        temppoint[cY] = temppoint[cY] - delta[cY]
                        # もとの位置に戻ったら終了
                        if temppoint == pointC:
                            break
                        # そこの位置をひっくり返すに
                        turnplaceA[temppoint[cX] - 1, temppoint[cY] - 1] = True
                        # ひっくり返す場所あるにする
                        putableornotB = Puttable
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(pointC又はboadsurface2)。強制終了します。")
            sys.exit(1)
        return (putableornotB, turnplaceA)

    # おける場所のみ示す
    @classmethod
    def Search(cls, boadsurface2, firstornotP=OtherP, firstornotT=OtherT):
        moveableornotB = NotMoveable
        putablepointB = np.zeros((TheNumberOfSquare, TheNumberOfSquare))
        tempfirstornotA = 0
        # 先行後攻を変換
        if not firstornotT == OtherT:
            tempfirstornotA = firstornotT
        else:
            if firstornotP == FirstP:
                tempfirstornotA = FirstT
            elif firstornotP == SecondP:
                tempfirstornotA = SecondT
            else:
                messagebox.showerror("error／(^o^)＼", "不正な値(firstornot)。強制終了します。")
                sys.exit(1)
        # 一マスごとにおける場所を調べておける場所があるかをおける場所を記録した配列に記録、これを全マスやり、一マスでもおける場所があるか調べる
        for i in range(TheNumberOfSquare):
            for j in range(TheNumberOfSquare):
                putableornotA, temp = cls.Scan(i, j, tempfirstornotA, boadsurface2)  # 暫定9ベクトル化
                if putableornotA == Puttable:
                    moveableornotB = Moveable
                    putablepointB[i, j] = Puttable
                else:
                    putablepointB[i, j] = NotPuttable
        # 置けないなら次ターンも調べる 両方パスに設定して　全マス調べておける場所があるなら片パスに設定する
        if moveableornotB == NotPuttable:
            moveableornotB = DoublePass
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    putableornotA, temp = cls.Scan(i, j, tempfirstornotA * -1, boadsurface2)  # 暫定9ベクトル化
                    if putableornotA == Puttable:
                        moveableornotB = NotPuttable
        return (moveableornotB, putablepointB)

    # おける場所とともにおいたときの挙動も示す
    @classmethod
    def Search2(cls, boadsurface2, firstornotP=OtherP, firstornotT=OtherT):
        moveableornotB = NotMoveable
        putablepointB = np.zeros((TheNumberOfSquare, TheNumberOfSquare))
        tempfirstornotA = 0
        trunplacelist = np.zeros((TheNumberOfSquare, TheNumberOfSquare, TheNumberOfSquare, TheNumberOfSquare))
        # 先行後攻を変換
        if not firstornotT == OtherT:
            tempfirstornotA = firstornotT
        else:
            if firstornotP == FirstP:
                tempfirstornotA = FirstT
            elif firstornotP == SecondP:
                tempfirstornotA = SecondT
            else:
                messagebox.showerror("error／(^o^)＼", "不正な値(firstornot)。強制終了します。")
                sys.exit(1)
        # 一マスごとにおける場所を調べておける場所があるかをおける場所を記録した配列に記録、これを全マスやり、一マスでもおける場所があるか調べる
        for i in range(TheNumberOfSquare):
            for j in range(TheNumberOfSquare):
                putableornotA, turnplaceC = cls.Scan2(i, j, tempfirstornotA, boadsurface2)  # 暫定9ベクトル化
                if putableornotA == Puttable:
                    moveableornotB = Moveable
                    putablepointB[i, j] = Puttable
                    trunplacelist[i][j] = copy.copy(turnplaceC)
                else:
                    putablepointB[i, j] = NotPuttable
        # 置けないなら次ターンも調べる 両方パスに設定して　全マス調べておける場所があるなら片パスに設定する
        if moveableornotB == NotPuttable:
            moveableornotB = DoublePass
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    putableornotA, turnplaceC = cls.Scan2(i, j, tempfirstornotA * -1, boadsurface2)  # 暫定9ベクトル化
                    if putableornotA == Puttable:
                        moveableornotB = NotPuttable
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
            height=GapSize * 2 + BoadSize + OptionsHight,
            width=GapSize + BoadSize + GapSize + 200 + GapSize,
            relief='sunken',
            borderwidth=5)
        self.mainframe.grid()

        # ゲーム画面用
        self.mainpanel = ttk.Frame(
            self.mainframe,
            relief='sunken',
            borderwidth=5)
        self.mainpanel.place(x=GapSize, y=GapSize)

        # ゲーム画面にボード用キャンバス作成
        self.gamecanvas = tk.Canvas(
            self.mainpanel,
            height=BoadSize,
            width=BoadSize)
        self.gamecanvas.create_rectangle(0, 0, BoadSize, BoadSize, fill='green')  # 塗りつぶし
        for i in range(TheNumberOfSquare - 1):
            tempx = (i + 1) * SquareSize
            self.gamecanvas.create_line(tempx, 0, tempx, BoadSize)
            self.gamecanvas.create_line(0, tempx, BoadSize, tempx)
        self.gamecanvas.bind("<1>", self.boadclick)
        self.gamecanvas.grid()

        # メッセージ用のラベル
        self.messagelabel = ttk.Label(
            self.mainframe,
            text='a',
            background='#0000aa',
            foreground='#ffffff')
        self.messagelabel.place(x=GapSize, y=GapSize + BoadSize + GapSize)

        # 一回戦う為のボタン
        self.gamestartbutton = ttk.Button(
            self.mainframe,
            text='game')
        self.gamestartbutton.bind("<1>", self.gamestartbuttonclick)
        self.gamestartbutton.place(x=GapSize + BoadSize + GapSize, y=GapSize)

        # 何回も試行するためのボタン
        self.runningstartbutton = ttk.Button(
            self.mainframe,
            text='run')
        self.runningstartbutton.bind("<1>", self.runningstartbuttonclick)
        self.runningstartbutton.place(x=GapSize + BoadSize + GapSize + 100, y=GapSize)

        # 先行のAI決める
        self.labelforfirst = ttk.Label(
            self.mainframe,
            text="先行"
        )
        self.labelforfirst.place(x=GapSize + BoadSize + GapSize, y=GapSize + OptionsHight)
        self.comboforfirstvalue = StringVar()
        self.comboforfirst = ttk.Combobox(
            self.mainframe,
            state="readonly",
            textvariable=self.comboforfirstvalue
        )
        self.comboforfirst['values'] = ["人間", "ランダム", "優先順位型", "先読み型", "強化学習", "進化学習"]
        self.comboforfirst.set("人間")
        self.comboforfirst.place(x=GapSize + BoadSize + GapSize + 50, y=GapSize + OptionsHight)

        # 後攻のAI決める
        self.labelforsecond = ttk.Label(
            self.mainframe,
            text="後攻"
        )
        self.labelforsecond.place(x=GapSize + BoadSize + GapSize, y=GapSize + OptionsHight * 2)
        self.comboforsecondvalue = StringVar()
        self.comboforsecond = ttk.Combobox(
            self.mainframe,
            state="readonly",
            textvariable=self.comboforsecondvalue
        )
        self.comboforsecond['values'] = ["人間", "ランダム", "優先順位型", "先読み型", "強化学習", "進化学習"]
        self.comboforsecond.set("人間")
        self.comboforsecond.place(x=GapSize + BoadSize + GapSize + 50, y=GapSize + OptionsHight * 2)

        # 学習するか否か設定用
        self.checkbuttonforlearnornotvalue = BooleanVar()
        self.checkbuttonforlearnornot = ttk.Checkbutton(
            self.mainframe,
            text="学習する",
            onvalue=True,
            offvalue=False,
            variable=self.checkbuttonforlearnornotvalue
        )
        self.checkbuttonforlearnornot.place(x=GapSize + BoadSize + GapSize + 20, y=GapSize + OptionsHight * 3 + GapSize)

        # 試合試行回数設定用
        self.labelforentry = ttk.Label(
            self.mainframe,
            text="試合回数"
        )
        self.labelforentry.place(x=GapSize + BoadSize + GapSize + 20,
                                 y=GapSize + OptionsHight * 3 + GapSize + OptionsHight)
        self.entryforrunnningtimevalue = StringVar()
        self.entryforrunnningtime = ttk.Entry(
            self.mainframe,
            textvariable=self.entryforrunnningtimevalue
        )
        self.entryforrunnningtime.place(x=GapSize + BoadSize + GapSize + 80,
                                        y=GapSize + OptionsHight * 3 + GapSize + OptionsHight)

        # 試合止めるよう
        self.stopbutton = ttk.Button(
            self.mainframe,
            text="stop"
        )
        self.stopbutton.bind("<1>", self.stopbuttonclick)
        self.stopbutton.place(x=GapSize + BoadSize + GapSize, y=GapSize + OptionsHight * 3 + GapSize + OptionsHight * 2)

        # 自己学習を始めるボタン
        self.selflearnbutton = ttk.Button(
            self.mainframe,
            text="selflern"
        )
        self.selflearnbutton.bind("<1>", self.selflearnbuttonclick)
        self.selflearnbutton.place(x=GapSize + BoadSize + GapSize,
                                   y=GapSize + OptionsHight * 3 + GapSize + OptionsHight * 4)

        # 自己学習回数設定用
        self.labelforentry2 = ttk.Label(
            self.mainframe,
            text="自己学習回数"
        )
        self.labelforentry2.place(x=GapSize + BoadSize + GapSize,
                                  y=GapSize + OptionsHight * 3 + GapSize + OptionsHight * 5)
        self.entryforselflearntimevalue = StringVar()
        self.entryforselflearntime = ttk.Entry(
            self.mainframe,
            textvariable=self.entryforselflearntimevalue
        )
        self.entryforselflearntime.place(x=GapSize + BoadSize + GapSize + 80,
                                         y=GapSize + OptionsHight * 3 + GapSize + OptionsHight * 5)

        # 変数宣言
        self.boadsurface = np.zeros((TheNumberOfSquare + 2, TheNumberOfSquare + 2), dtype=int)
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
            self.gameorrun = RunMode
        else:
            self.messagelabel.config(text="そのボタンは押せません")

    def OverTurn(self, x1, y1, option1, color=0):
        x2 = x1 + 1
        y2 = y1 + 1
        if option1 == True:
            color = self.boadsurface[x2][y2] * -1
        # 色変更
        self.boadsurface[x2][y2] = color
        if color == OutBoad:
            pass
        elif color == Black:
            self.gamecanvas.create_oval(x1 * SquareSize + 2, y1 * SquareSize + 2, (x1 + 1) * SquareSize - 2,
                                        (y1 + 1) * SquareSize - 2, fill="black")
        elif color == Green:
            self.gamecanvas.create_oval(x1 * SquareSize + 2, y1 * SquareSize + 2, (x1 + 1) * SquareSize - 2,
                                        (y1 + 1) * SquareSize - 2, fill="green", outline="green")
        elif color == White:
            self.gamecanvas.create_oval(x1 * SquareSize + 2, y1 * SquareSize + 2, (x1 + 1) * SquareSize - 2,
                                        (y1 + 1) * SquareSize - 2, fill="white")
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(color)。強制終了します。")
            sys.exit(1)

    def stopbuttonclick(self, event):
        messagebox.showwarning("error／(^o^)＼", "stopボタンは現在準備中です。")  # 暫定3

    def GameEnd1(self):

        print(self.record)
        # 勝敗
        gameendmessage = 0
        blackcount = np.count_nonzero(self.boadsurface == Black)
        whitecount = np.count_nonzero(self.boadsurface == White)
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
        for i in range(TheNumberOfSquare):
            for j in range(TheNumberOfSquare):
                self.OverTurn(i, j, False, Green)
        # AIにゲームの終わりを伝える
        if self.player[FirstP] == AIPlayer:
            self.playerAI[FirstP].endprocess()
        if self.player[SecondP] == AIPlayer:
            self.playerAI[SecondP].endprocess()
        # AI破壊先行から消してしまうとずれて後攻が先行になってしまうのでわかりやすく後攻から消す
        if self.player[SecondP] == AIPlayer:
            del self.playerAI[SecondP]
        if self.player[FirstP] == AIPlayer:
            del self.playerAI[FirstP]
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
        for i in range(TheNumberOfSquare):
            for j in range(TheNumberOfSquare):
                self.OverTurn(i, j, False, Green)
        self.OverTurn(3, 3, False, White)
        self.OverTurn(3, 4, False, Black)
        self.OverTurn(4, 4, False, White)
        self.OverTurn(4, 3, False, Black)
        for i in range(TheNumberOfSquare + 2):
            self.OverTurn(i - 1, -1, False, OutBoad)
            self.OverTurn(TheNumberOfSquare, i - 1, False, OutBoad)
            self.OverTurn(i - 1, TheNumberOfSquare, False, OutBoad)
            self.OverTurn(-1, i - 1, False, OutBoad)

    def PassTheTurn(self):
        self.Turn1()

    def Turn2(self):

        # ターン進める
        if self.turnnumber == 0:
            self.turnnumber = 1
            self.firstornot = FirstP
        else:
            if self.firstornot == FirstP:
                self.firstornot = SecondP
            elif self.firstornot == SecondP:
                self.turnnumber += 1
                self.firstornot = FirstP
            else:
                messagebox.showerror("error／(^o^)＼", "不正な値(firstornot)。強制終了します。")
                sys.exit(1)
        # おける場所確認
        moveableornotA, putablepointA = searchandscan.Search(self.boadsurface, self.firstornot)
        if moveableornotA == DoublePass:  # お互いパスなら
            # ゲーム終わり
            nextmoving = [DoublePass, [0, 0]]
        elif moveableornotA == NotMoveable:  # 置けないならパス
            if self.player[self.firstornot] == Human:
                messagebox.showinfo("パス", "おける場所がありません,ターンをパスします")
            else:
                self.playerAI[self.firstornot].passprocess()
            nextmoving = [NotMoveable, [0, 0]]
        elif moveableornotA == Moveable:  # おける場合
            if self.player[self.firstornot] == Human:
                messagebox.showerror("error／(^o^)＼", "不正な値(player[firstornot])。強制終了します。")
                sys.exit(1)
            else:
                # AIに情報渡す
                putpoint = self.playerAI[self.firstornot].playprocess(copy.copy(self.boadsurface), putablepointA,
                                                                      self.firstornot, self.turnnumber)
                # 次へ
                nextmoving = [Moveable, putpoint]
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(moveableornotA)。強制終了します。")
            sys.exit(1)
        return nextmoving

    def move2(self, pointB):

        tempfirstornotC = 0
        # 手を表記
        gamemessage = str(pointB[cX] + 1) + "," + str(pointB[cY] + 1)
        self.messagelabel.config(text=gamemessage)
        # 先行後攻を変換
        if self.firstornot == FirstP:
            tempfirstornotC = FirstT
        elif self.firstornot == SecondP:
            tempfirstornotC = SecondT
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(firstornot)。強制終了します。")
            sys.exit(1)
        # ひっくり返す場所をもらう
        putableornotC, turnplaceB = searchandscan.Scan(pointB[cX], pointB[cY], tempfirstornotC, self.boadsurface)
        # おけるか否か
        if putableornotC == NotPuttable:
            if self.player[self.firstornot] == Human:
                messagebox.showerror("error／(^o^)＼", "不正な値(player[firstornot])。強制終了します。")
                sys.exit(1)
            else:
                messagebox.showerror("error／(^o^)＼", "AIが不正な場所に駒がおこうとしました。強制終了します。")
                sys.exit(1)
        else:
            # 押せる場所表示を消す
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    self.gamecanvas.create_rectangle(i * SquareSize + 1, j * SquareSize + 1, (i + 1) * SquareSize - 1,
                                                     (j + 1) * SquareSize - 1, outline="green")
            # 押した場所表示をする
            self.gamecanvas.create_rectangle(pointB[cX] * SquareSize + 1, pointB[cY] * SquareSize + 1,
                                             (pointB[cX] + 1) * SquareSize - 1, (pointB[cY] + 1) * SquareSize - 1,
                                             outline="yellow")
            # 画面を更新して0.01秒待つ
            self.gamecanvas.update()
            sleep(0.01)
            # 押した場所表示を消す
            self.gamecanvas.create_rectangle(pointB[cX] * SquareSize + 1, pointB[cY] * SquareSize + 1,
                                             (pointB[cX] + 1) * SquareSize - 1, (pointB[cY] + 1) * SquareSize - 1,
                                             outline="green")
            # 全マス調べてひっくり返る場所表示をする
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    if turnplaceB[i][j] == True:
                        self.gamecanvas.create_rectangle(i * SquareSize + 1, j * SquareSize + 1,
                                                         (i + 1) * SquareSize - 1, (j + 1) * SquareSize - 1,
                                                         outline="yellow")
            # 画面を更新して0.01秒待つ
            self.gamecanvas.update()
            sleep(0.01)
            # 全マス調べてひっくり返す
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    if turnplaceB[i][j] == True:
                        self.OverTurn(x1=i, y1=j, option1=True)
            # 押した場所に駒をおく
            self.OverTurn(pointB[cX], pointB[cY], False, tempfirstornotC)
            # 画面を更新して0.01秒待つ
            self.gamecanvas.update()
            sleep(0.01)
            # 全マス調べてひっくり返る場所表示を消す
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    if turnplaceB[i][j] == True:
                        self.gamecanvas.create_rectangle(i * SquareSize + 1, j * SquareSize + 1,
                                                         (i + 1) * SquareSize - 1, (j + 1) * SquareSize - 1,
                                                         outline="green")
            # 相手AIに伝える為のデータ
            self.record.append(copy.copy(pointB))
            # 次へ

    def GameAIvsAI(self):
        while True:
            moveableornotC, putpointB = self.Turn2()
            if moveableornotC == Puttable:
                self.move2(putpointB)
            elif moveableornotC == NotPuttable:
                pass
            elif moveableornotC == DoublePass:
                break
            else:
                messagebox.showerror("error／(^o^)＼", "不正な値(moveableornotC)。強制終了します。")
                sys.exit(1)
        self.GameEnd1()

    def move1(self, pointB):

        tempfirstornotC = 0
        # 手を表記
        gamemessage = str(pointB[cX] + 1) + "," + str(pointB[cY] + 1)
        self.messagelabel.config(text=gamemessage)
        # 先行後攻を変換
        if self.firstornot == FirstP:
            tempfirstornotC = FirstT
        elif self.firstornot == SecondP:
            tempfirstornotC = SecondT
        else:
            messagebox.showerror("error／(^o^)＼", "不正な値(firstornot)。強制終了します。")
            sys.exit(1)
        # ひっくり返す場所をもらう
        putableornotC, turnplaceB = searchandscan.Scan(pointB[cX], pointB[cY], tempfirstornotC, self.boadsurface)
        # おけるか否か
        if putableornotC == NotPuttable:
            if self.player[self.firstornot] == Human:
                self.messagelabel.config(text="そこにはおけません")
                # boadclickで押せなくなっていたボードを押せるようにする
                self.boadclickable = True
            else:
                messagebox.showerror("error／(^o^)＼", "AIが不正な場所に駒がおこうとしました。強制終了します。")
                sys.exit(1)
        else:
            # 押せる場所表示を消す
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    self.gamecanvas.create_rectangle(i * SquareSize + 1, j * SquareSize + 1, (i + 1) * SquareSize - 1,
                                                     (j + 1) * SquareSize - 1, outline="green")
            # 押した場所表示をする
            self.gamecanvas.create_rectangle(pointB[cX] * SquareSize + 1, pointB[cY] * SquareSize + 1,
                                             (pointB[cX] + 1) * SquareSize - 1, (pointB[cY] + 1) * SquareSize - 1,
                                             outline="yellow")
            # 画面を更新して0.01秒待つ
            self.gamecanvas.update()
            sleep(0.01)
            # 押した場所表示を消す
            self.gamecanvas.create_rectangle(pointB[cX] * SquareSize + 1, pointB[cY] * SquareSize + 1,
                                             (pointB[cX] + 1) * SquareSize - 1, (pointB[cY] + 1) * SquareSize - 1,
                                             outline="green")
            # 全マス調べてひっくり返る場所表示をする
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    if turnplaceB[i][j] == True:
                        self.gamecanvas.create_rectangle(i * SquareSize + 1, j * SquareSize + 1,
                                                         (i + 1) * SquareSize - 1, (j + 1) * SquareSize - 1,
                                                         outline="yellow")
            # 画面を更新して0.01秒待つ
            self.gamecanvas.update()
            sleep(0.01)
            # 全マス調べてひっくり返す
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    if turnplaceB[i][j] == True:
                        self.OverTurn(x1=i, y1=j, option1=True)
            # 押した場所に駒をおく
            self.OverTurn(pointB[cX], pointB[cY], False, tempfirstornotC)
            # 画面を更新して0.01秒待つ
            self.gamecanvas.update()
            sleep(0.01)
            # 全マス調べてひっくり返る場所表示を消す
            for i in range(TheNumberOfSquare):
                for j in range(TheNumberOfSquare):
                    if turnplaceB[i][j] == True:
                        self.gamecanvas.create_rectangle(i * SquareSize + 1, j * SquareSize + 1,
                                                         (i + 1) * SquareSize - 1, (j + 1) * SquareSize - 1,
                                                         outline="green")
            # 相手AIに伝える為のデータ
            self.record.append(copy.copy(pointB))
            # 次へ
            self.Turn1()

    def boadclick(self, event):
        # クリック個所を調べて次につなげる
        x3 = self.gamecanvas.canvasx(event.x)
        y3 = self.gamecanvas.canvasx(event.y)
        x4 = int(x3 // SquareSize)
        y4 = int(y3 // SquareSize)
        pointA = [x4, y4]
        if self.boadclickable == False:
            self.messagelabel.config(text="現在ボードクリック不可です")
        else:
            # ボード押せないようにする
            self.boadclickable = False
            self.move1(pointA)

    def Turn1(self):

        # ターン進める
        if self.turnnumber == 0:
            self.turnnumber = 1
            self.firstornot = FirstP
        else:
            if self.firstornot == FirstP:
                self.firstornot = SecondP
            elif self.firstornot == SecondP:
                self.turnnumber += 1
                self.firstornot = FirstP
            else:
                messagebox.showerror("error／(^o^)＼", "不正な値(firstornot)。強制終了します。")
                sys.exit(1)
        # おける場所確認
        moveableornotA, putablepointA = searchandscan.Search(self.boadsurface, self.firstornot)
        if moveableornotA == DoublePass:  # お互いパスなら
            # ゲーム終わり
            self.GameEnd1()
        elif moveableornotA == NotMoveable:  # 置けないならパス
            if self.player[self.firstornot] == Human:
                messagebox.showinfo("パス", "おける場所がありません,ターンをパスします")
            else:
                self.playerAI[self.firstornot].passprocess()
            self.PassTheTurn()
        elif moveableornotA == Moveable:  # おける場合
            if self.player[self.firstornot] == Human:
                # おける場所を色で伝える
                for i in range(TheNumberOfSquare):
                    for j in range(TheNumberOfSquare):
                        if putablepointA[i][j] == Puttable:
                            self.gamecanvas.create_rectangle(i * SquareSize + 1, j * SquareSize + 1,
                                                             (i + 1) * SquareSize - 1, (j + 1) * SquareSize - 1,
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
            self.player[FirstP] = Human
            self.playerAI[FirstP] = 0
        elif self.comboforfirstvalue.get() == "ランダム":
            self.player[FirstP] = AIPlayer
            self.playerAI[FirstP] = AIRandom()
        elif self.comboforfirstvalue.get() == "優先順位型":
            self.player[FirstP] = AIPlayer
            self.playerAI[FirstP] = AILookPriority()
        elif self.comboforfirstvalue.get() == "先読み型":
            self.player[FirstP] = AIPlayer
            self.playerAI[FirstP] = AIReadAhead()
        elif self.comboforfirstvalue.get() == "強化学習":
            self.player[FirstP] = AIPlayer
            self.playerAI[FirstP] = AIReinforcementLearning(self.entryforrunnningtimevalue.get())
            messagebox.showerror("error／(^o^)＼", "指定された先行のAIがまだ実装されていません。強制終了します")  # 暫定2
            sys.exit(1)  # 暫定2
        elif self.comboforfirstvalue.get() == "進化学習":
            self.player[FirstP] = AIPlayer
            self.playerAI[FirstP] = AIGA(self.entryforrunnningtimevalue.get())
            messagebox.showerror("error／(^o^)＼", "指定された先行のAIがまだ実装されていません。強制終了します")  # 暫定2
            sys.exit(1)  # 暫定2
        else:
            messagebox.showerror("error／(^o^)＼", "先行のAI指定が不正です。強制終了します")
            sys.exit(1)

        if self.comboforsecondvalue.get() == "人間":
            self.player[SecondP] = Human
            self.playerAI[SecondP] = 0
        elif self.comboforsecondvalue.get() == "ランダム":
            self.player[SecondP] = AIPlayer
            self.playerAI[SecondP] = AIRandom()
        elif self.comboforsecondvalue.get() == "優先順位型":
            self.player[SecondP] = AIPlayer
            self.playerAI[SecondP] = AILookPriority()
        elif self.comboforsecondvalue.get() == "先読み型":
            self.player[SecondP] = AIPlayer
            self.playerAI[SecondP] = AIReadAhead()
        elif self.comboforsecondvalue.get() == "強化学習":
            self.player[SecondP] = AIPlayer
            if self.comboforfirstvalue.get() == "強化学習":
                self.playerAI[SecondP] = playerAI[FirstP]
            else:
                self.playerAI[SecondP] = AIReinforcementLearning(self.entryforrunnningtimevalue.get())
            messagebox.showerror("error／(^o^)＼", "指定された先行のAIがまだ実装されていません。強制終了します")  # 暫定2
            sys.exit(1)  # 暫定2
        elif self.comboforsecondvalue.get() == "進化学習":
            self.player[SecondP] = AIPlayer
            if self.comboforfirstvalue.get() == "進化学習":
                self.playerAI[SecondP] = playerAI[FirstP]
            else:
                self.playerAI[SecondP] = AIGA(self.entryforrunnningtimevalue.get())
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
        self.firstornot = FirstP
        # 人間がいるかどうかで分岐
        if self.player[FirstP] == Human:
            self.Turn1()
        elif self.player[SecondP] == Human:
            self.Turn1()
        else:
            self.GameAIvsAI()

    def gamestartbuttonclick(self, event):

        if self.gamestartbuttonclickable == True:
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
            self.gameorrun = GameMode
            self.Gamestart()
        else:
            self.messagelabel.config(text="そのボタンは押せません")

    def Start(self):
        # 開始
        self.root.mainloop()


myothello = mainclass()
myothello.Start()
