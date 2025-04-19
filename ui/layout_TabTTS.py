# # layout/tts_tab.py

# from PyQt6.QtWidgets import (
#     QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QWidget
# )
# import os

# from logic.text2speech import load_voice_sample, synthesize_voice


# def build_tts_tab(parent):
#     tts_tab = QWidget()
#     layout = QVBoxLayout()

#     parent.voice_sample_label = QLabel("Chưa chọn giọng mẫu")
#     parent.voice_sample_button = QPushButton("Chọn giọng nói mẫu (.wav)")
#     parent.voice_sample_button.clicked.connect(
#         lambda: load_voice_sample(parent))

#     parent.tts_text_input = QTextEdit()
#     parent.tts_text_input.setPlaceholderText(
#         "Nhập văn bản cần chuyển thành giọng nói...")

#     parent.synthesize_button = QPushButton("Tổng hợp giọng nói")
#     parent.synthesize_button.setStyleSheet(
#         "background-color: blue; color: white; font-weight: bold;")
#     parent.synthesize_button.clicked.connect(lambda: synthesize_voice(parent))

#     parent.tts_status = QLabel("")

#     layout.addWidget(parent.voice_sample_button)
#     layout.addWidget(parent.voice_sample_label)
#     layout.addWidget(parent.tts_text_input)
#     layout.addWidget(parent.synthesize_button)
#     layout.addWidget(parent.tts_status)

#     tts_tab.setLayout(layout)
#     return tts_tab
