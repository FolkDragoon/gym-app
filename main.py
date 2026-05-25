import sys
from PyQt6.QtWidgets import QApplication
from database.db import init_db
from ui.start_screen import StartScreen
from ui.main_window import MainWindow

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)

    main_window = MainWindow()

    def launch_main():
        main_window.show()

    start = StartScreen(on_branch_selected=launch_main)
    start.show()

    sys.exit(app.exec())