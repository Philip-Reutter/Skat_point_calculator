import sys

from PySide6.QtWidgets import QApplication, QDialog

from ui.main_window import MainWindow
from ui.player_setup_dialog import PlayerSetupDialog


def main():
    app = QApplication(sys.argv)

    setup_dialog = PlayerSetupDialog()
    if setup_dialog.exec() == QDialog.Accepted:
        players = setup_dialog.get_players()
        if not players:
            print("Keine Spieler angegeben")
            sys.exit(0)
    else:
        sys.exit(0)

    window = MainWindow(players)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
