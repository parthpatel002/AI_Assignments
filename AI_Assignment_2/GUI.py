"""
@author: Patel Parth (2016A7PS0150P)
"""

from heuristics import *
from algorithms import *

import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox, QSizePolicy
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QColor

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

### NOTE: These imports are used only for 3D plotting in matplotlib ###
import numpy as np # NumPy arrays are used as matplotlib's plot3D() function doesn't accept Python lists as input
from mpl_toolkits.mplot3d import Axes3D
### END OF NOTE ###

N = 10 # Size of warfield : NxN
P = 20 # Percentage of mines
heuristic = "heuristic1"
PIXEL_SIZE = 18

def select_N(text):
	global N
	N = int(text)

def select_P(text):
	global P
	P = int(text)

def select_h(text):
    global heuristic
    heuristic = text

class PlotCanvas_v1(FigureCanvas):

    def __init__(self, x, xlabel, y1, ylabel, title, y2=None, parent=None, width=8, height=8, dpi=75):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.setParent(parent)
        self.plot(x, xlabel, y1, ylabel, title, y2)

    def plot(self, x, xlabel, y1, ylabel, title, y2):
        ax = self.figure.add_subplot(111)
        if y2 is None:
            ax.plot(x, y1, color='green')
        else:
            ax.plot(x, y1, color='red', label='Heuristic 1')
            ax.plot(x, y2, color='blue', label='Heuristic 2')
            ax.legend(loc='upper left')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        self.draw()

class PlotCanvas_v2(FigureCanvas):

    def __init__(self, parent=None, width=9, height=9, dpi=75):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.setParent(parent)
        self.heuristic = "Heuristic1"
        self.X_label = "X1"
        self.Y_label = "X2"
        self.X, self.Y = get_X_Y()
        self.X = np.array(self.X)
        self.Y = np.array(self.Y)
        self.ax = Axes3D(self.figure)
        self.ax.set_title('State Space Landscape for Minesweeper Problem for chosen heuristic')
        self.plot()

    def plot(self):
        if self.heuristic == "Heuristic1":
            self.Z = np.array(get_h1_surface())
        else:
            self.Z = np.array(get_h2_surface())
        self.ax.plot_surface(self.X, self.Y, self.Z, rstride=1, cstride=1, cmap='viridis')
        self.ax.set_xlabel(self.X_label+' Label')
        self.ax.set_ylabel(self.Y_label+' Label')
        self.ax.set_zlabel(self.heuristic+" Value")
        self.draw()

class PlotCanvas_v3(FigureCanvas):

    def __init__(self, option, parent=None, width=5.5, height=6, dpi=75):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.option = option
        self.heuristic = "Heuristic1"
        self.X_label = "X1"
        self.Y_label = "X2"
        self.X, self.Y = get_X_Y()
        self.X = np.array(self.X)
        self.Y = np.array(self.Y)
        self.xline = [9, 9, 8, 8, 7, 7, 7, 6, 6, 5, 4, 4, 3, 2, 1, 0]
        self.yline = [9, 8, 8, 7, 6, 5, 4, 4, 3, 2, 2, 1, 1, 1, 0, 0]
        self.setParent(parent)
        self.plot()

    def plot(self):
        self.ax = Axes3D(self.figure)
        if self.option != 3:
            self.ax.set_title('State Space Landscape')
        if self.heuristic == "Heuristic1":
            self.Z = get_h1_surface()
        else:
            self.Z = get_h2_surface()
        self.zline = []
        for x1, y1 in zip(self.xline, self.yline):
            self.zline.append(self.Z[x1][y1])
        if self.option == 1:
            self.ax.plot_surface(np.array(self.X), np.array(self.Y), np.array(self.Z), rstride=1, cstride=1, cmap='viridis')
            self.ax.plot3D(np.array(self.xline), np.array(self.yline), np.array(self.zline), 'red')
        elif self.option == 2:
            self.ax.plot_wireframe(np.array(self.X), np.array(self.Y), np.array(self.Z), color='gray')
            self.ax.plot3D(np.array(self.xline), np.array(self.yline), np.array(self.zline), 'red')
        else:
            self.ax.plot3D(np.array(self.xline), np.array(self.yline), np.array(self.zline), 'red')
            self.ax.scatter3D(np.array([self.xline[0]]), np.array([self.yline[0]]), np.array([self.zline[0]]), color='gold', label='High Temperature')
            self.ax.scatter3D(np.array([self.xline[-1]]), np.array([self.yline[-1]]), np.array([self.zline[-1]]), color='green', label='Low Temperature')
            self.ax.legend(loc='upper left')
        self.ax.set_xlabel(self.X_label+' Label')
        self.ax.set_ylabel(self.Y_label+' Label')
        self.ax.set_zlabel(self.heuristic+" Value")
        self.draw()

class GUI_Layout(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Minesweeper Intelligent Agent')
        self.init_ui()
        # self.resize(1200, 800)
        # pt = self.palette()
        # pt.setColor(self.backgroundRole(), QColor( 245, 183, 5 ))
        # self.setPalette(pt)
        self.setGeometry(0, 0, 1200, 650)
        self.show()

    def init_ui(self):
        self.show_R_values()
        self.show_G_buttons()
        self.show_N_M_buttons()

    def show_R_values(self):
        self.w1 = QWidget(self)
        self.w1_texts = []
        self.w1_texts.append("R1 : Maximum memory allocated till the problem is solved (T1) - 11.2 KB")
        self.w1_texts.append("R2 : Time to reach goal state (T1) - 0.05319215059280395 seconds")
        self.w1_texts.append("R3 : Local Optima - Heuristic Value = 0.35")
        self.w1_texts.append("R4 : No. of times T1 reached global optima using heuristic h1 -  19/20")
        self.w1_texts.append("R5 : No. of times T1 reached global optima using heuristic h2 -  17/20")
        self.w1_texts.append("R6 : Avg. no. of steps taken by T1 to reach local/global optima - 41")
        self.w1_texts.append("R7 : No. of times Stochastic T1 reached global optima using heuristic h1 - 10/20")
        self.w1_texts.append("R8 : No. of times Stochastic T1 reached global optima using heuristic h2 - 8/20")
        self.w1_texts.append("R9 : Avg. no. of steps taken by local beam search (k=20) using h1 - 35, global optima")
        self.w1_texts.append("R10: Avg. no. of steps taken by local beam search (k=8) using h2 - 37, global optima")
        self.w1_texts.append("R11: Maximum memory allocated till the problem is solved (T2) - 8.3 KB")
        self.w1_texts.append("R12: Time to reach goal state (T2) - 0.03216370487213135 seconds")
        self.w1_texts.append("R13: Local Optima - Heuristic Value = 0.40; Bad move was chosen (with probability 0.3485)")
        self.w1_texts.append("R14: No. of times T2 reached global optima using heuristic h1 - 9/20")
        self.w1_texts.append("R15: No. of times T2 reached global optima using heuristic h2 - 7/20")
        self.w1_texts.append("R16: Avg. no. of steps taken by T2 to reach local/global optima - 39")
        self.w1_labels = []
        for idx in range(16):
            self.w1_labels.append(QLabel(self.w1))
            self.w1_labels[idx].setText(self.w1_texts[idx])
            self.w1_labels[idx].move(20, 100+idx*30)
            self.w1_labels[idx].setStyleSheet('color: Brown')
            self.w1_labels[idx].show()
        self.w1_display_label = QLabel(self.w1)
        self.w1_display_label.setText('Results for 16x16 warfield with 25 mines')
        self.w1_display_label.move(75, 50)
        self.w1_display_label.setStyleSheet('color: Brown')
        self.w1_display_label.show()
        self.w1.move(0, 0)
        # self.w1.resize(400, 1000)
        self.w1.show()

    def show_G_buttons(self):
        self.w2 = QWidget(self)
        self.w2_label = QLabel("View G1-G7", self.w2)
        self.w2_label.move(5, 150)
        self.w2_label.setStyleSheet('color: Brown')
        self.w2_functions = [self.G1_btn_clicked, self.G2_btn_clicked, self.G3_btn_clicked, self.G4_btn_clicked, self.G5_btn_clicked, self.G6_btn_clicked, self.G7_btn_clicked]
        self.w2_buttons = []
        for idx in range(7):
            self.w2_buttons.append(QPushButton("G"+str(idx+1), self.w2))
            self.w2_buttons[idx].clicked.connect(self.w2_functions[idx])
            self.w2_buttons[idx].move(0, 200+idx*40)
            self.w2_buttons[idx].setStyleSheet('QPushButton {background-color: #b41bf2 ; color: black;}')
            self.w2_buttons[idx].show()
        self.w2.move(600, 0)
        # self.w2.resize(200, 1000)
        self.w2.show()

    def show_N_M_buttons(self):
        self.w3 = QWidget(self)
        self.w3_label = QLabel("Choose following parameters for G1 and G5: ", self.w3)
        self.w3_label.move(40, 200)
        self.w3_label.setStyleSheet('color: Brown')
        self.w3_N_label = QLabel("Select size of square N: ", self.w3)
        self.w3_N_combo_box = QComboBox(self.w3)
        for idx in range(8, 33):
            self.w3_N_combo_box.addItem(str(idx))
        self.w3_N_label.move(50, 250)
        self.w3_N_label.setStyleSheet('color: Brown')
        self.w3_N_combo_box.move(195, 247)
        self.w3_N_combo_box.setStyleSheet('color: Brown')
        self.w3_N_combo_box.activated[str].connect(select_N)
        self.w3_P_label = QLabel("Select percentage of mines P: ", self.w3)
        self.w3_P_combo_box = QComboBox(self.w3)
        for idx in range(10, 16):
            self.w3_P_combo_box.addItem(str(idx))
        self.w3_P_label.move(50, 300)
        self.w3_P_label.setStyleSheet('color: Brown')
        self.w3_P_combo_box.move(235, 297)
        self.w3_P_combo_box.setStyleSheet('color: Brown')
        self.w3_P_combo_box.activated[str].connect(select_P)
        self.w3_h_label = QLabel("Select heuristic function: ", self.w3)
        self.w3_h_combo_box = QComboBox(self.w3)
        for idx in range(1, 3):
            self.w3_h_combo_box.addItem("heuristic"+str(idx))
        self.w3_h_label.move(50, 350)
        self.w3_h_label.setStyleSheet('color: Brown')
        self.w3_h_combo_box.move(205, 347)
        self.w3_h_combo_box.setStyleSheet('color: Brown')
        self.w3_h_combo_box.activated[str].connect(select_h)
        self.w3.move(700, 0)
        # self.w3.resize(300, 1000)
        self.w3.show()

    def G1_btn_clicked(self):
        global N, P, heuristic, PIXEL_SIZE
        M = P*N*N//100
        if heuristic == "heuristic1":
            self.G1_heuristic = heuristic1
        else:
            self.G1_heuristic = heuristic2
        self.G1_widget = QWidget()
        self.G1_state, self.G1_curr_x, self.G1_curr_y = first_click(mine_generator(N, M))
        self.G1_widget_buttons = []
        for i in range(self.G1_state.N):
            for j in range(self.G1_state.N):
                self.G1_widget_buttons.append(QPushButton(self.G1_widget))
                self.G1_widget_buttons[-1].resize(PIXEL_SIZE, PIXEL_SIZE)
                self.G1_widget_buttons[-1].move(150+(j+1)*PIXEL_SIZE, 25+(i+1)*PIXEL_SIZE)
                if self.G1_state.orig_board[i*self.G1_state.N+j] == 9 and self.G1_curr_x == i and self.G1_curr_y == j:
                    self.G1_widget_buttons[-1].setIcon(QIcon('imgs/mine_clicked.jpg'))
                    self.G1_widget_buttons[-1].setIconSize(QSize(PIXEL_SIZE+6, PIXEL_SIZE+6))
                elif self.G1_state.orig_board[i*self.G1_state.N+j] == 9:
                    self.G1_widget_buttons[-1].setIcon(QIcon('imgs/mine.jpg'))
                    self.G1_widget_buttons[-1].setIconSize(QSize(PIXEL_SIZE+6, PIXEL_SIZE+6))
                elif self.G1_curr_x == i and self.G1_curr_y == j:
                    self.G1_widget_buttons[-1].setText(" ")
                    self.G1_widget_buttons[-1].setStyleSheet('QPushButton {background-color: #0AEBF9 ; color: black;}')
                elif self.G1_state.curr_board[i*self.G1_state.N+j] == 10:
                    self.G1_widget_buttons[-1].setText(" ")
                    self.G1_widget_buttons[-1].setStyleSheet('QPushButton {background-color: #747D7E ; color: black;}')
                else:
                    if self.G1_state.curr_board[i*self.G1_state.N+j] == 0:
                        self.G1_widget_buttons[-1].setText(" ")
                        self.G1_widget_buttons[-1].setStyleSheet('QPushButton {background-color: #70E80C ; color: black;}')
                    else:
                        self.G1_widget_buttons[-1].setText(str(self.G1_state.curr_board[i*self.G1_state.N+j]))
                        self.G1_widget_buttons[-1].setStyleSheet('QPushButton {background-color: #70E80C ; color: black;}')
                self.G1_widget_buttons[-1].show()
        self.G1_button = QPushButton("Next Move", self.G1_widget)
        self.G1_button.clicked.connect(self.G1_next_move)
        self.G1_button.move(5, 200)
        self.G1_button.show()
        self.G1_move_no = 1
        self.G1_move_no_label = QLabel("Move No.: "+str(self.G1_move_no)+"    ", self.G1_widget)
        self.G1_move_no_label.move(5, 250)
        self.G1_move_no_label.show()
        self.G1_branching_factor = self.G1_state.get_branching_factor()
        self.G1_branching_factor_label = QLabel("Branching factor: "+str(self.G1_branching_factor), self.G1_widget)
        self.G1_branching_factor_label.move(5, 300)
        self.G1_branching_factor_label.show()
        if self.G1_state.game_over is False:
            self.G1_game_status = "GAME ON  "
        elif self.G1_state.game_lost is False:
            self.G1_game_status = "GAME WON "
        else:
            self.G1_game_status = "GAME LOST"
        self.G1_game_status_label = QLabel(self.G1_game_status+"  ", self.G1_widget)
        self.G1_game_status_label.move(5, 350)
        self.G1_game_status_label.show()
        self.G1_widget.setWindowTitle('Display G1')
        self.G1_widget.resize(1000, 1000)
        self.G1_widget.move(0, 0)
        self.G1_widget.show()

    def G1_next_move(self):
        if self.G1_state.game_over is True:
            return
        self.G1_curr_x, self.G1_curr_y = hill_climbing(self.G1_state, self.G1_heuristic)
        self.G1_state = next_state(self.G1_state, self.G1_curr_x, self.G1_curr_y)
        self.G1_move_no += 1
        self.G1_branching_factor = self.G1_state.get_branching_factor()
        if self.G1_state.game_over is False:
            if self.G1_state.is_goal_state():
                self.G1_game_status = "GAME WON "
        elif self.G1_state.game_over is True and self.G1_state.game_lost is True:
                self.G1_game_status = "GAME LOST"
        for i in range(self.G1_state.N):
            for j in range(self.G1_state.N):
                if self.G1_state.orig_board[i*self.G1_state.N+j] == 9 and self.G1_curr_x == i and self.G1_curr_y == j:
                    self.G1_widget_buttons[i*self.G1_state.N+j].setIcon(QIcon('imgs/mine_clicked.jpg'))
                    self.G1_widget_buttons[i*self.G1_state.N+j].setIconSize(QSize(PIXEL_SIZE+6, PIXEL_SIZE+6))
                elif self.G1_state.orig_board[i*self.G1_state.N+j] == 9:
                    continue
                elif self.G1_curr_x == i and self.G1_curr_y == j:
                    if self.G1_state.curr_board[i*self.G1_state.N+j] == 0:
                        self.G1_widget_buttons[i*self.G1_state.N+j].setText(" ")
                    else:
                        self.G1_widget_buttons[i*self.G1_state.N+j].setText(str(self.G1_state.curr_board[i*self.G1_state.N+j]))
                    self.G1_widget_buttons[i*self.G1_state.N+j].setStyleSheet('QPushButton {background-color: #0AEBF9 ; color: black;}')
                elif self.G1_state.curr_board[i*self.G1_state.N+j] == 10:
                    continue
                else:
                    if self.G1_state.curr_board[i*self.G1_state.N+j] == 0:
                        self.G1_widget_buttons[i*self.G1_state.N+j].setText(" ")
                    else:
                        self.G1_widget_buttons[i*self.G1_state.N+j].setText(str(self.G1_state.curr_board[i*self.G1_state.N+j]))
                    self.G1_widget_buttons[i*self.G1_state.N+j].setStyleSheet('QPushButton {background-color: #70E80C ; color: black;}')
        self.G1_move_no_label.setText("Move No.: "+str(self.G1_move_no))
        self.G1_branching_factor_label.setText("Branching factor: "+str(self.G1_branching_factor))
        self.G1_game_status_label.setText(self.G1_game_status)

    def G5_btn_clicked(self):
        global N, P, heuristic, PIXEL_SIZE
        M = P*N*N//100
        self.G5_alpha = 0.1
        self.G5_beta = 0.1
        self.G5_threshold = 0.475
        if heuristic == "heuristic1":
            self.G5_heuristic = heuristic1
        else:
            self.G5_heuristic = heuristic2
        self.G5_widget = QWidget()
        self.G5_state, self.G5_curr_x, self.G5_curr_y = first_click(mine_generator(N, M))
        self.G5_widget_buttons = []
        for i in range(self.G5_state.N):
            for j in range(self.G5_state.N):
                self.G5_widget_buttons.append(QPushButton(self.G5_widget))
                self.G5_widget_buttons[-1].resize(PIXEL_SIZE, PIXEL_SIZE)
                self.G5_widget_buttons[-1].move(150+(j+1)*PIXEL_SIZE, 25+(i+1)*PIXEL_SIZE)
                if self.G5_state.orig_board[i*self.G5_state.N+j] == 9 and self.G5_curr_x == i and self.G5_curr_y == j:
                    self.G5_widget_buttons[-1].setIcon(QIcon('imgs/mine_clicked.jpg'))
                    self.G5_widget_buttons[-1].setIconSize(QSize(PIXEL_SIZE+6, PIXEL_SIZE+6))
                elif self.G5_state.orig_board[i*self.G5_state.N+j] == 9:
                    self.G5_widget_buttons[-1].setIcon(QIcon('imgs/mine.jpg'))
                    self.G5_widget_buttons[-1].setIconSize(QSize(PIXEL_SIZE+6, PIXEL_SIZE+6))
                elif self.G5_curr_x == i and self.G5_curr_y == j:
                    self.G5_widget_buttons[-1].setText(" ")
                    self.G5_widget_buttons[-1].setStyleSheet('QPushButton {background-color: #0AEBF9 ; color: black;}')
                elif self.G5_state.curr_board[i*self.G5_state.N+j] == 10:
                    self.G5_widget_buttons[-1].setText(" ")
                    self.G5_widget_buttons[-1].setStyleSheet('QPushButton {background-color: #747D7E ; color: black;}')
                else:
                    if self.G5_state.curr_board[i*self.G5_state.N+j] == 0:
                        self.G5_widget_buttons[-1].setText(" ")
                        self.G5_widget_buttons[-1].setStyleSheet('QPushButton {background-color: #70E80C ; color: black;}')
                    else:
                        self.G5_widget_buttons[-1].setText(str(self.G5_state.curr_board[i*self.G5_state.N+j]))
                        self.G5_widget_buttons[-1].setStyleSheet('QPushButton {background-color: #70E80C ; color: black;}')
                self.G5_widget_buttons[-1].show()
        self.G5_button = QPushButton("Next Move", self.G5_widget)
        self.G5_button.clicked.connect(self.G5_next_move)
        self.G5_button.move(5, 200)
        self.G5_button.show()
        self.G5_move_no = 1
        self.G5_T = self.G5_alpha / pow(self.G5_move_no, self.G5_beta)
        self.G5_move_no_label = QLabel("Move No.: "+str(self.G5_move_no)+"    ", self.G5_widget)
        self.G5_move_no_label.move(5, 250)
        self.G5_move_no_label.show()
        self.G5_branching_factor = self.G5_state.get_branching_factor()
        self.G5_branching_factor_label = QLabel("Branching factor: "+str(self.G5_branching_factor), self.G5_widget)
        self.G5_branching_factor_label.move(5, 300)
        self.G5_branching_factor_label.show()
        if self.G5_state.game_over is False:
            self.G5_game_status = "GAME ON  "
        elif self.G5_state.game_lost is False:
            self.G5_game_status = "GAME WON "
        else:
            self.G5_game_status = "GAME LOST"
        self.G5_game_status_label = QLabel(self.G5_game_status+"  ", self.G5_widget)
        self.G5_game_status_label.move(5, 350)
        self.G5_game_status_label.show()
        self.G5_widget.setWindowTitle('Display G5')
        self.G5_widget.resize(1000, 1000)
        self.G5_widget.move(0, 0)
        self.G5_widget.show()

    def G5_next_move(self):
        if self.G5_state.game_over is True:
            return
        tmp_G5_move = simulated_annealing(self.G5_state, self.G5_heuristic, self.G5_T, self.G5_threshold)
        if tmp_G5_move is None:
            self.G5_move_no += 1
            self.G5_T = self.G5_alpha / pow(self.G5_move_no, self.G5_beta)
            self.G5_move_no_label.setText("Move No.: "+str(self.G5_move_no))
            return
        else:
            self.G5_curr_x, self.G5_curr_y = tmp_G5_move
        self.G5_state = next_state(self.G5_state, self.G5_curr_x, self.G5_curr_y)
        self.G5_move_no += 1
        self.G5_T = self.G5_alpha / pow(self.G5_move_no, self.G5_beta)
        self.G5_branching_factor = self.G5_state.get_branching_factor()
        if self.G5_state.game_over is False:
            if self.G5_state.is_goal_state():
                self.G5_game_status = "GAME WON "
        elif self.G5_state.game_over is True and self.G5_state.game_lost is True:
                self.G5_game_status = "GAME LOST"
        for i in range(self.G5_state.N):
            for j in range(self.G5_state.N):
                if self.G5_state.orig_board[i*self.G5_state.N+j] == 9 and self.G5_curr_x == i and self.G5_curr_y == j:
                    self.G5_widget_buttons[i*self.G5_state.N+j].setIcon(QIcon('imgs/mine_clicked.jpg'))
                    self.G5_widget_buttons[i*self.G5_state.N+j].setIconSize(QSize(PIXEL_SIZE+6, PIXEL_SIZE+6))
                elif self.G5_state.orig_board[i*self.G5_state.N+j] == 9:
                    continue
                elif self.G5_curr_x == i and self.G5_curr_y == j:
                    if self.G5_state.curr_board[i*self.G5_state.N+j] == 0:
                        self.G5_widget_buttons[i*self.G5_state.N+j].setText(" ")
                    else:
                        self.G5_widget_buttons[i*self.G5_state.N+j].setText(str(self.G5_state.curr_board[i*self.G5_state.N+j]))
                    self.G5_widget_buttons[i*self.G5_state.N+j].setStyleSheet('QPushButton {background-color: #0AEBF9 ; color: black;}')
                elif self.G5_state.curr_board[i*self.G5_state.N+j] == 10:
                    continue
                else:
                    if self.G5_state.curr_board[i*self.G5_state.N+j] == 0:
                        self.G5_widget_buttons[i*self.G5_state.N+j].setText(" ")
                    else:
                        self.G5_widget_buttons[i*self.G5_state.N+j].setText(str(self.G5_state.curr_board[i*self.G5_state.N+j]))
                    self.G5_widget_buttons[i*self.G5_state.N+j].setStyleSheet('QPushButton {background-color: #70E80C ; color: black;}')
        self.G5_move_no_label.setText("Move No.: "+str(self.G5_move_no))
        self.G5_branching_factor_label.setText("Branching factor: "+str(self.G5_branching_factor))
        self.G5_game_status_label.setText(self.G5_game_status)

    def choose_heuristic(self, text):
        self.G2_graph.heuristic = text
        self.G2_graph.plot()

    def choose_X(self, text):
        if self.G2_graph.Y_label == text:
            return
        self.G2_graph.X_label = text
        self.G2_graph.plot()

    def choose_Y(self, text):
        if self.G2_graph.X_label == text:
            return
        self.G2_graph.Y_label = text
        self.G2_graph.plot()

    def G2_btn_clicked(self):
        global N
        self.G2_widget = QWidget()
        self.G2_widget.setWindowTitle('Display Landscape')
        self.G2_widget.setGeometry(0, 0, 1000, 700)
        self.G2_graph = PlotCanvas_v2(self.G2_widget)
        self.G2_graph.move(10, 10)
        self.G2_h_label = QLabel('Choose Heuristic:', self.G2_widget)
        self.G2_h_combo = QComboBox(self.G2_widget)
        for idx in range(1, 3):
            self.G2_h_combo.addItem("Heuristic"+str(idx))
        self.G2_h_label.move(700, 200)
        self.G2_h_combo.move(810, 197)
        self.G2_h_combo.activated[str].connect(self.choose_heuristic)
        self.G2_X_label = QLabel('Choose X1:', self.G2_widget)
        self.G2_X_combo = QComboBox(self.G2_widget)
        for idx in range(1, N*N+1):
            self.G2_X_combo.addItem("X"+str(idx))
        self.G2_X_label.move(700, 250)
        self.G2_X_combo.move(780, 247)
        self.G2_X_combo.activated[str].connect(self.choose_X)
        self.G2_Y_label = QLabel('Choose X2:', self.G2_widget)
        self.G2_Y_combo = QComboBox(self.G2_widget)
        for idx in range(1, N*N+1):
            self.G2_Y_combo.addItem("X"+str(idx))
        self.G2_Y_label.move(700, 300)
        self.G2_Y_combo.move(780, 297)
        self.G2_Y_combo.activated[str].connect(self.choose_Y)
        self.G2_widget.show()

    def G3_btn_clicked(self):
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
        # y1 = [10, 11, 13, 11, 13, 15, 10, 10, 14, 10, 10, 9, 10, 11, 12, 12, 16, 11, 9, 8, 15, 15, 11, 10, 11, 9, 12, 15, 8, 11, 10, 14, 12, 15, 12, 10, 13, 8, 11, 10, 16, 11, 14, 12, 7, 9, 8, 12, 11, 9, 12, 11, 12, 12, 12, 15, 14, 7, 10, 8, 13, 10, 13, 14, 9, 9, 11, 8, 11, 11, 12, 9, 12, 9, 11, 13, 11, 11, 7, 11, 11, 8, 11, 9, 11, 11, 13, 9, 11, 11, 11, 15, 12, 11, 16, 12, 12, 12, 13, 11]
        y1 = [43, 45, 43, 41, 44, 45, 43, 42, 39, 42, 40, 39, 39, 39, 38, 36, 37, 37, 39, 36, 35, 37, 38, 36, 34, 33, 37, 34, 33, 35, 34, 34, 31, 33, 32, 30, 31, 32, 34, 33, 33, 34, 35, 32, 31, 33, 33, 32, 31, 29, 30, 30, 30, 30, 29, 31, 31, 30, 32, 31, 30, 33, 34, 32, 32, 35, 33, 31, 29, 30, 28, 29, 30, 30, 31, 31, 32, 29, 29, 28, 26, 30, 30, 29, 31, 30, 33, 32, 32, 28, 27, 26, 30, 29, 27, 26, 29, 31, 30, 28]
        y2 = [45, 43, 42, 44, 41, 44, 40, 39, 42, 44, 42, 42, 41, 39, 38, 39, 37, 36, 39, 40, 38, 38, 39, 36, 39, 36, 38, 38, 35, 36, 37, 40, 39, 39, 36, 37, 34, 35, 37, 36, 36, 38, 39, 35, 34, 33, 35, 34, 33, 33, 32, 33, 34, 32, 32, 34, 33, 32, 34, 36, 35, 31, 32, 34, 33, 30, 30, 31, 33, 32, 34, 33, 33, 33, 36, 38, 34, 32, 31, 32, 34, 31, 32, 30, 31, 29, 31, 30, 28, 30, 29, 29, 30, 27, 29, 28, 28, 27, 30, 29]
        self.G3_widget = QWidget()
        self.G3_widget.setWindowTitle('Display G3')
        self.G3_widget.setGeometry(10, 10, 650, 650)
        self.G3_graph = PlotCanvas_v1(x, 'k Value (Local Beam Search)', y1, 'Avg. no. of steps taken by local beam search', 'Effect of varying value of k in local beam search', y2=y2, parent=self.G3_widget)
        self.G3_graph.move(10, 10)
        self.G3_widget.show()
    
    def G4_btn_clicked(self):
        x = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        y1 = [9, 10, 10, 9, 10, 9, 9, 10, 8, 9]
        self.G4_widget = QWidget()
        self.G4_widget.setWindowTitle('Display G4')
        self.G4_widget.setGeometry(10, 10, 500, 500)
        self.G4_graph = PlotCanvas_v1(x, 'N (Size of Warfield)', y1, 'Avg. No. of successes in 10 independent runs', 'Effect of size of war field on success rate', parent=self.G4_widget, width=6, height=6)
        self.G4_graph.move(10, 10)
        self.G4_widget.show()

    def G6_btn_clicked(self):
        self.G2_btn_clicked()

    def choose_heuristic_G7(self, text):
        self.G7_graph1.heuristic = text
        self.G7_graph2.heuristic = text
        self.G7_graph3.heuristic = text
        self.G7_graph1.plot()
        self.G7_graph2.plot()
        self.G7_graph3.plot()

    def choose_X_G7(self, text):
        if self.G7_graph1.Y_label == text:
            return
        self.G7_graph1.X_label = text
        self.G7_graph2.X_label = text
        self.G7_graph3.X_label = text
        self.G7_graph1.plot()
        self.G7_graph2.plot()
        self.G7_graph3.plot()

    def choose_Y_G7(self, text):
        if self.G7_graph1.X_label == text:
            return
        self.G7_graph1.Y_label = text
        self.G7_graph2.Y_label = text
        self.G7_graph3.Y_label = text
        self.G7_graph1.plot()
        self.G7_graph2.plot()
        self.G7_graph3.plot()

    def G7_btn_clicked(self):
        global N
        self.G7_widget  = QWidget()
        self.G7_widget.setWindowTitle('Display G7')
        self.G7_widget.setGeometry(0, 0, 1300, 600)
        self.G7_graph1 = PlotCanvas_v3(1, parent=self.G7_widget)
        self.G7_graph1.move(0, 0)
        self.G7_graph2 = PlotCanvas_v3(2, parent=self.G7_widget)
        self.G7_graph2.move(420, 0)
        self.G7_graph3 = PlotCanvas_v3(3, parent=self.G7_widget)
        self.G7_graph3.move(840, 0)
        self.G7_h_label = QLabel('Choose Heuristic:', self.G7_widget)
        self.G7_h_combo = QComboBox(self.G7_widget)
        for idx in range(1, 3):
            self.G7_h_combo.addItem("Heuristic"+str(idx))
        self.G7_h_label.move(50, 500)
        self.G7_h_combo.move(165, 497)
        self.G7_h_combo.activated[str].connect(self.choose_heuristic_G7)
        self.G7_X_label = QLabel('Choose X1:', self.G7_widget)
        self.G7_X_combo = QComboBox(self.G7_widget)
        for idx in range(1, N*N+1):
            self.G7_X_combo.addItem("X"+str(idx))
        self.G7_X_label.move(300, 500)
        self.G7_X_combo.move(375, 497)
        self.G7_X_combo.activated[str].connect(self.choose_X_G7)
        self.G7_Y_label = QLabel('Choose X2:', self.G7_widget)
        self.G7_Y_combo = QComboBox(self.G7_widget)
        for idx in range(1, N*N+1):
            self.G7_Y_combo.addItem("X"+str(idx))
        self.G7_Y_label.move(500, 500)
        self.G7_Y_combo.move(575, 497)
        self.G7_Y_combo.activated[str].connect(self.choose_Y_G7)
        self.G7_widget.show()

def stochastic_hill_climbing_driver(heuristic_fn):
    # n = 10
    # m = 10
    n = 16
    m = 40
    no_of_wins = 0
    for idx in range(20):
        state, _, _ = first_click(mine_generator(n, m))
        no_of_moves = 1
        while True:
            if state.game_over is True:
                if state.game_lost is False:
                    no_of_wins += 1
                break
            next_x, next_y = stochastic_hill_climbing(state, heuristic_fn)
            state = next_state(state, next_x, next_y)
            no_of_moves += 1
            if state.game_over is False:
                state.is_goal_state()
    print(no_of_wins)

def hill_climbing_driver(heuristic_fn):
    # n = 10
    # m = 10
    n = 16
    m = 40
    no_of_wins = 0
    no_of_moves_list = []
    times_list = []
    for idx in range(20):
        start = time.time()
        state, _, _ = first_click(mine_generator(n, m))
        no_of_moves = 1
        while True:
            if state.game_over is True:
                end = time.time()
                if state.game_lost is False:
                    no_of_wins += 1
                no_of_moves_list.append(no_of_moves)
                times_list.append(end-start)
                break
            next_x, next_y = hill_climbing(state, heuristic_fn)
            state = next_state(state, next_x, next_y)
            no_of_moves += 1
            if state.game_over is False:
                state.is_goal_state()
    print(no_of_wins)
    no_of_moves_sum = 0 
    for move in no_of_moves_list:
        no_of_moves_sum += move
    print(no_of_moves_sum/len(no_of_moves_list))
    times_sum = 0 
    for tme in times_list:
        times_sum += tme
    print(times_sum/len(times_list))

def local_beam_search_driver(heuristic_fn, K):
    n = 16
    m = 40
    states_list = []
    for idx in range(K):
        state, _, _ = first_click(mine_generator(n, m))
        states_list.append(state)
    no_of_moves = 1
    while True:
        states_list_v2 = []
        for idx in range(len(states_list)):
            if states_list[idx].game_over is True:
                if states_list[idx].game_lost is False:
                    print(no_of_moves)
                    return no_of_moves
            else:
                states_list_v2.append(states_list[idx])
        next_moves = local_beam_search(states_list_v2, heuristic_fn, K)
        states_list = []
        for move in next_moves:
            idx, x, y = move
            states_list.append(next_state_v2(states_list_v2[idx], x, y))
        no_of_moves += 1
        for state in states_list:
            if state.game_over is False:
                state.is_goal_state()

def simulated_annealing_driver(heuristic_fn):
    n = 16
    m = 40
    alpha = 0.1
    beta = 0.1
    threshold = 0.475
    no_of_wins = 0
    no_of_moves_list = []
    times_list = []
    for idx in range(20):
        start = time.time()
        state, _, _ = first_click(mine_generator(n, m))
        no_of_moves = 1
        while True:
            if state.game_over is True:
                end = time.time()
                if state.game_lost is False:
                    no_of_wins += 1
                no_of_moves_list.append(no_of_moves)
                times_list.append(end-start)
                break
            next_move = simulated_annealing(state, heuristic_fn, alpha/pow(no_of_moves, beta), threshold)
            if next_move is None:
                no_of_moves += 1
                continue
            next_x, next_y = next_move
            state = next_state(state, next_x, next_y)
            no_of_moves += 1
            if state.game_over is False:
                state.is_goal_state()
    print(no_of_wins)
    no_of_moves_sum = 0 
    for move in no_of_moves_list:
        no_of_moves_sum += move
    print(no_of_moves_sum/len(no_of_moves_list))
    times_sum = 0 
    for tme in times_list:
        times_sum += tme
    print(times_sum/len(times_list))

def G3_plotter(heuristic_fn):
    no_of_moves_list = []
    for K in range(1, 101):
        no_of_moves_list.append(local_beam_search_driver(heuristic_fn, K))
    print(no_of_moves_list)

def G4_plotter(heuristic_fn):
    start = time.time()
    success_rate_list = []
    for idx_2 in range(10, 110, 10):
        no_of_wins = 0
        n = idx_2
        m = (7*idx_2)//4
        for idx in range(10):
            state, _, _ = first_click(mine_generator(n, m))
            no_of_moves = 1
            while True:
                if state.game_over is True:
                    if state.game_lost is False:
                        no_of_wins += 1
                    break
                next_x, next_y = hill_climbing(state, heuristic_fn)
                state = next_state(state, next_x, next_y)
                no_of_moves += 1
                if state.game_over is False:
                    state.is_goal_state()
        success_rate_list.append(no_of_wins)
    print(success_rate_list)
    end = time.time()
    print(end-start, " seconds")    

def get_X_Y():
    X = []
    for i in range(10):
        lst = []
        for j in range(10):
            lst.append(j)
        X.append(lst)
    Y = []
    for i in range(10):
        lst = []
        for j in range(10):
            lst.append(i)
        Y.append(lst)
    return X, Y

def get_h1_surface():
    Z = [[0.00, 0.03, 0.07, 0.12, 0.19, 0.25, 0.36, 0.39, 0.45, 1.00],
         [0.03, 0.09, 0.15, 0.23, 0.30, 0.42, 0.40, 0.45, 0.52, 1.00],
         [0.07, 0.15, 0.26, 0.40, 0.40, 0.46, 0.43, 0.50, 0.59, 1.00],
         [0.12, 0.23, 0.40, 0.47, 0.49, 0.51, 0.47, 0.55, 0.65, 1.00],
         [0.19, 0.30, 0.40, 0.49, 0.45, 0.45, 0.52, 0.60, 0.70, 1.00],
         [0.25, 0.42, 0.46, 0.51, 0.45, 0.35, 0.56, 0.65, 0.80, 1.00],
         [0.36, 0.40, 0.43, 0.47, 0.52, 0.56, 0.65, 0.72, 0.88, 1.00],
         [0.39, 0.45, 0.52, 0.55, 0.60, 0.65, 0.72, 0.74, 0.92, 1.00],
         [0.45, 0.50, 0.59, 0.65, 0.70, 0.80, 0.88, 0.92, 0.97, 1.00],
         [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00]]
    return Z

def get_h2_surface():
    Z = [[0.00, 0.02, 0.05, 0.11, 0.19, 0.25, 0.35, 0.45, 0.75, 1.00],
         [0.02, 0.05, 0.08, 0.13, 0.20, 0.28, 0.41, 0.53, 0.50, 1.00],
         [0.05, 0.08, 0.10, 0.17, 0.25, 0.35, 0.55, 0.58, 0.54, 1.00],
         [0.11, 0.13, 0.17, 0.22, 0.33, 0.50, 0.40, 0.61, 0.63, 1.00],
         [0.19, 0.20, 0.25, 0.33, 0.45, 0.37, 0.67, 0.69, 0.73, 1.00],
         [0.25, 0.28, 0.35, 0.50, 0.37, 0.62, 0.56, 0.72, 0.77, 1.00],
         [0.35, 0.41, 0.55, 0.40, 0.67, 0.56, 0.65, 0.75, 0.83, 1.00],
         [0.45, 0.53, 0.58, 0.61, 0.69, 0.72, 0.75, 0.80, 0.90, 1.00],
         [0.75, 0.50, 0.54, 0.63, 0.73, 0.77, 0.83, 0.90, 0.96, 1.00],
         [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00]]
    return Z

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI_Layout()
    sys.exit(app.exec_())

# stochastic_hill_climbing_driver(heuristic1)
# stochastic_hill_climbing_driver(heuristic2)

# hill_climbing_driver(heuristic1)
# hill_climbing_driver(heuristic2)

# simulated_annealing_driver(heuristic1)
# simulated_annealing_driver(heuristic2)

# G4_plotter(heuristic1)
# G4_plotter(heuristic2)

# local_beam_search_driver(heuristic1, 20)
# local_beam_search_driver(heuristic2, 8)

# G3_plotter(heuristic1)
# G3_plotter(heuristic2)

# class GUI_Layout(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Minesweeper Intelligent Agent')
#         self.grid = QGridLayout()
#         self.setLayout(self.grid)
#         self.init_ui()
#         pt = self.palette()
#         pt.setColor(self.backgroundRole(), QColor( 245, 183, 5 ))
#         self.setPalette(pt)
#         self.show()
#     def init_ui(self):
#         self.show_R_values()
#         self.show_G_buttons()
#         self.show_N_M_buttons()
#     def show_R_values(self):
#         self.w1 = QWidget(self)
#         self.grid.addWidget(self.w1, 0, 0)
#         self.w1_grid = QGridLayout()
#         self.w1.setLayout(self.w1_grid)
#         self.w1_texts = []
#         self.w1_texts.append("R1 : Maximum memory allocated till the problem is solved (T1) - 00000000")
#         self.w1_texts.append("R2 : Time to reach goal state (T1) - t seconds")
#         self.w1_texts.append("R3 : ")
#         self.w1_texts.append("R4 : No. of times T1 reached global optima using heuristic h1 -  /20")
#         self.w1_texts.append("R5 : No. of times T1 reached global optima using heuristic h2 -  /20")
#         self.w1_texts.append("R6 : Avg. no. of steps taken by T1 to reach local/global optima - ")
#         self.w1_texts.append("R7 : No. of times Stochastic T1 reached global optima using heuristic h1 -  /20")
#         self.w1_texts.append("R8 : No. of times Stochastic T1 reached global optima using heuristic h2 -  /20")
#         self.w1_texts.append("R9 : Avg. no. of steps taken by local beam search (k=20) using h1 - 20, global optima")
#         self.w1_texts.append("R10: Avg. no. of steps taken by local beam search (k=8) using h2 - 10, local optima")
#         self.w1_texts.append("R11: Maximum memory allocated till the problem is solved (T2) - ")
#         self.w1_texts.append("R12: Time to reach goal state (T2) - t seconds")
#         self.w1_texts.append("R13: ")
#         self.w1_texts.append("R14: No. of times T2 reached global optima using heuristic h1 -  /20")
#         self.w1_texts.append("R15: No. of times T2 reached global optima using heuristic h2 -  /20")
#         self.w1_texts.append("R16: Avg. no. of steps taken by T2 to reach local/global optima - ")
#         self.w1_labels = []
#         for idx in range(16):
#             self.w1_labels.append(QLabel(self.w1))
#             self.w1_grid.addWidget(self.w1_labels[-1], idx, 0)
#             self.w1_labels[idx].setText(self.w1_texts[idx])
#             self.w1_labels[idx].setStyleSheet('color: Brown')
#             self.w1_labels[idx].show()
#         self.w1.show()
#     def show_G_buttons(self):
#         self.w2 = QWidget(self)
#         self.grid.addWidget(self.w2, 0, 1)
#         self.w2_grid = QGridLayout()
#         self.w2_grid.setSpacing(10)
#         self.w2_grid.setColumnStretch(10, 10)
#         self.w2_grid.setVerticalSpacing(10)
#         self.w2.setLayout(self.w2_grid)
#         self.w2_functions = [G1, G2, G3, G4, G5, G6, G7]
#         self.w2_buttons = []
#         for idx in range(7):
#             self.w2_buttons.append(QPushButton("G"+str(idx+1), self.w2))
#             self.w2_buttons[idx].clicked.connect(self.w2_functions[idx])
#             self.w2_grid.addWidget(self.w2_buttons[idx], idx, 0)
#             self.w2_buttons[idx].setStyleSheet('QPushButton {background-color: #b41bf2 ; color: black;}')
#             self.w2_buttons[idx].show()
#         self.w2_label = QLabel("View G1-G7", self.w2)
#         self.w2_grid.addWidget(self.w2_label, 7, 0)
#         self.w2_label.setStyleSheet('color: Brown')
#         self.w2.show()
#     def show_N_M_buttons(self):
#         self.w3 = QWidget(self)
#         self.grid.addWidget(self.w3, 0, 2)
#         self.w3_grid = QGridLayout()
#         self.w3_grid.setSpacing(10)
#         self.w3.setLayout(self.w3_grid)
#         self.w3_label = QLabel("Choose N and P for G1 and G5: ", self.w3)
#         self.w3_grid.addWidget(self.w3_label, 0, 0)
#         self.w3_label.setStyleSheet('color: Brown')
#         self.w3_N_label = QLabel("Select size of square N: ", self.w3)
#         self.w3_N_combo_box = QComboBox(self.w3)
#         for idx in range(8, 41):
#             self.w3_N_combo_box.addItem(str(idx))
#         self.w3_grid.addWidget(self.w3_N_label, 1, 0)
#         self.w3_N_label.setStyleSheet('color: Brown')
#         self.w3_grid.addWidget(self.w3_N_combo_box, 1, 1)
#         self.w3_N_combo_box.setStyleSheet('color: Brown')
#         self.w3_N_combo_box.activated[str].connect(select_N)
#         self.w3_P_label = QLabel("Select percentage of mines P: ", self.w3)
#         self.w3_P_combo_box = QComboBox(self.w3)
#         for idx in range(5, 21):
#             self.w3_P_combo_box.addItem(str(idx))
#         self.w3_grid.addWidget(self.w3_P_label, 2, 0)
#         self.w3_P_label.setStyleSheet('color: Brown')
#         self.w3_grid.addWidget(self.w3_P_combo_box, 2, 2)
#         self.w3_P_combo_box.setStyleSheet('color: Brown')
#         self.w3_P_combo_box.activated[str].connect(select_P)
#         self.w3.show()
