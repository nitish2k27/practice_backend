import sys
import json
import os
from datetime import date, datetime
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QGridLayout, QPushButton, QHBoxLayout, QMenu, QInputDialog)
from PyQt6.QtCore import Qt, QPoint, QDate, QTimer

class ProgressSentinel(QWidget):
    def __init__(self):
        super().__init__()
        self.settings_file = "widget_settings.json"
        self.load_settings()
        self.old_pos = None
        self.view_mode = "month"
        
        # Update logic every minute (to catch midnight rollovers)
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.daily_refresh)
        self.refresh_timer.start(60000) 
        
        self.initUI()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = {"target_date": "2026-12-31"}
        else:
            self.config = {"target_date": "2026-12-31"}
        
        self.target_date = datetime.strptime(self.config["target_date"], "%Y-%m-%d").date()

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            self.config["target_date"] = self.target_date.strftime("%Y-%m-%d")
            json.dump(self.config, f)

    def daily_refresh(self):
        self.refresh_counters()
        self.render_calendar()

    def initUI(self):
        # Window Configuration for "Widget" behavior
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnBottomHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.main_layout = QVBoxLayout()
        self.setStyleSheet("""
            QWidget { 
                background-color: rgba(18, 18, 18, 230); 
                color: #ffffff; 
                border-radius: 15px; 
                font-family: 'Segoe UI Variable', 'Segoe UI', sans-serif; 
            }
            .Title { font-size: 11px; color: #00ffcc; font-weight: bold; letter-spacing: 2px; }
            .CounterLabel { color: #888; font-size: 10px; font-weight: bold; }
            .CounterNum { font-size: 36px; font-weight: 900; color: #ffffff; margin-top: -5px; }
            .ProgressBar { background-color: #333; height: 4px; border-radius: 2px; }
            .ProgressFill { background-color: #00ffcc; height: 4px; border-radius: 2px; }
            .PastDay { color: #444; text-decoration: line-through; font-size: 10px; }
            .CurrentDay { background-color: #00ffcc; color: #000; font-weight: bold; border-radius: 4px; font-size: 10px; }
            .FutureDay { font-size: 10px; border: 1px solid #222; border-radius: 4px; }
            QPushButton { background: #252525; border: 1px solid #333; padding: 5px; border-radius: 5px; font-size: 10px; color: #bbb; }
            QPushButton:hover { background: #00ffcc; color: black; border: 1px solid #00ffcc; }
        """)

        # --- Header ---
        header = QHBoxLayout()
        title = QLabel("PROGRESS SENTINEL")
        title.setProperty("class", "Title")
        header.addWidget(title)
        
        self.btn_view = QPushButton("Toggle View")
        self.btn_view.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_view.clicked.connect(self.toggle_view)
        header.addWidget(self.btn_view)
        self.main_layout.addLayout(header)

        # --- Counters & Progress Bar ---
        self.cnt_layout = QVBoxLayout()
        self.main_layout.addLayout(self.cnt_layout)
        
        self.progress_container = QWidget()
        self.progress_container.setFixedHeight(10)
        self.progress_bar_bg = QWidget(self.progress_container)
        self.progress_bar_bg.setObjectName("bar_bg")
        self.progress_bar_bg.setStyleSheet("background: #222; border-radius: 3px;")
        self.progress_fill = QWidget(self.progress_container)
        self.progress_fill.setStyleSheet("background: #00ffcc; border-radius: 3px;")
        
        self.main_layout.addWidget(self.progress_container)
        self.refresh_counters()

        # --- Calendar Area ---
        self.calendar_scroll = QHBoxLayout()
        self.main_layout.addLayout(self.calendar_scroll)
        self.render_calendar()

        # --- Right-Click Menu ---
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.setLayout(self.main_layout)
        self.setFixedSize(280, 480)
        self.show()

    def refresh_counters(self):
        # Clear counter layout
        for i in reversed(range(self.cnt_layout.count())): 
            self.cnt_layout.itemAt(i).widget().setParent(None)
            
        today = date.today()
        year_end = date(today.year, 12, 31)
        total_days_year = (year_end - date(today.year, 1, 1)).days
        days_passed = (today - date(today.year, 1, 1)).days
        
        rem_year = (year_end - today).days
        rem_target = (self.target_date - today).days

        # Year Remaining
        l1 = QLabel(f"YEAR {today.year} REMAINING")
        l1.setProperty("class", "CounterLabel")
        self.cnt_layout.addWidget(l1)
        c1 = QLabel(f"{rem_year}D")
        c1.setProperty("class", "CounterNum")
        self.cnt_layout.addWidget(c1)

        # Target Remaining
        l2 = QLabel(f"UNTIL {self.target_date}")
        l2.setProperty("class", "CounterLabel")
        self.cnt_layout.addWidget(l2)
        c2 = QLabel(f"{max(0, rem_target)}D")
        c2.setProperty("class", "CounterNum")
        self.cnt_layout.addWidget(c2)

        # Update progress bar width
        progress_pct = (days_passed / total_days_year)
        self.progress_bar_bg.setFixedSize(240, 6)
        self.progress_fill.setFixedSize(int(240 * progress_pct), 6)

    def render_calendar(self):
        for i in reversed(range(self.calendar_scroll.count())):
            item = self.calendar_scroll.itemAt(i)
            if item.widget(): item.widget().setParent(None)

        months_to_show = 6 if self.view_mode == "6month" else 1
        start_date = date.today()

        for m in range(months_to_show):
            month_widget = QWidget()
            grid = QGridLayout(month_widget)
            grid.setSpacing(2)
            
            curr_month_raw = start_date.month + m
            curr_m = (curr_month_raw - 1) % 12 + 1
            curr_y = start_date.year + (curr_month_raw - 1) // 12
            
            # FIXED LINE BELOW: Added the day '1' to the constructor
            days_in_month = QDate(curr_y, curr_m, 1).daysInMonth()
            
            month_name = datetime(curr_y, curr_m, 1).strftime("%b").upper()
            
            month_lbl = QLabel(month_name)
            month_lbl.setStyleSheet("font-size: 9px; color: #555; font-weight: bold;")
            grid.addWidget(month_lbl, 0, 0, 1, 7, Qt.AlignmentFlag.AlignCenter)

            for d in range(1, days_in_month + 1):
                day_date = date(curr_y, curr_m, d)
                lbl = QLabel(str(d))
                lbl.setFixedSize(22, 22)
                lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                if day_date < date.today():
                    lbl.setProperty("class", "PastDay")
                elif day_date == date.today():
                    lbl.setProperty("class", "CurrentDay")
                else:
                    lbl.setProperty("class", "FutureDay")
                
                grid.addWidget(lbl, ((d-1)//7)+1, (d-1)%7)
            
            self.calendar_scroll.addWidget(month_widget)

    def toggle_view(self):
        if self.view_mode == "month":
            self.view_mode = "6month"
            self.setFixedSize(1300, 260) 
        else:
            self.view_mode = "month"
            self.setFixedSize(280, 480)
        self.render_calendar()
        self.refresh_counters()

    def show_context_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background-color: #222; border: 1px solid #444; } QMenu::item:selected { background-color: #00ffcc; color: black; }")
        
        set_target = menu.addAction("Set Target Date (YYYY-MM-DD)")
        quit_app = menu.addAction("Exit Widget")
        
        action = menu.exec(self.mapToGlobal(pos))
        
        if action == set_target:
            text, ok = QInputDialog.getText(self, 'Target', 'Enter Target Date:', text=str(self.target_date))
            if ok:
                try:
                    self.target_date = datetime.strptime(text, "%Y-%m-%d").date()
                    self.save_settings()
                    self.refresh_counters()
                    self.render_calendar()
                except ValueError:
                    pass
        elif action == quit_app:
            QApplication.quit()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProgressSentinel()
    sys.exit(app.exec())