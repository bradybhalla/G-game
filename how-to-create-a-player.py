# To create a player, make a new file with the following code:

########
########

from player import Player

class <YOUR PLAYER NAME>(Player):
	def get_move(self, state):
		"""
		YOUR CODE FOR DECIDING A MOVE
		"""

########
########


"""
The get_move method can return either:
	- (row, col) --- the row and column to place the next stone
	- None --- does nothing and continues to the other player's move


The state object passed to the get_move method contains all information
about the state of the game as well as methods that can help process the board.
This object is only a copy of the state object used by the game, so feel free to
modify this copy.

The propereties of the state object are explained below:

	state.board_size --- the size of the board

	state.komi --- the points added to the second player's score

	state.board --- a 2D list containing the state of the board
				  - each cell with a 0 is empty
				  - each cell with a 1 or 2 has a stone from the respective player

	state.to_play --- the player whose turn it is

	state.current_scores[1] --- player 1's current score
	state.current_scores[2] --- player 2's current score


The (possibly) useful methods of the state object are explained below:

	state.copy() --- returns an exact copy of the object

	state.get_not_to_play()
		- returns the number of the player whose turn it is not
		- if state.to_play is 1, this will return 2 and vice versa

	state.get_positions_around(row, column)
		- returns a list of positions around (row, column)
		- usually returns 4 positions, but if (row, column) is
		  at an edge it will return 3 positions. If (row, column)
		  is in a corner it will only return 2 positions.
		- it does not matter if the surrounding positions are empty or not
		- Example:

			state.get_positions_around(2, 3)

			## returns [(1, 3), (3, 3), (2, 2), (2, 4)]


	state.get_group_info(row, column)
		- returns information about the group which includes the stone at (row, column)
		- returns a tuple with values (group, liberties)
		- group is a set of all stones connected to the stone at (row, column)
		- liberties is a set of all empty spaces touching the group
		- if there is no stone at (row, column), throws an error
		- Example usage:

			group, liberties = state.get_group_info(0, 3)
			if len(liberties) == 0:
				## the group including (0, 3) is dead
				## since there are no liberties

	state.is_legal_move(row, column)
		- returns True if the move at (row, column) is legal
		- Conditions for legality:
			- it must be on the board
			- it must be an empty space
			- playing the stone would not cause itself to be captured

	state.play(row, col):
		- simulates playing a stone at (row, col)
		- Note that in order to actually play the move, use:
				
				return (row, col)

		  instead of calling a method
		- After the move is played, resolves captured pieces and changes to
		  the other player's turn

	state.pass_play():
		- simulates passing instead of playing a stone
		- Note that in order to actually pass, use:
	
				return None

		  instead of calling a method
		- Changes to the other player's turn

	state.print_board():
		- prints the state of the current stones on the board
		- use for debugging

"""