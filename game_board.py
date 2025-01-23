from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QInputDialog, QLineEdit
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QPoint
from game_logic import GameLogic
from themes import GameThemes
from ai_player import AIPlayer
from PyQt6.QtWidgets import QApplication

class GameBoard(QWidget):
    GAME_MODE_NORMAL = "normal"
    GAME_MODE_PUZZLE = "puzzle"
    GAME_MODE_STAGE = "stage"

    def __init__(self):
        super().__init__()
        self.current_game_mode = GameBoard.GAME_MODE_NORMAL # 默认模式为普通模式
        self.board_size = 15  # 15x15的棋盘
        self.cell_size = 40   # 每个格子的大小
        self.margin = 40      # 边距
        self.pieces = []      # 存储棋子位置
        self.is_black_turn = True  # 黑子先手
        self.game_over = False
        self.current_theme = "classic" # 默认主题
        self.game_logic = GameLogic(self.board_size)
        self.ai_player = None
        self.is_ai_enabled = False
        self.themes = {
            "classic": {
                "board_background": "#DEB887", # 棕色
                "board_line": Qt.GlobalColor.black,
                "black_piece": Qt.GlobalColor.black,
                "white_piece": Qt.GlobalColor.white,
                "last_move_marker": Qt.GlobalColor.red,
                "background_color": "#f5f5f5", # 浅灰色
            },
            "modern": {
                "board_background": "#E0E0E0", # 浅灰色
                "board_line": QColor("#757575"), # 深灰色
                "black_piece": QColor("#212121"), # 深灰色
                "white_piece": QColor("#F5F5F5"), # 亮灰色
                "last_move_marker": Qt.GlobalColor.blue,
                "background_color": "#ECEFF1", # 蓝灰色
            }
        }
        
        self.init_ui()

    def init_ui(self):
        # 创建主布局
        main_layout = QHBoxLayout()
        
        # 创建棋盘容器
        self.board_container = QWidget()
        self.board_container.setFixedSize(
            self.board_size * self.cell_size + 2 * self.margin,
            self.board_size * self.cell_size + 2 * self.margin
        )
        self.board_container.paintEvent = self.paintEvent
        
        # 创建控制面板
        control_panel = QVBoxLayout()
        
        # 状态标签
        self.status_label = QLabel("当前回合：黑子")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 5px;
            }
        """)
        
        # 按钮样式
        button_style = """
            QPushButton {
                font-size: 14px;
                padding: 8px;
                min-width: 100px;
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2a5d8c;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """
        
        # 创建按钮
        undo_button = QPushButton("悔棋")
        restart_button = QPushButton("重新开始")
        puzzle_mode_button = QPushButton("残局模式")
        stage_mode_button = QPushButton("闯关模式")
        theme_button = QPushButton("切换主题")
        ai_button = QPushButton("启用AI")
        
        # 设置按钮样式
        for button in [undo_button, restart_button, puzzle_mode_button, stage_mode_button, theme_button, ai_button]:
            button.setStyleSheet(button_style)
        
        # 连接按钮信号
        undo_button.clicked.connect(self.undo_move)
        restart_button.clicked.connect(self.restart_game)
        puzzle_mode_button.clicked.connect(self.enter_puzzle_mode)
        stage_mode_button.clicked.connect(self.enter_stage_mode)
        theme_button.clicked.connect(self.toggle_theme)
        ai_button.clicked.connect(self.toggle_ai)
        
        # 添加控件到控制面板
        control_panel.addWidget(self.status_label)
        control_panel.addWidget(undo_button)
        control_panel.addWidget(restart_button)
        control_panel.addWidget(puzzle_mode_button)
        control_panel.addWidget(stage_mode_button)
        control_panel.addWidget(theme_button)
        control_panel.addWidget(ai_button)
        control_panel.addStretch()
        
        # 设置布局
        main_layout.addWidget(self.board_container)
        main_layout.addLayout(control_panel)
        self.setLayout(main_layout)
        
        # 设置窗口
        self.setWindowTitle('五子棋')
        theme = GameThemes.get_theme(self.current_theme)
        self.setStyleSheet(f"background-color: {theme['background_color']};")
        self.setFixedSize(
            self.board_size * self.cell_size + 2 * self.margin + 150,  # 额外空间给控制面板
            self.board_size * self.cell_size + 2 * self.margin
        )

    def paintEvent(self, event):
        # 创建一个画家对象，绘制到棋盘容器上
        painter = QPainter(self.board_container)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制棋盘背景
        board_rect = QPoint(self.margin, self.margin)
        board_size = (self.board_size - 1) * self.cell_size
        painter.fillRect(
            board_rect.x() - 10, 
            board_rect.y() - 10,
            board_size + 20,
            board_size + 20,
            QBrush(QColor(self.themes[self.current_theme]["board_background"]))  # 棋盘底色
        )
        
        # 绘制棋盘
        self._draw_board(painter)
        # 绘制棋子
        self._draw_pieces(painter)

    def _draw_board(self, painter):
        # 设置画笔
        pen = QPen(self.themes[self.current_theme]["board_line"], 1, Qt.PenStyle.SolidLine)
        painter.setPen(pen)
        
        # 绘制横线和竖线
        for i in range(self.board_size):
            # 横线
            start_y = self.margin + i * self.cell_size
            painter.drawLine(
                self.margin, start_y,
                self.margin + (self.board_size - 1) * self.cell_size, start_y
            )
            
            # 竖线
            start_x = self.margin + i * self.cell_size
            painter.drawLine(
                start_x, self.margin,
                start_x, self.margin + (self.board_size - 1) * self.cell_size
            )
        
        # 绘制天元和星位
        star_points = [(3, 3), (11, 3), (7, 7), (3, 11), (11, 11)]
        for x, y in star_points:
            center = QPoint(self.margin + x * self.cell_size,
                          self.margin + y * self.cell_size)
            painter.setBrush(Qt.GlobalColor.black)
            painter.drawEllipse(center, 3, 3)

    def _draw_pieces(self, painter):
        for i, piece in enumerate(self.game_logic.pieces):
            x, y, is_black = piece
            
            # 设置棋子颜色和效果
            if is_black:
                painter.setBrush(self.themes[self.current_theme]["black_piece"])
                painter.setPen(QPen(QColor("#666666"), 1)) # Pen color remains fixed for outline
            else:
                painter.setBrush(self.themes[self.current_theme]["white_piece"])
                painter.setPen(QPen(QColor("#CCCCCC"), 1)) # Pen color remains fixed for outline
            
            # 绘制棋子
            center = QPoint(self.margin + x * self.cell_size,
                          self.margin + y * self.cell_size)
            radius = self.cell_size // 2 - 2
            painter.drawEllipse(center, radius, radius)
            
            # 标记最后一手棋
            if i == len(self.game_logic.pieces) - 1:
                painter.setPen(QPen(self.themes[self.current_theme]["last_move_marker"], 2))
                marker_size = 3
                painter.drawLine(center.x() - marker_size, center.y(),
                               center.x() + marker_size, center.y())
                painter.drawLine(center.x(), center.y() - marker_size,
                               center.x(), center.y() + marker_size)

    def mousePressEvent(self, event):
        if self.game_logic.game_over:
            return
            
        # 如果是AI的回合，不允许玩家操作
        if self.is_ai_enabled and not self.game_logic.is_black_turn:
            QMessageBox.warning(self, "提示", "当前是AI的回合！")
            return
            
        # 获取相对于board_container的位置
        pos = self.board_container.mapFromParent(event.pos())
        x = round((pos.x() - self.margin) / self.cell_size)
        y = round((pos.y() - self.margin) / self.cell_size)
        
        # 检查是否在有效范围内
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            # 检查该位置是否已有棋子
            if not self.game_logic.is_valid_move(x, y):
                return
                    
            # 添加新棋子
            if self.game_logic.add_piece(x, y):
                # 检查是否获胜
                if self.game_logic.game_over:
                    winner = "黑方" if not self.game_logic.is_black_turn else "白方"
                    QMessageBox.information(self, "游戏结束", f"{winner}获胜！")
                elif self.is_ai_enabled:
                    # 更新状态为等待AI
                    self.status_label.setText("AI思考中...")
                    QApplication.processEvents()  # 立即更新UI
                    # AI下棋
                    self.make_ai_move()
                
                self.update_status()
                self.update()
                
    def make_ai_move(self):
        """AI下棋"""
        if self.ai_player and not self.game_logic.game_over:
            try:
                x, y = self.ai_player.get_move(self.game_logic.pieces, self.board_size)
                if self.game_logic.add_piece(x, y):
                    if self.game_logic.game_over:
                        winner = "AI" if not self.game_logic.is_black_turn else "玩家"
                        QMessageBox.information(self, "游戏结束", f"{winner}获胜！")
                    self.update_status()
                    self.update()
            except Exception as e:
                QMessageBox.warning(self, "AI错误", f"AI下棋出错：{str(e)}")
                self.game_logic.is_black_turn = not self.game_logic.is_black_turn  # 切换回玩家回合
                
    def update_status(self):
        """更新状态标签"""
        if self.game_logic.game_over:
            return
            
        if self.is_ai_enabled:
            current_player = "你的回合" if self.game_logic.is_black_turn else "AI思考中..."
        else:
            current_player = "黑" if self.game_logic.is_black_turn else "白"
            current_player += "子回合"
        self.status_label.setText(current_player)

    def undo_move(self):
        if self.is_ai_enabled:
            # AI模式下悔棋需要撤销两步
            self.game_logic.undo_move()
            self.game_logic.undo_move()
        else:
            self.game_logic.undo_move()
        self.update_status()
        self.update()

    def restart_game(self):
        self.game_logic.reset_game()
        self.update_status()
        self.update()

    def _check_win(self, x, y):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 水平、垂直、对角线方向
        for dx, dy in directions:
            count = 1  # 当前方向的连续棋子数
            
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
        for piece in self.game_logic.pieces:
            if piece[0] == x and piece[1] == y and piece[2] == self.game_logic.is_black_turn:
                return True
        return False

    def update_board(self):
        self.board_container.update()

    def enter_puzzle_mode(self):
        if self.current_game_mode != GameBoard.GAME_MODE_PUZZLE:
            self.current_game_mode = GameBoard.GAME_MODE_PUZZLE
            self.status_label.setText("当前模式：残局模式")
            self.game_logic.pieces = self._load_puzzle_scenario() # 加载残局
            self.game_logic.is_black_turn = True # 默认黑子先
            self.game_logic.game_over = False
            self.update()

    def enter_stage_mode(self):
        if self.current_game_mode != GameBoard.GAME_MODE_STAGE:
            self.current_game_mode = GameBoard.GAME_MODE_STAGE
            self.status_label.setText("当前模式：闯关模式")
            self.game_logic.pieces = [] # 闯关模式初始为空棋盘，或者可以加载关卡数据
            self.game_logic.is_black_turn = True # 默认黑子先
            self.game_logic.game_over = False
            self.update()

    def enter_normal_mode(self):
        if self.current_game_mode != GameBoard.GAME_MODE_NORMAL:
            self.current_game_mode = GameBoard.GAME_MODE_NORMAL
            self.status_label.setText("当前模式：普通模式")
            self.game_logic.pieces = [] # 普通模式重置棋盘
            self.game_logic.is_black_turn = True # 默认黑子先
            self.game_logic.game_over = False
            self.update()

    def _load_puzzle_scenario(self):
        # 这里定义一个残局的初始棋盘配置
        # 示例：一个简单的残局，执黑先走
        return [
            (7, 7, False),  # 白子
            (8, 7, False),
            (9, 7, False),
            (10, 7, False),
            (7, 8, False),
            (8, 8, True),   # 黑子
            (9, 8, True),
            (10, 8, True),
            (7, 9, False),
            (8, 9, True),
            (9, 9, True),
            (7, 10, False),
            (8, 10, True),
        ] 

    def toggle_theme(self):
        if self.current_theme == "classic":
            self.current_theme = "modern"
        else:
            self.current_theme = "classic"
        theme = GameThemes.get_theme(self.current_theme)
        self.setStyleSheet(f"background-color: {theme['background_color']};")
        self.update()

    def toggle_ai(self):
        """切换AI状态"""
        if not self.is_ai_enabled:
            api_key, ok = QInputDialog.getText(
                self, "启用AI", "请输入Gemini API密钥：", 
                QLineEdit.EchoMode.Password
            )
            if ok and api_key:
                try:
                    # 创建临时AI对象测试API密钥
                    test_ai = AIPlayer(api_key)
                    # 测试API是否可用
                    test_response = test_ai.model.generate_content("测试API连接")
                    if test_response:
                        self.ai_player = test_ai
                        self.is_ai_enabled = True
                        self.game_logic.reset_game()  # 重置游戏
                        QMessageBox.information(self, "成功", "AI已启用！你执黑子（先手），AI执白子。")
                        self.update_status()
                except Exception as e:
                    QMessageBox.warning(self, "错误", f"API密钥无效或连接失败：{str(e)}")
        else:
            self.is_ai_enabled = False
            self.ai_player = None
            self.game_logic.reset_game()  # 重置游戏
            QMessageBox.information(self, "提示", "AI已禁用！返回双人模式。")
            self.update_status()