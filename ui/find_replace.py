from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox
)


class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tìm kiếm & Thay thế")
        self.find_text = ""
        self.replace_text = ""
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Hàng nhập từ cần tìm
        h_layout_find = QHBoxLayout()
        lbl_find = QLabel("Từ cần tìm:")
        self.find_input = QLineEdit()
        h_layout_find.addWidget(lbl_find)
        h_layout_find.addWidget(self.find_input)
        layout.addLayout(h_layout_find)

        # Hàng nhập từ thay thế
        h_layout_replace = QHBoxLayout()
        lbl_replace = QLabel("Thay thế bằng:")
        self.replace_input = QLineEdit()
        h_layout_replace.addWidget(lbl_replace)
        h_layout_replace.addWidget(self.replace_input)
        layout.addLayout(h_layout_replace)

        # Nút OK và Cancel
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("Thay thế")
        ok_btn.clicked.connect(self.on_accept)
        cancel_btn = QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_accept(self):
        self.find_text = self.find_input.text().strip()
        self.replace_text = self.replace_input.text().strip()
        if not self.find_text:
            QMessageBox.information(
                self, "Thông báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return
        self.accept()
