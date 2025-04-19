import time
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ReloadHandler(FileSystemEventHandler):
    def __init__(self, restart_callback):
        self.restart_callback = restart_callback

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"📝 File thay đổi: {event.src_path}")
            self.restart_callback()


class AppReloader:
    def __init__(self, script_name):
        self.script_name = script_name
        self.process = None
        self.start_app()

    def start_app(self):
        print("🚀 Khởi chạy lại ứng dụng...")
        self.process = subprocess.Popen(["python", self.script_name])

    def stop_app(self):
        if self.process:
            print("🛑 Dừng ứng dụng cũ...")
            self.process.terminate()
            self.process.wait()

    def restart_app(self):
        self.stop_app()
        self.start_app()


if __name__ == "__main__":
    reloader = AppReloader("main.py")

    event_handler = ReloadHandler(reloader.restart_app)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    print("👀 Đang theo dõi thay đổi file...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        reloader.stop_app()
    observer.join()
