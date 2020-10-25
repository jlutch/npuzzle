import math
import copy

###############################################################
#Author: Jonathan Lutch
#Date: 10/25/2020
#Description: This is a program that uses three algorithms 
#(BFS, DFS, and Bidirectional Search) to solve the n puzzle 
#game. Bidirectional Search is the fastest, while DFS is the
# slowest. The BFS algorithm can do all 3x3 and most 4x4
# puzzles in under a minute.
###############################################################

#lets read in the file!
def LoadFromFile(filepath):
	#our game board
	board = []
	
	#the puzzle
	f = open(filepath, "r")
	
	#grabbing one charecter at a time
	finished_reading = False
	while not finished_reading:
		charecter = f.read(1)
		if charecter == "*":
			charecter = "0"
		if not charecter:
			finished_reading = True
		board.append(charecter)	
	
	#formatting the list before returning it
	return FormatBoard(board)

#formats the board
def FormatBoard(state):
	#doing a basic check to see if the input we are given is valid
	if CheckForBadInput(state):
		print("This board is not valid")
		exit()
	
	#getting the demension variable
	deminesion = int(state.pop(0))
	state.pop(0)
	
	#this section finds clumps of numbers
	#it is to prevent a 15 being read in 
	#as a 1 and a 5
	nums = [] 
	i = 0
	entry = []	
	while len(state) != 0:
		if state[i] != "\n" and state[i] != "\t" and state[i] != "":
			entry.append(state[i])
		else:
			nums.append(entry)   
			entry = []
		state.pop(0)	

	#fusing the number with more that two digits
	board = []
	blank = ""
	for x in nums:
		board.append(blank.join(x))

	#one more validity check
	if len(board) != (deminesion*deminesion):
		print("This board is not valid")
		exit()
	
	#filling our 2D list
	new_board = []
	for make_row in range(deminesion):
			row = []
			for entry in range(deminesion):
				row.append(int(board.pop(0)))
			new_board.append(row)
	 
	return new_board

#this is a basic function that catches some bad inputs
def CheckForBadInput(board):
	#if the first charecter of the board is 
	#out of place (also catches empty files)
	if board[0] == '':
		return True
	
	#all valid chars
	valid = ['\n', '\t', '']
	numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
	
	for x in board:
		if x not in numbers and x not in valid:			
			return True
	if board[0] not in numbers or board[2] not in numbers:
		return True
	
	return False

#neatly prints out the board
def PrintBoard(board):
	for row in board:
		print(row)

#shoots out all possible searches
def ComputeNeighbors(board):
	states = []
	#for each position in the board
	for row in range(len(board)):
		for col in range(len(board)):
			#these functions check if a certain position has any neighbors
			#the 1s and 0s are the shift that the tile may experience
			states.append(CheckForEmptySlot(1,0, row, col, board))
			states.append(CheckForEmptySlot(-1,0, row, col, board))
			states.append(CheckForEmptySlot(0,1, row, col, board))			
			states.append(CheckForEmptySlot(0,-1, row, col, board))
	
	#filtering out the "None" data we got
	possible_states = []
	for entry in states:
		if entry != None:
			possible_states.append(entry)
	return possible_states			

#checks for all possible states
def CheckForEmptySlot(vert, hori, row, col, board):
	state = copy.deepcopy(board)
	
	#if the shift will end up being valid
	if ((row + vert != -1 and row + vert != len(board)) and (col + hori != -1 and col + hori != len(board))):
		#if the shift puts you ontop of the empty tile
		if ((board[row + vert][col + hori] == 0)):
			#have the empty tile and the one that is being moved 
			#switch places
			state[row + vert][col + hori] = board[row][col]
			state[row][col] = board[row + vert][col + hori]
			return (board[row][col], state)
	return 

#checks if given state is final state
def IsGoal(board):
	last_term = (len(board)**2) - 1
	board = Flatten(board)
	
	#if the last tile is 0
	if board[len(board)-1] == 0:
		board.remove(board[len(board)-1])
		#checks if the numbers go up in sequential order
		previous = 0
		for x in board:
			if x == previous + 1:
				previous = x
				if previous == last_term:
					return True
			else:
				return False
	return False

#flattens a lsit
def Flatten(board):
	#we only need to worry about a list being 2D 
	flat = []
	for i in range(len(board)):
		for j in range(len(board[i])):
			flat.append(board[i][j])
	return flat

#makes a list a string
def MakeStr(state):
	blank = ''
	str1 = blank.join(str(Flatten(state)))
	return str1

#bredth first search algorithim
def BFS(state):
	board = copy.deepcopy(state)
	final_state = CreateSolvedBoard(state)
	#makes sure that the given state is not in solved position
	if IsGoal(state):
		return []

	#our initial state for the start of the search
	str_state = MakeStr(state)
	frontier = [state]
	discovered = set(str_state)
	parents = [[state, None]]
	
	print("searching...")
	#while nodes can be explored
	while len(frontier) != 0:
		current_state = frontier.pop(0)
		#add to our discovered set
		discovered.add(str_state)
		if final_state == (current_state):
			#finds the tiles that need to be moved
			print("deriving paths...")
			parents = DerivePath(parents, CreateSolvedBoard(board), True)
			return parents
		#for the nearby states to the one we are in
		for neighbor in ComputeNeighbors(current_state):
			str_neighbor = MakeStr(neighbor[1])
			#if neighbor is a new state
			if str_neighbor not in discovered:
				frontier.append(neighbor[1])
				discovered.add(str_neighbor)
				parents.append([neighbor[1], current_state])
	
	#if no path is possible			
	return None			

#depth first search algorithim
def DFS(state):
	board = copy.deepcopy(state)
	#makes sure that the given state is not in solved position
	if IsGoal(state):
		return []

	#our initial state
	frontier = [state]
	discovered = set(MakeStr(state))
	parents = [[state, None]]
	
	#while nodes can be explored
	while len(frontier) != 0:
		current_state = frontier.pop(0)
		#add to our discovered set
		discovered.add(MakeStr(state))
		if IsGoal(current_state):
			#finds the tiles that need to be moved
			parents = DerivePath(parents, CreateSolvedBoard(board), True)
			return parents
		#for the nearby states to the one we are in
		for neighbor in ComputeNeighbors(current_state):
			#if neighbor is a new state
			if MakeStr(neighbor[1]) not in discovered:
				frontier.insert(0, neighbor[1])
				discovered.add(MakeStr(neighbor[1]))
				parents.append([neighbor[1], current_state])
	
	#if no path is possible			
	return None		

#finding the tile movements from the parents
def DerivePath(parents, target, find_tiles):
	#the path vairable will store the 
	#path, in terms of states, from
	#the unsolved state to the 
	#solved one.
	path = []
	start = 0
	#we are looking for the solved state here
	for x in parents:
		if  target == (x[0]):
			start = x
			path.append(x[0])
	
	#From here we can do parent matching
	#We can look at the parent of our end position
	#and find his parent
	#we can keep doing this until we hit our
	#initial state
	#we then have a path of states
	not_done = True
	while not_done:
		placeholder = 0
		for entry in parents:
			if start[1] == entry[0]:
				path.append(start[1])
				placeholder = entry
				if entry[1] == None:
					not_done = False
		start = placeholder
	
	#becuase we want initial to final, not vice versa
	path.reverse()
	#if we want tiles moved
	if find_tiles:
		path = FindTiles(path)
	return path

#find the tiles moved
def FindTiles(path):
	#Since we know all the sates are in choronological order,
	#exactly two charecters should be swapped each time. If 
	#we string cast all the states (two at a time) and figure out 
	#which two chars moved, then we know which tile has to be moved.
	#One of those tiles ALWAYS has to be 0. We can take the one that
	#is not 0 as the tile that needs to be moved.
	condensed_path = []
	#for every index in the list
	for x in range(len(path) - 1):
		#for every charecter index in the entry
		for i in range(len(Flatten(path[x]))):
			#if the two charecters do not equal each other and that char is not 0 
			if ((Flatten(path[x])[i] != Flatten(path[x + 1])[i]) and Flatten(path[x])[i] != 0):
				condensed_path.append(Flatten(path[x])[i])
	return condensed_path

#bidirectional search algorithm
def BidirectionalSearch(state):
	print("searching...")
	#checking to see if the given state is solved
	if IsGoal(state):
		return []

	#our initial state when we are working from the front
	frontier = [state]
	discovered = set(MakeStr(state))
	parents = [[state, None]]

	#our initial state when we are working from the back
	state_back = CreateSolvedBoard(state)
	frontier_back = [state_back]
	discovered_back = set(MakeStr(state_back))
	parents_back = [[state_back, None]]

	#until we find a solution or know that one does not exist
	not_done = True
	while not_done:
		
		#if there is nothing left to explore
		if len(frontier) == 0 or len(frontier_back) == 0:
			return None
			
		#one iteration of BFS from the front
		current_state = frontier.pop(0)
		discovered.add(MakeStr(state))
		for neighbor in ComputeNeighbors(current_state):
			if MakeStr(neighbor[1]) not in discovered:
				frontier.append(neighbor[1])
				discovered.add(MakeStr(neighbor[1]))
				parents.append([neighbor[1], current_state])
	
		#one iteration of BFS from the back
		current_state_back = frontier_back.pop(0)
		discovered_back.add(MakeStr(state_back)) 
		for neighbor in ComputeNeighbors(current_state_back):
			if MakeStr(neighbor[1]) not in discovered_back:
				frontier_back.append(neighbor[1])
				discovered_back.add(MakeStr(neighbor[1]))
				parents_back.append([neighbor[1], current_state_back])

		#if there is an overlapping node
		for entry in parents:
			if entry in parents_back:
				#we will send this in as the end goal to DerivePath function
				common_state = entry[0]
				print("deriving paths...")
				part1 = DerivePath(parents, common_state, False)
				part2 = DerivePath(parents_back, common_state, False)
				part2.reverse()
				#link the two paths together
				for x in range(1, len(part2)):
					part1.append(part2[x])
				return FindTiles(part1)


#creates a solved board
def CreateSolvedBoard(state):
	solved = []
	nums = []
	#fills a 2D list with the solved state based on
	#the demesniosn of the given state
	for x in range(1, len(state)**2 + 1):
		nums.append(x)
	for row in range(len(state)):
		make_row = []
		for col in range(len(state)):
			make_row.append(nums.pop(0))
		solved.append(make_row)
	solved[len(state)-1][len(state)-1] = 0
	return solved
