from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                              QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from logic.member_service import get_all_members
from datetime import datetime

class MembersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("All Members")
        self.setMinimumSize(780, 500)
        self.all_members = []
        self._build_ui()
        self._load_members()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("All Members")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #a0a8d0;")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by name...")
        self.search_bar.setFixedHeight(36)
        self.search_bar.textChanged.connect(self._filter)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Phone", "Birthday", "Subscription", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(1, 130)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 110)
        self.table.setColumnWidth(4, 160)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.horizontalHeader().setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.table.cellDoubleClicked.connect(self._open_profile)

        hint = QLabel("Double-click a row to view member profile")
        hint.setStyleSheet("color: #4a4a7a; font-size: 11px;")

        self.count_label = QLabel()
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.count_label.setStyleSheet("color: #5a5a8a; font-size: 12px;")

        layout.addWidget(title)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.table)
        layout.addWidget(hint)
        layout.addWidget(self.count_label)
        self.setLayout(layout)
        self._apply_styles()

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #1a1a2e; font-family: Segoe UI; color: #e0e0e0; }
            QLabel { color: #e0e0e0; }
            QLineEdit {
                border: 1px solid #3a3a5c; border-radius: 6px;
                padding: 6px 12px; font-size: 13px;
                background: #16213e; color: #e0e0e0;
            }
            QLineEdit:focus { border: 1px solid #5a5aab; }
            QTableWidget {
                background: #16213e; border: 1px solid #2a2a4a;
                border-radius: 8px; font-size: 13px;
                alternate-background-color: #1e1e3a; color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: #0f3460; color: #a0a8d0;
                padding: 8px; border: none;
                border-bottom: 1px solid #2a2a4a; font-weight: bold;
            }
            QTableWidget::item { padding: 6px 10px; }
            QTableWidget::item:selected { background-color: #0f3460; color: #fff; }
            QScrollBar:vertical { background: #16213e; width: 8px; border-radius: 4px; }
            QScrollBar::handle:vertical { background: #3a3a5c; border-radius: 4px; }
            QScrollBar::handle:vertical:hover { background: #5a5aab; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

    def _load_members(self):
        self.all_members = get_all_members()
        self._populate_table(self.all_members)

    def _populate_table(self, members):
        self.table.setRowCount(len(members))
        now = datetime.now()

        for row, member in enumerate(members):
            days_left = (member.subscription_expires - now).days

            if days_left < 0:
                status = "Expired"
                status_color = "#e05555"
            elif days_left <= 7:
                status = f"Expiring in {days_left}d"
                status_color = "#e0a020"
            else:
                status = f"{days_left} days left"
                status_color = "#4aaa70"

            sub_label = f"{member.subscription_months} Month{'s' if member.subscription_months > 1 else ''}"
            birthday_str = member.birthday.strftime("%d %b %Y") if member.birthday else "—"
            phone_str = member.phone or "—"

            name_item  = QTableWidgetItem(f"  {member.name}")
            phone_item = QTableWidgetItem(f"  {phone_str}")
            bday_item  = QTableWidgetItem(f"  {birthday_str}")
            sub_item   = QTableWidgetItem(f"  {sub_label}")
            status_item = QTableWidgetItem(f"  {status}")

            name_item.setData(Qt.ItemDataRole.UserRole, member.id)
            sub_item.setForeground(QColor("#7a9ad0"))
            status_item.setForeground(QColor(status_color))

            for item in [name_item, phone_item, bday_item, sub_item, status_item]:
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)

            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, phone_item)
            self.table.setItem(row, 2, bday_item)
            self.table.setItem(row, 3, sub_item)
            self.table.setItem(row, 4, status_item)
            self.table.setRowHeight(row, 42)

        self.count_label.setText(f"{len(members)} member{'s' if len(members) != 1 else ''}")

    def _filter(self, text):
        filtered = [m for m in self.all_members if text.lower() in m.name.lower()]
        self._populate_table(filtered)

    def _open_profile(self, row, _col):
        from ui.profile_window import ProfileWindow
        member_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        self.profile_window = ProfileWindow(member_id)
        self.profile_window.show()