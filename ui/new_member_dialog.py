from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit,
                              QPushButton, QComboBox, QMessageBox,
                              QDateEdit)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate
from logic.member_service import add_member
from logic.qr_service import generate_qr
import uuid

class NewMemberDialog(QDialog):
    def __init__(self, qr_value: str = None, parent=None):
        super().__init__(parent)
        self.qr_value = qr_value or str(uuid.uuid4())
        self.setWindowTitle("New Member Registration")
        self.setFixedSize(380, 340)
        self._build_ui()
        self._apply_styles()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("New Member Registration")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #a0a8d0;")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        self.name_input.setFixedHeight(38)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number (optional)")
        self.phone_input.setFixedHeight(38)

        #Birthday and Age
        birthday_label = QLabel("Birthday")
        birthday_label.setStyleSheet("color: #6a6a9a; font-size: 12px;")

        self.selected_birthday = None

        self.birthday_btn = QPushButton("📅  Select Birthday")
        self.birthday_btn.setFixedHeight(38)
        self.birthday_btn.clicked.connect(self._open_calendar)


        sub_label = QLabel("Subscription Plan")
        sub_label.setStyleSheet("color: #6a6a9a; font-size: 12px;")

        self.subscription_dropdown = QComboBox()
        self.subscription_dropdown.setFixedHeight(38)
        self.subscription_dropdown.addItem("1 Month",   1)
        self.subscription_dropdown.addItem("3 Months",  3)
        self.subscription_dropdown.addItem("6 Months",  6)
        self.subscription_dropdown.addItem("12 Months", 12)

        self.register_btn = QPushButton("Register & Generate QR")
        self.register_btn.setFixedHeight(40)
        self.register_btn.clicked.connect(self.register_member)

        layout.addWidget(title)
        layout.addWidget(self.name_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(birthday_label)
        layout.addWidget(self.birthday_btn)
        layout.addWidget(sub_label)
        layout.addWidget(self.subscription_dropdown)
        layout.addWidget(self.register_btn)
        self.setLayout(layout)

    def _apply_styles(self):
        self.setStyleSheet("""
            QDialog { background-color: #1a1a2e; font-family: Segoe UI; }
            QLabel { color: #e0e0e0; }
            QLineEdit, QComboBox, QDateEdit {
                background: #16213e;
                border: 1px solid #3a3a5c;
                border-radius: 8px;
                padding: 6px 14px;
                font-size: 13px;
                color: #e0e0e0;
            }
            QLineEdit:focus, QDateEdit:focus { border: 1px solid #5a5aab; }
            QDateEdit::drop-down { border: none; width: 30px; }
            QDateEdit::down-arrow { image: none; }
            QComboBox::drop-down { border: none; width: 30px; }
            QComboBox::down-arrow { image: none; }
            QComboBox QAbstractItemView, QDateEdit QAbstractItemView {
                background: #16213e;
                border: 1px solid #3a3a5c;
                color: #e0e0e0;
                selection-background-color: #0f3460;
            }
            QCheckBox { color: #6a6a9a; font-size: 12px; }
            QCheckBox::indicator {
                width: 16px; height: 16px;
                border: 1px solid #3a3a5c;
                border-radius: 4px;
                background: #16213e;
            }
            QCheckBox::indicator:checked { background: #0f3460; border-color: #5a5aab; }
            QPushButton {
                background-color: #0f3460;
                color: #c0c8f0;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #1a4a80; }
            QPushButton:pressed { background-color: #0a2540; }
            QDateEdit::drop-down {
                border: none;
                width: 30px;
                background: #0f3460;
                border-radius: 4px;
            }
            QDateEdit::down-arrow { image: none; }
        """)

    def register_member(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing Info", "Name is required.")
            return
        if not self.selected_birthday:
            QMessageBox.warning(self, "Missing Info", "Birthday is required.")
            return

        phone = self.phone_input.text().strip() or None
        months = self.subscription_dropdown.currentData()
        member_id, qr_code = add_member(name, phone, months, self.selected_birthday)
        qr_path = generate_qr(qr_code, name)

        QMessageBox.information(self, "Registered!",
            f"{name} registered successfully.\n"
            f"Subscription: {months} month{'s' if months > 1 else ''}\n"
            f"QR code saved to:\n{qr_path}")
        self.accept()

    def eventFilter(self, obj, event):
        from PyQt6.QtCore import QEvent
        if obj == self.birthday_picker and event.type() == QEvent.Type.MouseButtonPress:
            self.birthday_picker.showPopup()
            return True
        return super().eventFilter(obj, event)
    
    def _open_calendar(self):
        from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                                    QCalendarWidget, QPushButton, QComboBox)
        from PyQt6.QtCore import QDate
        import datetime

        dialog = QDialog(self)
        dialog.setWindowTitle("Select Birthday")
        dialog.setFixedSize(340, 320)
        dialog.setStyleSheet("""
            QDialog { background-color: #1a1a2e; }
            QCalendarWidget { background-color: #16213e; color: #e0e0e0; }
            QCalendarWidget QToolButton {
                background-color: #0f3460; color: #c0c8f0;
                border: none; border-radius: 4px;
                padding: 4px 8px; font-weight: bold; font-size: 12px;
            }
            QCalendarWidget QToolButton:hover { background-color: #1a4a80; }
            QCalendarWidget QWidget#qt_calendar_navigationbar { 
                background-color: #0f3460; padding: 4px; 
            }
            QCalendarWidget QAbstractItemView {
                background-color: #16213e; color: #e0e0e0;
                selection-background-color: #0f3460; selection-color: #ffffff;
            }
            QCalendarWidget QAbstractItemView:disabled { color: #3a3a5c; }
            QComboBox {
                background: #16213e; border: 1px solid #3a3a5c;
                border-radius: 6px; padding: 4px 10px;
                font-size: 12px; color: #e0e0e0;
            }
            QComboBox QAbstractItemView {
                background: #16213e; color: #e0e0e0;
                border: 1px solid #3a3a5c;
                selection-background-color: #0f3460;
            }
            QPushButton {
                background-color: #0f3460; color: #c0c8f0;
                border: none; border-radius: 8px;
                font-size: 13px; font-weight: bold; padding: 8px;
            }
            QPushButton:hover { background-color: #1a4a80; }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # --- Day / Month / Year dropdowns ---
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(6)

        current = self.selected_birthday or datetime.date(2000, 1, 1)

        day_box = QComboBox()
        for d in range(1, 32):
            day_box.addItem(str(d), d)
        day_box.setCurrentIndex(current.day - 1)

        month_box = QComboBox()
        months = ["January","February","March","April","May","June",
                "July","August","September","October","November","December"]
        for i, m in enumerate(months):
            month_box.addItem(m, i + 1)
        month_box.setCurrentIndex(current.month - 1)

        year_box = QComboBox()
        current_year = datetime.date.today().year
        for y in range(current_year, 1919, -1):
            year_box.addItem(str(y), y)
        year_box.setCurrentIndex(current_year - current.year)

        nav_layout.addWidget(day_box)
        nav_layout.addWidget(month_box)
        nav_layout.addWidget(year_box)

        # --- Calendar widget ---
        cal = QCalendarWidget()
        cal.setGridVisible(False)
        cal.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        cal.setNavigationBarVisible(False)   # hide the buggy built-in nav bar
        cal.setMinimumDate(QDate(1920, 1, 1))
        cal.setMaximumDate(QDate.currentDate())
        cal.setSelectedDate(QDate(current.year, current.month, current.day))

        # sync dropdowns → calendar
        def update_calendar():
            y = year_box.currentData()
            m = month_box.currentData()
            d = day_box.currentData()
            import calendar
            max_day = calendar.monthrange(y, m)[1]
            if d > max_day:
                day_box.setCurrentIndex(max_day - 1)
                d = max_day
            new_date = QDate(y, m, d)
            if new_date.isValid():
                cal.setSelectedDate(new_date)
                cal.showSelectedDate()

        # sync calendar → dropdowns
        def update_dropdowns(qdate):
            day_box.setCurrentIndex(qdate.day() - 1)
            month_box.setCurrentIndex(qdate.month() - 1)
            year_box.setCurrentIndex(current_year - qdate.year())

        day_box.currentIndexChanged.connect(lambda _: update_calendar())
        month_box.currentIndexChanged.connect(lambda _: update_calendar())
        year_box.currentIndexChanged.connect(lambda _: update_calendar())
        cal.selectionChanged.connect(lambda: update_dropdowns(cal.selectedDate()))

        # --- Confirm button ---
        confirm_btn = QPushButton("Confirm")

        def confirm():
            qdate = cal.selectedDate()
            import datetime
            self.selected_birthday = datetime.date(qdate.year(), qdate.month(), qdate.day())
            self.birthday_btn.setText(f"📅  {self.selected_birthday.strftime('%d %b %Y')}")
            dialog.accept()

        confirm_btn.clicked.connect(confirm)

        layout.addLayout(nav_layout)
        layout.addWidget(cal)
        layout.addWidget(confirm_btn)
        dialog.setLayout(layout)
        dialog.exec()