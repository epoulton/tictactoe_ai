"""
A derived Tic Tac Toe Player class that implements the minimax search
algorithm (with alpha beta pruning) when placing tokens.

"""

import math
import random

import tictactoe


class MinimaxPlayer(tictactoe.Player):
    def select_index(self, board):
        for index in range(9):
            removed_token = board.remove_token(index)

            if removed_token is None:
                pass
            elif removed_token == self.token:
                board.place_token(1, index)
            else:
                board.place_token(-1, index)

        actions = self._list_actions(board, 1)
        random.shuffle(actions)

        for action in actions:
            self._do_action(board, action)

            action.value = -self._evaluate_board(
                board,
                -math.inf,
                math.inf,
                -1)

            self._undo_action(board, action)

        return max(actions, key=lambda item: item.value).index

    def notify_outcome(self, record):
        pass

    @staticmethod
    def _list_actions(board, token):
        return [Action(token, index, None)
                for index in range(9) if board[index] is None]

    @staticmethod
    def _do_action(board, action):
        board.place_token(action.token, action.index)

    @staticmethod
    def _evaluate_if_terminal_state(board, token):
        value = 0

        for token_set in board.generate_sets():
            if None in token_set:
                value = None

            elif len(token_set) == 1:
                if token in token_set:
                    value = 1
                    break
                else:
                    value = -1
                    break

        return value

    @staticmethod
    def _undo_action(board, action):
        board.remove_token(action.index)

    def _evaluate_board(self, board, alpha, beta, token):
        value = self._evaluate_if_terminal_state(board, token)

        if value is None:
            value = -math.inf

            actions = self._list_actions(board, token)

            for action in actions:
                self._do_action(board, action)

                value = max(
                    value,
                    -self._evaluate_board(
                        board,
                        -beta,
                        -alpha,
                        -token))

                self._undo_action(board, action)

                if alpha is not None and beta is not None:
                    alpha = max(alpha, value)

                    if alpha >= beta:
                        break

        return value

    @staticmethod
    def _stringify_board(board):
        return ''.join([str(token) for token in board])


class Action:
    def __init__(self, token, index, value):
        self.token = token
        self.index = index
        self.value = value

    def __str__(self):
        return 'Place token {0} at index {1} with value {2}.'.format(
            self.token,
            self.index,
            self.value)


if __name__ == '__main__':
    import _terminalplayer

    x = _terminalplayer.TerminalPlayer('X')
    o = MinimaxPlayer('O')

    g = tictactoe.Game([x, o])
    g.play()
