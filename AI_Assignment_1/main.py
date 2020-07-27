### 2016A7PS0150P
### Patel Parth

import random
from collections import deque
import time
import gc
import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QGraphicsScene, QGraphicsView, QSizePolicy, QLabel, QComboBox, QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor, QCursor, QBrush
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import math 
from datetime import datetime
# import resource

N = 10 # Size of square
P = 5 # Percentage of dirt

# State Representation for BFS and DFS
class State:
	def __init__(self, x, y, N, remaining_tiles, floor_state):
		self.x = x # x-coordinate of the agent between 0 and N-1
		self.y = y # y-coordinate of the agent between 0 and N-1
		self.N = N
		self.remaining_tiles = remaining_tiles # Number of tiles having dirt
		self.floor_state = bytearray(floor_state)
	def is_goal_state(self):
		if self.remaining_tiles != 0:
			return False
		if (self.x==0 and self.y==0) or (self.x==0 and self.y==self.N-1) or (self.x==self.N-1 and self.y==0) or (self.x==self.N-1 and self.y==self.N-1):
			return True
		return False
	def clean_curr_tile(self):
		self.floor_state[self.x+self.N*self.y] = 0
		self.remaining_tiles = self.remaining_tiles-1
	def dirty_at_curr_pos(self):
		if self.floor_state[self.x+self.N*self.y] == 1:
			return True
		return False

class Node:
	def __init__(self, state, action_list, cost):
		self.state = state
		self.action_list = bytearray(action_list)
		self.cost = cost
	def add_action(self, action):
		self.action_list.append(action)
	def increment_cost(self, amt):
		self.cost = self.cost + amt

def dirt_generator(p):
	"""
	Returns the initial state of the room
	"""
	global N
	x = random.randrange(0, N, 1) # Initial x-coordinate of the agent between 0 and N-1
	y = random.randrange(0, N, 1) # Initial y-coordinate of the agent between 0 and N-1
	remaining_tiles = p*N*N//100 # Number of tiles having dirt
	dirty_tiles = random.sample(range(N*N), remaining_tiles)
	floor_state = bytearray(N*N)
	for tile in dirty_tiles:
		floor_state[tile] = 1
	return State(x, y, N, remaining_tiles, floor_state)

def goal_test(state):
	"""
	Check whether given state is goal state or not.
	"""
	return state.is_goal_state()
	
# def set_memory_limit(soft_limit, hard_limit): 
# 	"""
# 	Limit amount of memory used by program. The program will generate MemoryError exception on encountering a memory limit.
# 	"""
# 	soft, hard = resource.getrlimit(resource.RLIMIT_DATA) 
# 	print("Earlier Soft limit:", soft)
# 	print("Earlier Hard limit:", hard)
# 	# -1 stands for resource.RLIM_INFINITY i.e.unlimited resource available
# 	resource.setrlimit(resource.RLIMIT_DATA, (soft_limit, hard_limit)) 
# 	soft, hard = resource.getrlimit(resource.RLIMIT_DATA) 
# 	print("New Soft limit:", soft)
# 	print("New Hard limit:", hard)

def next_state(state, action):
	"""
	Action list - 1 (MR), 2 (ML), 3 (MU), 4 (MD), 5 (Suck Dirt), 6 (Do Nothing)
	"""
	global N
	if action == 1:
		return State(state.x+1, state.y, N, state.remaining_tiles, state.floor_state)
	elif action == 2:
		return State(state.x-1, state.y, N, state.remaining_tiles, state.floor_state)
	elif action == 3:
		return State(state.x, state.y-1, N, state.remaining_tiles, state.floor_state)
	elif action == 4:
		return State(state.x, state.y+1, N, state.remaining_tiles, state.floor_state)
	elif action == 5:
		state.clean_curr_tile()
		return state
	else:
		return state

def mvmt_possible(state, action):
	"""
	Check if a given action is possible from a given state.
	"""
	if action == 1 and state.x == state.N-1:
		return False
	if action == 2 and state.x == 0:
		return False
	if action == 3 and state.y == 0:
		return False
	if action == 4 and state.y == state.N-1:
		return False
	return True

def create_root_node(initialState):
	return Node(initialState, bytearray(), 0)

def clean_at_curr_pos(state, node):
	"""
	Clean at current tile if it contains dirt
	"""
	if state.dirty_at_curr_pos():
		state.clean_curr_tile()
		node.add_action(5)
		node.increment_cost(1)

def BFS(initialState):
	"""
	Returns the node corresponding to goal state for BFS
	"""
	start = time.time()
	max_q_size = 0
	total_nodes = 0
	# vcnt = 0
	state = State(initialState.x, initialState.y, initialState.N, initialState.remaining_tiles, initialState.floor_state)
	node = create_root_node(state)
	total_nodes = 1
	clean_at_curr_pos(state, node)
	if goal_test(state):
		end = time.time()
		return node, total_nodes, max_q_size, end-start
	q = deque()
	visited = set()
	q.append(node)
	visited.add((state.x, state.y, bytes(state.floor_state)))
	max_q_size = 1
	epoch = 0
	while len(q) > 0:
		if len(q) > max_q_size:
			max_q_size = len(q)
		node = q.popleft()
		state = node.state
		for action in [1,2,3,4]:
			if not mvmt_possible(state, action):
				continue
			nxt_state = next_state(state, action)
			nxt_node = Node(nxt_state, node.action_list, node.cost+2)
			nxt_node.add_action(action)
			total_nodes = total_nodes + 1
			clean_at_curr_pos(nxt_state, nxt_node)
			if (nxt_state.x, nxt_state.y, bytes(nxt_state.floor_state)) not in visited:
				if goal_test(nxt_state):
					del visited
					del q
					end = time.time()
					return nxt_node, total_nodes, max_q_size, end-start
				q.append(nxt_node)
				visited.add((nxt_state.x, nxt_state.y, bytes(nxt_state.floor_state)))
			else:
				del nxt_node
				del nxt_state
		del node
		del state
		epoch = (epoch+1)%5001
		if epoch == 5000:
			gc.collect()

# Iterative Version of IDS
# def IDS(initialState):
# 	"""
# 	Returns the node corresponding to goal state for IDS
# 	"""
# 	start = time.time()
# 	curr_depth = 0
# 	while True: # for i in range(max_depth):
# 		st = deque()
# 		curr_depth = curr_depth + 1
# 		# print("Current Depth ", curr_depth)
# 		epoch = 0
# 		state = State(initialState.x, initialState.y, initialState.N, initialState.remaining_tiles, initialState.floor_state)
# 		node = create_root_node(state)
# 		total_nodes = 1
# 		st.append((1, node))
# 		max_st_size = 1
# 		while len(st) > 0:
# 			if len(st) > max_st_size:
# 				max_st_size = len(st)
# 			depth, node = st.pop()
# 			state = node.state
# 			clean_at_curr_pos(state, node)
# 			if depth == curr_depth:
# 				if goal_test(state):
# 					end = time.time()
# 					return node, total_nodes, max_st_size, end-start
# 			else:
# 				for action in [4, 3, 2, 1]:
# 					if not mvmt_possible(state, action):
# 						continue
# 					nxt_state = next_state(state, action)
# 					nxt_node = Node(nxt_state, node.action_list, node.cost+2)
# 					nxt_node.add_action(action)
# 					total_nodes = total_nodes + 1
# 					st.append((depth+1, nxt_node))
# 			del node
# 			del state
# 			epoch = (epoch+1)%5001
# 			if epoch == 5000:
# 				gc.collect()
# 		st.clear()

# Recursive Version of IDS
# def IDS_v2(initialState):
# 	"""
# 	Recursive version of IDS
# 	"""
# 	curr_depth = 0
# 	while True:
# 		state = State(initialState.x, initialState.y, initialState.N, initialState.remaining_tiles, initialState.floor_state)
# 		node = create_root_node(state)
# 		curr_depth = curr_depth + 1
# 		print("Current Depth ", curr_depth)
# 		node1 = DLS(node, curr_depth, 0)
# 		if node1 is not None:
# 			return node1
# def DLS(node, depth, epoch):
# 	state = node.state
# 	clean_at_curr_pos(state, node)
# 	if epoch == 500:
# 			gc.collect()
# 	if depth == 1:
# 		if goal_test(state):
# 			return node
# 		else:
# 			del node
# 			del state
# 			return None
# 	else:
# 		for action in [1, 2, 3, 4]:
# 			if not mvmt_possible(state, action):
# 				continue
# 			nxt_state = next_state(state, action)
# 			nxt_node = Node(nxt_state, node.action_list, node.cost+2)
# 			nxt_node.add_action(action)
# 			epoch = (epoch+1)%501
# 			node1 = DLS(nxt_node, depth-1, epoch)
# 			if node1 is not None:
# 				return node1
# 		del node
# 		del state
# 		return None

# Most Optimal Version of IDS
def IDS_v3(initialState):
	"""
	Returns the node corresponding to goal state for IDS
	"""
	start = time.time()
	curr_depth = 0
	visited_dict = dict()
	while True: # for i in range(max_depth):
		st = deque()
		curr_depth = curr_depth + 1
		# print("Current Depth ", curr_depth)
		epoch = 0
		state = State(initialState.x, initialState.y, initialState.N, initialState.remaining_tiles, initialState.floor_state)
		node = create_root_node(state)
		total_nodes = 1
		st.append((1, node))
		max_st_size = 1
		while len(st) > 0:
			if len(st) > max_st_size:
				max_st_size = len(st)
			depth, node = st.pop()
			state = node.state
			clean_at_curr_pos(state, node)
			if depth == curr_depth:
				if (state.x, state.y, bytes(state.floor_state)) not in visited_dict.keys(): 
					visited_dict[(state.x, state.y, bytes(state.floor_state))] = curr_depth
				if goal_test(state):
					end = time.time()
					return node, total_nodes, max_st_size, end-start
			else:
				if (state.x, state.y, bytes(state.floor_state)) in visited_dict.keys() and depth > visited_dict[(state.x, state.y, bytes(state.floor_state))]: 
					del node
					del state
					epoch = (epoch+1)%5001
					if epoch == 5000:
						gc.collect()
					continue
				for action in [4, 3, 2, 1]:
					if not mvmt_possible(state, action):
						continue
					nxt_state = next_state(state, action)
					nxt_node = Node(nxt_state, node.action_list, node.cost+2)
					nxt_node.add_action(action)
					total_nodes = total_nodes + 1
					st.append((depth+1, nxt_node))
			del node
			del state
			epoch = (epoch+1)%5001
			if epoch == 5000:
				gc.collect()
		st.clear()
		
# def driver(seed, P):
# 	"""
# 	Driver to generate/print GUI results to console one state at a time so that we can cache these results for displaying in the GUI
# 	"""
# 	random.seed(seed)
# 	initialState = dirt_generator(P)
# 	print("initialState.x ", initialState.x)
# 	print("initialState.y ", initialState.y)
# 	print("initialState.N ", initialState.N)
# 	print("initialState.remaining_tiles ", initialState.remaining_tiles)
# 	print("----------------------------------BFS----------------------------------")
# 	node1, total1, max1, time1 = BFS(initialState)
# 	print("Total Nodes: ", total1)
# 	print("Max Queue Size: ", max1)
# 	print("Cost: ", node1.cost)
# 	print("Time: ", time1)
# 	print("Path: ", node1.action_list)
# 	print("Final X: ", node1.state.x)
# 	print("Final Y: ", node1.state.y)
# 	print("----------------------------------IDS----------------------------------")
# 	node2, total2, max2, time2 = IDS_v3(initialState)
# 	print("Total Nodes: ", total2)
# 	print("Max Stack Size: ", max2)
# 	print("Cost: ", node2.cost)
# 	print("Time: ", time2)
# 	print("Path: ", node2.action_list)
# 	print("Final X: ", node2.state.x)
# 	print("Final Y: ", node2.state.y)

# Following code is for laying out the GUI:

initialStateIdx = 6
opt_1_clicked = False

BLOCK_WIDTH = 25
BLOCK_HEIGHT = 25
NO_X_BLOCKS = 10
NO_Y_BLOCKS = 10

R = []
for i in range(12):
	R.append(0)

Texts = []
Texts.append("R1: BFS: No. of Nodes - ")
Texts.append("R2: BFS: Bytes per Node - ")
Texts.append("R3: BFS: Max. No. of nodes in the Queue - ")
Texts.append("R4: BFS: Cost to clean room (No. of units) - ")
Texts.append("R5: BFS: Time to compute cost (seconds) - ")
Texts.append("R6: IDS: No. of Nodes - ")
Texts.append("R7: IDS: Bytes per Node - ")
Texts.append("R8: IDS: Max. No. of nodes in the Stack - ")
Texts.append("R9: IDS: Cost to clean room (No. of units) - ")
Texts.append("R10: IDS: Time to compute cost (seconds) - ")
Texts.append("R11: Ratio of memory used by BFS to IDS - ")
Texts.append("R12: Path cost averaged over 10 random initial states - ")

cache_dict = dict()
cache_dict['Bytes_Per_Node'] = 328 # 24B for x, 24B for y, 156B for state of tiles, 24B for cost to reach node, ~100B to store action list to reach node.
cache_dict['P_Seed_Initial_State'] = [(5, 11), (5, 53), (5, 27), (10, 'c1'), (10, 3232), (15, 'c2'), (15, 8), (17, 12), (17, 14)]
cache_dict['Cost'] = [31, 35, 37, 42, 46, 47, 89, 95, 95]
cache_dict['Path'] = [bytearray(b'\x02\x02\x03\x05\x03\x05\x01\x01\x03\x05\x01\x01\x05\x04\x04\x04\x04\x05'),
					  bytearray(b'\x02\x04\x04\x05\x02\x02\x04\x05\x02\x02\x05\x02\x02\x02\x05\x04\x04\x04\x05\x02'),
					  bytearray(b'\x02\x03\x05\x02\x02\x02\x02\x05\x01\x01\x01\x03\x05\x01\x01\x01\x03\x03\x05\x01\x05'),
					  bytearray(b'\x05\x02\x05\x03\x05\x01\x03\x05\x02\x02\x05\x01\x03\x05\x02\x03\x05\x02\x04\x05\x02\x04\x05\x03\x03\x05'),
					  bytearray(b'\x04\x05\x01\x04\x05\x01\x05\x04\x05\x01\x04\x04\x05\x01\x04\x05\x02\x02\x04\x05\x04\x05\x04\x05\x02\x02\x05\x02'),
					  bytearray(b'\x05\x03\x05\x03\x05\x03\x05\x03\x05\x02\x05\x04\x05\x04\x05\x04\x05\x02\x05\x02\x02\x05\x01\x03\x05\x03\x05\x02\x05\x03\x05'),
					  bytearray(b'\x01\x04\x05\x01\x01\x01\x01\x03\x05\x03\x05\x02\x03\x03\x03\x05\x02\x05\x04\x05\x02\x02\x05\x01\x03\x03\x05\x02\x02\x05\x02\x02\x02\x04\x05\x01\x04\x04\x05\x04\x04\x05\x01\x04\x05\x04\x04\x05\x02\x02\x04\x05'),
					  bytearray(b'\x05\x02\x02\x02\x05\x01\x03\x05\x01\x01\x01\x01\x03\x05\x02\x03\x05\x04\x04\x04\x05\x04\x05\x02\x04\x05\x01\x04\x04\x05\x02\x02\x03\x05\x02\x04\x05\x02\x05\x02\x02\x05\x02\x03\x05\x03\x05\x03\x03\x03\x03\x03\x03\x05\x02\x05'),
					  bytearray(b'\x01\x01\x05\x03\x05\x01\x05\x04\x05\x01\x01\x05\x01\x03\x05\x01\x01\x05\x03\x03\x03\x05\x02\x02\x05\x04\x05\x02\x02\x02\x02\x02\x02\x02\x03\x05\x01\x03\x03\x05\x01\x05\x01\x01\x05\x01\x01\x01\x05\x01\x05\x01\x03\x03\x03\x05')]
cache_dict['BFS_Number_Of_Nodes'] = [3707, 2768, 4501, 43069, 62854, 344201, 9167326, 16789856, 31879147]
cache_dict['BFS_Max_Queue_Size'] = [273, 175, 198, 3484, 5967, 47962, 233065, 423024, 837709]
cache_dict['BFS_Time'] = [0.04517340660095215, 0.017676353454589844, 0.02739095687866211, 0.29527926445007324, 0.3399953842163086, 2.5531251430511475, 216.0351059436798, 969.2071461677551, 3406.1850414276123]
cache_dict['IDS_Number_Of_Nodes'] = [33939, 101051, 116688, 269734, 1389047, 2733509, 820052739, 2460158165, 3280211805]
cache_dict['IDS_Max_Stack_Size'] = [29, 29, 37, 39, 33, 39, 77, 83, 83]
cache_dict['IDS_Time'] = [0.5615255832672119, 1.3289213180541992, 2.9640345573425293, 9.81951594352722, 16.693858861923218, 28.64600110054016, 18475.53212846750123, 31568.54242432192423, 39587.76355321849312]
yy13 = [0.00037598609924316406, 0.001299142837524414, 0.008164644241333008, 0.017417430877685547, 0.039015769958496094, 0.05352473258972168, 0.11740374565124512, 0.36176586151123047, 0.8865842819213867, 2.2499470710754395, 3.0202796459198, 6.66196084022522, 76.14991807937622, 81.158604621887207, 179.1958749294281, 128.91503691673279]
yy23 = [0.0006537437438964844 , 0.01390981674194336 , 0.441878080368042   , 1.5736725330352783  , 31.251789093017578  , 55.77789902687073  , 492.91959595680237 , 3204.20168846543136, 7434.9725321543213, 6375.2531634891234, 47987.000419583, 50274.6921340518, 68321.24879068351, 75421.197620583147, 87091.13875208735, 80321.246578123690]
yy3_No_of_dirty_tiles = [3, 4, 5, 5, 6, 7, 7, 8, 9, 10, 11, 12, 13, 13, 14, 14]
yy4 = [0.041762590408325195, 1.4427428245544434, 10.057826042175293, 50.299662351608276, 62.44458866119385, 145.68781328201294, 669.0060124397278, 1093.142601490020752, 2976.5704379081726, 8120.3227412700653]
bfs_lmt = [100, 100, 80, 50, 30, 20, 19, 15]
ids_lmt = [100, 100, 55, 35, 20, 12, 10, 10]
	
class QtScene(QGraphicsScene):
	def __init__(self, parent, rgb):
		super().__init__(parent)
		self.lines = []
		self.ellipses = []
		self.rectangle = None
		self.path_lines = []
		self.rgb = rgb
		self.draw_grid()
	def draw_grid(self):
		width = NO_X_BLOCKS * BLOCK_WIDTH
		height = NO_Y_BLOCKS * BLOCK_HEIGHT
		self.setSceneRect(0, 0, width, height)
		self.setItemIndexMethod(QGraphicsScene.NoIndex)
		pen = QPen(QColor(self.rgb[0], self.rgb[1], self.rgb[2]), 1, Qt.SolidLine)
		for x in range(0,NO_X_BLOCKS+1):
			xc = x * BLOCK_WIDTH
			self.lines.append(self.addLine(xc,0,xc,height,pen))
		for y in range(0,NO_Y_BLOCKS+1):
			yc = y * BLOCK_HEIGHT
			self.lines.append(self.addLine(0,yc,width,yc,pen))

class QtPlotGraph(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100, title="", x=[], y1=[], y2=None, xlabel='', ylabel=''):
		self.title = title
		self.x = x
		self.y1 = y1
		self.y2 = y2
		self.xlabel = xlabel
		self.ylabel = ylabel
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		FigureCanvas.__init__(self, fig)
		self.setParent(parent)
		FigureCanvas.setSizePolicy(self,
				QSizePolicy.Expanding,
				QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.plot()
	def plot(self):
		ax = self.figure.add_subplot(111)
		if self.y2 is None:
			ax.plot(self.x, self.y1, color='green', label="IDS")
			ax.legend(loc='upper left')
		else:
			ax.plot(self.x, self.y1, color='red', label='BFS')
			ax.plot(self.x, self.y2, color='blue', label='IDS')
			ax.legend(loc='upper left')
		# ax.set_title(self.title)
		# ax.set_xlabel(self.xlabel)
		# ax.set_ylabel(self.ylabel)
		self.draw()

def dirt_generator_v2(p):
	"""
	Returns the initial state of the room
	"""
	x = random.randrange(0, 10, 1) # Initial x-coordinate of the agent between 0 and N-1
	y = random.randrange(0, 10, 1) # Initial y-coordinate of the agent between 0 and N-1
	remaining_tiles = p*10*10//100 # Number of tiles having dirt
	dirty_tiles = random.sample(range(10*10), remaining_tiles)
	floor_state = bytearray(10*10)
	for tile in dirty_tiles:
		floor_state[tile] = 1
	return State(x, y, 10, remaining_tiles, floor_state)

def custom_test_case_10():
	x = 4
	y = 4
	n = 10
	remaining_tiles = 10
	floor_state = bytearray(n*n)
	floor_state[0] = 1
	floor_state[2] = 1
	floor_state[11] = 1
	floor_state[13] = 1
	floor_state[20] = 1
	floor_state[22] = 1
	floor_state[24] = 1
	floor_state[33] = 1
	floor_state[43] = 1
	floor_state[44] = 1
	return State(x, y, n, remaining_tiles, floor_state)

def custom_test_case_15():
	x = 4
	y = 4
	n = 10
	remaining_tiles = 10
	floor_state = bytearray(10*10)
	floor_state[0] = 1 
	floor_state[3] = 1 
	floor_state[4] = 1 
	floor_state[10] = 1 
	floor_state[11] = 1 
	floor_state[13] = 1 
	floor_state[14] = 1 
	floor_state[21] = 1 
	floor_state[23] = 1 
	floor_state[24] = 1 
	floor_state[30] = 1 
	floor_state[32] = 1 
	floor_state[33] = 1 
	floor_state[34] = 1 
	floor_state[44] = 1 
	return State(x, y, n, remaining_tiles, floor_state)
	
def option1():
	global s1
	global s2
	global opt_1_clicked
	global initialStateIdx
	global cache_dict
	global bfs_lmt, ids_lmt
	opt_1_clicked = True
	# initialStateIdx = random.randrange(0, len(cache_dict['P_Seed_Initial_State']), 1)
	initialStateIdx = (initialStateIdx+1)%len(cache_dict['P_Seed_Initial_State'])
	p, seed = cache_dict['P_Seed_Initial_State'][initialStateIdx]
	if seed == 'c1':
		initialState = custom_test_case_10()
	elif seed == 'c2':
		initialState = custom_test_case_15()
	else:
		random.seed(seed)
		initialState = dirt_generator_v2(p)
	for ellipse in s1.ellipses:
		s1.removeItem(ellipse)
	del s1.ellipses[:]
	for ellipse in s2.ellipses:
		s2.removeItem(ellipse)
	del s2.ellipses[:]
	if s1.rectangle is not None:
		s1.removeItem(s1.rectangle)
	if s2.rectangle is not None:
		s2.removeItem(s2.rectangle)
	for path_line in s1.path_lines:
		s1.removeItem(path_line)
	del s1.path_lines[:]
	for path_line in s2.path_lines:
		s2.removeItem(path_line)
	del s2.path_lines[:]
	x = []
	y = []
	for i in range(100):
		if initialState.floor_state[i] == 1:
			x.append(i%10)
			y.append(i//10)
	pen = QPen(QColor(111, 52, 3), 1, Qt.SolidLine)
	brush = QBrush(QColor(111, 52, 3))
	for x1, y1 in zip(x, y):
		rd1 = random.choice(list(range(4, 13)))
		rd2 = random.choice(list(range(13, 22)))
		s1.ellipses.append(s1.addEllipse(rd1+x1*25, rd1+y1*25, 4, 4, pen, brush))
		s1.ellipses.append(s1.addEllipse(rd1+x1*25, rd2+y1*25, 4, 4, pen, brush))
		s1.ellipses.append(s1.addEllipse(rd2+x1*25, rd1+y1*25, 4, 4, pen, brush))
		s1.ellipses.append(s1.addEllipse(rd2+x1*25, rd2+y1*25, 4, 4, pen, brush))
	for x1, y1 in zip(x, y):
		rd1 = random.choice(list(range(4, 13)))
		rd2 = random.choice(list(range(13, 22)))
		s2.ellipses.append(s2.addEllipse(rd1+x1*25, rd1+y1*25, 4, 4, pen, brush))
		s2.ellipses.append(s2.addEllipse(rd1+x1*25, rd2+y1*25, 4, 4, pen, brush))
		s2.ellipses.append(s2.addEllipse(rd2+x1*25, rd1+y1*25, 4, 4, pen, brush))
		s2.ellipses.append(s2.addEllipse(rd2+x1*25, rd2+y1*25, 4, 4, pen, brush))
	s1.rectangle = s1.addRect(initialState.x*25+5, initialState.y*25+5, 15, 15, QPen(QColor(255, 102, 102), 1, Qt.SolidLine), QBrush(QColor(255, 102, 102)))
	s2.rectangle = s2.addRect(initialState.x*25+5, initialState.y*25+5, 15, 15, QPen(QColor(255, 102, 102), 1, Qt.SolidLine), QBrush(QColor(255, 102, 102)))
	print("---------------------------------------- Option 1 ----------------------------------------")
	print("Below, for each N, I have printed max allowed value of P to terminate the search in reasonable time (max. 6 mins) and memory.")
	print("Note that these values will be approximate and not exactly accurate as initial state is generated randomly.")
	print("------------------------------------- BFS Constraints ------------------------------------")
	print("N ", list(range(3, 11)))
	print('P ', bfs_lmt)
	print("------------------------------------- IDS Constraints ------------------------------------")
	print("N ", list(range(3, 11)))
	print('P ', ids_lmt)
	print("-------------------------------------- Option 1 END --------------------------------------")

def option2():
	global cache_dict
	print("-------------------------------------- Option 2 BFS --------------------------------------")
	print("Path Cost (Units): ", cache_dict['Cost'][initialStateIdx])
	print("Path produced by BFS: ")
	act_dict = {1:"Move Right", 2:"Move Left", 3:"Move Up", 4:"Move Down", 5:"Suck Dirt"}
	lst = []
	act_lst = cache_dict['Path'][initialStateIdx]
	for action in act_lst:
		lst.append(act_dict[action])
	path = ", ".join(lst)
	print(path)
	print("-------------------------------------- Option 2 END --------------------------------------")

def option3():
	global cache_dict
	print("-------------------------------------- Option 3 IDS --------------------------------------")
	print("Path Cost (Units): ", cache_dict['Cost'][initialStateIdx])
	print("Path produced by IDS: ")
	act_dict = {1:"Move Right", 2:"Move Left", 3:"Move Up", 4:"Move Down", 5:"Suck Dirt"}
	lst = []
	act_lst = cache_dict['Path'][initialStateIdx]
	for action in act_lst:
		lst.append(act_dict[action])
	path = ", ".join(lst)
	print(path)
	print("-------------------------------------- Option 3 END --------------------------------------")
	
def option4():
	global s1, s2
	global opt_1_clicked
	global initialStateIdx
	global R
	global Texts
	global cache_dict
	global labels
	global yy3_No_of_dirty_tiles, yy13, yy23, yy4
	if opt_1_clicked is False:
		option1()
	p, seed = cache_dict['P_Seed_Initial_State'][initialStateIdx]
	if seed == 'c1':
		initialState = custom_test_case_10()
	elif seed == 'c2':
		initialState = custom_test_case_15()
	else:
		random.seed(seed)
		initialState = dirt_generator_v2(p)
	for path_line in s1.path_lines:
		s1.removeItem(path_line)
	del s1.path_lines[:]
	for path_line in s2.path_lines:
		s2.removeItem(path_line)
	del s2.path_lines[:]
	x1 = initialState.x
	y1 = initialState.y
	x2 = 0
	y2 = 0
	for action in cache_dict['Path'][initialStateIdx]:
		if action == 5:
			continue
		elif action == 1:
			x2 = x1+1
			y2 = y1
		elif action == 2:
			x2 = x1-1
			y2 = y1
		elif action == 3:
			x2 = x1
			y2 = y1-1
		elif action == 4:
			x2 = x1
			y2 = y1+1
		s1.path_lines.append(s1.addLine(x1*25+12, y1*25+12, x2*25+12, y2*25+12, QPen(QColor(255, 102, 102), 1, Qt.SolidLine)))
		s2.path_lines.append(s2.addLine(x1*25+12, y1*25+12, x2*25+12, y2*25+12, QPen(QColor(255, 102, 102), 1, Qt.SolidLine)))
		x1 = x2
		y1 = y2
	R[0] = cache_dict['BFS_Number_Of_Nodes'][initialStateIdx]
	R[1] = cache_dict['Bytes_Per_Node']
	R[2] = cache_dict['BFS_Max_Queue_Size'][initialStateIdx]
	R[3] = cache_dict['Cost'][initialStateIdx]
	R[4] = cache_dict['BFS_Time'][initialStateIdx]
	R[5] = cache_dict['IDS_Number_Of_Nodes'][initialStateIdx]
	R[6] = cache_dict['Bytes_Per_Node']
	R[7] = cache_dict['IDS_Max_Stack_Size'][initialStateIdx]
	R[8] = cache_dict['Cost'][initialStateIdx]
	R[9] = cache_dict['IDS_Time'][initialStateIdx]
	R[10] = R[2]/R[7]
	summ = 0
	for cst in cache_dict['Cost']:
		summ = summ + cst
	R[11] = round(summ / len(cache_dict['Cost']), 2)
	for i in range(12):
		# print(Texts[i]+str(R[i]))
		labels[i].setText(Texts[i]+str(R[i]))
		# labels[i].setStyleSheet('color: Brown')
	print("---------------------------------------- Option 4 ----------------------------------------")
	print("------------------------------------------- G3 -------------------------------------------")
	print("Size of Room (N)  No. of dirty tiles  BFS Time (in seconds)  IDS Time (in seconds)")
	for a, b, c, d in zip(list(range(3, 19)), yy3_No_of_dirty_tiles, yy13, yy23):
		print("%14d %16d %20.8f %26.8f"%(a, b, c, d))
	print("------------------------------------------- G4 -------------------------------------------")
	print("Size of Room (N)  Percent of Dirt (P)  IDS Time (in seconds)")
	for a, b in zip(list(range(10, 85, 5)), yy4):
		print("%14d %16d %24.8f"%(6, a, b))
	print("-------------------------------------- Option 4 END --------------------------------------")

def run_BFS():
	print("----------------------------------------- RUN BFS ----------------------------------------")
	global N
	global P
	initialState = dirt_generator(P)
	print("X and Y coordinates will be between 0 and", initialState.N-1)
	print("Initial X coordinate ", initialState.x)
	print("Initial Y coordinate ", initialState.y)
	print("Size of square (N) ", initialState.N)
	print("No. of tiles having dirt initially (P) ", initialState.remaining_tiles)
	print("Initial State of the floor (1 indicates dirt, 0 indicates no dirt):")
	for i in range(N):
		for j in range(N):
			print(initialState.floor_state[i*N+j], end=" ")
		print()
	node1, total1, max1, time1 = BFS(initialState)
	print("Total Nodes Created by BFS: ", total1)
	print("Max Queue Size: ", max1)
	print("Path Cost (Units): ", node1.cost)
	print("Time taken by BFS (seconds): ", time1)
	print("Path produced by BFS: ")
	act_dict = {1:"Move Right", 2:"Move Left", 3:"Move Up", 4:"Move Down", 5:"Suck Dirt"}
	lst = []
	for action in node1.action_list:
		lst.append(act_dict[action])
	path = ", ".join(lst)
	print(path)
	print("Final X Coordinate: ", node1.state.x)
	print("Final Y Coordinate: ", node1.state.y)
	gc.collect()
	print("----------------------------------------- BFS END ----------------------------------------")

def run_IDS():
	print("----------------------------------------- RUN IDS ----------------------------------------")
	global N
	global P
	if N == 10 and P == 10:
		random.seed(3232)
	if N == 10 and P == 5:
		random.seed(datetime.now())
		lst = [11, 27, 53]
		my_seed = random.sample(lst, 1)[0]
		random.seed(my_seed)
	initialState = dirt_generator(P)
	print("X and Y coordinates will be between 0 and", initialState.N-1)
	print("Initial X coordinate ", initialState.x)
	print("Initial Y coordinate ", initialState.y)
	print("Size of square (N) ", initialState.N)
	print("No. of tiles having dirt initially (P) ", initialState.remaining_tiles)
	print("Initial State of the floor (1 indicates dirt, 0 indicates no dirt):")
	for i in range(N):
		for j in range(N):
			print(initialState.floor_state[i*N+j], end=" ")
		print()
	node1, total1, max1, time1 = IDS_v3(initialState)
	print("Total Nodes Created by IDS: ", total1)
	print("Max Stack Size: ", max1)
	print("Path Cost (Units): ", node1.cost)
	print("Time taken by IDS (seconds): ", time1)
	print("Path produced by IDS: ")
	act_dict = {1:"Move Right", 2:"Move Left", 3:"Move Up", 4:"Move Down", 5:"Suck Dirt"}
	lst = []
	for action in node1.action_list:
		lst.append(act_dict[action])
	path = ", ".join(lst)
	print(path)
	print("Final X Coordinate: ", node1.state.x)
	print("Final Y Coordinate: ", node1.state.y)
	gc.collect()
	print("----------------------------------------- IDS END ----------------------------------------")

def select_N(text):
	global N
	N = int(text)
	
def select_P(text):
	global P
	P = int(text)

"""
GUI Layout in terms of widgets:
		w1  w2
	w5          w7
		w3  w4
"""

if __name__ == '__main__':
	app = QApplication(sys.argv)
	parent = QWidget()
	parent.setWindowTitle('Vacuum Cleaner Intelligent Agent')
	w5 = QWidget(parent)
	labels = []
	for i in range(12):
		labels.append(QLabel(w5))
		labels[i].move(5, 100+i*30)
		labels[i].setText(Texts[i]+"0                         ")
		labels[i].setStyleSheet('color: Brown')
		labels[i].show()
	w5.resize(400, 1000)
	w5.show()
	w1 = QWidget(parent)
	s1 = QtScene(w1, (0, 179, 0))
	v1 = QGraphicsView(w1)
	v1.setScene(s1)
	v1.move(385, 0)
	v1.resize(300, 300)
	v1.show()
	l1 = QLabel(w1)
	l1.setText('BFS')
	l1.move(510, 5)
	l1.setStyleSheet('color: Brown')
	l1.show()
	w1.show()
	w2 = QWidget(parent)
	s2 = QtScene(w2, ( 255, 224, 0))
	v2 = QGraphicsView(w2)
	v2.setScene(s2)
	v2.move(730, 0)
	v2.resize(300, 300)
	v2.show()
	l2 = QLabel(w2)
	l2.setText('IDS')
	l2.move(855, 5)
	l2.setStyleSheet('color: Brown')
	l2.show()
	w2.show()
	w3 = QWidget(parent)
	xx3 = list(range(3, 19))
	yy13c = [random.random()*100 for i in range(16)]
	yy23c = [random.random() for i in range(16)]
	for i in range(len(yy13)):
		yy13c[i] = math.log(yy13[i]*10000)
	for i in range(len(yy23)):
		yy23c[i] = math.log(yy23[i]*10000)
	g3 = QtPlotGraph(w3, width=3.4, height=3.4, title='Time in 100s of sec.(Y) Vs Room size(X)', x=xx3, y1=yy13c, y2=yy23c, xlabel='Room size N', ylabel='Time')
	lbl31 = QLabel("X: Room Size: From 3x3 to 18x18", w3)
	lbl31.move(70, 5)
	lbl32 = QLabel("Y: ln((Time in secs.)*10000))", w3)
	lbl32.move(80, 20)
	lbl33 = QLabel("(Press Option4 to see actual values printed on Console)", w3)
	lbl33.move(3, 325)
	w3.resize(500, 500)
	w3.move(385, 325)
	w3.show()
	w4 = QWidget(parent)
	xx4 = list(range(10, 60, 5))
	yy4c = [random.random() for i in range(10)]
	for i in range(len(yy4)):
		yy4c[i] = math.log(yy4[i]*100)
	g4 = QtPlotGraph(w4, width=3.4, height=3.4, title='Time in 100s of sec.(Y) vs Dirt %age(X)', x=xx4, y1=yy4c, xlabel='Percent of Dirt P', ylabel='Time')
	lbl41 = QLabel("Room Size: 6x6", w4)
	lbl41.move(115, 0)
	lbl42 = QLabel("X: Percentage of dirt : From 10% to 55%", w4)
	lbl42.move(55, 11)
	lbl43 = QLabel("Y: ln((Time in secs.)*100)", w4)
	lbl43.move(85, 25)
	lbl44 = QLabel("(Press Option4 to see actual values printed on Console)", w4)
	lbl44.move(3, 325)
	w4.resize(600, 600)
	w4.move(730, 325)
	w4.show()
	w7 = QWidget(parent)
	t1 = QLabel("Test My Code (Results displayed on Console)", w7)
	t1.move(1075, 395)
	t1.setStyleSheet('color: Brown')
	t2 = QLabel("[Choose N and P after seeing console", w7)
	t2.move(1095, 425)
	t2.setStyleSheet('color: Brown')
	t2 = QLabel("output of Option1 Button]", w7)
	t2.move(1130, 440)
	t2.setStyleSheet('color: Brown')
	opt_N = QLabel("Select size of square N: ", w7)
	combo_N = QComboBox(w7)
	combo_N.addItem("3")
	combo_N.addItem("4")
	combo_N.addItem("5")
	combo_N.addItem("6")
	combo_N.addItem("7")
	combo_N.addItem("8")
	combo_N.addItem("9")
	combo_N.addItem("10")
	opt_N.move(1095, 473)
	opt_N.setStyleSheet('color: Brown')
	combo_N.move(1240, 470)
	combo_N.setStyleSheet('color: Brown')
	combo_N.activated[str].connect(select_N)
	opt_P = QLabel("Select percent of dirt P:", w7)
	combo_P = QComboBox(w7)
	combo_P.addItem("5")
	combo_P.addItem("8")
	combo_P.addItem("10")
	combo_P.addItem("12")
	combo_P.addItem("15")
	combo_P.addItem("16")
	combo_P.addItem("18")
	combo_P.addItem("19")
	combo_P.addItem("20")
	combo_P.addItem("30")
	combo_P.addItem("35")
	combo_P.addItem("50")
	combo_P.addItem("55")
	combo_P.addItem("70")
	combo_P.addItem("75")
	combo_P.addItem("100")
	opt_P.move(1095, 503)
	opt_P.setStyleSheet('color: Brown')
	combo_P.move(1240, 500)
	combo_P.setStyleSheet('color: Brown')
	combo_P.activated[str].connect(select_P)
	b1 = QPushButton("Run BFS", w7)
	b1.move(1145, 545)
	b1.setStyleSheet('color: Brown')
	b1.clicked.connect(run_BFS)
	i1 = QPushButton("Run IDS", w7)
	i1.move(1145, 585)
	i1.setStyleSheet('color: Brown')
	i1.clicked.connect(run_IDS)
	opt1 = QPushButton("Option 1", w7)
	opt1.move(1080, 100)
	opt1.setStyleSheet('QPushButton {background-color: #b41bf2 ; color: black;}')
	opt1.show()
	opt1.clicked.connect(option1)
	opt2 = QPushButton("Option 2", w7)
	opt2.move(1180, 100)
	opt2.setStyleSheet('QPushButton {background-color: #b41bf2 ; color: black;}')
	opt2.show()
	opt2.clicked.connect(option2)
	opt3 = QPushButton("Option 3", w7)
	opt3.move(1080, 150)
	opt3.setStyleSheet('QPushButton {background-color: #b41bf2 ; color: black;}')
	opt3.show()
	opt3.clicked.connect(option3)
	opt4 = QPushButton("Option 4", w7)
	opt4.move(1180, 150)
	opt4.setStyleSheet('QPushButton {background-color: #b41bf2 ; color: black;}')
	opt4.show()
	opt4.clicked.connect(option4)
	w7.show()
	parent.resize(1500, 1000)
	pt = parent.palette()
	pt.setColor(parent.backgroundRole(), QColor( 245, 183, 5 ))
	parent.setPalette(pt)
	parent.show()
	sys.exit(app.exec_())

