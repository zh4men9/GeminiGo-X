import sys
from PyQt6.QtWidgets import QApplication
from game_board import GameBoard

if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = GameBoard()
    board.show()
    sys.exit(app.exec()) 