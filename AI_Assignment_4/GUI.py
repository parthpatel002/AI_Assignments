"""
@author: Patel Parth (2016A7PS0150P)
"""

import my_stats

from algo import *

import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox
# from PyQt5.QtWidgets import QSizePolicy, QToolButton
# from PyQt5.QtCore import QSize
# from PyQt5.QtGui import QIcon, QColor

# Both laureates and slots are assigned numbers starting from 1.
GROUP_CHOICES_ORIGINAL = [[3, 5, 8, 9, 12, 18, 19], [8, 9, 12, 19, 2], [3, 5, 4, 16, 8, 9, 19], [8, 9, 12, 15], [15, 16, 17, 18, 19, 20], [3, 5, 7, 11, 14, 20], [3, 5, 12, 2, 18, 19, 20, 1], [3, 5, 8, 9, 10, 18, 19, 20], [3, 13, 8, 9, 7, 19, 20], [1, 8, 9, 13, 20], [18, 19, 20], [3, 11, 8, 18, 19, 20], [3, 8, 10, 12, 4, 20], [3, 5, 11, 9, 10, 17, 19, 20], [2, 8, 12, 18, 19, 20]]
LAUREATE_CHOICES_ORIGINAL = [[2, 5, 7], [1, 4, 6, 2], [2, 5, 6, 1], [2, 4, 6, 8], [2, 6, 5], [1, 5, 3], [2, 4, 6, 1, 8], [1, 3, 4], [4, 1, 5, 8, 6], [8], [2, 3], [1, 2, 3, 4, 7], [7, 1, 8], [5, 3, 6, 1], [2, 5], [2, 5, 1, 4], [1, 4, 5, 6], [5, 4], [1, 3, 6, 8], [6]]

GROUP_CHOICES = GROUP_CHOICES_ORIGINAL
LAUREATE_CHOICES = LAUREATE_CHOICES_ORIGINAL
GROUP_SELECTED = 1 # 1-indexed
LAUREATE_SELECTED = 1 # 1-indexed
HEURISTIC = 'default'
BTN_LENGTH = 30

class GUI_Layout(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Constraint Satisfaction Problem: Students meet Nobel laureates')
        self.init_ui()
        self.setGeometry(0, 0, 1200, 550)
        self.show()
    def init_ui(self):
        self.show_R_values()
        self.show_statistics()
    def show_R_values(self):
        self.w1 = QWidget(self)
        self.w1_texts = []
        self.w1_texts.append("R1 : DFS+BT: Total number of nodes generated - 8545")
        self.w1_texts.append("R2 : DFS+BT: Bytes allocated per node - 64")
        self.w1_texts.append("R3 : DFS+BT: Maximum stack size - 18")
        self.w1_texts.append("R4 : DFS+BT: Total time taken to compute the values - 0.11493351936 secs.")
        self.w1_texts.append("R5 : DFS+BT: No. of nodes generated (MRV with degree as tiebreak) - 13")
        self.w1_texts.append("R6 : DFS+BT+AC3: Total number of nodes generated - 370")
        self.w1_texts.append("R7 : Saving using constraint propagation = (R1-R6)/R1 = 0.956699824")
        self.w1_texts.append("R8 : DFS+BT+AC3: Total time taken to compute the values - 0.01493120193 secs.")
        self.w1_texts.append("R9 : Ratio of time taken = R4/R8 = 7.697539682")
        self.w1_labels = []
        for idx in range(9):
            self.w1_labels.append(QLabel(self.w1_texts[idx], self.w1))
            self.w1_labels[idx].move(20, 100+idx*30)
            self.w1_labels[idx].setStyleSheet('color: Brown')
            self.w1_labels[idx].show()
        self.w1.move(0, 0)
        self.w1.show()
    def show_statistics(self):
        self.w2 = QWidget(self)
        self.w2_reset_btn = QPushButton('Reset group and laureate details to default values', self.w2)
        self.w2_reset_btn.clicked.connect(self.reset_details)
        self.w2_reset_btn.setStyleSheet('color: Brown')
        self.w2_reset_btn.setGeometry(25, 75, 325, 20)
        self.w2_reset_btn.show()
        self.w2_empty_btn = QPushButton('Initialize details to NO groups and NO laureates', self.w2)
        self.w2_empty_btn.clicked.connect(self.empty_details)
        self.w2_empty_btn.setStyleSheet('color: Brown')
        self.w2_empty_btn.setGeometry(25, 125, 325, 20)
        self.w2_empty_btn.show()
        self.w2_new_grp_btn = QPushButton('Add new group', self.w2)
        self.w2_new_grp_btn.clicked.connect(self.add_new_grp)
        self.w2_new_grp_btn.setStyleSheet('color: Brown')
        self.w2_new_grp_btn.setGeometry(400, 75, 125, 20)
        self.w2_new_grp_btn.show()
        self.w2_new_laureate_btn = QPushButton('Add new laureate', self.w2)
        self.w2_new_laureate_btn.clicked.connect(self.add_new_laureate)
        self.w2_new_laureate_btn.setStyleSheet('color: Brown')
        self.w2_new_laureate_btn.setGeometry(400, 125, 125, 20)
        self.w2_new_laureate_btn.show()
        self.w2_1_1_label = QLabel("Select Group:", self.w2) 
        self.w2_1_1_combo_box = QComboBox(self.w2)
        for idx in range(1, 40):
            self.w2_1_1_combo_box.addItem(str(idx))
        self.w2_1_1_label.move(0, 200)
        self.w2_1_1_label.setStyleSheet('color: Green')
        self.w2_1_1_combo_box.move(100, 197)
        self.w2_1_1_combo_box.setStyleSheet('color: Green')
        self.w2_1_1_combo_box.activated[str].connect(self.select_group)
        self.w2_1_2_label = QLabel("Add Laureate To Group:", self.w2) 
        self.w2_1_2_combo_box = QComboBox(self.w2)
        for idx in range(1, 40):
            self.w2_1_2_combo_box.addItem(str(idx))
        self.w2_1_2_label.move(175, 200)
        self.w2_1_2_label.setStyleSheet('color: Green')
        self.w2_1_2_combo_box.move(325, 197)
        self.w2_1_2_combo_box.setStyleSheet('color: Green')
        self.w2_1_2_combo_box.activated[str].connect(self.add_laureate_to_group)
        self.w2_1_3_label = QLabel("Remove Laureate from Group:", self.w2) 
        self.w2_1_3_combo_box = QComboBox(self.w2)
        for idx in range(1, 40):
            self.w2_1_3_combo_box.addItem(str(idx))
        self.w2_1_3_label.move(400, 200)
        self.w2_1_3_label.setStyleSheet('color: Green')
        self.w2_1_3_combo_box.move(590, 197)
        self.w2_1_3_combo_box.setStyleSheet('color: Green')
        self.w2_1_3_combo_box.activated[str].connect(self.remove_laureate_from_group)
        self.w2_2_1_label = QLabel("Select Laureate:", self.w2) 
        self.w2_2_1_combo_box = QComboBox(self.w2)
        for idx in range(1, 40):
            self.w2_2_1_combo_box.addItem(str(idx))
        self.w2_2_1_label.move(0, 250)
        self.w2_2_1_label.setStyleSheet('color: Red')
        self.w2_2_1_combo_box.move(100, 247)
        self.w2_2_1_combo_box.setStyleSheet('color: Red')
        self.w2_2_1_combo_box.activated[str].connect(self.select_laureate)
        self.w2_2_2_label = QLabel("Add Slot To Laureate:", self.w2) 
        self.w2_2_2_combo_box = QComboBox(self.w2)
        for idx in range(1, 100):
            self.w2_2_2_combo_box.addItem(str(idx))
        self.w2_2_2_label.move(175, 250)
        self.w2_2_2_label.setStyleSheet('color: Red')
        self.w2_2_2_combo_box.move(325, 247)
        self.w2_2_2_combo_box.setStyleSheet('color: Red')
        self.w2_2_2_combo_box.activated[str].connect(self.add_slot_to_laureate)
        self.w2_2_3_label = QLabel("Remove Slot from Laureate:", self.w2) 
        self.w2_2_3_combo_box = QComboBox(self.w2)
        for idx in range(1, 100):
            self.w2_2_3_combo_box.addItem(str(idx))
        self.w2_2_3_label.move(400, 250)
        self.w2_2_3_label.setStyleSheet('color: Red')
        self.w2_2_3_combo_box.move(590, 247)
        self.w2_2_3_combo_box.setStyleSheet('color: Red')
        self.w2_2_3_combo_box.activated[str].connect(self.remove_slot_from_laureate)
        self.w2_print_btn = QPushButton("Print current group and laureate details to console", self.w2)
        self.w2_print_btn.clicked.connect(self.print_to_console)
        self.w2_print_btn.setStyleSheet('color: Purple')
        self.w2_print_btn.setGeometry(75, 300, 400, 20)
        self.w2_print_btn.show()
        self.w2_select_heuristic_label = QLabel("Select Heuristic:", self.w2) 
        self.w2_select_heuristic_combo_box = QComboBox(self.w2)
        self.w2_select_heuristic_combo_box.addItem("default")
        self.w2_select_heuristic_combo_box.addItem("MRV_with_degree")
        self.w2_select_heuristic_label.move(0, 400)
        self.w2_select_heuristic_label.setStyleSheet('color: Brown')
        self.w2_select_heuristic_combo_box.move(100, 397)
        self.w2_select_heuristic_combo_box.setStyleSheet('color: Brown')
        self.w2_select_heuristic_combo_box.activated[str].connect(self.select_heuristic)
        self.w2_run_DFS_BT_btn = QPushButton("Run DFS_BT", self.w2)
        self.w2_run_DFS_BT_btn.clicked.connect(self.run_DFS_BT)
        self.w2_run_DFS_BT_btn.setStyleSheet('color: Brown')
        self.w2_run_DFS_BT_btn.setGeometry(300, 400, 100, 20)
        self.w2_run_DFS_BT_btn.show()
        self.w2_run_DFS_BT_AC3_btn = QPushButton("Run DFS_BT_AC3", self.w2)
        self.w2_run_DFS_BT_AC3_btn.clicked.connect(self.run_DFS_BT_AC3)
        self.w2_run_DFS_BT_AC3_btn.setStyleSheet('color: Brown')
        self.w2_run_DFS_BT_AC3_btn.setGeometry(450, 400, 125, 20)
        self.w2_run_DFS_BT_AC3_btn.show()
        self.w2_label1 = QLabel("1: Group, laureate and slot nos. should be used incrementally starting from 1.", self.w2)
        self.w2_label1.setStyleSheet('color: Black')
        self.w2_label1.setGeometry(0, 475, 600, 20)
        self.w2_label1.show()
        self.w2_label2 = QLabel("2: If you don't want to go through all partial assignments, just see final result (printed on console).", self.w2)
        self.w2_label2.setStyleSheet('color: Blue')
        self.w2_label2.setGeometry(0, 500, 600, 20)
        self.w2_label2.show()
        self.w2.move(525, 0)
        self.w2.show()
    def reset_details(self):
        global GROUP_CHOICES, LAUREATE_CHOICES, GROUP_CHOICES_ORIGINAL, LAUREATE_CHOICES_ORIGINAL
        GROUP_CHOICES = GROUP_CHOICES_ORIGINAL
        LAUREATE_CHOICES = LAUREATE_CHOICES_ORIGINAL
        return
    def empty_details(self):
        global GROUP_CHOICES, LAUREATE_CHOICES, GROUP_CHOICES_ORIGINAL, LAUREATE_CHOICES_ORIGINAL
        GROUP_CHOICES = []
        LAUREATE_CHOICES = []
        return
    def add_new_grp(self):
        global GROUP_CHOICES
        GROUP_CHOICES.append([])
        return
    def add_new_laureate(self):
        global LAUREATE_CHOICES
        LAUREATE_CHOICES.append([])
        return
    def select_group(self, text):
        global GROUP_SELECTED
        GROUP_SELECTED = int(text)
        # print(GROUP_SELECTED)
        return
    def add_laureate_to_group(self, text):
        global GROUP_SELECTED, GROUP_CHOICES, LAUREATE_CHOICES
        if GROUP_SELECTED-1 >= len(GROUP_CHOICES):
            return
        laureate = int(text)
        if laureate-1 >= len(LAUREATE_CHOICES):
            return
        if laureate not in GROUP_CHOICES[GROUP_SELECTED-1]:
            GROUP_CHOICES[GROUP_SELECTED-1].append(laureate)
        return
    def remove_laureate_from_group(self, text):
        global GROUP_SELECTED, GROUP_CHOICES
        if GROUP_SELECTED-1 >= len(GROUP_CHOICES):
            return
        laureate = int(text)
        if laureate in GROUP_CHOICES[GROUP_SELECTED-1]:
            GROUP_CHOICES[GROUP_SELECTED-1].remove(laureate)
        return
    def select_laureate(self, text):
        global LAUREATE_SELECTED
        LAUREATE_SELECTED = int(text)
        # print(LAUREATE_SELECTED)
        return
    def add_slot_to_laureate(self, text):
        global LAUREATE_SELECTED, LAUREATE_CHOICES
        if LAUREATE_SELECTED-1 >= len(LAUREATE_CHOICES):
            return
        slot = int(text)
        if slot not in LAUREATE_CHOICES[LAUREATE_SELECTED-1]:
            LAUREATE_CHOICES[LAUREATE_SELECTED-1].append(slot)
        return
    def remove_slot_from_laureate(self, text):
        global LAUREATE_SELECTED, LAUREATE_CHOICES
        if LAUREATE_SELECTED-1 >= len(LAUREATE_CHOICES):
            return
        slot = int(text)
        if slot in LAUREATE_CHOICES[LAUREATE_SELECTED-1]:
            LAUREATE_CHOICES[LAUREATE_SELECTED-1].remove(slot)
        return
    def print_to_console(self):
        global GROUP_CHOICES, LAUREATE_CHOICES
        print("-----------------------GROUP DETAILS-----------------------")
        for idx, grp in enumerate(GROUP_CHOICES):
            print("GROUP"+str(idx+1)+":", end=' ')
            if grp == []:
                print('', end='\n')
                continue
            for elem in grp[:-1]:
                print("N"+str(elem), end=', ')
            print('N'+str(grp[-1]), end='\n')
        print("-----------------------LAUREATE DETAILS-----------------------")
        for idx, slots in enumerate(LAUREATE_CHOICES):
            print('N'+str(idx+1)+':', end=' ')
            if slots == []:
                print('', end='\n')
                continue
            for slot in slots[:-1]:
                print(slot, end=', ')
            print(slots[-1], end='\n')
        print("-----------------------END-----------------------")
        return
    def select_heuristic(self, text):
        global HEURISTIC
        HEURISTIC = text
        return
    def run_DFS_BT(self):
        global GROUP_CHOICES, LAUREATE_CHOICES, HEURISTIC, BTN_LENGTH
        if len(GROUP_CHOICES) == 0 or len(LAUREATE_CHOICES) == 0:
            return
        self.csp = CSP(GROUP_CHOICES, LAUREATE_CHOICES)
        self.initial_state = State(self.csp.no_of_laureates)
        self.variable_order = []
        my_stats.NO_OF_NODES = 0
        my_stats.assignment_seq = []
        my_stats.variable_seq =[]
        my_stats.MAX_DEPTH = 0
        my_stats.TIME_TAKEN = 0.0
        start = time.time()
        self.final_state = dfs_backtracking(self.csp, HEURISTIC, self.initial_state, self.variable_order)
        end = time.time()
        my_stats.TIME_TAKEN = end-start
        my_stats.assignment_seq.append(list(self.final_state.assignment))
        my_stats.variable_seq.append(list(self.variable_order))
        # print(my_stats.NO_OF_NODES)
        # print(sys.getsizeof(self.final_state))
        # print(my_stats.MAX_DEPTH)
        # print(end-start, "secs.")
        print("-------------------------------------------------")
        print("No. of nodes generated: ", my_stats.NO_OF_NODES)
        print("Time taken: ", my_stats.TIME_TAKEN, "secs.")
        # print("Max depth reached: ", my_stats.MAX_DEPTH)
        if self.final_state.is_assignment_complete():
            print("Final assignment for N1 to N"+str(self.final_state.no_of_laureates)+": ", self.final_state.assignment)
        else:
            print("No valid complete assignment possible")
        print("-------------------------------------------------")
        self.G1 = QWidget()
        self.G1_1_btns = []
        for idx in range(self.csp.no_of_laureates):
            self.G1_1_btns.append(QPushButton(self.G1))
            self.G1_1_btns[-1].setGeometry(10+idx*BTN_LENGTH, 100, BTN_LENGTH, 20)
            self.G1_1_btns[-1].show()
        self.G1_2_btns = []
        for idx in range(self.csp.no_of_laureates):
            self.G1_2_btns.append(QPushButton(self.G1))
            self.G1_2_btns[-1].setGeometry(10+idx*BTN_LENGTH, 125, BTN_LENGTH, 20)
            self.G1_2_btns[-1].show()
        self.G1_next_btn = QPushButton("Show assignment after creation of next 100 nodes", self.G1)
        self.G1_next_btn.setGeometry(75, 175, 400, 25)
        self.G1_next_btn.clicked.connect(self.next_move)
        self.G1_next_btn.show()
        self.G1_idx = 0
        complete_order = complete_variable_ordering(my_stats.variable_seq[self.G1_idx], self.csp.no_of_laureates)
        for idx in range(self.csp.no_of_laureates):
            self.G1_1_btns[idx].setText('N'+str(complete_order[idx]))
            if complete_order[idx]-1 in my_stats.variable_seq[self.G1_idx]:
                self.G1_2_btns[idx].setText(str(my_stats.assignment_seq[self.G1_idx][complete_order[idx]-1]))
                self.G1_1_btns[idx].setStyleSheet('color: Red')
                self.G1_2_btns[idx].setStyleSheet('color: Red')
            else:
                self.G1_2_btns[idx].setText(' ')
                self.G1_1_btns[idx].setStyleSheet('color: Black')
                self.G1_2_btns[idx].setStyleSheet('color: Black')
        self.G1_idx += 1
        if self.G1_idx == len(my_stats.assignment_seq):
            self.G1_status_label = QLabel(self.G1)
            self.G1_status_label.setGeometry(75, 225, 500, 25)
            if self.final_state.is_assignment_complete():
                self.G1_status_label.setText("SUCCESS: SOLUTION EXISTS. %d nodes generated. %.6f secs. taken"%(my_stats.NO_OF_NODES, my_stats.TIME_TAKEN))
                self.G1_status_label.setStyleSheet('color: Green')
            else:
                self.G1_status_label.setText("FAILURE: NO SOLUTION EXISTS. %d nodes generated. %.6f secs. taken"%(my_stats.NO_OF_NODES, my_stats.TIME_TAKEN))
                self.G1_status_label.setStyleSheet('color: Red')
            self.G1_status_label.show()
        self.G1_flag = True
        self.G1.setGeometry(10, 10, 1100, 400)
        self.G1.show()
        return
    def next_move(self):
        if self.G1_flag == False or self.G1_idx >= len(my_stats.assignment_seq):
            if self.G1_flag == True:
                self.G1_flag = False
                del my_stats.assignment_seq, my_stats.variable_seq, self.csp, self.initial_state, self.variable_order
            return
        complete_order = complete_variable_ordering(my_stats.variable_seq[self.G1_idx], self.csp.no_of_laureates)
        for idx in range(self.csp.no_of_laureates):
            self.G1_1_btns[idx].setText('N'+str(complete_order[idx]))
            if complete_order[idx]-1 in my_stats.variable_seq[self.G1_idx]:
                self.G1_2_btns[idx].setText(str(my_stats.assignment_seq[self.G1_idx][complete_order[idx]-1]))
                self.G1_1_btns[idx].setStyleSheet('color: Red')
                self.G1_2_btns[idx].setStyleSheet('color: Red')
            else:
                self.G1_2_btns[idx].setText(' ')
                self.G1_1_btns[idx].setStyleSheet('color: Black')
                self.G1_2_btns[idx].setStyleSheet('color: Black')
        if self.G1_idx == len(my_stats.assignment_seq)-1:
            self.G1_status_label = QLabel(self.G1)
            self.G1_status_label.setGeometry(75, 225, 500, 25)
            if self.final_state.is_assignment_complete():
                self.G1_status_label.setText("SUCCESS: SOLUTION EXISTS.  %d nodes generated. %.6f secs. taken"%(my_stats.NO_OF_NODES, my_stats.TIME_TAKEN))
                self.G1_status_label.setStyleSheet('color: Green')
            else:
                self.G1_status_label.setText("FAILURE: NO SOLUTION EXISTS.  %d nodes generated. %.6f secs. taken"%(my_stats.NO_OF_NODES, my_stats.TIME_TAKEN))
                self.G1_status_label.setStyleSheet('color: Red')
            self.G1_status_label.show()
        self.G1_idx += 1
        return
    def run_DFS_BT_AC3(self):
        global GROUP_CHOICES, LAUREATE_CHOICES, HEURISTIC, BTN_LENGTH
        if len(GROUP_CHOICES) == 0 or len(LAUREATE_CHOICES) == 0:
            return
        self.csp = CSP(GROUP_CHOICES, LAUREATE_CHOICES)
        my_stats.TIME_TAKEN = 0.0
        start = time.time()
        self.csp = AC3(self.csp)
        end = time.time()
        my_stats.TIME_TAKEN += (end-start)
        self.initial_state = State(self.csp.no_of_laureates)
        self.variable_order = []
        my_stats.NO_OF_NODES = 0
        my_stats.assignment_seq = []
        my_stats.variable_seq =[]
        my_stats.MAX_DEPTH = 0
        start = time.time()
        self.final_state = dfs_backtracking(self.csp, HEURISTIC, self.initial_state, self.variable_order)
        end = time.time()
        my_stats.TIME_TAKEN += (end-start)
        my_stats.assignment_seq.append(list(self.final_state.assignment))
        my_stats.variable_seq.append(list(self.variable_order))
        # print(my_stats.NO_OF_NODES)
        print("-------------------------------------------------")
        print("No. of nodes generated: ", my_stats.NO_OF_NODES)
        print("Time taken: ", my_stats.TIME_TAKEN, "secs.")
        # print("Max depth reached: ", my_stats.MAX_DEPTH)
        if self.final_state.is_assignment_complete():
            print("Final assignment for N1 to N"+str(self.final_state.no_of_laureates)+": ", self.final_state.assignment)
        else:
            print("No valid complete assignment possible")
        print("-------------------------------------------------")
        self.G1 = QWidget()
        self.G1_1_btns = []
        for idx in range(self.csp.no_of_laureates):
            self.G1_1_btns.append(QPushButton(self.G1))
            self.G1_1_btns[-1].setGeometry(10+idx*BTN_LENGTH, 100, BTN_LENGTH, 20)
            self.G1_1_btns[-1].show()
        self.G1_2_btns = []
        for idx in range(self.csp.no_of_laureates):
            self.G1_2_btns.append(QPushButton(self.G1))
            self.G1_2_btns[-1].setGeometry(10+idx*BTN_LENGTH, 125, BTN_LENGTH, 20)
            self.G1_2_btns[-1].show()
        self.G1_next_btn = QPushButton("Show assignment after creation of next 100 nodes", self.G1)
        self.G1_next_btn.setGeometry(75, 175, 400, 25)
        self.G1_next_btn.clicked.connect(self.next_move)
        self.G1_next_btn.show()
        self.G1_idx = 0
        complete_order = complete_variable_ordering(my_stats.variable_seq[self.G1_idx], self.csp.no_of_laureates)
        for idx in range(self.csp.no_of_laureates):
            self.G1_1_btns[idx].setText('N'+str(complete_order[idx]))
            if complete_order[idx]-1 in my_stats.variable_seq[self.G1_idx]:
                self.G1_2_btns[idx].setText(str(my_stats.assignment_seq[self.G1_idx][complete_order[idx]-1]))
                self.G1_1_btns[idx].setStyleSheet('color: Red')
                self.G1_2_btns[idx].setStyleSheet('color: Red')
            else:
                self.G1_2_btns[idx].setText(' ')
                self.G1_1_btns[idx].setStyleSheet('color: Black')
                self.G1_2_btns[idx].setStyleSheet('color: Black')
        self.G1_idx += 1
        if self.G1_idx == len(my_stats.assignment_seq):
            self.G1_status_label = QLabel(self.G1)
            self.G1_status_label.setGeometry(75, 225, 500, 25)
            if self.final_state.is_assignment_complete():
                self.G1_status_label.setText("SUCCESS: SOLUTION EXISTS.  %d nodes generated. %.6f secs. taken"%(my_stats.NO_OF_NODES, my_stats.TIME_TAKEN))
                self.G1_status_label.setStyleSheet('color: Green')
            else:
                self.G1_status_label.setText("FAILURE: NO SOLUTION EXISTS.  %d nodes generated. %.6f secs. taken"%(my_stats.NO_OF_NODES, my_stats.TIME_TAKEN))
                self.G1_status_label.setStyleSheet('color: Red')
            self.G1_status_label.show()
        self.G1_flag = True
        self.G1.setGeometry(10, 10, 1100, 400)
        self.G1.show()
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI_Layout()
    sys.exit(app.exec_())