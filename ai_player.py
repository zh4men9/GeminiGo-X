import google.generativeai as genai
import json
import os
from typing import Tuple, List

class AIPlayer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.board_size = 15  # 设置棋盘大小
        
    def get_move(self, board_state: List[Tuple[int, int, bool]], board_size: int) -> Tuple[int, int]:
        """
        获取AI的下一步移动
        
        Args:
            board_state: 当前棋盘状态，每个元素为(x, y, is_black)
            board_size: 棋盘大小
        
        Returns:
            (x, y): AI选择的位置
        """
        self.board_size = board_size  # 更新棋盘大小
        # 将棋盘状态转换为更易理解的格式
        board = [[None for _ in range(board_size)] for _ in range(board_size)]
        for x, y, is_black in board_state:
            board[y][x] = "黑" if is_black else "白"
            
        # 构建提示信息
        prompt = self._create_prompt(board)
        
        try:
            # 获取AI响应
            response = self.model.generate_content(prompt)
            if not response.text:
                raise ValueError("AI返回空响应")
                
            move = self._parse_response(response.text)
            
            # 验证移动是否有效
            if self._is_valid_move(move, board_state, board_size):
                return move
                
        except Exception as e:
            print(f"AI错误: {str(e)}")
            
        # 如果出现错误或无效移动，使用简单的策略
        return self._fallback_strategy(board_state, board_size)
        
    def _create_prompt(self, board: List[List[str]]) -> str:
        """创建提示信息"""
        board_str = "\n".join([" ".join(["_" if cell is None else cell for cell in row]) for row in board])
        return f"""
作为五子棋AI，分析当前棋盘状态并给出最佳落子位置。棋盘状态如下（'_'表示空位，'黑'表示黑子，'白'表示白子）：

{board_str}

你执白子。请分析局势并给出下一步最佳落子位置，要求：
1. 优先选择进攻位置
2. 必须阻挡对手即将连成五子的位置
3. 返回格式：{{"x": 数字, "y": 数字}}
只需要返回坐标JSON，不要其他解释。
"""

    def _parse_response(self, response: str) -> Tuple[int, int]:
        """解析AI响应"""
        try:
            # 提取JSON部分
            start = response.find("{")
            end = response.find("}") + 1
            if start != -1 and end != -1:
                move_json = json.loads(response[start:end])
                x, y = int(move_json["x"]), int(move_json["y"])
                if 0 <= x < self.board_size and 0 <= y < self.board_size:
                    return x, y
        except Exception as e:
            print(f"解析AI响应时出错: {str(e)}")
        raise ValueError("无法解析AI响应")

    def _is_valid_move(self, move: Tuple[int, int], board_state: List[Tuple[int, int, bool]], board_size: int) -> bool:
        """检查移动是否有效"""
        x, y = move
        if not (0 <= x < board_size and 0 <= y < board_size):
            return False
        return not any(piece[0] == x and piece[1] == y for piece in board_state)

    def _fallback_strategy(self, board_state: List[Tuple[int, int, bool]], board_size: int) -> Tuple[int, int]:
        """简单的后备策略：找到第一个空位"""
        occupied = set((x, y) for x, y, _ in board_state)
        # 优先选择中心位置
        center = board_size // 2
        if (center, center) not in occupied:
            return (center, center)
            
        # 然后选择靠近中心的位置
        for d in range(1, board_size):
            for i in range(-d, d+1):
                for j in range(-d, d+1):
                    x, y = center + i, center + j
                    if 0 <= x < board_size and 0 <= y < board_size and (x, y) not in occupied:
                        return (x, y)
        raise ValueError("棋盘已满") 