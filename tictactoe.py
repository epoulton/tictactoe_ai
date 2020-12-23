"""
Module containing the code necessary to play a headless game of
Tic-Tac-Toe.

"""

import itertools
import random


class Game:

    def __init__(self, players):
        self.players = list(players)

    def play(self):
        board = Board()
        game_record = GameRecord()

        random.shuffle(self.players)
        players = itertools.cycle(self.players)

        for ply in range(9):
            if game_record.winner is not None:
                break

            current_player = next(players)

            selected_index = current_player.select_index(Board(board))
            board.place_token(current_player.token, selected_index)
            game_record.log_ply(ply, current_player.token, selected_index)

            for token_set in board.generate_sets():
                if len(token_set) == 1 and current_player.token in token_set:
                    game_record.winner = current_player
                    break

        game_record.final_board = Board(board)

        for player in self.players:
            player.notify_outcome(game_record)


class GameRecord:

    class Ply:

        def __init__(self, ply, token, index):
            self.ply = ply
            self.token = token
            self.index = index

    def __init__(self):
        self.plys = []
        self.winner = None
        self.final_board = None

    def log_ply(self, ply, token, index):
        self.plys.append(GameRecord.Ply(ply, token, index))


class Board:

    def __init__(self, board=None):
        if board is not None:
            self._tokens = [token for token in board]
        else:
            self._tokens = [None for _ in range(9)]

    def __iter__(self):
        return iter(self._tokens)

    def __getitem__(self, item):
        return self._tokens[item]

    def place_token(self, token, index):
        if self._tokens[index] is None:
            self._tokens[index] = token
        else:
            raise RulesViolation('Cannot place a token in an occupied cell.')

    def remove_token(self, index):
        removed = self._tokens[index]
        self._tokens[index] = None
        return removed

    def generate_sets(self):
        # Horizontal lines
        for row in range(3):
            yield set(self[3 * row: 3 * row + 3])

        # Vertical lines
        for column in range(3):
            yield set(self[column: column + 7: 3])

        # Down-right diagonal line
        yield set(self[0:: 4])

        # Down-left diagonal line
        yield set(self[2: 7: 2])


class RulesViolation(Exception):
    pass


class Player:

    def __init__(self, token):
        if token is None:
            raise ValueError('Player token cannot be None.')

        self.token = token

        if len(str(self.token)) != 1:
            # TODO: Change this to a proper warning.
            print(
                'Warning: Player {}: String representation of token is longer '
                'than one character and may cause confusion to players using '
                'the terminal.'.format(self))

    def __str__(self):
        return str(self.token)

    def select_index(self, board):
        raise NotImplementedError

    def notify_outcome(self, outcome):
        raise NotImplementedError


if __name__ == '__main__':
    import _guiplayer
    import _minimaxplayer

    x = _guiplayer.GuiPlayer('X')
    o = _minimaxplayer.MinimaxPlayer('O')
    g = Game([x, o])
    g.play()
