from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QDialog, QLabel
)
from PySide6.QtGui import QPixmap, QFont, QPainter, QPainterPath
from PySide6.QtCore import Qt
from ui.new_game_dialog import NewGameDialog
from ui.player_setup_dialog import PlayerSetupDialog

def empty_avatar(diameter: int) -> QPixmap:
    pm = QPixmap(diameter, diameter)
    pm.fill(Qt.transparent)

    painter = QPainter(pm)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(Qt.lightGray)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, diameter, diameter)
    painter.end()

    return pm

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
        self.width = 650
        self.height = 800
        self.init_ui()

    def init_ui(self):
        self.resize(self.width, self.height)
        central = QWidget()
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setColumnCount(len(self.players))
        self.col_width = 120
        for col in range(self.table.columnCount()):
            self.table.setColumnWidth(col, self.col_width)

        self.font = QFont()
        self.font.setPointSize(14)
        self.table.setFont(self.font)
        self.table.verticalHeader().setDefaultSectionSize(30)

        # Avatar and name rows
        self.has_avatar = any(p.get("avatar") and not p["avatar"].isNull() for p in self.players)
        name_row = 1 if self.has_avatar else 0
        self.table.setRowCount(2 if self.has_avatar else 1)

        if self.has_avatar:
            for col, player in enumerate(self.players):
                avatar_pixmap = player.get("avatar") 
                img_label = QLabel()
                img_label.setAlignment(Qt.AlignCenter)
                img_label.setStyleSheet("border-bottom: 1px solid #ccc;")
                if avatar_pixmap and not avatar_pixmap.isNull():
                    pixmap = circular_avatar(avatar_pixmap, self.col_width)
                else:
                    pixmap = empty_avatar(self.col_width)
                img_label.setPixmap(pixmap)
                self.table.setCellWidget(0, col, img_label)
            self.table.setRowHeight(0, self.col_width)

        for col, player in enumerate(self.players):
            name_item = QTableWidgetItem(player["name"])
            name_item.setTextAlignment(Qt.AlignCenter)
            header_font = QFont(self.font)
            header_font.setBold(True)
            name_item.setFont(header_font)
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

        self.add_player_btn = QPushButton("Spieler hinzufügen")
        self.add_player_btn.setFont(self.font)
        self.add_player_btn.setMinimumHeight(40)
        self.add_player_btn.clicked.connect(self.add_new_player)
        layout.addWidget(self.add_player_btn)
        self.update_add_player_button_visibility() # Show button only if <5 players

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

    def update_add_player_button_visibility(self):
        """Show button only if <5 players"""
        self.add_player_btn.setVisible(len(self.players) < 5)

    def add_new_player(self):
        # Open PlayerSetupDialog for just 1 player
        dialog = PlayerSetupDialog(max_players=1)
        dialog.setWindowTitle("Neuen Spieler hinzufügen")
        if dialog.exec() == QDialog.Accepted:
            new_players = dialog.get_players()
            if not new_players:
                return

            new_player = new_players[0]
            self.players.append(new_player)
            self.player_names.append(new_player["name"])
            self.player_avatars.append(new_player.get("avatar"))
            self.total_scores[new_player["name"]] = 0

            # Add new column in table
            col_index = self.table.columnCount()
            self.table.setColumnCount(col_index + 1)
            self.table.setColumnWidth(col_index, 120)

            avatar_pixmap = new_player.get("avatar")
            avatar_present = avatar_pixmap and not avatar_pixmap.isNull()

            # If this is the first avatar
            if avatar_present and not self.has_avatar:
                self.has_avatar = True
                self.table.insertRow(0)
                self.table.setRowHeight(0, self.col_width)

                # Placeholder avatars for existing players
                for c in range(col_index):
                    placeholder = QLabel()
                    placeholder.setAlignment(Qt.AlignCenter)
                    placeholder.setPixmap(empty_avatar(self.col_width))
                    self.table.setCellWidget(0, c, placeholder)

            # If avatar row exists
            if self.has_avatar:
                img_label = QLabel()
                img_label.setAlignment(Qt.AlignCenter)
                if avatar_present:
                    pixmap = circular_avatar(avatar_pixmap, self.col_width)
                else:
                    pixmap = empty_avatar(self.col_width)
                img_label.setPixmap(pixmap)
                self.table.setCellWidget(0, col_index, img_label)

            # Add name
            name_row = 1 if self.has_avatar else 0
            name_item = QTableWidgetItem(new_player["name"])
            name_item.setTextAlignment(Qt.AlignCenter)
            header_font = QFont(self.font)
            header_font.setBold(True)
            name_item.setFont(header_font)
            name_item.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(name_row, col_index, name_item)
            self.table.setRowHeight(name_row, 40)

            self.update_add_player_button_visibility()
