class GameLogic:
    def __init__(self, board_size=15):
        self.board_size = board_size
        self.pieces = []
        self.is_black_turn = True
        self.game_over = False

    def add_piece(self, x, y):
        """添加一个棋子到棋盘"""
        if self.is_valid_move(x, y):
            self.pieces.append((x, y, self.is_black_turn))
            if self.check_win(x, y):
                self.game_over = True
                return True
            self.is_black_turn = not self.is_black_turn
            return True
        return False

    def is_valid_move(self, x, y):
        """检查移动是否有效"""
        if not (0 <= x < self.board_size and 0 <= y < self.board_size):
            return False
        return not any(piece[0] == x and piece[1] == y for piece in self.pieces)

    def check_win(self, x, y):
        """检查是否获胜"""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            
            # 正向检查
            tx, ty = x + dx, y + dy
            while 0 <= tx < self.board_size and 0 <= ty < self.board_size:
                if not self._has_same_piece(tx, ty):
                    break
                count += 1
                tx += dx
                ty += dy
            
            # 反向检查
            tx, ty = x - dx, y - dy
            while 0 <= tx < self.board_size and 0 <= ty < self.board_size:
                if not self._has_same_piece(tx, ty):
                    break
                count += 1
                tx -= dx
                ty -= dy
            
            if count >= 5:
                return True
        return False

    def _has_same_piece(self, x, y):
        """检查指定位置是否有相同颜色的棋子"""
        return any(piece[0] == x and piece[1] == y and piece[2] == self.is_black_turn 
                  for piece in self.pieces)

    def undo_move(self):
        """悔棋"""
        if self.pieces:
            self.pieces.pop()
            self.is_black_turn = not self.is_black_turn
            self.game_over = False
            return True
        return False

    def reset_game(self):
        """重置游戏"""
        self.pieces = []
        self.is_black_turn = True
        self.game_over = False 