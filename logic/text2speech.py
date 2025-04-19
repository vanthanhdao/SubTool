# # logic/tts.py

# from utils import audio
# from vocoder import inference as vocoder
# from synthesizer.inference import Synthesizer
# from encoder import inference as encoder
# import os
# import sys
# from pathlib import Path
# import numpy as np
# import torch
# from scipy.io.wavfile import write
# from typing import Union

# # --- Thêm đường dẫn đến thư mục Real-Time-Voice-Cloning nếu chưa có ---
# rtvc_path = Path(__file__).resolve().parent.parent / "Real-Time-Voice-Cloning"
# if str(rtvc_path) not in sys.path:
#     sys.path.insert(0, str(rtvc_path))

# # Import mô-đun từ RTVC

# # Trạng thái khởi tạo mô hình
# initialized = False
# synthesizer = None


# def init_rtvc_models():
#     global initialized, synthesizer
#     if initialized:
#         return

#     print("🔊 Đang tải mô hình RTVC...")
#     encoder.load_model(rtvc_path / "encoder/saved_models/pretrained.pt")
#     synthesizer = Synthesizer(
#         rtvc_path / "synthesizer/saved_models/logs-pretrained")
#     vocoder.load_model(
#         rtvc_path / "vocoder/saved_models/pretrained/pretrained.pt")
#     initialized = True
#     print("✅ Đã tải mô hình RTVC thành công.")


# def synthesize_from_text(text: str, speaker_wav: Union[str, Path], output_path: str = "output.wav") -> str:
#     """
#     Tạo file giọng nói từ văn bản và file giọng mẫu sử dụng Real-Time-Voice-Cloning.
#     """
#     init_rtvc_models()

#     if not os.path.exists(speaker_wav):
#         raise FileNotFoundError(
#             f"Không tìm thấy file giọng mẫu: {speaker_wav}")

#     # Bước 1: Tạo embedding từ giọng mẫu
#     preprocessed_wav = encoder.preprocess_wav(Path(speaker_wav))
#     embed = encoder.embed_utterance(preprocessed_wav)

#     # Bước 2: Tổng hợp spectrogram từ văn bản
#     texts = [text]
#     embeds = [embed]
#     specs = synthesizer.synthesize_spectrograms(texts, embeds)
#     spec = specs[0]

#     # Bước 3: Tạo waveform từ spectrogram
#     generated_wav = vocoder.infer_waveform(spec)

#     # Chuẩn hoá và lưu file âm thanh
#     generated_wav = np.pad(generated_wav, (0, 4000), mode="constant")
#     write(output_path, 22050, (generated_wav * 32767).astype(np.int16))

#     print(f"✅ Giọng nói đã được lưu tại: {output_path}")
#     return output_path
