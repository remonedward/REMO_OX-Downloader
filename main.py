import sys
import os
from PyQt5.QtWidgets import QApplication
from ui_main import MainWindow

def main():
    # Set high DPI scaling for modern displays
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    
    # Set application-wide font (optional, but good for consistency)
    from PyQt5.QtGui import QFont
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    from PyQt5.QtCore import Qt
    main()
