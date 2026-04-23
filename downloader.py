import yt_dlp
import os
from PyQt5.QtCore import QThread, pyqtSignal

class DownloaderThread(QThread):
    progress = pyqtSignal(dict)
    finished = pyqtSignal(bool, str)
    status = pyqtSignal(str)

    def __init__(self, url, options, target_folder):
        super().__init__()
        self.url = url
        self.options = options
        self.target_folder = target_folder
        self._is_cancelled = False

    def run(self):
        try:
            ydl_opts = {
                'format': self.options.get('format', 'bestvideo+bestaudio/best'),
                'outtmpl': os.path.join(self.target_folder, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'logger': MyLogger(self),
                'nocheckcertificate': True,
                'quiet': True,
                'no_warnings': True,
            }

            # If audio only requested
            if self.options.get('audio_only'):
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]

            # Set ffmpeg location if provided
            if self.options.get('ffmpeg_location'):
                ydl_opts['ffmpeg_location'] = self.options.get('ffmpeg_location')

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            
            if not self._is_cancelled:
                self.finished.emit(True, "Success")
        except Exception as e:
            self.finished.emit(False, str(e))

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            self.progress.emit(d)
        elif d['status'] == 'finished':
            self.status.emit("Processing...")

    def cancel(self):
        self._is_cancelled = True

class MyLogger:
    def __init__(self, thread):
        self.thread = thread

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        self.thread.status.emit(f"Error: {msg}")

def get_info(url):
    """Fetches video information without downloading."""
    ydl_opts = {
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info
        except Exception as e:
            return {"error": str(e)}
