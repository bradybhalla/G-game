from random import random

from state import State, IllegalMoveError

class Game:
    def __init__(self, first_player, second_player, board_size=9):
        first_player_object = first_player()
        second_player_object = second_player()


        self.players = {}
        self.players[1] = first_player_object if random() < 0.5 else second_player_object
        self.players[2] = second_player_object if self.players[1] is first_player_object else first_player_object

        self.state = State(board_size)
        self.state.create_board()

        self._num_passes = 0

        self.winner = None

    def run(self):
        while self._num_passes < 2:
            move = self.players[self.state.to_play].get_move(self.state.copy())

            if move is not None:
                try:
                    self.state.play(move[0], move[1])
                except IllegalMoveError:
                    print("Illegal move by {}".format(type(self.players[self.state.to_play]).__name__))
                    self.winner = self.players[self.state.get_not_to_play()]
                    return

                self._num_passes = 0
            else:
                self.state.pass_play()
                self._num_passes += 1

        print("Game complete")

        # if there is a tie, player 2 wins
        # if komi is not a whole number, there won't be a tie
        self.winner = self.players[1] if self.state.current_scores[1] > self.state.current_scores[2] else self.players[2]


from player import BasedBrady, Ryan

g = Game(BasedBrady, Ryan)

g.run()

print(type(g.winner).__name__, "won")


