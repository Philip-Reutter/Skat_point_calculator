from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QDialog, QLabel
)
from PySide6.QtGui import QPixmap, QFont, QPainter, QPainterPath
from PySide6.QtCore import Qt
from ui.new_game_dialog import NewGameDialog

def circular_avatar(pixmap: QPixmap, diameter: int) -> QPixmap:
    """
    Returns a circular QPixmap of given diameter, fully filled.
    The circle is fully visible; image is centered and zoomed if needed.
    """
    if pixmap.isNull():
        empty = QPixmap(diameter, diameter)
        empty.fill(Qt.transparent)
        return empty

    # Crop a square from center to fill the circle
    w, h = pixmap.width(), pixmap.height()
    side = min(w, h)
    x = (w - side) // 2
    y = (h - side) // 2
    square = pixmap.copy(x, y, side, side)

    # Scale to diameter
    scaled = square.scaled(diameter, diameter, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

    # Create circular mask
    result = QPixmap(diameter, diameter)
    result.fill(Qt.transparent)
    painter = QPainter(result)
    painter.setRenderHint(QPainter.Antialiasing)
    path = QPainterPath()
    path.addEllipse(0, 0, diameter, diameter)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, scaled)
    painter.end()

    return result


class MainWindow(QMainWindow):
    def __init__(self, players):
        super().__init__()
        self.setWindowTitle("Skat Punkterechner")
        self.players = players
        self.player_names = [p["name"] for p in self.players]
        self.player_avatars = [p.get("avatar") for p in self.players]
        self.games = [] 
        self.total_scores = {p: 0 for p in self.player_names}
        self.resize(550, 800)
        self.width = 550
        self.height = 800
        self.init_ui()

    def init_ui(self):
        self.resize(self.width, self.height)
        central = QWidget()
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)

        # Hide default header
        self.table.horizontalHeader().setVisible(False)
        self.table.setColumnCount(len(self.players))
        col_width = 120
        for col in range(self.table.columnCount()):
            self.table.setColumnWidth(col, col_width)

        self.font = QFont()
        self.font.setPointSize(14)
        self.table.setFont(self.font)
        self.table.verticalHeader().setDefaultSectionSize(30)

        self.has_avatar = any(p.get("avatar") and not p["avatar"].isNull() for p in self.players)

        if self.has_avatar:
            name_row = 1
            self.table.setRowCount(2)
        else:
            name_row = 0
            self.table.setRowCount(1)

        # Track max height for row 0
        if self.has_avatar:

            for col, player in enumerate(self.players):
                avatar_pixmap = player.get("avatar") 
                img_label = QLabel()
                img_label.setAlignment(Qt.AlignCenter)
                img_label.setStyleSheet("border-bottom: 1px solid #ccc;")

                if avatar_pixmap and not avatar_pixmap.isNull():
                        avatar_size = col_width  # width of the column
                        pixmap = circular_avatar(avatar_pixmap, avatar_size)
                        img_label.setPixmap(pixmap)

                self.table.setCellWidget(0, col, img_label)
            self.table.setRowHeight(0, col_width)

        for col, player in enumerate(self.players):
            name_item = QTableWidgetItem(player["name"])
            name_item.setTextAlignment(Qt.AlignCenter)
            header_font = QFont(self.font)
            header_font.setBold(True)
            name_item.setFont(header_font)
            #name_item.setBackground(Qt.lightGray)
            name_item.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(name_row, col, name_item)

        self.table.setRowHeight(name_row, 40)
        layout.addWidget(self.table)

        # Buttons
        self.new_game_btn = QPushButton("Neues Spiel hinzufügen")
        self.new_game_btn.setFont(self.font)
        self.new_game_btn.setMinimumHeight(40)
        self.new_game_btn.clicked.connect(self.add_new_game)
        layout.addWidget(self.new_game_btn)

        self.undo_btn = QPushButton("Letztes Spiel löschen")
        self.undo_btn.setFont(self.font)
        self.undo_btn.setMinimumHeight(40)
        self.undo_btn.clicked.connect(self.undo_last_game)
        layout.addWidget(self.undo_btn)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def add_new_game(self):
        dialog = NewGameDialog(self.player_names)
        if dialog.exec() == QDialog.Accepted:
            game_data = dialog.get_game_data()
            self.games.append(game_data)
            self.update_score_table()

    def update_score_table(self):
        # Keep 2 rows for avatar and name
        score_start_row = 2 if self.has_avatar else 1
        max_rows = max([len([g for g in self.games if g["player"] == p]) for p in self.player_names])
        self.table.setRowCount(score_start_row + max_rows)
        self.total_scores = {p: 0 for p in self.player_names}

        for row_index in range(max_rows):
            for col_index, player in enumerate(self.player_names):
                player_games = [g for g in self.games if g["player"] == player]

                if row_index < len(player_games):
                    score = player_games[row_index]["score"]
                    if row_index > 0:
                        prev_item = self.table.item(score_start_row + row_index - 1, col_index)
                        prev_score = int(prev_item.text()) if prev_item else 0
                        score += prev_score
                    item = QTableWidgetItem(str(score))
                    item.setFont(self.font)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(score_start_row + row_index, col_index, item)
                else:
                    self.table.setItem(score_start_row + row_index, col_index, QTableWidgetItem(""))

        for player in self.player_names:
            player_games = [g for g in self.games if g["player"] == player]
            if player_games:
                self.total_scores[player] = int(
                    self.table.item(score_start_row + len(player_games)-1, self.player_names.index(player)).text()
                )

    def undo_last_game(self):
        if self.games:
            self.games.pop()  # entfernt das letzte Spiel
            self.update_score_table()
