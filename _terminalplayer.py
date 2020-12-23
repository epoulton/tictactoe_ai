"""
A derived Tic Tac Toe Player class that interacts with the terminal when
placing tokens.

"""

import tictactoe


class TerminalPlayer(tictactoe.Player):

    last_outcome_notified = None

    def select_index(self, board):
        print(self.token, 'to play')
        self._print_board(board)

        while True:
            entry = input(
                'Enter the index of the cell into which the token shall be '
                'placed.')

            try:
                index = int(entry)
            except ValueError:
                print('Entry could not be converted to an integer index.')
                continue

            if not 0 <= index < 9:
                print('Index must be within the valid range [0,8].')
                continue

            if board[index] is not None:
                print('Cannot place a token in an occupied cell.')
                continue

            break

        # noinspection PyUnboundLocalVariable
        return index

    @classmethod
    def notify_outcome(cls, game_record):
        if cls.last_outcome_notified is not game_record:
            cls.last_outcome_notified = game_record

            if game_record.winner is None:
                print('The game was a draw.')
            else:
                print(game_record.winner, 'won!')

            cls._print_board(game_record.final_board)

    @staticmethod
    def _print_board(board):
        print(
            '\n'.join(
                ['[{}]'.format(
                    ' '.join(
                        [str(token) if token is not None else ' '
                         for token in board[row * 3: row * 3 + 3]]))
                 for row in range(3)]))


if __name__ == '__main__':
    x = TerminalPlayer('X')
    o = TerminalPlayer('O')
    g = tictactoe.Game([x, o])
    g.play()
