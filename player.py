from abc import ABCMeta, abstractmethod

class Player(metaclass=ABCMeta):
	@abstractmethod
	def get_move(self, state):
		pass

class HumanPlayer(Player):
	def get_move(self, state):
		print()
		print("{} ({}) to move...".format(type(self).__name__, state.to_play))
		state.print_board()
		print()
		move = input()
		if move == "":
			return None
		return [int(i) for i in move.split(" ")]

class BasedBrady(HumanPlayer):
	pass

class Ryan(HumanPlayer):
	pass