import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QPushButton, QStatusBar)
from PyQt5.QtCore import Qt, QSettings
from .screens.split_screen import SplitScreen
from .screens.merge_screen import MergeScreen
from .screens.rotate_screen import RotateScreen
from .utils.settings import Settings

class LightPDF(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.window_settings = QSettings('Codeium', 'LightPDF')
        self.init_ui()
        self.restore_window_state()

    def init_ui(self):
        self.setWindowTitle('LightPDF')
        
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Create main buttons
        self.split_btn = QPushButton('Split PDF', self)
        self.merge_btn = QPushButton('Merge PDFs', self)
        self.rotate_btn = QPushButton('Rotate PDF', self)

        # Add widgets to layout
        layout.addWidget(self.split_btn)
        layout.addWidget(self.merge_btn)
        layout.addWidget(self.rotate_btn)

        # Connect button signals
        self.split_btn.clicked.connect(self.show_split_screen)
        self.merge_btn.clicked.connect(self.show_merge_screen)
        self.rotate_btn.clicked.connect(self.show_rotate_screen)

        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('Ready')

    def restore_window_state(self):
        """Restore window geometry and state from settings"""
        geometry = self.window_settings.value('geometry')
        if geometry is not None:
            self.restoreGeometry(geometry)
        else:
            # Default position and size if no saved state
            self.setGeometry(100, 100, 800, 600)

    def save_window_state(self):
        """Save window geometry and state to settings"""
        self.window_settings.setValue('geometry', self.saveGeometry())

    def show_split_screen(self):
        self.save_window_state()  # Save current state before switching
        self.split_screen = SplitScreen(self)
        self.setCentralWidget(self.split_screen)
        self.restore_window_state()  # Restore state after switching

    def show_merge_screen(self):
        self.save_window_state()
        self.merge_screen = MergeScreen(self)
        self.setCentralWidget(self.merge_screen)
        self.restore_window_state()

    def show_rotate_screen(self):
        self.save_window_state()
        self.rotate_screen = RotateScreen(self)
        self.setCentralWidget(self.rotate_screen)
        self.restore_window_state()

    def closeEvent(self, event):
        """Save window state when closing the application"""
        self.save_window_state()
        super().closeEvent(event)

    def show_main_screen(self):
        """Return to main screen while preserving window state"""
        self.save_window_state()
        self.init_ui()
        self.restore_window_state()

def main():
    app = QApplication(sys.argv)
    window = LightPDF()
    window.show()
    sys.exit(app.exec_())
