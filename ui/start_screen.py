from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import state
from config import BRANCHES

class StartScreen(QWidget):
    def __init__(self, on_branch_selected):
        super().__init__()
        self.on_branch_selected = on_branch_selected
        self.setWindowTitle("Gym App")
        self.setFixedSize(400, 280)
        self._build_ui()
        self._apply_styles()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(14)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Select Branch")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #a0a8d0;")

        subtitle = QLabel("Which branch are you operating from?")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #5a5a8a; font-size: 12px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)

        for branch in BRANCHES:
            btn = QPushButton(branch)
            btn.setFixedHeight(46)
            btn.clicked.connect(lambda _, b=branch: self.select_branch(b))
            layout.addWidget(btn)

        self.setLayout(layout)

    def select_branch(self, branch):
        state.CURRENT_BRANCH = branch
        self.on_branch_selected()
        self.close()

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #1a1a2e; font-family: Segoe UI; }
            QLabel { color: #e0e0e0; }
            QPushButton {
                background-color: #0f3460; color: #c0c8f0;
                border: none; border-radius: 10px;
                font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background-color: #1a4a80; }
            QPushButton:pressed { background-color: #0a2540; }
        """)