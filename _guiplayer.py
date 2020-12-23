"""
A derived Tic Tac Toe Player class that interacts via a GUI when placing
tokens. Very quick and dirty.

"""

import math
import pygame
import sys

import tictactoe


class GuiPlayer(tictactoe.Player):
    def __init__(self, token):
        super().__init__(token)

        pygame.init()

        self.gui = pygame.display.set_mode((300, 300))
        self.font = pygame.font.Font(None, 72)

    def select_index(self, board):
        selection = None

        while selection is None:
            self.gui.fill((0, 0, 0))

            pygame.draw.line(self.gui, (255, 255, 255), (100, 0), (100, 300), 5)
            pygame.draw.line(self.gui, (255, 255, 255), (200, 0), (200, 300), 5)
            pygame.draw.line(self.gui, (255, 255, 255), (0, 100), (300, 100), 5)
            pygame.draw.line(self.gui, (255, 255, 255), (0, 200), (300, 200), 5)

            for index in range(9):
                if board[index] is None:
                    continue

                token = self.font.render(str(board[index]), True, (255, 255, 255))

                self.gui.blit(
                    token,
                    (100 * (index % 3) + 50 - token.get_width() / 2,
                     100 * math.floor(index / 3) + 50 - token.get_height() / 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    row = math.floor(event.pos[1] / 100)
                    column = math.floor(event.pos[0] / 100)

                    selection = row * 3 + column

                    token = self.font.render(str(self), True, (255, 255, 255))
                    self.gui.blit(
                        token,
                        (100 * (selection % 3) + 50 - token.get_width() / 2,
                         100 * math.floor(selection / 3) + 50 - token.get_height() / 2))

            pygame.display.update()

        return selection

    def notify_outcome(self, outcome):
        self.gui.fill((0, 0, 0))

        if outcome.winner is None:
            text = self.font.render('DRAW', True, (255, 255, 255))
        else:
            text = self.font.render(' '.join([str(outcome.winner), 'won!']), True, (255, 255, 255))

        self.gui.blit(text, (150 - text.get_width() / 2, 150 - text.get_height() / 2))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


if __name__ == '__main__':
    import _minimaxplayer

    x = GuiPlayer('X')
    o = _minimaxplayer.MinimaxPlayer('O')
    g = tictactoe.Game([x, o])
    g.play()
