
from PyQt6.QtWidgets import QFileDialog, QDialog
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QApplication
from PyQt6.QtCore import QTimer

from dotenv import load_dotenv
from PyQt6.QtCore import QTimer
from google import genai
import os
import re
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem
from ui.find_replace import FindReplaceDialog


load_dotenv()


def select_file(self):
    file_path, _ = QFileDialog.getOpenFileName(
        self, "Chọn file", "", "Subtitle Files (*.srt *.txt)")
    if file_path:
        self.file_label.setText(file_path)

        # Đọc nội dung file SRT và thêm vào bảng
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()+["\n"]

        self.subtitle_data.clear()
        self.table.setRowCount(0)

        subtitle_block = []  # Khởi tạo block cho mỗi subtitle
        index = 0
        # RegEx cho thời gian
        time_pattern = r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})'

        for i, line in enumerate(lines):
            line = line.strip()
            if line == "":
                if len(subtitle_block) == 3:
                    # Add data vào bảng khi subtitle_block có đủ 3 phần tử
                    self.table.insertRow(self.table.rowCount())
                    self.table.setItem(index, 0, QTableWidgetItem(
                        subtitle_block[1]))  # Start Time
                    self.table.setItem(index, 1, QTableWidgetItem(
                        subtitle_block[2]))  # End Time
                    self.table.setItem(index, 2, QTableWidgetItem(
                        subtitle_block[0]))  # Content
                    # Translated Content
                    self.table.setItem(index, 3, QTableWidgetItem(""))
                    index += 1
                subtitle_block = []  # Reset subtitle_block cho subtitle mới
            else:
                # Kiểm tra xem dòng có phải là thời gian không
                time_match = re.match(time_pattern, line)
                if time_match:
                    start_time = time_match.group(1)
                    end_time = time_match.group(2)
                    # Thêm Start Time và End Time vào subtitle_block
                    subtitle_block = [line, start_time, end_time]
                else:
                    if len(subtitle_block) >= 1:
                        subtitle_block[0] = line

        self.subtitle_data = subtitle_block  # Lưu trữ toàn bộ dữ liệu subtitle


def clear_data(self):
    row_count = self.table.rowCount()
    for row in range(row_count):
        # Đặt lại nội dung ô của cột Translated Content thành chuỗi rỗng
        self.table.setItem(row, 3, QTableWidgetItem(""))

    QMessageBox.information(
        self, "Clear Data", "Đã xóa dữ liệu cột Translated Content.")


def save_translated_file(self):
    save_path, _ = QFileDialog.getSaveFileName(
        self, "Lưu file đã dịch", "", "Subtitle Files (*.srt *.txt)"
    )
    if not save_path:
        return

    try:
        srt_lines = []
        row_count = self.table.rowCount()
        for row in range(row_count):
            # Giả sử bảng của bạn có 4 cột:
            #   Cột 0: Start Time
            #   Cột 1: End Time
            #   Cột 2: Content (nguyên bản)
            #   Cột 3: Translated Content
            start_time_item = self.table.item(row, 0)
            end_time_item = self.table.item(row, 1)
            translated_item = self.table.item(row, 3)

            # Nếu một trong các ô không tồn tại thì bỏ qua dòng đó.
            if not (start_time_item and end_time_item and translated_item):
                continue

            start_time = start_time_item.text().strip()
            end_time = end_time_item.text().strip()
            translated_text = translated_item.text().strip()

            # Xây dựng block theo định dạng SRT:
            srt_lines.append(f"{row + 1}")
            srt_lines.append(f"{start_time} --> {end_time}")
            srt_lines.append(translated_text)
            srt_lines.append("")  # Dòng trống phân cách block

        with open(save_path, "w", encoding="utf-8") as f:
            f.write("\n".join(srt_lines))

        QMessageBox.information(
            self, "Thành công", f"Đã lưu file tại: {save_path}")
        self.save_button.setVisible(False)
    except Exception as e:
        QMessageBox.critical(self, "Lỗi lưu file",
                             f"Lỗi khi lưu file:\n{str(e)}")


def open_find_replace_dialog(self):
    dialog = FindReplaceDialog(self)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        find_text = dialog.find_text
        replace_text = dialog.replace_text
        row_count = self.table.rowCount()
        count_replacements = 0
        for row in range(row_count):
            # Cột "Translated Content" là cột thứ 4 (index 3)
            item = self.table.item(row, 3)
            if item:
                original_text = item.text()
                if find_text in original_text:
                    new_text = original_text.replace(
                        find_text, replace_text)
                    self.table.setItem(row, 3, QTableWidgetItem(new_text))
                    count_replacements += 1
        QMessageBox.information(
            self, "Kết quả", f"Đã thay thế {count_replacements} trường chứa từ '{find_text}'.")


def stop_translation(self):
    self.stop_requested = True
    # Cập nhật giao diện: bật lại nút bắt đầu, ẩn progress bar, thông báo đã dừng
    self.start_button.setEnabled(True)
    self.progress_bar.setVisible(False)
    self.progress_label.setText("Đã dừng dịch")
    QMessageBox.information(self, "Thông báo", "Đã dừng quá trình dịch.")


def start_batch_translation(self):
    total_rows = self.table.rowCount()
    rows = []

    for i in range(total_rows):
        content_item = self.table.item(i, 2)
        if content_item:
            content = content_item.text().strip()
            if content:
                rows.append((i, content))

    if not rows:
        QMessageBox.information(self, "Không có dữ liệu",
                                "Không tìm thấy dòng nào để dịch.")
        return

    # Hiển thị tiến trình
    self.progress_bar.setVisible(True)
    self.progress_bar.setMaximum(len(rows))
    self.progress_bar.setValue(0)

    self.progress_label.setVisible(True)
    self.progress_label.setText("Đang dịch...")

    self.batch_index = 0
    self.batches = [rows[i:i+190] for i in range(0, len(rows), 190)]

    process_next_batch(self)


def process_next_batch(self):
    if self.batch_index >= len(self.batches):
        self.start_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_label.setText("✅ Dịch hoàn tất!")
        self.check_button.setVisible(True)

        if self.overwrite_checkbox.isChecked():
            file_path = self.file_label.text()
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.translated_content.strip())
                self.prompt_input.append(
                    f"\n✅ Đã ghi đè vào file: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi ghi file", str(e))
        else:
            self.save_button.setVisible(True)
        return

    current_batch = self.batches[self.batch_index]

    def after_batch_done():
        # Cập nhật progress
        self.progress_bar.setValue(
            self.progress_bar.value() + len(current_batch))
        self.batch_index += 1
        # Delay 1 giây trước khi dịch batch tiếp theo
        QTimer.singleShot(1000, lambda: process_next_batch(self))

    translate_batch_streaming(self, current_batch, on_done=after_batch_done)


def translate_batch_streaming(self, batch_data, on_done=None):
    api_key = os.getenv("API_KEY_GENAI")
    target = self.target_lang.currentText()
    source = self.source_lang.currentText()
    if not api_key:
        QMessageBox.warning(self, "API Error",
                            "Không tìm thấy API key trong môi trường.")
        return

    try:
        client = genai.Client(api_key=api_key)

        prompt = (
            f"Văn bản sau là phụ đề phim bằng tiếng {source}, hãy dịch sang tiếng {target}. "
            f"Dịch chính xác, văn phong tự nhiên, chỉ hiển thị văn bản dịch, dịch chính xác số dòng là 190 dòng:"
        )

        contents = prepare_prompt_text([text for _, text in batch_data])
        respone = client.models.generate_content(
            model=self.model_select.currentText(),
            contents=[prompt+"\n" + contents]
        )
        respone_array = respone.text.strip().split("\n")

        self.table.setUpdatesEnabled(False)
        for (row_idx, _), translated in zip(batch_data, respone_array):
            format = translated.strip()
            self.table.setItem(
                row_idx, 3, QTableWidgetItem(format))
        self.table.setUpdatesEnabled(True)

        if on_done:
            on_done()

    except Exception as e:
        QMessageBox.critical(self, "Lỗi khi dịch", str(e))


def prepare_prompt_text(sub_contents):
    prompt_lines = []
    for _, text in enumerate(sub_contents, start=1):
        prompt_lines.append(f"{text.strip()}")
    return "\n".join(prompt_lines)
