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
                counter = 0
                while True:
                    # 位置ずらす
                    t_point = (t_point[X_AXIS] + delta[X_AXIS], t_point[Y_AXIS] + delta[Y_AXIS])
                    counter += 1
                    # 値を評価
                    z1 = board_state[t_point] * the_turn
                    if z1 == -1:
                        # 違う色なので続ける
                        pass
                    elif z1 == 1:
                        if counter > 1:
                            # 挟んでることが確認できたのでひっくり返しへ(ひっくり返しonにする)
                            flag_of_reverse = True
                            break
                        else:
                            # 自分の色と隣り合っていたので、終える。
                            flag_of_reverse = False
                            break
                    elif z1 == -2 or z1 == 0 or z1 == 2:
                        # 自分の色がないまま空白のマス又は盤外になったので何もせず終わる
                        flag_of_reverse = False
                        break
                    else:
                        messagebox.showerror("error", "不正な値639。強制終了します。")
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
            messagebox.showerror("error", "不正な値654。強制終了します。")
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
                        messagebox.showerror("error", "不正な値693。強制終了します。")
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
            messagebox.showerror("error", "不正な値708。強制終了します。")
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
                tempfirstornotA = TURN_OF_LIGHT
            else:
                messagebox.showerror("error", "不正な値727。強制終了します。")
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
                tempfirstornotA = TURN_OF_LIGHT
            else:
                messagebox.showerror("error", "不正な値765。強制終了します。")
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

