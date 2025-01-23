from PyQt6.QtCore import QThread, pyqtSignal
import time
import numpy as np
from typing import List, Tuple, Optional

class AIWorker(QThread):
    move_ready = pyqtSignal(tuple)  # 发送AI的落子位置
    error = pyqtSignal(str)         # 发送错误信息
    
    def __init__(self, ai_player, board_state, board_size, timeout=5000):
        super().__init__()
        self.ai_player = ai_player
        self.board_state = board_state
        self.board_size = board_size
        self.timeout = timeout
        self.is_running = False
        
    def run(self):
        if self.is_running:
            return
            
        self.is_running = True
        try:
            # 启动Gemini AI，设置超时
            start_time = time.time()
            move = None
            
            try:
                # 在新线程中执行AI操作
                move = self.ai_player.get_move(self.board_state, self.board_size)
                if time.time() - start_time > self.timeout:
                    print("Gemini AI timeout, switching to fallback AI")
                    move = self.fallback_ai_move()
            except Exception as e:
                print(f"Gemini AI error: {str(e)}, switching to fallback AI")
                move = self.fallback_ai_move()
                
            if move and self.is_running:  # 检查是否仍在运行
                self.move_ready.emit(move)
            elif self.is_running:
                raise ValueError("无法获取有效的落子位置")
                
        except Exception as e:
            if self.is_running:  # 只在仍在运行时发送错误
                self.error.emit(str(e))
        finally:
            self.is_running = False
            
    def stop(self):
        """停止AI操作"""
        self.is_running = False
        self.wait()  # 等待线程结束
        
    def fallback_ai_move(self) -> Tuple[int, int]:
        """
        备用的五子棋AI算法
        使用评分机制来选择最佳落子位置
        """
        board = self._convert_to_numpy_board()
        best_score = float('-inf')
        best_move = None
        
        # 获取所有可能的落子位置
        empty_positions = self._get_empty_positions(board)
        if not empty_positions:
            return None
            
        # 如果是第一步，优先选择天元或者靠近天元的位置
        if len(self.board_state) == 0:
            center = self.board_size // 2
            return (center, center)
            
        # 评估每个可能的位置
        for x, y in empty_positions:
            score = self._evaluate_position(board, x, y)
            if score > best_score:
                best_score = score
                best_move = (x, y)
                
        return best_move
        
    def _convert_to_numpy_board(self) -> np.ndarray:
        """将游戏状态转换为numpy数组"""
        board = np.zeros((self.board_size, self.board_size), dtype=int)
        for x, y, is_black in self.board_state:
            board[y, x] = 1 if is_black else 2
        return board
        
    def _get_empty_positions(self, board: np.ndarray) -> List[Tuple[int, int]]:
        """获取所有空位置"""
        empty_positions = []
        # 只考虑已有棋子周围的空位
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y, x] == 0 and self._has_neighbor(board, x, y):
                    empty_positions.append((x, y))
        return empty_positions
        
    def _has_neighbor(self, board: np.ndarray, x: int, y: int, distance: int = 2) -> bool:
        """检查指定位置周围是否有棋子"""
        for dy in range(-distance, distance + 1):
            for dx in range(-distance, distance + 1):
                ny, nx = y + dy, x + dx
                if (0 <= ny < self.board_size and 
                    0 <= nx < self.board_size and 
                    board[ny, nx] != 0):
                    return True
        return False
        
    def _evaluate_position(self, board: np.ndarray, x: int, y: int) -> float:
        """评估某个位置的分数"""
        # 模拟在此位置落子
        board = board.copy()
        board[y, x] = 2  # AI是白子
        
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            # 评估防守分数（黑子）
            defense_score = self._evaluate_line(board, x, y, dx, dy, 1)
            # 评估进攻分数（白子）
            attack_score = self._evaluate_line(board, x, y, dx, dy, 2)
            
            # 防守权重略高于进攻
            score += defense_score * 1.1 + attack_score
            
        return score
        
    def _evaluate_line(self, board: np.ndarray, x: int, y: int, dx: int, dy: int, player: int) -> float:
        """评估某个方向的连子情况"""
        count = 1
        block = 0
        
        # 正向检查
        tx, ty = x + dx, y + dy
        while (0 <= ty < self.board_size and 
               0 <= tx < self.board_size and 
               board[ty, tx] == player):
            count += 1
            tx += dx
            ty += dy
        if (0 <= ty < self.board_size and 
            0 <= tx < self.board_size and 
            board[ty, tx] != 0):
            block += 1
            
        # 反向检查
        tx, ty = x - dx, y - dy
        while (0 <= ty < self.board_size and 
               0 <= tx < self.board_size and 
               board[ty, tx] == player):
            count += 1
            tx -= dx
            ty -= dy
        if (0 <= ty < self.board_size and 
            0 <= tx < self.board_size and 
            board[ty, tx] != 0):
            block += 1
            
        # 评分规则
        if count >= 5:
            return 100000  # 五连
        if count == 4:
            if block == 0:
                return 10000  # 活四
            elif block == 1:
                return 1000  # 冲四
        if count == 3:
            if block == 0:
                return 1000  # 活三
            elif block == 1:
                return 100  # 冲三
        if count == 2:
            if block == 0:
                return 100  # 活二
            elif block == 1:
                return 10  # 冲二
                
        return 1  # 其他情况 