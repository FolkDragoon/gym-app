from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from logic.member_service import get_member_by_id, get_member_logs
from datetime import datetime

class ProfileWindow(QWidget):
    def __init__(self, member_id: str):
        super().__init__()
        self.member_id = member_id
        self.setWindowTitle("Member Profile")
        self.setMinimumSize(520, 560)
        self._build_ui()
        self._apply_styles()

    def _build_ui(self):
        member = get_member_by_id(self.member_id)
        logs = get_member_logs(self.member_id)

        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        name_label = QLabel(member.name)
        name_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("color: #c0c8f0;")

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card_layout.setSpacing(10)
        card_layout.setContentsMargins(20, 16, 20, 16)

        phone = member.phone or "Not provided"
        sub_label = f"{member.subscription_months} Month{'s' if member.subscription_months > 1 else ''}"
        expires = member.subscription_expires
        now = datetime.now()
        days_left = (expires - now).days
        expired = days_left < 0

        # Birthday & age
        bday = member.birthday
        age = now.year - bday.year - ((now.month, now.day) < (bday.month, bday.day))
        birthday_display = f"{bday.strftime('%d %b %Y')}  ({age} years old)"

        card_layout.addWidget(self._info_row("📞  Phone", phone))
        card_layout.addWidget(self._divider())
        card_layout.addWidget(self._info_row("🎂  Birthday", birthday_display))
        card_layout.addWidget(self._divider())
        card_layout.addWidget(self._info_row("📋  Subscription", sub_label))
        card_layout.addWidget(self._divider())
        card_layout.addWidget(self._info_row("📅  Expires", expires.strftime("%d %b %Y")))
        card_layout.addWidget(self._divider())

        if expired:
            status_val = f"Expired {abs(days_left)} days ago"
            status_color = "#e05555"
        elif days_left <= 7:
            status_val = f"Expiring in {days_left} day{'s' if days_left != 1 else ''}"
            status_color = "#e0a020"
        else:
            status_val = f"{days_left} days remaining"
            status_color = "#4aaa70"

        status_row = self._info_row("🟢  Status", status_val)
        status_row.findChildren(QLabel)[1].setStyleSheet(f"color: {status_color}; font-weight: bold;")
        card_layout.addWidget(status_row)
        card.setLayout(card_layout)

        activity_label = QLabel("Recent Activity")
        activity_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        activity_label.setStyleSheet("color: #a0a8d0;")

        self.log_table = QTableWidget()
        self.log_table.setColumnCount(2)
        self.log_table.setHorizontalHeaderLabels(["Action", "Date & Time"])
        self.log_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.log_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.log_table.setColumnWidth(0, 100)
        self.log_table.verticalHeader().setVisible(False)
        self.log_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.log_table.setShowGrid(False)
        self.log_table.setAlternatingRowColors(True)
        self.log_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.log_table.horizontalHeader().setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))

        self.log_table.setRowCount(len(logs))
        for row, (action, timestamp) in enumerate(logs):
            action_item = QTableWidgetItem(f"  {'🟢 IN' if action == 'IN' else '🔴 OUT'}")
            time_item = QTableWidgetItem(f"  {timestamp.strftime('%a, %d %b %Y  —  %I:%M %p')}")
            action_item.setForeground(QColor("#1a7a3e" if action == "IN" else "#b02020"))
            for item in [action_item, time_item]:
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.log_table.setItem(row, 0, action_item)
            self.log_table.setItem(row, 1, time_item)
            self.log_table.setRowHeight(row, 38)

        layout.addWidget(name_label)
        layout.addWidget(card)
        layout.addWidget(activity_label)
        layout.addWidget(self.log_table)
        self.setLayout(layout)

    def _info_row(self, label: str, value: str):
        row = QWidget()
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        lbl = QLabel(label)
        lbl.setStyleSheet("color: #6a6a9a; font-size: 12px;")
        val = QLabel(value)
        val.setStyleSheet("color: #e0e0e0; font-size: 13px;")
        val.setAlignment(Qt.AlignmentFlag.AlignRight)
        row_layout.addWidget(lbl)
        row_layout.addWidget(val)
        row.setLayout(row_layout)
        return row

    def _divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #2a2a4a;")
        return line

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #1a1a2e; font-family: Segoe UI; color: #e0e0e0; }
            QFrame#card {
                background-color: #16213e;
                border: 1px solid #2a2a4a;
                border-radius: 10px;
            }
            QTableWidget {
                background: #16213e;
                border: 1px solid #2a2a4a;
                border-radius: 8px;
                font-size: 13px;
                alternate-background-color: #1e1e3a;
                color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: #0f3460;
                color: #a0a8d0;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #2a2a4a;
                font-weight: bold;
            }
            QTableWidget::item { padding: 6px 10px; }
            QTableWidget::item:selected { background-color: #0f3460; color: #fff; }
            QScrollBar:vertical {
                background: #16213e; width: 8px; border-radius: 4px;
            }
            QScrollBar::handle:vertical { background: #3a3a5c; border-radius: 4px; }
            QScrollBar::handle:vertical:hover { background: #5a5aab; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)