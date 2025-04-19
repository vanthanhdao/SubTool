
# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QComboBox, QLabel,
#     QHBoxLayout, QTabWidget, QFileDialog, QProgressBar, QCheckBox
# )
# from PyQt6.QtGui import QIcon

# from dotenv import load_dotenv
# from PyQt6.QtCore import Qt, QTimer
# from google import genai
# import sys
# import os
# import re
# from PyQt6.QtWidgets import QMessageBox

# load_dotenv()


# class TranslationApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("AI Translator")
#         self.setGeometry(100, 100, 700, 500)

#         layout = QVBoxLayout()
#         self.tabs = QTabWidget()
#         self.file_translation_tab = QWidget()
#         self.tts_tab = QWidget()
#         self.tabs.addTab(self.file_translation_tab, "Dịch File")
#         self.tabs.addTab(self.tts_tab, "TTS")

#         model_layout = QHBoxLayout()
#         self.model_label = QLabel("Mô hình:")
#         self.model_label.setStyleSheet("font-weight: bold;")
#         self.model_select = QComboBox()
#         self.model_select.addItems(
#             ["gemini-1.5-pro", "gemini-2.5-pro-exp-03-25", "mistral-7b"])
#         model_layout.addWidget(self.model_label)
#         model_layout.addWidget(self.model_select)

#         lang_layout = QHBoxLayout()
#         self.source_lang_label = QLabel("Ngôn ngữ nguồn:")
#         self.target_lang_label = QLabel("Ngôn ngữ đích:")
#         self.source_lang = QComboBox()
#         self.source_lang.addItems(["Trung", "Anh", "Việt", "German"])
#         self.target_lang = QComboBox()
#         self.target_lang.addItems(
#             ["Việt", "Trung", "English", "French", "German"])
#         self.source_lang.currentTextChanged.connect(self.update_prompt)
#         self.target_lang.currentTextChanged.connect(self.update_prompt)
#         lang_layout.addWidget(self.source_lang_label)
#         lang_layout.addWidget(self.source_lang)
#         lang_layout.addWidget(self.target_lang_label)
#         lang_layout.addWidget(self.target_lang)

#         file_layout = QHBoxLayout()
#         self.file_label = QLabel("Chưa chọn tệp")
#         self.file_button = QPushButton("Chọn File")
#         self.file_button.clicked.connect(self.select_file)
#         file_layout.addWidget(self.file_button)
#         file_layout.addWidget(self.file_label)

#         text_layout = QHBoxLayout()

#         # Khung bên trái (file_content)
#         self.file_content = QTextEdit()
#         self.file_content.setReadOnly(True)
#         self.file_content.setVisible(False)

#         # Khung bên phải: prompt_input + find & replace
#         right_text_layout = QVBoxLayout()
#         self.prompt_input = QTextEdit()
#         self.prompt_input.setReadOnly(True)

#         # --- Tìm và Thay Thế ---
#         find_replace_layout = QHBoxLayout()
#         self.find_input = QTextEdit()
#         self.find_input.setPlaceholderText("Tìm...")
#         self.find_input.setFixedHeight(30)

#         self.replace_input = QTextEdit()
#         self.replace_input.setPlaceholderText("Thay bằng...")
#         self.replace_input.setFixedHeight(30)

#         self.replace_button = QPushButton("Thay thế tất cả")
#         self.replace_button.clicked.connect(self.find_and_replace)

#         find_replace_layout.addWidget(self.find_input)
#         find_replace_layout.addWidget(self.replace_input)
#         find_replace_layout.addWidget(self.replace_button)

#         right_text_layout.addWidget(self.prompt_input)
#         right_text_layout.addLayout(find_replace_layout)

#         # Thêm vào layout tổng
#         text_layout.addWidget(self.file_content, 1)
#         text_layout.addLayout(right_text_layout, 1)

#         self.progress_bar = QProgressBar()
#         self.progress_bar.setVisible(False)

#         self.progress_label = QLabel("")
#         self.progress_label.setVisible(False)

#         # Tuỳ chọn ghi đè
#         self.overwrite_checkbox = QCheckBox("Ghi đè file gốc sau khi dịch")

#         # Nút lưu file kết quả (nếu không ghi đè)
#         self.save_button = QPushButton("Lưu file kết quả")
#         self.save_button.setVisible(False)
#         self.save_button.setStyleSheet(
#             "background-color: orange; font-weight: bold;")
#         self.save_button.clicked.connect(self.save_translated_file)

#         button_layout = QHBoxLayout()
#         self.start_button = QPushButton("Bắt Đầu Dịch")
#         self.start_button.setStyleSheet(
#             "background-color: green; font-weight: bold;")
#         self.start_button.clicked.connect(self.start_translate)

#         self.clear_button = QPushButton("Clear v2")
#         self.clear_button.setStyleSheet(
#             "background-color: grey; font-weight: bold;")
#         self.clear_button.clicked.connect(self.clear_data)

#         self.check_button = QPushButton("Check")
#         self.check_button.setVisible(False)
#         self.check_button.setStyleSheet(
#             "background-color: yellow; font-weight: bold;")
#         self.check_button.clicked.connect(self.check_translated_output)

#         button_layout.addWidget(self.start_button)
#         button_layout.addWidget(self.check_button)
#         button_layout.addWidget(self.clear_button)

#         file_tab_layout = QVBoxLayout()
#         file_tab_layout.addLayout(model_layout)
#         file_tab_layout.addLayout(lang_layout)
#         file_tab_layout.addLayout(file_layout)
#         file_tab_layout.addLayout(text_layout)
#         file_tab_layout.addWidget(self.progress_bar)
#         file_tab_layout.addWidget(self.progress_label)
#         file_tab_layout.addWidget(self.overwrite_checkbox)
#         file_tab_layout.addWidget(self.save_button)
#         file_tab_layout.addLayout(button_layout)
#         file_tab_layout.addLayout(find_replace_layout)

#         self.file_translation_tab.setLayout(file_tab_layout)

#         layout.addWidget(self.tabs)
#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)

#         self.translated_content = ""

#     def select_file(self):
#         file_name, _ = QFileDialog.getOpenFileName(
#             self, "Chọn file", "", "Subtitle Files (*.srt *.txt)")
#         if file_name:
#             self.file_label.setText(file_name)
#             try:
#                 with open(file_name, "r", encoding="utf-8") as file:
#                     file_content = file.read()
#                     self.file_content.setText(file_content)
#                     self.file_content.setVisible(True)
#                     self.file_content.setReadOnly(False)
#             except Exception as e:
#                 self.file_content.setText(f"Lỗi khi đọc file: {str(e)}")
#                 self.file_content.setVisible(True)
#         else:
#             self.file_content.setVisible(False)

#     def clear_data(self):
#         self.file_label.setText("Chưa chọn tệp")
#         self.file_content.clear()
#         self.file_content.setVisible(False)
#         self.prompt_input.clear()
#         self.progress_bar.setVisible(False)
#         self.progress_label.setVisible(False)
#         self.translated_content = ""
#         self.save_button.setVisible(False)

#     def update_prompt(self):
#         target = self.target_lang.currentText()
#         source = self.source_lang.currentText()
#         self.prompt_input.setText(f"Văn bản sau là phụ đề phim bằng tiếng {source}, hãy dịch sang tiếng {target}. "
#                                   f"Giữ nguyên định dạng số thứ tự và thời gian. "
#                                   f"Chỉ dịch phần nội dung thoại, không dịch số và thời gian. ")

#     def split_subtitles(self, srt_content, batch_size=150):
#         blocks = []
#         current_block = []
#         lines = srt_content.split("\n")

#         for line in lines:
#             current_block.append(line)
#             if line.strip() == "":
#                 if current_block:
#                     blocks.append("\n".join(current_block))
#                     current_block = []

#         if current_block:
#             blocks.append("\n".join(current_block))

#         return [blocks[i:i + batch_size] for i in range(0, len(blocks), batch_size)], len(blocks)

#     def translate_next_batch(self):
#         if self.current_batch_index >= len(self.sub_batches):
#             self.start_button.setEnabled(True)
#             self.progress_bar.setVisible(False)
#             self.progress_label.setText("\u2705 Dịch hoàn tất!")
#             self.prompt_input.setReadOnly(False)
#             self.check_button.setVisible(True)

#             if self.overwrite_checkbox.isChecked():
#                 file_path = self.file_label.text()
#                 try:
#                     with open(file_path, "w", encoding="utf-8") as f:
#                         f.write(self.translated_content.strip())
#                     self.prompt_input.append(
#                         f"\n✅ Đã ghi đè vào file: {file_path}")
#                 except Exception as e:
#                     self.prompt_input.append(
#                         f"\n❌ Lỗi khi ghi đè file: {str(e)}")
#             else:
#                 self.save_button.setVisible(True)
#             return

#         batch_group = self.sub_batches[self.current_batch_index]
#         batch_text = "\n".join(batch_group)
#         num_segments = len(batch_group)
#         self.current_segment_index += num_segments

#         target = self.target_lang.currentText()
#         source = self.source_lang.currentText()
#         prompt = (
#             f"Văn bản sau là phụ đề phim bằng tiếng {source}, hãy dịch sang tiếng {target}. "
#             f"Giữ nguyên định dạng số thứ tự và thời gian. "
#             f"Chỉ dịch phần nội dung thoại, không dịch số và thời gian. ")

#         api_key = os.getenv("API_KEY_GENAI")
#         if not api_key:
#             self.prompt_input.append("\u274c Lỗi: Không tìm thấy API key.")
#             return

#         try:
#             client = genai.Client(api_key=api_key)
#             response = client.models.generate_content(
#                 model=self.model_select.currentText(),
#                 contents=[f"{prompt}\n\n{batch_text}"]
#             )
#             self.prompt_input.append(f"{response.text}")
#             self.translated_content += f"{response.text}\n\n"
#         except Exception as e:
#             error_message = str(e)
#             if 'RESOURCE_EXHAUSTED' in error_message:
#                 self.prompt_input.append(
#                     "\n❌ Lỗi: Quá giới hạn số yêu cầu. Đợi 32 giây và thử lại.")
#                 retry_delay = 60
#                 QTimer.singleShot(retry_delay * 1000,
#                                   self.translate_next_batch)
#                 return
#             self.prompt_input.append(
#                 f"\n❌ Lỗi khi dịch đoạn {self.current_segment_index + 1}: {str(e)}")

#         self.progress_bar.setValue(self.current_segment_index)
#         self.progress_label.setText(
#             f"{self.current_segment_index} / {self.total_segments} đoạn phụ đề đã dịch")
#         self.current_batch_index += 1
#         QTimer.singleShot(5000, self.translate_next_batch)

#     def start_translate(self):
#         content = self.file_content.toPlainText()

#         if not content.strip():
#             self.prompt_input.setText("Không có nội dung để dịch!")
#             return

#         self.prompt_input.clear()
#         self.start_button.setEnabled(False)
#         self.sub_batches, self.total_segments = self.split_subtitles(
#             content, batch_size=150)
#         self.current_batch_index = 0
#         self.current_segment_index = 0
#         self.translated_content = ""

#         self.progress_bar.setVisible(True)
#         self.progress_bar.setMaximum(self.total_segments)
#         self.progress_bar.setValue(0)

#         self.progress_label.setVisible(True)
#         self.progress_label.setText(
#             f"0 / {self.total_segments} đoạn phụ đề đã dịch")

#         self.translate_next_batch()

#     def save_translated_file(self):
#         save_path, _ = QFileDialog.getSaveFileName(
#             self, "Lưu file đã dịch", "", "Subtitle Files (*.srt *.txt)")
#         if save_path:
#             try:
#                 with open(save_path, "w", encoding="utf-8") as f:
#                     f.write(self.translated_content.strip())
#                 self.prompt_input.append(f"\n✅ Đã lưu file tại: {save_path}")
#                 self.save_button.setVisible(False)
#             except Exception as e:
#                 self.prompt_input.append(f"\n❌ Lỗi khi lưu file: {str(e)}")

#     def check_translated_output(self):
#         content = self.prompt_input.toPlainText()

#         # Tách từng block bằng khoảng trắng giữa các đoạn
#         blocks = re.split(r"\n\s*\n", content.strip())
#         error_blocks = []

#         for i, block in enumerate(blocks):
#             lines = block.strip().splitlines()
#             if len(lines) < 3:
#                 error_blocks.append(i + 1)  # đánh số thứ tự từ 1
#             continue

#         text_line = lines[2].strip()
#         if not text_line or text_line.lower() in ["...", "??", "###", "-", "_"]:
#             error_blocks.append(i + 1)

#         if error_blocks:
#             msg = (
#                 f"⚠️ Có {len(error_blocks)} đoạn bị bỏ trống hoặc lỗi định dạng.\n"
#                 f"Các đoạn lỗi gồm: {', '.join(map(str, error_blocks))}"
#             )
#             QMessageBox.warning(self, "Phát hiện lỗi dịch", msg)
#         else:
#             QMessageBox.information(self, "Kiểm tra hoàn tất",
#                                     "✅ Tất cả các đoạn đều hợp lệ.")

#     def find_and_replace(self):
#         find_text = self.find_input.toPlainText()
#         replace_text = self.replace_input.toPlainText()

#         if not find_text:
#             return

#         content = self.prompt_input.toPlainText()
#         updated_content = content.replace(find_text, replace_text)

#         self.prompt_input.setText(updated_content)
#         self.translated_content = updated_content


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setWindowIcon(QIcon("icon.ico"))
#     window = TranslationApp()
#     window.show()
#     sys.exit(app.exec())


from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import sys

from ui.layout import TranslationApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = TranslationApp()
    window.show()
    sys.exit(app.exec())
