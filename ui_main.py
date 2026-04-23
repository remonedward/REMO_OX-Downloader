import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QLabel, QComboBox, 
                             QProgressBar, QFileDialog, QFrame)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

from translations import TRANSLATIONS
from downloader import DownloaderThread, get_info
from ffmpeg_utils import FFmpegDownloader, get_ffmpeg_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = 'ar'  # Default language is Arabic
        self.download_thread = None
        self.ffmpeg_thread = None
        self.ffmpeg_path = get_ffmpeg_path()
        self.init_ui()
        self.apply_styles()
        self.update_texts()

    def init_ui(self):
        self.setWindowTitle(TRANSLATIONS[self.lang]['title'])
        self.setMinimumSize(600, 450)
        
        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # Header with Title and Language Toggle
        header_layout = QHBoxLayout()
        self.title_label = QLabel(TRANSLATIONS[self.lang]['title'])
        self.title_label.setFont(QFont('Segoe UI', 18, QFont.Bold))
        self.title_label.setStyleSheet("color: #00d2ff;")
        
        self.lang_btn = QPushButton(TRANSLATIONS[self.lang]['lang_toggle'])
        self.lang_btn.setFixedWidth(100)
        self.lang_btn.setCursor(Qt.PointingHandCursor)
        self.lang_btn.clicked.connect(self.toggle_language)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.lang_btn)
        self.main_layout.addLayout(header_layout)

        # URL Input Section
        url_section = QVBoxLayout()
        self.url_label = QLabel(TRANSLATIONS[self.lang]['url_label'])
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://...")
        self.url_input.setFixedHeight(40)
        
        url_section.addWidget(self.url_label)
        url_section.addWidget(self.url_input)
        self.main_layout.addLayout(url_section)

        # Format and Quality Section
        options_layout = QHBoxLayout()
        
        # Format
        format_vbox = QVBoxLayout()
        self.format_label = QLabel(TRANSLATIONS[self.lang]['format_label'])
        self.format_combo = QComboBox()
        self.format_combo.addItems([TRANSLATIONS[self.lang]['video'], TRANSLATIONS[self.lang]['audio']])
        self.format_combo.setFixedHeight(35)
        format_vbox.addWidget(self.format_label)
        format_vbox.addWidget(self.format_combo)
        
        # Quality
        quality_vbox = QVBoxLayout()
        self.quality_label = QLabel(TRANSLATIONS[self.lang]['quality_label'])
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["1080p", "720p", "480p", "360p", "Best Available"])
        self.quality_combo.setFixedHeight(35)
        quality_vbox.addWidget(self.quality_label)
        quality_vbox.addWidget(self.quality_combo)
        
        options_layout.addLayout(format_vbox)
        options_layout.addLayout(quality_vbox)
        self.main_layout.addLayout(options_layout)

        # Download Path Section
        path_layout = QHBoxLayout()
        self.path_label = QLabel(TRANSLATIONS[self.lang]['path_label'])
        self.path_input = QLineEdit()
        self.path_input.setText(os.path.join(os.path.expanduser('~'), 'Downloads'))
        self.path_btn = QPushButton(TRANSLATIONS[self.lang]['browse_btn'])
        self.path_btn.clicked.connect(self.browse_folder)
        
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.path_btn)
        
        self.main_layout.addWidget(self.path_label)
        self.main_layout.addLayout(path_layout)

        # Progress and Status
        self.status_label = QLabel(TRANSLATIONS[self.lang]['status_ready'])
        self.status_label.setAlignment(Qt.AlignCenter)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.progress_bar)

        # Action Buttons
        self.download_btn = QPushButton(TRANSLATIONS[self.lang]['download_btn'])
        self.download_btn.setFixedHeight(50)
        self.download_btn.setFont(QFont('Segoe UI', 12, QFont.Bold))
        self.download_btn.setCursor(Qt.PointingHandCursor)
        self.download_btn.clicked.connect(self.start_download)
        self.main_layout.addWidget(self.download_btn)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #1e1e1e;
                border: 2px solid #333;
                border-radius: 8px;
                padding: 8px;
                color: white;
                selection-background-color: #00d2ff;
            }
            QLineEdit:focus {
                border-color: #0078d7;
            }
            QPushButton {
                background-color: #333;
                border: none;
                border-radius: 8px;
                padding: 10px;
                color: white;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QPushButton#DownloadButton {
                background-color: #0078d7;
            }
            QPushButton#DownloadButton:hover {
                background-color: #008aff;
            }
            QComboBox {
                background-color: #1e1e1e;
                border: 2px solid #333;
                border-radius: 8px;
                padding: 5px;
                color: white;
            }
            QProgressBar {
                background-color: #1e1e1e;
                border: 1px solid #333;
                border-radius: 6px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #00d2ff, stop:1 #3a7bd5);
                border-radius: 6px;
            }
        """)
        self.download_btn.setObjectName("DownloadButton")

    def toggle_language(self):
        self.lang = 'en' if self.lang == 'ar' else 'ar'
        self.update_texts()

    def update_texts(self):
        t = TRANSLATIONS[self.lang]
        self.setWindowTitle(t['title'])
        self.title_label.setText(t['title'])
        self.lang_btn.setText(t['lang_toggle'])
        self.url_label.setText(t['url_label'])
        self.format_label.setText(t['format_label'])
        self.quality_label.setText(t['quality_label'])
        self.path_label.setText(t['path_label'])
        self.path_btn.setText(t['browse_btn'])
        self.download_btn.setText(t['download_btn'])
        self.status_label.setText(t['status_ready'])
        
        # Update combo items
        self.format_combo.clear()
        self.format_combo.addItems([t['video'], t['audio']])
        
        # RTL support
        layout_dir = Qt.RightToLeft if self.lang == 'ar' else Qt.LeftToRight
        self.central_widget.setLayoutDirection(layout_dir)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, self.path_label.text())
        if folder:
            self.path_input.setText(folder)

    def start_download(self):
        url = self.url_input.text()
        if not url:
            self.status_label.setText(TRANSLATIONS[self.lang]['status_error'].format("Empty URL"))
            return

        # Check FFmpeg
        if not self.ffmpeg_path:
            self.download_ffmpeg()
            return

        self.download_btn.setEnabled(False)
        self.status_label.setText(TRANSLATIONS[self.lang]['checking_btn'])
        self.progress_bar.setValue(0)

        options = {
            'format': 'bestvideo+bestaudio/best',
            'audio_only': self.format_combo.currentIndex() == 1,
            'ffmpeg_location': self.ffmpeg_path
        }
        
        # Map quality
        quality_map = ["1080", "720", "480", "360", "best"]
        quality = quality_map[self.quality_combo.currentIndex()]
        if not options['audio_only'] and quality != "best":
            options['format'] = f"bestvideo[height<={quality}]+bestaudio/best"

        self.download_thread = DownloaderThread(url, options, self.path_input.text())
        self.download_thread.progress.connect(self.on_progress)
        self.download_thread.finished.connect(self.on_finished)
        self.download_thread.status.connect(self.on_status)
        self.download_thread.start()

    def download_ffmpeg(self):
        self.status_label.setText(TRANSLATIONS[self.lang]['ffmpeg_not_found'])
        self.download_btn.setEnabled(False)
        
        bin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
        self.ffmpeg_thread = FFmpegDownloader(bin_dir)
        self.ffmpeg_thread.progress.connect(self.on_ffmpeg_progress)
        self.ffmpeg_thread.status.connect(self.on_status)
        self.ffmpeg_thread.finished.connect(self.on_ffmpeg_finished)
        self.ffmpeg_thread.start()

    def on_progress(self, d):
        percent_str = d.get('_percent_str', '0%').replace('%', '').strip()
        try:
            percent = float(percent_str)
            self.progress_bar.setValue(int(percent))
            self.status_label.setText(TRANSLATIONS[self.lang]['status_downloading'].format(int(percent)))
        except:
            pass

    def on_finished(self, success, message):
        self.download_btn.setEnabled(True)
        if success:
            self.status_label.setText(TRANSLATIONS[self.lang]['status_finished'])
            self.progress_bar.setValue(100)
        else:
            self.status_label.setText(TRANSLATIONS[self.lang]['status_error'].format(message))

    def on_status(self, text):
        self.status_label.setText(text)

    def on_ffmpeg_progress(self, percent):
        self.progress_bar.setValue(percent)
        self.status_label.setText(TRANSLATIONS[self.lang]['ffmpeg_downloading'].format(percent))

    def on_ffmpeg_finished(self, success):
        if success:
            self.ffmpeg_path = get_ffmpeg_path()
            self.status_label.setText(TRANSLATIONS[self.lang]['ffmpeg_ready'])
            self.download_btn.setEnabled(True)
            # Auto start download after ffmpeg is ready
            self.start_download()
        else:
            self.status_label.setText(TRANSLATIONS[self.lang]['status_error'].format("FFmpeg Download Failed"))
            self.download_btn.setEnabled(True)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
