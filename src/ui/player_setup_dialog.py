from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

class PlayerSetupDialog(QDialog):
    def __init__(self, max_players=5):
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
            name_edit.textChanged.connect(
                lambda text, idx=i: self.try_load_saved_avatar(idx, text)
            )
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

    def try_load_saved_avatar(self, index: int, name: str):
        name = name.strip()
        if not name:
            return

        # Only load if user has NOT manually selected an avatar yet
        if self.original_images[index] is not None:
            return

        pixmap = self._load_saved_avatar(name)
        if pixmap:
            self.original_images[index] = pixmap

            preview = pixmap.scaled(
                40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.avatar_labels[index].setPixmap(preview)
            self.avatar_labels[index].setStyleSheet("")

    def _avatar_dir(self, name: str) -> str:
        return os.path.join("avatars", name.lower())

    def _load_saved_avatar(self, name: str) -> QPixmap | None:
        folder = self._avatar_dir(name)
        if not os.path.isdir(folder):
            return None

        for ext in ("png", "jpg", "jpeg"):
            path = os.path.join(folder, f"avatar.{ext}")
            if os.path.exists(path):
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    return pixmap
        return None

    def _save_avatar(self, name: str, pixmap: QPixmap):
        folder = self._avatar_dir(name)
        os.makedirs(folder, exist_ok=True)

        path = os.path.join(folder, "avatar.png")
        pixmap.save(path, "PNG")

    def pick_avatar(self, index):
        file_path, _ = QFileDialog.getOpenFileName(self, "Avatar auswählen", "", "Images (*.png *.jpg *.bmp)")
        if not file_path:
            return

        original_pixmap = QPixmap(file_path)
        if original_pixmap.isNull():
            return

        self.original_images[index] = original_pixmap

        preview_pixmap = original_pixmap.scaled(
            40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.avatar_labels[index].setPixmap(preview_pixmap)
        self.avatar_labels[index].setStyleSheet("") # remove border

        # Save avatar if name exists
        name = self.name_edits[index].text().strip()
        if name:
            self._save_avatar(name, original_pixmap)

    def get_players(self):
        result = []
        for i in range(self.max_players):
            name = self.name_edits[i].text().strip()
            avatar = self.original_images[i] 
            
            if name:
                result.append({"name": name, "avatar": avatar})
        return result
