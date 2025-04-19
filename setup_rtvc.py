import subprocess
import os
from pathlib import Path

RTVC_REPO = "https://github.com/CorentinJ/Real-Time-Voice-Cloning.git"
DEST_DIR = Path(__file__).resolve().parent / "Real-Time-Voice-Cloning"


def clone_rtvc():
    if DEST_DIR.exists():
        print("✅ RTVC đã tồn tại.")
        return
    print("🔁 Đang clone RTVC về project...")
    subprocess.run(["git", "clone", RTVC_REPO, str(DEST_DIR)], check=True)
    print("✅ Clone xong!")


def install_requirements():
    print("📦 Đang cài dependencies từ requirements.txt...")
    subprocess.run(
        ["pip", "install", "-r", str(DEST_DIR / "requirements.txt")], check=True)
    print("✅ Đã cài dependencies.")


def main():
    clone_rtvc()
    install_requirements()
    print("\n✅ Setup hoàn tất!\nBạn có thể chạy từ logic/tts.py và import encoder/synthesizer/vocoder bình thường.\n")


if __name__ == "__main__":
    main()
