import sys

class Node:
	def __init__(self, board, depth):
		self.position = board
		self.depth = depth
		self.code = ''.join(board)


class MiniMaxGame:
	def __init__(self, maxDepth):
		self.evaluatedPositions = 0
		self.bestResponse = None
		self.maxDepth = maxDepth

		self.neighbors = {
			0: [1, 3, 9],
			1: [0, 4, 2],
			2: [1, 5, 14],
			3: [0, 10, 6, 4],
			4: [1, 3, 5, 7],
			5: [2, 4, 8, 13],
			6: [3, 7, 11],
			7: [4, 6, 8],
			8: [5, 7, 12],
			9: [0, 10, 21],
			10: [3, 9, 11, 18],
			11: [6, 10, 15],
			12: [8, 13, 17],
			13: [5, 12, 14, 20],
			14: [2, 13, 23],
			15: [11, 16, 18],
			16: [15, 17, 19],
			17: [12, 16, 20],
			18: [10, 19, 21],
			19: [16, 18, 20, 22],
			20: [13, 17, 19, 23],
			21: [9, 18, 22],
			22: [19, 21, 23],
			23: [14, 20, 22]
		}

		self.checkMillMap = {
			0: [[1,2],[9,21],[3,6]],
			1: [[0,2],[4,7]],
			2: [[0,1],[14,23],[5,8]],
			3: [[4,5],[10,18],[0,6]],
			4: [[1,7],[3,5]],
			5: [[3,4],[13,20],[8,2]],
			6: [[7,8],[11,15],[0,3]],
			7: [[1,4],[6,8]],
			8: [[6,7],[12,17],[5,2]],
			9: [[0,21],[10,11]],
			10: [[9,11],[3,18]],
			11: [[9,10],[6,15]],
			12: [[8,17],[13,14]],
			13: [[5,20],[12,14]],
			14: [[2,23],[12,13]],
			15: [[6,11],[16,17],[18,21]],
			16: [[15,17],[19,22]],
			17: [[15,16],[8,12],[20,23]],
			18: [[3,10],[19,20],[15,21]],
			19: [[16,22],[18,20]],
			20: [[18,19],[5,13],[17,23]],
			21: [[0,9],[22,23],[18,15]],
			22: [[16,19],[21,23]],
			23: [[2,14],[21,22],[17,20]]
		}


		
	def closeMill(self, j, b):
		for millNeighbors in self.checkMillMap[j]:
			if (b[millNeighbors[0]] == b[j]) and (b[millNeighbors[1]] == b[j]):
				return True

		return False


	def potentialCloseMill(self, j, b):
		for millNeighbors in self.checkMillMap[j]:
			if (b[millNeighbors[0]] == b[j]) and (b[millNeighbors[1]] == 'x'):
				return True
			if (b[millNeighbors[0]] == 'x') and (b[millNeighbors[1]] == b[j]):
				return True

		return False


	def countMills(self, board):
		numBlackCloseMills = 0
		numWhiteCloseMills = 0
		numPotBlackCloseMills = 0
		numPotWhiteCloseMills = 0

		for loc in range(len(board)):
			if board[loc] == 'W':
				if self.closeMill(loc, board):
					numWhiteCloseMills += 1
				if self.potentialCloseMill(loc, board):
					numPotWhiteCloseMills += 1
			if board[loc] == 'B':
				if self.closeMill(loc, board):
					numBlackCloseMills += 1
				if self.potentialCloseMill(loc, board):
					numPotBlackCloseMills += 1
		
		return numWhiteCloseMills, numBlackCloseMills, \
			numPotWhiteCloseMills, numPotBlackCloseMills


	def countPieces(self, board):
		numWhitePieces = 0
		numBlackPieces = 0

		for b in board:
			if b=='W':
				numWhitePieces += 1
			if b=='B':
				numBlackPieces += 1

		return numWhitePieces, numBlackPieces

	def checkBlocked(self, board, loc):
		res = True
		n = self.neighbors[loc]
		for ni in n:
			if board[ni] == 'x':
				res = False
		return res

	def blocked(self, board):
		whiteBlocked = 0
		blackBlocked = 0

		for loc in range(len(board)):
			if board[loc] == 'W':
				if self.checkBlocked(board, loc):
					whiteBlocked += 1
			if board[loc] == 'B':
				if self.checkBlocked(board, loc):
					blackBlocked += 1
		
		return whiteBlocked - blackBlocked	

	def static(self, board):
		numWhitePieces = 0
		numBlackPieces = 0
		for b in board:
			if b=='W':
				numWhitePieces += 1
			if b=='B':
				numBlackPieces += 1

		numBlackMoves = len(self.GenerateMovesMidgameEndgame(board, True))

		numWhiteCloseMills, numBlackCloseMills, \
		numPotWhiteCloseMills, numPotBlackCloseMills = self.countMills(board)

		if numBlackPieces <= 2:
			return 10000
		elif numWhitePieces <= 2:
			return -10000
		elif numBlackMoves == 0:
			return 10000
		else:
			return 100 * ((numWhitePieces - numBlackPieces) + \
				3*(numWhiteCloseMills - numBlackCloseMills) + \
				2*(numPotWhiteCloseMills - numPotBlackCloseMills) + \
				self.blocked(board)) - numBlackMoves


	def MinMax(self, x, alpha, beta):
		depth = x.depth
		if self.maxDepth == depth:
			self.evaluatedPositions += 1
			return self.static(x.position)

		
		v = 50000 - depth
		children = self.GenerateMovesMidgameEndgame(x.position, switchColor=True)

		for y in children:
			node_y = Node(y, depth+1)
			v = min(v, self.MaxMin(node_y, alpha, beta))
			
			if v <= alpha:
				return v
			else:
				beta = min(v,beta)
		return v


	def MaxMin(self, x, alpha, beta):
		depth = x.depth
		if self.maxDepth == depth:
			self.evaluatedPositions += 1
			return self.static(x.position)
		
		v = -50000 + depth
		children = self.GenerateMovesMidgameEndgame(x.position)

		for y in children:
			node_y = Node(y, depth+1)
			tmpV = v
			v = max(v, self.MinMax(node_y, alpha, beta))
			
			if v > tmpV and node_y.depth==1:
					self.bestResponse = y
			
			if v >= beta:
				return v
			else:
				alpha = max(v,alpha)

		return v


	def switchColors(self, board):
		for i in range(len(board)):
			if type(board[i]) == list:
				for j in range(len(board[i])):
					if board[i][j] == 'W':
						board[i][j] = 'B'
					elif board[i][j] == 'B':
						board[i][j] = 'W'

			else:
				if board[i] == 'W':
					board[i] = 'B'
				elif board[i] == 'B':
					board[i] = 'W'
		return board



	def GenerateRemove(self, board, L):
		numPositions = 0

		for loc in range(len(board)):
			if board[loc] == 'B':
				if not self.closeMill(loc, board):
					b = board.copy()
					b[loc] = 'x'
					L.append(b)
					numPositions += 1

		if numPositions == 0:
			L.append(board.copy())


	def GenerateAdd(self, board):
		L = []

		for loc in range(len(board)):
			if board[loc] == 'x':
				b = board.copy()
				b[loc] = 'W'
				if self.closeMill(loc, b):
					self.GenerateRemove(b, L)
				else:
					L.append(b)
		
		return L



	def GenerateHopping(self, board):
		L = []
		for loc1 in range(len(board)):
			if board[loc1] == 'W':
				for loc2 in range(len(board)):
					if board[loc2] == 'x':
						b = board.copy()
						b[loc1] = 'x'
						b[loc2] = 'W'
						if self.closeMill(loc2, b):
							self.GenerateRemove(b, L)
						else:
							L.append(b)
		return L


	def GenerateMove(self, board):
		L = []
		for loc in range(len(board)):
			if board[loc] == 'W':
				n = self.neighbors[loc]
				for j in n:
					if board[j] == 'x':
						b = board.copy()
						b[loc] = 'x'
						b[j] = 'W'
						if self.closeMill(j,b):
							self.GenerateRemove(b, L)
						else:
							L.append(b)
		return L


	def GenerateMovesMidgameEndgame(self, board, switchColor=False):
		if switchColor:
			board = self.switchColors(board)

		numWhitePieces = 0
		for b in board:
			if b=='W':
				numWhitePieces += 1

		if numWhitePieces == 3:
			L = self.GenerateHopping(board)
		else:
			L = self.GenerateMove(board)

		if switchColor:
			board = self.switchColors(board)
			L = self.switchColors(L)
		
		return L
