from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from logic.member_service import get_member_by_qr, log_action, get_last_action
from ui.new_member_dialog import NewMemberDialog
from ui.history_window import HistoryWindow
from ui.members_window import MembersWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gym Check-In")
        self.setFixedSize(500, 320)
        self._build_ui()
        self._apply_styles()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(14)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Gym Check-In System")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #a0a8d0;")

        self.status_label = QLabel("Scan QR Code to check in / out")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Segoe UI", 11))
        self.status_label.setStyleSheet("color: #7a7aaa;")

        self.scan_input = QLineEdit()
        self.scan_input.setPlaceholderText("QR code appears here...")
        self.scan_input.setFixedHeight(42)
        self.scan_input.returnPressed.connect(self.handle_scan)

        self.history_btn = QPushButton("View History")
        self.history_btn.setFixedHeight(38)
        self.history_btn.clicked.connect(self.open_history)

        self.add_member_btn = QPushButton("Add New Member")
        self.add_member_btn.setFixedHeight(38)
        self.add_member_btn.clicked.connect(self.open_new_member)

        self.members_btn = QPushButton("View All Members")
        self.members_btn.setFixedHeight(38)
        self.members_btn.clicked.connect(self.open_members)

        layout.addWidget(title)
        layout.addSpacing(6)
        layout.addWidget(self.status_label)
        layout.addWidget(self.scan_input)
        layout.addWidget(self.history_btn)
        layout.addWidget(self.members_btn)
        layout.addWidget(self.add_member_btn)
        self.setLayout(layout)
        self.scan_input.setFocus()

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a2e;
                font-family: Segoe UI;
                color: #e0e0e0;
            }
            QLineEdit {
                background: #16213e;
                border: 1px solid #3a3a5c;
                border-radius: 8px;
                padding: 6px 14px;
                font-size: 13px;
                color: #e0e0e0;
            }
            QLineEdit:focus {
                border: 1px solid #5a5aab;
            }
            QPushButton {
                background-color: #0f3460;
                color: #c0c8f0;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1a4a80;
            }
            QPushButton:pressed {
                background-color: #0a2540;
            }
        """)

    def handle_scan(self):
        qr_value = self.scan_input.text().strip()
        self.scan_input.clear()

        member = get_member_by_qr(qr_value)

        if not member:
            dialog = NewMemberDialog(qr_value, self)
            dialog.exec()
            self.status_label.setText("New member registered ✓")
            self.status_label.setStyleSheet("color: #4aaa70;")
        else:
            last = get_last_action(member.id)
            action = "OUT" if last == "IN" else "IN"
            log_action(member.id, action)
            color = "#4aaa70" if action == "IN" else "#e05555"
            self.status_label.setText(f"{member.name} checked {action} ✓")
            self.status_label.setStyleSheet(f"color: {color};")

    def open_history(self):
        self.history_window = HistoryWindow()
        self.history_window.show()

    def open_new_member(self):
        dialog = NewMemberDialog(parent=self)
        dialog.exec()
    
    def open_members(self):
        self.members_window = MembersWindow()
        self.members_window.show()