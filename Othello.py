import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import numpy as np
from time import sleep
import copy
import random
import sys

from board_object import BoardObject

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

# クラス群
# ランダム
class AIRandom:
    def __init__(self):
        pass

    def playprocess(self, board_object, turn_d_or_l, turn_number):
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
            messagebox.showerror("error", "AILookPriorityはおける場所を見つけられませんでした。強制終了します。")
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
            self.firstornotT2 = TURN_OF_LIGHT
        else:
            messagebox.showerror("error", "不正な値(firstornot)。強制終了します。")
            sys.exit(1)
        firstornotT = self.firstornotT2
        moveableornot, putableplace, trunplacelist = CalculateBoard.Search2(aiboadsurface, firstornotT=firstornotT)
        if moveableornot != STATE_PLACE:
            messagebox.showerror("error", "不正な値(moveableornot)。強制終了します。")
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



# メインクラス
class MainClass:

    def __init__(self):

        # 核となるもの？
        self.tk_root = Tk()
        self.tk_root.title('othello')

        # ウィンドウ作成
        self.main_frame = ttk.Frame(
            self.tk_root,
            height=GAP_SIZE * 2 + BOARD_SIZE + OPTIONS_HEIGHT,
            width=GAP_SIZE + BOARD_SIZE + GAP_SIZE + 200 + GAP_SIZE,
            relief='sunken',
            borderwidth=5)
        self.main_frame.grid()

        # ゲーム画面用
        self.main_panel = ttk.Frame(
            self.main_frame,
            relief='sunken',
            borderwidth=5)
        self.main_panel.place(x=GAP_SIZE, y=GAP_SIZE)

        # ゲーム画面にボード用キャンバス作成
        self.game_canvas = tk.Canvas(
            self.main_panel,
            height=BOARD_SIZE,
            width=BOARD_SIZE)
        self.game_canvas.create_rectangle(0, 0, BOARD_SIZE, BOARD_SIZE, fill='green')  # 塗りつぶし
        for i in range(NUMBER_OF_SQUARE - 1):
            temp = (i + 1) * SQUARE_SIZE
            self.game_canvas.create_line(temp, 0, temp, BOARD_SIZE)
            self.game_canvas.create_line(0, temp, BOARD_SIZE, temp)
        self.game_canvas.bind("<1>", self.board_click)
        self.game_canvas.grid()

        # メッセージ用のラベル
        self.message_label = ttk.Label(
            self.main_frame,
            text='a',
            background='#0000aa',
            foreground='#ffffff')
        self.message_label.place(x=GAP_SIZE, y=GAP_SIZE + BOARD_SIZE + GAP_SIZE)

        # 一回戦う為のボタン
        self.gamestart_button = ttk.Button(
            self.main_frame,
            text='game')
        self.gamestart_button.bind("<1>", self.game_start_button_click)
        self.gamestart_button.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE, y=GAP_SIZE)

        # 何回も試行するためのボタン
        self.running_start_button = ttk.Button(
            self.main_frame,
            text='run')
        self.running_start_button.bind("<1>", self.running_start_button_click)
        self.running_start_button.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE,
                                        y=GAP_SIZE + OPTIONS_HEIGHT * 3 + GAP_SIZE + OPTIONS_HEIGHT * 4)

        # 先行のAI決める
        self.label_for_dirk = ttk.Label(
            self.main_frame,
            text="先行"
        )
        self.label_for_dirk.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE, y=GAP_SIZE + OPTIONS_HEIGHT)
        self.combo_for_dirk_ai_value = StringVar()
        self.combo_for_dirk_ai = ttk.Combobox(
            self.main_frame,
            state="readonly",
            textvariable=self.combo_for_dirk_ai_value
        )
        self.combo_for_dirk_ai['values'] = ["人間", "ランダム", "優先順位型", "先読み型", "強化学習", "進化学習"]
        self.combo_for_dirk_ai.set("人間")
        self.combo_for_dirk_ai.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE + 50, y=GAP_SIZE + OPTIONS_HEIGHT)

        # 後攻のAI決める
        self.label_for_light = ttk.Label(
            self.main_frame,
            text="後攻"
        )
        self.label_for_light.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE, y=GAP_SIZE + OPTIONS_HEIGHT * 2)
        self.combo_for_light_ai_value = StringVar()
        self.combo_for_light_ai = ttk.Combobox(
            self.main_frame,
            state="readonly",
            textvariable=self.combo_for_light_ai_value
        )
        self.combo_for_light_ai['values'] = ["人間", "ランダム", "優先順位型", "先読み型", "強化学習", "進化学習"]
        self.combo_for_light_ai.set("人間")
        self.combo_for_light_ai.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE + 50, y=GAP_SIZE + OPTIONS_HEIGHT * 2)

        # 学習用に記録するか否か設定用
        self.check_button_for_learn_or_not_value = BooleanVar()
        self.check_button_for_learn_or_not = ttk.Checkbutton(
            self.main_frame,
            text="学習用に記録する",
            onvalue=True,
            offvalue=False,
            variable=self.check_button_for_learn_or_not_value
        )
        self.check_button_for_learn_or_not.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE + 20,
                                                 y=GAP_SIZE + OPTIONS_HEIGHT * 3 + GAP_SIZE)

        # 試合試行回数設定用
        self.label_for_entry = ttk.Label(
            self.main_frame,
            text="試合回数"
        )
        self.label_for_entry.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE,
                                   y=GAP_SIZE + OPTIONS_HEIGHT * 3 + GAP_SIZE + OPTIONS_HEIGHT * 5)
        self.entry_for_running_time_value = StringVar()
        self.entry_for_running_time = ttk.Entry(
            self.main_frame,
            textvariable=self.entry_for_running_time_value
        )
        self.entry_for_running_time.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE + 80,
                                          y=GAP_SIZE + OPTIONS_HEIGHT * 3 + GAP_SIZE + OPTIONS_HEIGHT * 5)

        # 試合止めるよう
        self.stop_button = ttk.Button(
            self.main_frame,
            text="stop"
        )
        self.stop_button.bind("<1>", self.stop_button_click)
        self.stop_button.place(x=GAP_SIZE + BOARD_SIZE + GAP_SIZE,
                               y=GAP_SIZE + OPTIONS_HEIGHT * 3 + GAP_SIZE + OPTIONS_HEIGHT * 2)

        # 変数宣言
        self.board_object = BoardObject()
        self.human_or_ai = [0, 0]
        self.ai_object = [AIRandom, AIRandom]
        self.turn_number = 0
        self.turn_d_or_l = 0
        self.game_or_running = 0
        self.stop_trigger = False
        self.record = []

        # ボタン押せるかの管理
        self.game_start_button_enabled = True
        self.running_start_button_enabled = False  # 暫定5
        self.running_start_button.config(state="disable")  # 暫定5
        self.board_enabled = False
        self.stop_button_enabled = False
        self.stop_button.config(state="disable")
        self.entry_for_running_time.config(state="disable")  # 暫定5
        self.check_button_for_learn_or_not.config(state="disable")  # 暫定5

    # フォームの実体化
    def start_form(self):
        # 開始
        self.tk_root.mainloop()

    def game_start_button_click(self, event):

        if self.game_start_button_enabled:
            # 全ボタン不可
            self.game_start_button_enabled = False
            self.gamestart_button.config(state="disable")
            self.running_start_button_enabled = False
            self.running_start_button.config(state="disable")
            self.board_enabled = False
            self.stop_button_enabled = False
            self.stop_button.config(state="disable")
            self.combo_for_dirk_ai.config(state="disable")
            self.combo_for_light_ai.config(state="disable")
            self.entry_for_running_time.config(state="disable")
            self.check_button_for_learn_or_not.config(state="disable")
            # ゲームをスタートさせる
            self.game_or_running = PLAY_GAME_MODE
            self.game_start()
        else:
            self.message_label.config(text="そのボタンは押せません")

    # 暫定
    def running_start_button_click(self, event):

        if self.running_start_button_enabled:
            self.game_start_button_enabled = False
            self.gamestart_button.config(state="disable")
            self.running_start_button_enabled = False
            self.running_start_button.config(state="disable")
            self.board_enabled = False
            self.stop_button_enabled = False
            self.stop_button.config(state="disable")
            self.combo_for_dirk_ai.config(state="disable")
            self.combo_for_light_ai.config(state="disable")
            self.entry_for_running_time.config(state="disable")
            self.check_button_for_learn_or_not.config(state="disable")
            messagebox.showwarning("error", "そのボタンは現在準備中です。")  # 暫定5
            self.game_or_running = LEARNING_MODE
        else:
            self.message_label.config(text="そのボタンは押せません")

    def game_start(self):

        # モードを読み込みAIを作る
        if self.combo_for_dirk_ai_value.get() == "人間":
            self.human_or_ai[T_DARK] = HUMAN
            self.ai_object[T_DARK] = 0
        elif self.combo_for_dirk_ai_value.get() == "ランダム":
            self.human_or_ai[T_DARK] = AI_PLAYER
            self.ai_object[T_DARK] = AIRandom()
        elif self.combo_for_dirk_ai_value.get() == "優先順位型":
            self.human_or_ai[T_DARK] = AI_PLAYER
            self.ai_object[T_DARK] = AILookPriority()
        elif self.combo_for_dirk_ai_value.get() == "先読み型":
            self.human_or_ai[T_DARK] = AI_PLAYER
            self.ai_object[T_DARK] = AIReadAhead()
        elif self.combo_for_dirk_ai_value.get() == "強化学習":
            self.human_or_ai[T_DARK] = AI_PLAYER
            self.ai_object[T_DARK] = AIReinforcementLearning(self.check_button_for_learn_or_not_value.get())
            messagebox.showerror("error", "指定された先行のAIがまだ実装されていません。強制終了します")  # 暫定2
            sys.exit(1)  # 暫定2
        elif self.combo_for_dirk_ai_value.get() == "進化学習":
            self.human_or_ai[T_DARK] = AI_PLAYER
            self.ai_object[T_DARK] = AIGA(self.check_button_for_learn_or_not_value.get())
            messagebox.showerror("error", "指定された先行のAIがまだ実装されていません。強制終了します")  # 暫定2
            sys.exit(1)  # 暫定2
        else:
            messagebox.showerror("error", "先行のAI指定が不正です。強制終了します")
            sys.exit(1)

        if self.combo_for_light_ai_value.get() == "人間":
            self.human_or_ai[T_LIGHT] = HUMAN
            self.ai_object[T_LIGHT] = 0
        elif self.combo_for_light_ai_value.get() == "ランダム":
            self.human_or_ai[T_LIGHT] = AI_PLAYER
            self.ai_object[T_LIGHT] = AIRandom()
        elif self.combo_for_light_ai_value.get() == "優先順位型":
            self.human_or_ai[T_LIGHT] = AI_PLAYER
            self.ai_object[T_LIGHT] = AILookPriority()
        elif self.combo_for_light_ai_value.get() == "先読み型":
            self.human_or_ai[T_LIGHT] = AI_PLAYER
            self.ai_object[T_LIGHT] = AIReadAhead()
        elif self.combo_for_light_ai_value.get() == "強化学習":
            self.human_or_ai[T_LIGHT] = AI_PLAYER
            self.ai_object[T_LIGHT] = AIReinforcementLearning(self.check_button_for_learn_or_not_value.get())
            messagebox.showerror("error", "指定された先行のAIがまだ実装されていません。強制終了します")  # 暫定2
            sys.exit(1)  # 暫定2
        elif self.combo_for_light_ai_value.get() == "進化学習":
            self.human_or_ai[T_LIGHT] = AI_PLAYER
            self.ai_object[T_LIGHT] = AIGA(self.check_button_for_learn_or_not_value.get())
            messagebox.showerror("error", "指定された先行のAIがまだ実装されていません。強制終了します")  # 暫定2
            sys.exit(1)  # 暫定2
        else:
            messagebox.showerror("error", "後攻のAI指定が不正です。強制終了します")
            sys.exit(1)
        # 初期準備
        self.standby()
        # ストップボタン可　　暫定で不可3
        self.stop_button_enabled = True
        self.stop_button.config(state="normal")
        # ターン数初期化
        self.turn_number = 0
        self.turn_d_or_l = T_DARK
        # 人間がいるかどうかで分岐
        if self.human_or_ai[T_DARK] == HUMAN:
            self.before_place_phase()
        elif self.human_or_ai[T_LIGHT] == HUMAN:
            self.before_place_phase()
        else:
            self.game_ai_vs_ai()

    def standby(self):
        # キャンバスを破壊しメモリ解放。
        self.game_canvas.destroy()
        # ゲーム画面にボード用キャンバス再生成
        self.game_canvas = tk.Canvas(
            self.main_panel,
            height=BOARD_SIZE,
            width=BOARD_SIZE)
        self.game_canvas.create_rectangle(0, 0, BOARD_SIZE, BOARD_SIZE, fill='green')  # 塗りつぶし
        for i in range(NUMBER_OF_SQUARE - 1):
            temp = (i + 1) * SQUARE_SIZE
            self.game_canvas.create_line(temp, 0, temp, BOARD_SIZE)
            self.game_canvas.create_line(0, temp, BOARD_SIZE, temp)
        self.game_canvas.bind("<1>", self.board_click)
        self.game_canvas.grid()
        # 駒を初期配置にする
        self.board_object = BoardObject()
        self.delete_and_drawing_pieces()

    def before_place_phase(self):

        # ターン進める
        if self.turn_number == 0:
            self.turn_number += 1
            self.turn_d_or_l = T_DARK
        elif self.turn_d_or_l == T_LIGHT:
            self.turn_number += 1
            self.turn_d_or_l = T_DARK
        else:
            self.turn_d_or_l = T_LIGHT

        # おける場所確認
        if self.board_object.get_placeable_or_pass() == STATE_GAME_END:  # お互いパスなら
            # ゲーム終わり
            self.game_end()
        elif self.board_object.get_placeable_or_pass() == STATE_PASS:  # 置けないならパス
            if self.human_or_ai[self.turn_d_or_l] == HUMAN:
                messagebox.showinfo("パス", "おける場所がありません,ターンをパスします")
            else:
                self.ai_object[self.turn_d_or_l].passprocess()
            self.board_object.pass_the_turn(self.turn_d_or_l)
            self.pass_the_turn()
        elif self.board_object.get_placeable_or_pass() == STATE_PLACE:  # おける場合
            if self.human_or_ai[self.turn_d_or_l] == HUMAN:
                # おける場所を色で伝える
                for i in range(NUMBER_OF_SQUARE):
                    for j in range(NUMBER_OF_SQUARE):
                        if self.board_object.get_placeable_or_not_board(i, j) == PLACEABLE:
                            self.drawing_rectangle(i, j)
                # ボードクリック可
                self.board_enabled = True
            else:
                # AIに情報渡す
                place_point = self.ai_object[self.turn_d_or_l].playprocess(copy.deepcopy(self.board_object),
                                                                           self.turn_d_or_l, self.turn_number)
                # 次へ
                self.after_place_phase(place_point)
        else:
            messagebox.showerror("error", "不正な値1110(placeable_or_pass)。強制終了します。")
            sys.exit(1)

    def pass_the_turn(self):
        self.before_place_phase()

    def board_click(self, event):
        # クリック個所を調べて次につなげる
        x = self.game_canvas.canvasx(event.x)
        y = self.game_canvas.canvasx(event.y)
        x = int(x // SQUARE_SIZE)
        y = int(y // SQUARE_SIZE)
        point_vec = [x, y]
        if not self.board_enabled:
            self.message_label.config(text="現在ボードクリック不可です")
        else:
            # ボード押せないようにする
            self.board_enabled = False
            self.after_place_phase(point_vec)

    def after_place_phase(self, place_point):

        # 手を表記
        game_message = str(place_point[X_AXIS] + 1) + "," + str(place_point[Y_AXIS] + 1)
        self.message_label.config(text=game_message)
        # ひっくり返せるかどうかをもらう
        placeable_or_not = self.board_object.get_placeable_or_not_board(place_point[X_AXIS], place_point[Y_AXIS])
        # おけるか否か
        if placeable_or_not == NOT_PLACEABLE:
            if self.human_or_ai[self.turn_d_or_l] == HUMAN:
                self.message_label.config(text="そこにはおけません")
                # board_clickで押せなくなっていたボードを押せるようにする
                self.board_enabled = True
            else:
                messagebox.showerror("error", "AIが不正な場所に駒がおこうとしました。強制終了します。")
                sys.exit(1)
        else:
            placeable_or_not = self.board_object.place_piece(place_point[X_AXIS], place_point[Y_AXIS], self.turn_d_or_l)
            if not placeable_or_not:
                messagebox.showerror("error", "不正な場所に駒がおかれました。強制終了します。")
                sys.exit(1)
            # 押せる場所表示を消す
            self.rectangle_delete_all()
            # 押した場所表示をする
            self.drawing_rectangle(place_point[X_AXIS], place_point[Y_AXIS])
            # 画面を更新して0.01秒待つ
            self.game_canvas.update()
            sleep(0.01)
            # 押した場所表示を消す
            self.rectangle_delete_all()
            # 画面を更新して0.01秒待つ
            self.game_canvas.update()
            sleep(0.01)
            # 全マス調べてコマを描画し直す
            self.piece_delete_all()
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    self.piece_drawing(i, j, self.board_object.get_board_state(i, j))
            # 画面を更新して0.01秒待つ
            self.game_canvas.update()
            sleep(0.01)
            # 相手AIに伝える為のデータ
            self.record.append(copy.copy(place_point))
            # 次へ
            self.before_place_phase()

    # AIとAIの戦いでは関数が関数を呼び出すことが繰り返されるので、whileで行う。
    def game_ai_vs_ai(self):
        while True:
            placeable_or_pass, place_point = self.before_place_phase_ai_vs_ai()
            if placeable_or_pass == STATE_PLACE:
                self.after_place_phase_ai_vs_ai(place_point)
            elif placeable_or_pass == STATE_PASS:
                self.board_object.pass_the_turn(self.turn_d_or_l)
            elif placeable_or_pass == STATE_GAME_END:
                break
            else:
                messagebox.showerror("error", "不正な値1187(placeable_or_pass)。強制終了します。")
                sys.exit(1)
        self.game_end()

    def before_place_phase_ai_vs_ai(self):

        # ターン進める
        if self.turn_number == 0:
            self.turn_number = 1
            self.turn_d_or_l = T_DARK
        else:
            if self.turn_d_or_l == T_DARK:
                self.turn_d_or_l = T_LIGHT
            elif self.turn_d_or_l == T_LIGHT:
                self.turn_number += 1
                self.turn_d_or_l = T_DARK
            else:
                messagebox.showerror("error", "不正な値(turn_d_or_l)。強制終了します。")
                sys.exit(1)

        if self.board_object.get_placeable_or_pass() == STATE_GAME_END:  # お互いパスなら
            # ゲーム終わり
            state_and_point = [STATE_GAME_END, None]
        elif self.board_object.get_placeable_or_pass() == STATE_PASS:  # 置けないならパス
            if self.human_or_ai[self.turn_d_or_l] == HUMAN:
                messagebox.showerror("error", "不正な値(player[turn_d_or_l])。強制終了します。")
                sys.exit(1)
            else:
                self.ai_object[self.turn_d_or_l].passprocess()
            state_and_point = [STATE_PASS, None]
        elif self.board_object.get_placeable_or_pass() == STATE_PLACE:  # おける場合
            if self.human_or_ai[self.turn_d_or_l] == HUMAN:
                messagebox.showerror("error", "不正な値(player[turn_d_or_l])。強制終了します。")
                sys.exit(1)
            else:
                # AIに情報渡す
                place_point = self.ai_object[self.turn_d_or_l].playprocess(copy.deepcopy(self.board_object),
                                                                           self.turn_d_or_l, self.turn_number)
                # 次へ
                state_and_point = [STATE_PLACE, place_point]
        else:
            messagebox.showerror("error", "不正な値(placeable_or_pass)。強制終了します。")
            sys.exit(1)
        return state_and_point

    def after_place_phase_ai_vs_ai(self, place_point):

        # 手を表記
        game_massage = str(place_point[X_AXIS] + 1) + "," + str(place_point[Y_AXIS] + 1)
        self.message_label.config(text=game_massage)
        # ひっくり返せるかどうかをもらう
        placeable_or_not = self.board_object.get_placeable_or_not_board(place_point[X_AXIS], place_point[Y_AXIS])
        # おけるか否か
        if placeable_or_not == NOT_PLACEABLE:
            if self.human_or_ai[self.turn_d_or_l] == HUMAN:
                messagebox.showerror("error", "aiでなければならない値が人間でした。強制終了します。")
                sys.exit(1)
            else:
                messagebox.showerror("error", "AIが不正な場所に駒がおこうとしました。強制終了します。")
                sys.exit(1)
        else:
            # 押した場所に駒をおく
            placeable_or_not = self.board_object.place_piece(place_point[X_AXIS], place_point[Y_AXIS], self.turn_d_or_l)
            if not placeable_or_not:
                messagebox.showerror("error", "不正な場所に駒がおかれました。強制終了します。")
                sys.exit(1)
            # 全マス調べてコマを描画し直す
            self.piece_delete_all()
            for i in range(NUMBER_OF_SQUARE):
                for j in range(NUMBER_OF_SQUARE):
                    self.piece_drawing(i, j, self.board_object.get_board_state(i, j))
            # 画面を更新して
            self.game_canvas.update()
            # 相手AIに伝える為のデータ
            self.record.append(copy.copy(place_point))
            # 次へ

    def stop_button_click(self, event):
        if self.stop_button_enabled:
            self.game_end()

    def game_end(self):
        print(self.record)
        # 勝敗
        dark_count = 0
        light_count = 0
        for i in range(NUMBER_OF_SQUARE):
            for j in range(NUMBER_OF_SQUARE):
                if self.board_object.get_board_state(i, j) == DARK:
                    dark_count += 1
                if self.board_object.get_board_state(i, j) == LIGHT:
                    light_count += 1
        if dark_count > light_count:
            game_end_message = str(dark_count) + "対" + str(light_count) + "で黒の勝ち"
            messagebox.showinfo("勝敗", game_end_message)
        elif dark_count < light_count:
            game_end_message = str(dark_count) + "対" + str(light_count) + "で白の勝ち"
            messagebox.showinfo("勝敗", game_end_message)
        else:
            game_end_message = str(dark_count) + "対" + str(light_count) + "で引き分け"
            messagebox.showinfo("勝敗", game_end_message)
        # 全部green
        self.piece_delete_all()
        self.rectangle_delete_all()
        # AIにゲームの終わりを伝える
        if self.human_or_ai[T_DARK] == AI_PLAYER:
            self.ai_object[T_DARK].endprocess()
        if self.human_or_ai[T_LIGHT] == AI_PLAYER:
            self.ai_object[T_LIGHT].endprocess()
        # AI破壊先行から消してしまうとずれて後攻が先行になってしまうのでわかりやすく後攻から消す
        if self.human_or_ai[T_LIGHT] == AI_PLAYER:
            del self.ai_object[T_LIGHT]
        if self.human_or_ai[T_DARK] == AI_PLAYER:
            del self.ai_object[T_DARK]
        # 枠確保
        self.ai_object = [None, None]
        # ボードクリック不可stop不可その他可
        self.game_start_button_enabled = True
        self.gamestart_button.config(state="normal")
        self.running_start_button_enabled = False  # 暫定5
        self.running_start_button.config(state="disable")  # 暫定5
        self.board_enabled = False
        self.stop_button_enabled = False
        self.stop_button.config(state="disable")
        self.combo_for_dirk_ai.config(state="normal")
        self.combo_for_light_ai.config(state="normal")
        self.entry_for_running_time.config(state="disable")  # 暫定5
        self.check_button_for_learn_or_not.config(state="disable")  # 暫定5
        self.entry_for_running_time.config(state="disable")  # 暫定5

    def delete_and_drawing_pieces(self):
        self.piece_delete_all()
        for i in range(NUMBER_OF_SQUARE):
            for j in range(NUMBER_OF_SQUARE):
                self.piece_drawing(i, j, self.board_object.get_board_state(i, j))

    def piece_drawing(self, x1, y1, color):
        if color == OUT_OF_BOARD:
            pass
        elif color == DARK:
            self.game_canvas.create_oval(x1 * SQUARE_SIZE + 2, y1 * SQUARE_SIZE + 2, (x1 + 1) * SQUARE_SIZE - 2,
                                         (y1 + 1) * SQUARE_SIZE - 2, fill="black", tags="piece")
        elif color == GREEN:
            self.game_canvas.create_oval(x1 * SQUARE_SIZE + 2, y1 * SQUARE_SIZE + 2, (x1 + 1) * SQUARE_SIZE - 2,
                                         (y1 + 1) * SQUARE_SIZE - 2, fill="green", outline="green", tags="piece")
        elif color == LIGHT:
            self.game_canvas.create_oval(x1 * SQUARE_SIZE + 2, y1 * SQUARE_SIZE + 2, (x1 + 1) * SQUARE_SIZE - 2,
                                         (y1 + 1) * SQUARE_SIZE - 2, fill="white", tags="piece")
        else:
            messagebox.showerror("error", "不正な値(color)。強制終了します。")
            sys.exit(1)

    def piece_delete_all(self):
        self.game_canvas.delete("piece")

    def drawing_rectangle(self, x1, y1):
        self.game_canvas.create_rectangle(x1 * SQUARE_SIZE + 1, y1 * SQUARE_SIZE + 1,
                                          (x1 + 1) * SQUARE_SIZE - 1, (y1 + 1) * SQUARE_SIZE - 1,
                                          outline="yellow", tags="rectangle")

    def rectangle_delete_all(self):
        self.game_canvas.delete("rectangle")


if __name__ == '__main__':
    my_othello = MainClass()
    my_othello.start_form()
