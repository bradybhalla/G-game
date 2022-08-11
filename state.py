from collections import deque

class IllegalMoveError(Exception):
	pass

class State:
	def __init__(self, board_size=9, komi=0.5):
		self.board_size = board_size
		self.komi = komi

		self.board = None

		self.to_play = None

		self.current_scores = None

		self._cached_enemy_groups = None

	def get_not_to_play(self):
		return 1 if self.to_play == 2 else 2

	def create_board(self):
		self.board = [[0 for j in range(self.board_size)] for i in range(self.board_size)]

		self.to_play = 1

		self.current_scores = {1:0, 2:self.komi}


	def copy(self):
		state_copy = State(board_size=self.board_size, komi=self.komi)

		state_copy.board = [[j for j in i] for i in self.board]

		state_copy.to_play = self.to_play

		state_copy.current_scores = {1:self.current_scores[1], 2:self.current_scores[2]}


		return state_copy

	# return (group, liberties) for the stone at (row, col)
	def get_group_info(self, row, col):

		color = self.board[row][col]

		# if there is no stone, there is no group
		# possibly remove later
		if color == 0:
			raise ValueError("There is no stone at ({}, {})".format(row, col))

		group = set()
		liberties = set()

		to_check = deque()
		to_check.append((row, col))

		while len(to_check) > 0:
			node = to_check.popleft()
			group.add(node)

			for i in self._get_positions_around(node[0], node[1]):
				# if the stone is the same color, add to the queue
				if self.board[i[0]][i[1]] == color and i not in group:
					to_check.append(i)

				# if there is no stone, add a liberty
				elif self.board[i[0]][i[1]] == 0 and i not in liberties:
					liberties.add(i)

		return group, liberties



	def _get_positions_around(self, row, col):
		positions = []

		if row-1 >= 0:
			positions.append((row-1, col))

		if row+1 < self.board_size:
			positions.append((row+1, col))

		if col-1 >= 0:
			positions.append((row, col-1))

		if col+1 < self.board_size:
			positions.append((row, col+1))

		return positions

	def _get_enemy_groups_around(self, row, col):
		# get positions around which are the other color
		positions = [(r,c) for (r,c) in self._get_positions_around(row, col) if self.board[r][c] == self.get_not_to_play()]

		contained_positions = set()

		group_infos = []

		for i in positions:
			if i not in contained_positions:
				group, liberties = self.get_group_info(i[0], i[1])
				contained_positions.update(group)
				group_infos.append((group, liberties))

		self._cached_enemy_groups = group_infos

		return group_infos

	def is_legal_move(self, row, col):
		if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
			return False

		if self.board[row][col] != 0:
			return False

		# pretend move has been played
		self.board[row][col] = self.to_play

		# check all stones around for possible captures
		for _, liberties in self._get_enemy_groups_around(row, col):

			# if an enemy group can be captured, the move is legal
			if len(liberties) == 0:
				self.board[row][col] = 0
				return True

		# if there are no possible captures, make sure the move
		# won't cause itself to be captured
		_, liberties = self.get_group_info(row, col)

		self.board[row][col] = 0

		if len(liberties) == 0:
			return False

		return True

	def play(self, row, col):
		if not self.is_legal_move(row, col):
			raise IllegalMoveError

		self.board[row][col] = self.to_play
		self.current_scores[self.to_play] += 1

		for group, liberties in self._cached_enemy_groups:
			if len(liberties) == 0:
				for r,c in group:
					self.board[r][c] = 0
				self.current_scores[self.get_not_to_play()] -= len(group)

		self.pass_play()

	def pass_play(self):
		self.to_play = self.get_not_to_play()

	def print_board(self):
		for i in self.board:
			for j in i:
				print(j, end=" ")
			print()



