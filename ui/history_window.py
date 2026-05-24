from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from logic.member_service import get_all_logs
from ui.profile_window import ProfileWindow

class HistoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Entry / Exit History")
        self.setMinimumSize(820, 500)
        self.all_logs = []
        self._build_ui()
        self._load_logs()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Entry / Exit History")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #a0a8d0;")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by member name...")
        self.search_bar.setFixedHeight(36)
        self.search_bar.textChanged.connect(self._filter_logs)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Member", "Subscription", "Action", "Date & Time"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 230)
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
        hint.setAlignment(Qt.AlignmentFlag.AlignLeft)

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
                border: 1px solid #3a3a5c;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                background: #16213e;
                color: #e0e0e0;
            }
            QLineEdit:focus { border: 1px solid #5a5aab; }
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
            QTableWidget::item:selected { background-color: #0f3460; color: #ffffff; }
            QScrollBar:vertical {
                background: #16213e; width: 8px; border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #3a3a5c; border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover { background: #5a5aab; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

    def _load_logs(self):
        self.all_logs = get_all_logs()
        self._populate_table(self.all_logs)

    def _populate_table(self, logs):
        self.table.setRowCount(len(logs))

        for row, (member_id, name, sub_months, action, timestamp) in enumerate(logs):
            sub_label = f"{sub_months} Month{'s' if sub_months > 1 else ''}"

            name_item = QTableWidgetItem(f"  {name}")
            sub_item = QTableWidgetItem(f"  {sub_label}")
            action_item = QTableWidgetItem(f"  {'🟢 IN' if action == 'IN' else '🔴 OUT'}")
            time_item = QTableWidgetItem(f"  {timestamp.strftime('%a, %d %b %Y  —  %I:%M %p')}")

            # store member_id for profile lookup on double click
            name_item.setData(Qt.ItemDataRole.UserRole, member_id)

            action_item.setForeground(QColor("#1a7a3e" if action == "IN" else "#b02020"))
            sub_item.setForeground(QColor("#7a9ad0"))

            for item in [name_item, sub_item, action_item, time_item]:
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)

            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, sub_item)
            self.table.setItem(row, 2, action_item)
            self.table.setItem(row, 3, time_item)
            self.table.setRowHeight(row, 42)

        self.count_label.setText(f"{len(logs)} record{'s' if len(logs) != 1 else ''}")

    def _filter_logs(self, text):
        filtered = [l for l in self.all_logs if text.lower() in l[1].lower()]
        self._populate_table(filtered)

    def _open_profile(self, row, _col):
        member_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        self.profile_window = ProfileWindow(member_id)
        self.profile_window.show()