from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QSpinBox, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from logic.skat_calculator import calculate_score


class Tile(QFrame):
    toggled = Signal(bool)  # emits True if active, False if inactive
    def __init__(self, text, total_width, active_color="#075ad6", inactive_color="#a5a1a1", parent=None):
        super().__init__(parent)
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.active = False

        self.setStyleSheet(f"background-color: {self.inactive_color}; border-radius: 8px;")
        self.setFixedSize(total_width/2 - total_width/10, 40)  # size of the tile

        # label
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 14px;")
        self.label.setGeometry(0, 0, total_width/2 - total_width/10, 40)

    def mousePressEvent(self, event):
        self.active = not self.active
        color = self.active_color if self.active else self.inactive_color
        self.setStyleSheet(f"background-color: {color}; border-radius: 8px;")
        self.toggled.emit(self.active)


class ExclusiveTile(Tile):
    """A Tile that is part of a mutually exclusive group."""
    def __init__(self, text, total_width, group=None, start_active=False, active_color="#075ad6", inactive_color="#a5a1a1"):
        super().__init__(text, total_width, active_color, inactive_color)
        self.group = group
        if group is not None:
            group.append(self)
        self.active = start_active
        if self.active:
            self.setStyleSheet(f"background-color: {self.active_color}; border-radius: 8px;")

    def mousePressEvent(self, event):
        if not self.active:
            # deactivate all other tiles in group
            if self.group is not None:
                for tile in self.group:
                    tile.active = False
                    tile.setStyleSheet(f"background-color: {tile.inactive_color}; border-radius: 8px;")
            # activate this tile
            self.active = True
            self.setStyleSheet(f"background-color: {self.active_color}; border-radius: 8px;")
            self.toggled.emit(True)


class NewGameDialog(QDialog):
    def __init__(self, players):
        super().__init__()
        self.setWindowTitle("Neues Spiel hinzufügen")
        self.players = players
        self.selected_player = None
        self.score = 0
        self.init_ui()

    def init_ui(self):
        self.width = 520
        self.height = 450

        self.font = QFont()
        self.font.setPointSize(12)

        layout = QVBoxLayout()

        # Player selector
        player_layout = QHBoxLayout()
        self.player_label = QLabel("Spieler:", self)
        #self.player_label.setAlignment(Qt.AlignCenter)
        self.player_label.setStyleSheet("font-size: 14px;")
        player_layout.addWidget(self.player_label)
        self.player_combo = QComboBox()
        self.player_combo.setFont(self.font)
        self.player_combo.addItems(self.players)
        player_layout.addWidget(self.player_combo)
        layout.addLayout(player_layout)

        # Game type dropdown
        type_layout = QHBoxLayout()
        self.game_type_label = QLabel("Spiel:", self)
        #self.game_type_label.setAlignment(Qt.AlignCenter)
        self.game_type_label.setStyleSheet("font-size: 14px;")
        type_layout.addWidget(self.game_type_label)
        self.game_type_combo = QComboBox()
        self.game_type_combo.setFont(self.font)
        self.game_type_combo.addItems(["Grand", "Kreuz", "Pik", "Herz", "Karo", "Null"])
        type_layout.addWidget(self.game_type_combo)
        layout.addLayout(type_layout)

        # Base value (spinbox) - simple, starts at 0
        base_layout = QHBoxLayout()
        self.game_label = QLabel("Mit/Ohne:", self)
        #self.game_label.setAlignment(Qt.AlignCenter)
        self.game_label.setStyleSheet("font-size: 14px;")
        base_layout.addWidget(self.game_label)
        self.game_spin = QSpinBox()
        self.game_spin.setFont(self.font)
        self.game_spin.setRange(1, 4)
        base_layout.addWidget(self.game_spin)
        layout.addLayout(base_layout)

        # Checkboxes for Hand, Schneider, Schwarz, Ouvert, Kontra, Re
        self.hand_tile = Tile("Hand", self.width)
        self.schneider_announced_tile = Tile("Schneider angesagt", self.width)
        self.schneider_tile = Tile("Schneider", self.width)
        self.schwarz_announced_tile = Tile("Schwarz angesagt", self.width)
        self.schwarz_tile = Tile("Schwarz", self.width)
        self.ouvert_tile = Tile("Ouvert", self.width)
        self.kontra_tile = Tile("Kontra", self.width)
        self.re_tile = Tile("Re", self.width)

        layout.addSpacing(20)

        # Row 1: Hand, Ouvert
        row1 = QHBoxLayout()
        row1.addWidget(self.hand_tile)
        row1.addWidget(self.ouvert_tile)
        layout.addLayout(row1)

        # Row 2: Schneider, Schneider angesagt
        row2 = QHBoxLayout()
        row2.addWidget(self.schneider_tile)
        row2.addWidget(self.schneider_announced_tile)
        layout.addLayout(row2)

        # Row 3: Schwarz, Schwarz angesagt
        row3 = QHBoxLayout()
        row3.addWidget(self.schwarz_tile)
        row3.addWidget(self.schwarz_announced_tile)
        layout.addLayout(row3)

        # Row 4: Kontra, Re
        row4 = QHBoxLayout()
        row4.addWidget(self.kontra_tile)
        row4.addWidget(self.re_tile)
        layout.addLayout(row4)
        
        layout.addSpacing(20)

        self.all_non_null_boxes = [
            self.game_label, self.game_spin, self.schneider_announced_tile, self.schneider_tile,
            self.schwarz_announced_tile, self.schwarz_tile
        ]

        self.result_tiles_group = []
        self.won_tile = ExclusiveTile("Gewonnen", self.width, group=self.result_tiles_group, start_active=True, active_color="#0a8106")
        self.lost_tile = ExclusiveTile("Verloren", self.width, group=self.result_tiles_group, active_color="#c51010")
        result_layout = QHBoxLayout()
        result_layout.addWidget(self.won_tile)
        result_layout.addWidget(self.lost_tile)
        layout.addLayout(result_layout)

        # Result label
        self.result_label = QLabel("Punkte: 0")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.result_label)

        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Speichern")
        self.save_btn.setStyleSheet("font-size: 14px;")
        self.cancel_btn = QPushButton("Abbrechen")
        self.cancel_btn.setStyleSheet("font-size: 14px;")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Connect signals
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        self.game_type_combo.currentTextChanged.connect(self.update_checkboxes)
        self.game_type_combo.currentTextChanged.connect(self.update_score)
        self.game_spin.valueChanged.connect(self.update_score)
        for tile in [self.hand_tile, self.schneider_announced_tile,self.schneider_tile, self.schwarz_announced_tile,
                     self.schwarz_tile, self.kontra_tile, self.re_tile, self.ouvert_tile]:
            tile.toggled.connect(self.update_score)
        self.won_tile.toggled.connect(self.update_score)
        self.lost_tile.toggled.connect(self.update_score)

        # Initial score
        self.update_checkboxes(self.game_type_combo.currentText())
        self.update_score()

        self.resize(self.width, self.height)

    def update_checkboxes(self, game_type):
        if game_type == "Null":
            for box in self.all_non_null_boxes:
                box.setVisible(False)
        else:
            for box in self.all_non_null_boxes:
                box.setVisible(True)

    def update_score(self):
        self.score = calculate_score(
            hand=self.hand_tile.active,
            ouvert=self.ouvert_tile.active,
            schneider=self.schneider_tile.active,
            game_type=self.game_type_combo.currentText(),
            jacks=self.game_spin.value(),
            schneider_announced=self.schneider_announced_tile.active,
            schwarz_announced=self.schwarz_announced_tile.active,
            schwarz=self.schwarz_tile.active,
            kontra=self.kontra_tile.active,
            re=self.re_tile.active,
            won=self.won_tile.active
        )
        self.result_label.setText(f"Punkte: {self.score}")

    def get_game_data(self):
        return {
            "player": self.player_combo.currentText(),
            "game_type": self.game_type_combo.currentText(),
            "spiel": self.game_spin.value(),
            "hand": self.hand_tile.active,
            "schneider_announced": self.schneider_announced_tile.active,
            "schneider": self.schneider_tile.active,
            "schwarz_announced": self.schwarz_announced_tile.active,
            "schwarz": self.schwarz_tile.active,
            "ouvert": self.ouvert_tile.active,
            "kontra": self.kontra_tile.active,
            "re": self.re_tile.active,
            "won": self.won_tile.active,
            "score": self.score
        }
