from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class PlayerSetupDialog(QDialog):
    def __init__(self, max_players=4):
        super().__init__()
        self.setWindowTitle("Spieler einrichten")
        self.max_players = max_players

        # List to store original High-Res images
        self.original_images = [None] * max_players 

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.name_edits = []
        self.avatar_labels = []

        for i in range(self.max_players):
            row = QHBoxLayout()

            # Player name
            name_edit = QLineEdit()
            name_edit.setPlaceholderText(f"Spieler {i+1} Name")
            row.addWidget(name_edit)
            self.name_edits.append(name_edit)

            # Avatar Label (Small Preview)
            avatar_label = QLabel()
            avatar_label.setFixedSize(40, 40)
            avatar_label.setStyleSheet("border: 1px solid gray;")
            avatar_label.setAlignment(Qt.AlignCenter)
            row.addWidget(avatar_label)
            self.avatar_labels.append(avatar_label)

            # Avatar picker button
            pick_btn = QPushButton("Avatar wählen")
            pick_btn.clicked.connect(lambda checked, idx=i: self.pick_avatar(idx))
            row.addWidget(pick_btn)

            layout.addLayout(row)

        # Buttons
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Abbrechen")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def pick_avatar(self, index):
        file_path, _ = QFileDialog.getOpenFileName(self, "Avatar auswählen", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            # 1. Load image
            original_pixmap = QPixmap(file_path)
            
            # 2. Store full size image
            self.original_images[index] = original_pixmap

            # 3. Create a SMALL copy just for the preview label
            preview_pixmap = original_pixmap.scaled(
                40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            
            self.avatar_labels[index].setPixmap(preview_pixmap)
            self.avatar_labels[index].setStyleSheet("") # remove border

    def get_players(self):
        result = []
        for i in range(self.max_players):
            name = self.name_edits[i].text().strip()
            avatar = self.original_images[i] 
            
            if name:
                result.append({"name": name, "avatar": avatar})
        return result
