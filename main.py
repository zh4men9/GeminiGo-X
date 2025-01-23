import sys
from PyQt6.QtWidgets import QApplication
from game_board import GameBoard
import os

if __name__ == '__main__':
    # 设置proxy
    os.environ['http_proxy'] = 'http://127.0.0.1:7890'
    os.environ['https_proxy'] = 'http://127.0.0.1:7890'
    
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }
    app = QApplication(sys.argv)
    board = GameBoard()
    board.show()
    sys.exit(app.exec()) 