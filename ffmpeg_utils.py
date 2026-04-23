import os
import sys
import requests
import zipfile
import shutil
from PyQt5.QtCore import QThread, pyqtSignal

# URL for a static FFmpeg build for Windows (using a reliable GitHub source)
# This is a slightly older but very stable and small build (approx 20MB zipped)
FFMPEG_URL = "https://github.com/GyanD/codexffmpeg/releases/download/2024-02-15-git-4566f11/ffmpeg-2024-02-15-git-4566f11-full_build.zip"

class FFmpegDownloader(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool)
    status = pyqtSignal(str)

    def __init__(self, bin_path):
        super().__init__()
        self.bin_path = bin_path

    def run(self):
        if not os.path.exists(self.bin_path):
            os.makedirs(self.bin_path)

        ffmpeg_exe = os.path.join(self.bin_path, "ffmpeg.exe")
        if os.path.exists(ffmpeg_exe):
            self.finished.emit(True)
            return

        try:
            self.status.emit("Downloading FFmpeg...")
            zip_path = os.path.join(self.bin_path, "ffmpeg.zip")
            
            # Streaming download to show progress
            response = requests.get("https://github.com/ffbinaries/ffbinaries-prebuilt/releases/download/v4.4.1/ffmpeg-4.4.1-win-64.zip", stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            downloaded = 0
            with open(zip_path, 'wb') as f:
                for data in response.iter_content(chunk_size=4096):
                    downloaded += len(data)
                    f.write(data)
                    if total_size > 0:
                        percent = int((downloaded / total_size) * 100)
                        self.progress.emit(percent)

            self.status.emit("Extracting FFmpeg...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.bin_path)
            
            os.remove(zip_path)
            self.finished.emit(True)
        except Exception as e:
            print(f"Error downloading FFmpeg: {e}")
            self.status.emit(f"Error: {e}")
            self.finished.emit(False)

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

def get_ffmpeg_path():
    """Returns the path to the ffmpeg executable."""
    # Check bundled path first
    bundled_ffmpeg = get_resource_path(os.path.join("bin", "ffmpeg.exe"))
    if os.path.exists(bundled_ffmpeg):
        return bundled_ffmpeg

    base_dir = os.path.dirname(os.path.abspath(__file__))
    bin_dir = os.path.join(base_dir, "bin")
    ffmpeg_exe = os.path.join(bin_dir, "ffmpeg.exe")
    
    if os.path.exists(ffmpeg_exe):
        return ffmpeg_exe
    
    # Also check if it's in the system PATH
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg
        
    return None
