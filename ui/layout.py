

import os
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QMainWindow, QHBoxLayout, QComboBox, QTabWidget,
    QProgressBar, QCheckBox, QTableWidget, QAbstractItemView
)
from PyQt6.QtCore import Qt
from logic.translator import (
    select_file, clear_data, start_batch_translation,

    save_translated_file, open_find_replace_dialog, stop_translation
)

from utils.checker import check_translated_output


class TranslationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Translator")
        self.setGeometry(100, 100, 900, 600)

        self.translated_content = ""
        self.subtitle_data = []  # [(index, start, end, text, translated_text)]

        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.file_translation_tab = QWidget()
        self.tabs.addTab(self.file_translation_tab, "Dịch File")

        # --- Model Selection ---
        model_layout = QHBoxLayout()
        self.model_label = QLabel("Mô hình:")
        self.model_label.setStyleSheet("font-weight: bold;")
        self.model_select = QComboBox()
        self.model_select.addItems(
            ["gemini-2.5-pro-exp-03-25", "gemini-1.5-pro", "mistral-7b"]
        )
        model_layout.addWidget(self.model_label)
        model_layout.addWidget(self.model_select)

        # --- Language Selection ---
        lang_layout = QHBoxLayout()
        self.source_lang_label = QLabel("Ngôn ngữ nguồn:")
        self.target_lang_label = QLabel("Ngôn ngữ đích:")
        self.source_lang = QComboBox()
        self.source_lang.addItems(["Trung", "Anh", "Việt", "German"])
        self.target_lang = QComboBox()
        self.target_lang.addItems(
            ["Việt", "Trung", "English", "French", "German"])
        lang_layout.addWidget(self.source_lang_label)
        lang_layout.addWidget(self.source_lang)
        lang_layout.addWidget(self.target_lang_label)
        lang_layout.addWidget(self.target_lang)

        # --- File Selection ---
        file_layout = QHBoxLayout()
        self.file_label = QLabel("Chưa chọn tệp")
        self.file_button = QPushButton("Chọn File")
        self.file_button.clicked.connect(lambda: select_file(self))
        # --- Find & Replace ---
        self.search_replace_button = QPushButton("Find/Replace")
        self.search_replace_button.clicked.connect(
            lambda: open_find_replace_dialog(self))
        file_layout.addWidget(self.file_button)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.search_replace_button)

        # --- Subtitle Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Start Time", "End Time", "Content", "Translated Content"
        ])
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 250)
        self.table.setColumnWidth(3, 350)
        # Cho phép chỉnh sửa bằng double click hoặc khi ô được chọn
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked | QAbstractItemView.EditTrigger.SelectedClicked
        )

        # --- Progress Bar & Label ---
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        self.progress_label = QLabel("")
        self.progress_label.setVisible(False)

        # --- Overwrite Checkbox ---
        self.overwrite_checkbox = QCheckBox("Ghi đè file gốc sau khi dịch")

        # --- Save Button ---
        self.save_button = QPushButton("Lưu file kết quả")
        self.save_button.setVisible(False)
        self.save_button.setStyleSheet(
            "background-color: orange; font-weight: bold;")
        self.save_button.clicked.connect(lambda: save_translated_file(self))

        # --- Buttons ---
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Bắt Đầu Dịch")
        self.start_button.setStyleSheet(
            "background-color: green; font-weight: bold;")
        self.start_button.clicked.connect(
            lambda: start_batch_translation(self))

        self.stop_button = QPushButton("Hủy")
        self.stop_button.setStyleSheet(
            "background-color: red; font-weight: bold;")
        self.stop_button.clicked.connect(lambda: stop_translation(self))

        self.clear_button = QPushButton("Clear v2")
        self.clear_button.setStyleSheet(
            "background-color: grey; font-weight: bold;")
        self.clear_button.clicked.connect(lambda: clear_data(self))

        self.check_button = QPushButton("Check")
        self.check_button.setVisible(False)
        self.check_button.setStyleSheet(
            "background-color: yellow; font-weight: bold;")
        self.check_button.clicked.connect(
            lambda: check_translated_output(self))

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.check_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.stop_button)

        # --- Layout Assembly ---
        file_tab_layout = QVBoxLayout()
        file_tab_layout.addLayout(model_layout)
        file_tab_layout.addLayout(lang_layout)
        file_tab_layout.addLayout(file_layout)
        file_tab_layout.addWidget(self.table)
        file_tab_layout.addWidget(self.progress_bar)
        file_tab_layout.addWidget(self.progress_label)
        file_tab_layout.addWidget(self.overwrite_checkbox)
        file_tab_layout.addWidget(self.save_button)
        file_tab_layout.addLayout(button_layout)

        self.file_translation_tab.setLayout(file_tab_layout)
        layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            print("ESC pressed! Restarting app...")
            self.restart_app()

    def restart_app(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
