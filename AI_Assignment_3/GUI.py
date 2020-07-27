"""
@author: Patel Parth (2016A7PS0150P)
"""

from algo import * 

import sys
import time

from functools import partial
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox, QSizePolicy, QToolButton
from PyQt5.QtCore import QSize, Qt, QRect, QSize
from PyQt5.QtGui import QIcon, QColor

N = 4 # NxN board
PIXEL_SIZE = 40
decision_fn = alpha_beta_pruning_decision
first_chance = "Machine"
TOTAL_TIME = 0

def select_decision_fn(text):
    global decision_fn
    if text == "Mini-Max":
        decision_fn = minimax_decision
    else:
        decision_fn = alpha_beta_pruning_decision

def select_first_chance(text):
    global first_chance
    first_chance = text

def select_N(text):
    global N
    N = int(text)

def select_max_depth(text):
    global MAX_DEPTH, N
    if text == "Infinity":
        MAX_DEPTH = N*N
        # print(MAX_DEPTH)
        return
    MAX_DEPTH = int(text)

class GUI_Layout(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Align3 - Custom Tic Tac Toe Board Game')
        self.init_ui()
        self.setGeometry(0, 0, 1100, 550)
        self.show()
    def init_ui(self):
        self.show_R_values()
        self.display_play_btn()
    def show_R_values(self):
        self.w1 = QWidget(self)
        self.w1_texts = []
        self.w1_texts.append("R1 : Mini-Max: Total number of nodes generated - 617282")
        self.w1_texts.append("R2 : Mini-Max: Bytes allocated per node - 64")
        self.w1_texts.append("R3 : Mini-Max: Max stack size reached in reasonable time - 16")
        self.w1_texts.append("R4 : Mini-Max: Total time (taken by machine) to play the game - 24.969320536 secs.")
        self.w1_texts.append("R5 : Mini-Max: Number of nodes created in one microsecond - 0.024721618")
        self.w1_texts.append("R6 : AlphaBeta Pruning: Total number of nodes generated - 8472")
        self.w1_texts.append("R7 : Memory saved (as ratio) using pruning = (R1-R6)/R1 = 0.986275317")
        self.w1_texts.append("R8 : AlphaBeta Pruning: Total time (taken by machine) to play the game - 0.37395587 secs.")
        self.w1_texts.append("R9 : Ratio of memory used = Mini-Max/AlphaBeta-Pruning =  1.12")
        self.w1_texts.append("R10: Avg. time taken by machine: Mini-Max/AlphaBeta-Pruning = 62.932871593")
        self.w1_texts.append("R11: No. of times machine M wins - 8/10")
        self.w1_texts.append("R12: Avg. no. of times machine M wins - 7.25/10")
        self.w1_texts.append("R13: Compare times taken by Mini-Max and AlphaBeta-Pruning = R4/R8 = 66.770767727")
        self.w1_labels = []
        for idx in range(13):
            self.w1_labels.append(QLabel(self.w1))
            self.w1_labels[idx].setText(self.w1_texts[idx])
            self.w1_labels[idx].move(20, 100+idx*30)
            self.w1_labels[idx].setStyleSheet('color: Brown')
            self.w1_labels[idx].show()
        self.w1.move(0, 0)
        self.w1.show()
    def display_play_btn(self):
        self.G1_widget = QWidget(self)
        self.G1_N_label = QLabel("Board Size, N:", self.G1_widget)
        self.G1_N_combo_box = QComboBox(self.G1_widget)
        self.G1_N_combo_box.addItem("4")
        self.G1_N_combo_box.addItem("3")
        for idx in range(5, 9):
            self.G1_N_combo_box.addItem(str(idx))
        self.G1_N_label.move(125, 100)
        self.G1_N_label.setStyleSheet('color: Brown')
        self.G1_N_combo_box.move(235, 97)
        self.G1_N_combo_box.setStyleSheet('color: Brown')
        self.G1_N_combo_box.activated[str].connect(select_N)
        self.G1_max_recursion_depth_label = QLabel("Max. Recursion Depth:", self.G1_widget)
        self.G1_max_recursion_depth_combo_box = QComboBox(self.G1_widget)
        for idx in range(4, 10):
            self.G1_max_recursion_depth_combo_box.addItem(str(idx))
        self.G1_max_recursion_depth_combo_box.addItem("Infinity")
        self.G1_max_recursion_depth_label.move(125, 150)
        self.G1_max_recursion_depth_label.setStyleSheet('color: Brown')
        self.G1_max_recursion_depth_combo_box.move(275, 147)
        self.G1_max_recursion_depth_combo_box.setStyleSheet('color: Brown')
        self.G1_max_recursion_depth_combo_box.activated[str].connect(select_max_depth)
        self.G1_chance_label = QLabel("First turn for:", self.G1_widget)
        self.G1_chance_combo_box = QComboBox(self.G1_widget)
        self.G1_chance_combo_box.addItem("Machine")
        self.G1_chance_combo_box.addItem("Human")
        self.G1_chance_label.move(125, 200)
        self.G1_chance_label.setStyleSheet('color: Brown')
        self.G1_chance_combo_box.move(235, 197)
        self.G1_chance_combo_box.setStyleSheet('color: Brown')
        self.G1_chance_combo_box.activated[str].connect(select_first_chance)
        self.G1_decision_label = QLabel("Select Algorithm:", self.G1_widget)
        self.G1_decision_combo_box = QComboBox(self.G1_widget)
        self.G1_decision_combo_box.addItem("Alpha-Beta-Pruning")
        self.G1_decision_combo_box.addItem("Mini-Max")
        self.G1_decision_label.move(125, 250)
        self.G1_decision_label.setStyleSheet('color: Brown')
        self.G1_decision_combo_box.move(235, 247)
        self.G1_decision_combo_box.setStyleSheet('color: Brown')
        self.G1_decision_combo_box.activated[str].connect(select_decision_fn)
        self.G1_play_btn = QPushButton("Play Now", self.G1_widget)
        self.G1_play_btn.clicked.connect(self.play_game)
        self.G1_play_btn.setStyleSheet('color: Brown')
        self.G1_play_btn.move(200, 300)
        self.G1_play_btn.show()
        self.G1_txt1 = QLabel("For N >= 8, for larger tree depths (>=10), the algorithm, especially Mini-Max,", self.G1_widget)
        self.G1_txt1.move(100, 350)
        self.G1_txt1.show()
        self.G1_txt2 = QLabel("takes more than 1 minute to make a decision. So, I have used a heuristic", self.G1_widget)
        self.G1_txt2.move(100, 370)
        self.G1_txt2.show()
        self.G1_txt3 = QLabel("function to limit the depth of the tree, which you can select from above menu.", self.G1_widget)
        self.G1_txt3.move(100, 390)
        self.G1_txt3.show()
        self.G1_txt4 = QLabel("If you don't want the heuristic to be used, choose Max. Depth as Infinity.", self.G1_widget)
        self.G1_txt4.move(100, 410)
        self.G1_txt4.show()
        self.G1_widget.move(500, 0)
        self.G1_widget.show()
    def btnListener(self, button_id):
        global N, PIXEL_SIZE, decision_fn
        global TOTAL_NODES, TOTAL_TIME
        if self.play_state.game_over:
            # print('Hello1')
            # print(TOTAL_NODES, TOTAL_TIME)
            return
        lst = button_id.split("_")
        x = int(lst[0])
        y = int(lst[1])
        # print(x, y)
        if (x, y) in self.play_clicked_btns:
            # print('Hello2')
            return
        action_lst = return_next_possible_actions(self.play_state)
        # print(action_lst)
        action_set = set()
        for action in action_lst:
            action_set.add((action[1], action[0]))
        # print(action_set)
        # print(x, y)
        if (x, y) not in action_set:
            # print('Hello3')
            return
        self.play_state.place_coin(x, y, 2)
        self.play_clicked_btns.add((x, y))
        self.play_btns[x*N+y].setIcon(QIcon('imgs/b.png'))
        self.play_btns[x*N+y].setIconSize(QSize(PIXEL_SIZE-2, PIXEL_SIZE-2))
        cond, val = self.play_state.is_game_over()
        if cond:
            stlstr = "+" if val == 1 else ""
            self.play_status_label.setText("GAME OVER: Utility="+stlstr+str(val))
            self.play_status_label.move(10, 200)
            # print(TOTAL_NODES, TOTAL_TIME)
            return
        start = time.time()
        action = decision_fn(self.play_state)
        end = time.time()
        TOTAL_TIME += (end-start)
        if action == None:
            # print("Hello4")
            return
        y, x = action
        # print(x, y)
        self.play_state.place_coin(x, y, 1)
        self.play_clicked_btns.add((x, y))
        self.play_btns[x*N+y].setIcon(QIcon('imgs/g.png'))
        self.play_btns[x*N+y].setIconSize(QSize(PIXEL_SIZE-2, PIXEL_SIZE-2))
        cond, val = self.play_state.is_game_over()
        if cond:
            stlstr = "+" if val == 1 else ""
            self.play_status_label.setText("GAME OVER: Utility="+stlstr+str(val))
            self.play_status_label.move(10, 200)
            # print(TOTAL_NODES, TOTAL_TIME)
            return
    def play_game(self):
        global N, PIXEL_SIZE, decision_fn, first_chance
        global TOTAL_TIME, TOTAL_NODES
        TOTAL_NODES = 0
        TOTAL_TIME = 0.0
        self.play_widget = QWidget()
        self.play_widget.setWindowTitle("Play Align3")
        self.play_label1 = QLabel("Green - Machine M", self.play_widget)
        self.play_label1.setStyleSheet('color: #03c724')
        self.play_label1.move(25, 150)
        self.play_label2 = QLabel("Blue - Human H", self.play_widget)
        self.play_label2.setStyleSheet('color: #5203fa')
        self.play_label2.move(37, 175)
        self.play_status_label = QLabel("GAME ON                        " ,self.play_widget)
        self.play_status_label.move(50, 200)
        self.play_base_line_label = QLabel(self.play_widget)
        self.play_base_line_label.setStyleSheet('QLabel {background-color:#de0310}')
        self.play_base_line_label.setGeometry(150+PIXEL_SIZE, PIXEL_SIZE, N*PIXEL_SIZE, 10)
        self.play_state = State(N)
        self.play_clicked_btns = set()
        self.play_btns = []
        for i in range(N):
            for j in range(N):
                self.play_btns.append(QPushButton(self.play_widget))
                self.play_btns[-1].setObjectName(str(i)+"_"+str(j))
                self.play_btns[-1].clicked.connect(partial(self.btnListener, str(i)+"_"+str(j)))
                self.play_btns[-1].setGeometry(QRect(150+(j+1)*PIXEL_SIZE, 25+(i+1)*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
                self.play_btns[-1].show()
        if first_chance == "Machine":
            start = time.time()
            initial_action = decision_fn(self.play_state)
            end = time.time()
            TOTAL_TIME += (end-start)
            y, x = initial_action
            self.play_state.place_coin(x, y, 1)
            self.play_clicked_btns.add((x, y))
            self.play_btns[x*N+y].setIcon(QIcon('imgs/g.png'))
            self.play_btns[x*N+y].setIconSize(QSize(PIXEL_SIZE-2, PIXEL_SIZE-2))
        self.play_widget.setGeometry(25, 25, 800, 600)
        self.play_widget.show()        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI_Layout()
    sys.exit(app.exec_())
