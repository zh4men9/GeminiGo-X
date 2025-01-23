from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class GameThemes:
    THEMES = {
        "classic": {
            "board_background": "#DEB887",  # 棕色
            "board_line": Qt.GlobalColor.black,
            "black_piece": Qt.GlobalColor.black,
            "white_piece": Qt.GlobalColor.white,
            "last_move_marker": Qt.GlobalColor.red,
            "background_color": "#f5f5f5",  # 浅灰色
        },
        "modern": {
            "board_background": "#E0E0E0",  # 浅灰色
            "board_line": QColor("#757575"),  # 深灰色
            "black_piece": QColor("#212121"),  # 深灰色
            "white_piece": QColor("#F5F5F5"),  # 亮灰色
            "last_move_marker": Qt.GlobalColor.blue,
            "background_color": "#ECEFF1",  # 蓝灰色
        }
    }

    @staticmethod
    def get_theme(theme_name):
        return GameThemes.THEMES.get(theme_name, GameThemes.THEMES["classic"])

    @staticmethod
    def get_available_themes():
        return list(GameThemes.THEMES.keys()) 