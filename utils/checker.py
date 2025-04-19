

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QComboBox, QLabel,
    QHBoxLayout, QTabWidget, QFileDialog, QProgressBar, QCheckBox
)
from PyQt6.QtGui import QIcon

from dotenv import load_dotenv
from PyQt6.QtCore import Qt, QTimer
from google import genai
import sys
import os
import re
from PyQt6.QtWidgets import QMessageBox


import re
from PyQt6.QtWidgets import QMessageBox


def check_translated_output(self):

    error_rows = []
    # Biểu thức chính quy để phát hiện ký tự tiếng Trung (Unicode range)
    pattern_chinese = re.compile(r'[\u4e00-\u9fff]')

    row_count = self.table.rowCount()
    for row in range(row_count):
        # Giả sử cột Translated Content là cột thứ 4 (index 3)
        item = self.table.item(row, 3)
        if item is None:
            error_rows.append(row + 1)
        else:
            text = item.text().strip()
            # Kiểm tra nếu dòng để trống hoặc chứa ký tự tiếng Trung
            if not text or pattern_chinese.search(text):
                error_rows.append(row + 1)

    if error_rows:
        msg = (
            f"Có {len(error_rows)} dòng lỗi (hàng: {', '.join(map(str, error_rows))}).\n"
            "Vui lòng kiểm tra lại: cột Dịch không được để trống và không chứa tiếng Trung."
        )
        QMessageBox.warning(self, "Phát hiện lỗi dịch", msg)
    else:
        QMessageBox.information(self, "Kiểm tra hoàn tất",
                                "✅ Tất cả các dòng dịch đều hợp lệ.")
