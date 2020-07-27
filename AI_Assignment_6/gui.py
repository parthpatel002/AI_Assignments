"""
@author: 2016A7PS0150P (Patel Parth)
"""

from algo import *

import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox

INPUT_FILE = 'input1.txt'
QUERY_VARS = dict()
CONDITION_VARS = dict()
MARKOV_BLANKET_VAR = None

class GUI_Layout(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bayesian Network')
        self.init_ui()
        self.setGeometry(200, 200, 500, 250)
        self.show()
    def init_ui(self):
        self.input_file_label = QLabel("Select Input File:", self) 
        self.input_file_combo_box = QComboBox(self)
        for idx in range(1, 5):
            self.input_file_combo_box.addItem("input"+str(idx)+".txt")
        self.input_file_label.move(25, 50)
        self.input_file_label.setStyleSheet('color: #36af08')
        self.input_file_combo_box.move(150, 47)
        self.input_file_combo_box.setStyleSheet('color: #36af08')
        self.input_file_combo_box.activated[str].connect(self.select_input_file)
        self.inference_btn = QPushButton('Run Inference With Selected File', self)
        self.inference_btn.clicked.connect(self.run_inference)
        self.inference_btn.setStyleSheet('color: Blue')
        self.inference_btn.setGeometry(25, 100, 250, 20)
        self.inference_btn.show()
        self.note_label = QLabel("Note: Use input4.txt for specifying any other custom network", self)
        self.note_label.setStyleSheet('color: #fd5800')
        self.note_label.move(25, 150)
    def select_input_file(self, text):
        global INPUT_FILE
        INPUT_FILE = text
    def run_inference(self):
        global INPUT_FILE
        if INPUT_FILE not in os.listdir(os.getcwd()):
            print("File %s not present"%(INPUT_FILE))
            self.temporary_widget = QWidget()
            self.temporary_label = QLabel("File %s not present"%(INPUT_FILE), self.temporary_widget)
            self.temporary_label.move(10, 10)
            self.temporary_label.setStyleSheet('color: Red')
            self.temporary_widget.setGeometry(250, 250, 300, 100)
            self.temporary_widget.show()
        else:
            global QUERY_VARS, CONDITION_VARS, MARKOV_BLANKET_VAR
            QUERY_VARS = dict()
            CONDITION_VARS = dict()
            MARKOV_BLANKET_VAR = None
            self.bayesian_net = Bayesian_Network(INPUT_FILE)
            self.inference_widget = QWidget()
            self.query_label = QLabel("Query Variables", self.inference_widget)
            # self.query_label.setStyleSheet('color: #3fb906')
            self.query_label.setGeometry(125, 25, 200, 25)
            self.condition_label = QLabel("Condition Variables", self.inference_widget)
            # self.condition_label.setStyleSheet('color: #3fb906')
            self.condition_label.setGeometry(525, 25, 200, 25)
            self.query_var_positive_label = QLabel("Select +ve literal:", self.inference_widget)
            self.query_var_positive_combo_box = QComboBox(self.inference_widget)
            for var in self.bayesian_net.var_set:
                self.query_var_positive_combo_box.addItem(var)
            self.query_var_positive_label.setStyleSheet('color: Purple')
            self.query_var_positive_label.move(15, 65)
            self.query_var_positive_combo_box.setStyleSheet('color: Purple')
            self.query_var_positive_combo_box.move(125, 62)
            self.query_var_positive_combo_box.activated[str].connect(self.add_positive_query_var)
            self.query_var_negative_label = QLabel("Select -ve literal:", self.inference_widget)
            self.query_var_negative_combo_box = QComboBox(self.inference_widget)
            for var in self.bayesian_net.var_set:
                self.query_var_negative_combo_box.addItem(var)
            self.query_var_negative_label.setStyleSheet('color: Red')
            self.query_var_negative_label.move(180, 65)
            self.query_var_negative_combo_box.setStyleSheet('color: Red')
            self.query_var_negative_combo_box.move(285, 62)
            self.query_var_negative_combo_box.activated[str].connect(self.add_negative_query_var)
            self.remove_query_var_label = QLabel("Remove literal from query:", self.inference_widget)
            self.remove_query_var_combo_box = QComboBox(self.inference_widget)
            for var in self.bayesian_net.var_set:
                self.remove_query_var_combo_box.addItem(var)
            self.remove_query_var_label.move(15, 100)
            self.remove_query_var_combo_box.move(180, 97)
            self.remove_query_var_combo_box.activated[str].connect(self.remove_query_var)
            self.reset_query_vars = QPushButton("Reset query variables list to empty", self.inference_widget)
            self.reset_query_vars.clicked.connect(self.initialize_query_var_list_empty)
            # self.reset_query_vars.setStyleSheet('color: #fd5800')
            self.reset_query_vars.setGeometry(25, 125, 300, 20)
            self.reset_query_vars.show()
            self.condition_var_positive_label = QLabel("Select +ve literal:", self.inference_widget)
            self.condition_var_positive_combo_box = QComboBox(self.inference_widget)
            for var in self.bayesian_net.var_set:
                self.condition_var_positive_combo_box.addItem(var)
            self.condition_var_positive_label.setStyleSheet('color: Purple')
            self.condition_var_positive_label.move(415, 65)
            self.condition_var_positive_combo_box.setStyleSheet('color: Purple')
            self.condition_var_positive_combo_box.move(525,62)
            self.condition_var_positive_combo_box.activated[str].connect(self.add_positive_condition_var)
            self.condition_var_negative_label = QLabel("Select -ve literal:", self.inference_widget)
            self.condition_var_negative_combo_box = QComboBox(self.inference_widget)
            for var in self.bayesian_net.var_set:
                self.condition_var_negative_combo_box.addItem(var)
            self.condition_var_negative_label.setStyleSheet('color: Red')
            self.condition_var_negative_label.move(580, 65)
            self.condition_var_negative_combo_box.setStyleSheet('color: Red')
            self.condition_var_negative_combo_box.move(685, 62)
            self.condition_var_negative_combo_box.activated[str].connect(self.add_negative_condition_var)
            self.remove_condition_var_label = QLabel("Remove literal from conditional:", self.inference_widget)
            self.remove_condition_var_combo_box = QComboBox(self.inference_widget)
            for var in self.bayesian_net.var_set:
                self.remove_condition_var_combo_box.addItem(var)
            self.remove_condition_var_label.move(415, 100)
            self.remove_condition_var_combo_box.move(610, 97)
            self.remove_condition_var_combo_box.activated[str].connect(self.remove_condition_var)
            self.reset_condition_vars = QPushButton("Reset condition variables list to empty", self.inference_widget)
            self.reset_condition_vars.clicked.connect(self.initialize_cond_var_list_empty)
            # self.reset_condition_vars.setStyleSheet('color: #fd5800')
            self.reset_condition_vars.setGeometry(425, 125, 300, 20)
            self.reset_condition_vars.show()
            self.display_query_btn = QPushButton("Display Query: ", self.inference_widget)
            self.display_query_btn.clicked.connect(self.display_query)
            # self.display_query_btn.setStyleSheet('color: #f90468')
            self.display_query_btn.setGeometry(25, 175, 100, 20)
            self.display_query_btn.show()
            self.display_query_label = QLabel("----------------------------------------------------------------------------------------------------------------------------------", self.inference_widget)
            self.display_query_label.setStyleSheet('color: #f90468')
            self.display_query_label.setGeometry(130, 175, 500, 20)
            self.calculate_probability_btn = QPushButton("Compute Probability of displayed expression: ", self.inference_widget)
            self.calculate_probability_btn.clicked.connect(self.calculate_probability)
            # self.calculate_probability_btn.setStyleSheet('color: #3fb906')
            self.calculate_probability_btn.setGeometry(25, 225, 300, 20)
            self.calculate_probability_btn.show()
            self.calculate_probability_label = QLabel("----------------------------------------------------------------------------------------------------------------------------------------------", self.inference_widget)
            self.calculate_probability_label.setStyleSheet('color: #3fb906')
            self.calculate_probability_label.setGeometry(330, 225, 625, 20)
            self.markov_blanket_label = QLabel("Select variable for Markov Blanket Computation: ", self.inference_widget)
            self.markov_blanket_combo_box = QComboBox(self.inference_widget)
            for var in self.bayesian_net.var_set:
                self.markov_blanket_combo_box.addItem(var)
            # self.markov_blanket_label.setStyleSheet('color: #3d00fd')
            self.markov_blanket_label.setGeometry(25, 275, 300, 20)
            self.markov_blanket_combo_box.setStyleSheet('color: #3d00fd')
            self.markov_blanket_combo_box.move(330, 275)
            self.markov_blanket_combo_box.activated[str].connect(self.select_markov_blanket_variable)
            self.markov_blanket_btn = QPushButton("Compute Markov Blanket of Selected Variable: ", self.inference_widget)
            self.markov_blanket_btn.clicked.connect(self.calculate_markov_blanket)
            self.markov_blanket_btn.setGeometry(25, 325, 300, 20)
            self.markov_blanket_btn.show()
            self.markov_blanket_display_label = QLabel("-------------------------------------------------------------------------------------------------------------------------------------------------------------------", self.inference_widget)
            self.markov_blanket_display_label.setStyleSheet('color: #fa8902')
            self.markov_blanket_display_label.setGeometry(330, 325, 525, 20)
            self.note_label = QLabel("Note: Variable elimination algorithm is used prior to computing the probabilities, as just like Markov blanket, it helps in greatly reducing time complexity.", self.inference_widget)
            self.note_label.setStyleSheet('color: #fd5800')
            self.note_label.setGeometry(20, 375, 950, 20)
            self.inference_widget.setWindowTitle(INPUT_FILE)
            self.inference_widget.setGeometry(0, 0, 1000, 450)
            self.inference_widget.show()
            return
    def add_positive_query_var(self, text):
        global QUERY_VARS, CONDITION_VARS     
        if text in CONDITION_VARS.keys():
            self.extra_widget = QWidget()
            self.extra_label = QLabel("Cannot have same variable in both Q and C", self.extra_widget)
            self.extra_label.setStyleSheet('color: Red')
            self.extra_label.setGeometry(15, 15, 350, 20)
            self.extra_widget.setGeometry(100, 100, 400, 50)
            self.extra_widget.show()
            return
        if text not in QUERY_VARS and len(QUERY_VARS)==10:
            self.extra_widget = QWidget()
            self.extra_label = QLabel("Cannot have more than 10 variables in Q", self.extra_widget)
            self.extra_label.setStyleSheet('color: Red')
            self.extra_label.setGeometry(15, 15, 350, 20)
            self.extra_widget.setGeometry(100, 100, 400, 50)
            self.extra_widget.show()
            return
        QUERY_VARS[text] = 1
        return
    def add_negative_query_var(self, text):
        global QUERY_VARS, CONDITION_VARS
        if text in CONDITION_VARS.keys():
            self.extra_widget = QWidget()
            self.extra_label = QLabel("Cannot have same variable in both Q and C", self.extra_widget)
            self.extra_label.setStyleSheet('color: Red')
            self.extra_label.setGeometry(15, 15, 350, 20)
            self.extra_widget.setGeometry(100, 100, 400, 50)
            self.extra_widget.show()
            return
        if text not in QUERY_VARS and len(QUERY_VARS)==10:
            self.extra_widget = QWidget()
            self.extra_label = QLabel("Cannot have more than 10 variables in Q", self.extra_widget)
            self.extra_label.setStyleSheet('color: Red')
            self.extra_label.setGeometry(15, 15, 350, 20)
            self.extra_widget.setGeometry(100, 100, 400, 50)
            self.extra_widget.show()
            return
        QUERY_VARS[text] = 0
        return
    def add_positive_condition_var(self, text):
        global CONDITION_VARS, QUERY_VARS
        if text in QUERY_VARS.keys():
            self.extra_widget = QWidget()
            self.extra_label = QLabel("Cannot have same variable in both Q and C", self.extra_widget)
            self.extra_label.setStyleSheet('color: Red')
            self.extra_label.setGeometry(15, 15, 350, 20)
            self.extra_widget.setGeometry(100, 100, 400, 50)
            self.extra_widget.show()
            return
        if text not in CONDITION_VARS and len(CONDITION_VARS)==10:
            self.extra_widget = QWidget()
            self.extra_label = QLabel("Cannot have more than 10 variables in C", self.extra_widget)
            self.extra_label.setStyleSheet('color: Red')
            self.extra_label.setGeometry(15, 15, 350, 20)
            self.extra_widget.setGeometry(100, 100, 400, 50)
            self.extra_widget.show()
            return
        CONDITION_VARS[text] = 1
        return
    def add_negative_condition_var(self, text):
        global CONDITION_VARS, QUERY_VARS
        if text in QUERY_VARS.keys():
            self.extra_widget = QWidget()
            self.extra_label = QLabel("Cannot have same variable in both Q and C", self.extra_widget)
            self.extra_label.setStyleSheet('color: Red')
            self.extra_label.setGeometry(15, 15, 350, 20)
            self.extra_widget.setGeometry(100, 100, 400, 50)
            self.extra_widget.show()
            return
        if text not in CONDITION_VARS and len(CONDITION_VARS)==10:
            self.extra_widget = QWidget()
            self.extra_label = QLabel("Cannot have more than 10 variables in C", self.extra_widget)
            self.extra_label.setStyleSheet('color: Red')
            self.extra_label.setGeometry(15, 15, 350, 20)
            self.extra_widget.setGeometry(100, 100, 400, 50)
            self.extra_widget.show()
            return
        CONDITION_VARS[text] = 0
        return
    def display_query(self):
        global QUERY_VARS, CONDITION_VARS
        if len(QUERY_VARS) == 0:
            self.display_query_label.setText("INVALID QUERY: CHOOSE A QUERY VARIABLE")
            return
        display_str = "P("
        query_keys = []
        for key in QUERY_VARS.keys():
            query_keys.append(key)
        if QUERY_VARS[query_keys[0]] == 0:
            display_str += ('~'+query_keys[0])
        else:
            display_str += (query_keys[0])
        for key in query_keys[1:]:
            if QUERY_VARS[key] == 0:
                display_str += (',~'+key)
            else:
                display_str += (','+key)
        if len(CONDITION_VARS) == 0:
            display_str += ")"
            self.display_query_label.setText(display_str)
            return
        display_str += "|"
        condition_keys = []
        for key in CONDITION_VARS.keys():
            condition_keys.append(key)
        if CONDITION_VARS[condition_keys[0]] == 0:
            display_str += ('~'+condition_keys[0])
        else:
            display_str += (condition_keys[0])
        for key in condition_keys[1:]:
            if CONDITION_VARS[key] == 0:
                display_str += (',~'+key)
            else:
                display_str += (','+key)
        display_str += ")"
        self.display_query_label.setText(display_str)
        return
    def initialize_query_var_list_empty(self):
        global QUERY_VARS
        keys_list = []
        for key in QUERY_VARS.keys():
            keys_list.append(key)
        for key in keys_list:
            del QUERY_VARS[key]
        return
    def initialize_cond_var_list_empty(self):
        global CONDITION_VARS
        keys_list = []
        for key in CONDITION_VARS.keys():
            keys_list.append(key)
        for key in keys_list:
            del CONDITION_VARS[key]
        return
    def calculate_probability(self):
        global QUERY_VARS, CONDITION_VARS
        if len(QUERY_VARS) == 0:
            self.calculate_probability_label.setText("INVALID QUERY: CHOOSE A QUERY VARIABLE")
            return
        self.calculate_probability_label.setText(str(compute_probability(self.bayesian_net, QUERY_VARS, CONDITION_VARS)))
        return
    def select_markov_blanket_variable(self, text):
        global MARKOV_BLANKET_VAR
        MARKOV_BLANKET_VAR = text
        return
    def calculate_markov_blanket(self):
        global MARKOV_BLANKET_VAR 
        if MARKOV_BLANKET_VAR not in self.bayesian_net.var_set:
            self.markov_blanket_display_label.setText("CHOOSE A VALID VARIABLE")
            return
        markov_blanket = list(compute_markov_blanket(self.bayesian_net.graph, self.bayesian_net.rev_graph, MARKOV_BLANKET_VAR))
        self.markov_blanket_display_label.setText(str(markov_blanket))
        return
    def remove_query_var(self, text):
        global QUERY_VARS
        bool_val = (text in QUERY_VARS)
        if bool_val:
            del QUERY_VARS[text]
    def remove_condition_var(self, text):
        global CONDITION_VARS
        bool_val = (text in CONDITION_VARS)
        if bool_val:
            del CONDITION_VARS[text]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI_Layout()
    sys.exit(app.exec_())
