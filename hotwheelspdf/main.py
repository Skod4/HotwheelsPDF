import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QPushButton, QStatusBar, QLabel)
from PyQt5.QtCore import Qt, QSettings, QTimer, QEvent
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from .screens.split_screen import SplitScreen
from .screens.merge_screen import MergeScreen
from .screens.rotate_screen import RotateScreen
from .utils.settings import Settings

class HotwheelsPDF(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.window_settings = QSettings('Codeium', 'HotwheelsPDF')
        self.init_ui()
        self.restore_window_state()

    def init_ui(self):
        self.setWindowTitle('HotwheelsPDF')
        
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Setup background first (so it's behind everything)
        self.setup_background()

        # Add logo at the top
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), 'images', 'LogoBackground01.png')
        logo_pixmap = QPixmap(logo_path)
        scaled_logo = logo_pixmap.scaled(265, 132, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_logo)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Add spacing for better layout
        layout.addSpacing(20)

        # Create main buttons
        self.split_btn = QPushButton('Split PDF', self)
        self.merge_btn = QPushButton('Merge PDFs', self)
        self.rotate_btn = QPushButton('Rotate PDF', self)

        # Style the buttons
        button_style = """
            QPushButton {
                background-color: rgba(40, 40, 40, 180);
                color: white;
                border: 2px solid #FF4400;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(60, 60, 60, 180);
                border: 2px solid #FF6600;
            }
        """
        self.split_btn.setStyleSheet(button_style)
        self.merge_btn.setStyleSheet(button_style)
        self.rotate_btn.setStyleSheet(button_style)

        # Add widgets to layout
        layout.addWidget(self.split_btn)
        layout.addWidget(self.merge_btn)
        layout.addWidget(self.rotate_btn)

        # Add stretching space to push buttons up
        layout.addStretch()

        # Connect button signals
        self.split_btn.clicked.connect(self.show_split_screen)
        self.merge_btn.clicked.connect(self.show_merge_screen)
        self.rotate_btn.clicked.connect(self.show_rotate_screen)

        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('Ready')
        self.statusBar.setStyleSheet("background-color: rgba(40, 40, 40, 180); color: white;")

    def setup_background(self):
        """Set up the background image"""
        try:
            # Remove any existing background label
            if hasattr(self, 'background_label') and self.background_label:
                self.background_label.deleteLater()
                
            # Create and set up the background
            flames_path = os.path.join(os.path.dirname(__file__), 'images', 'flamesBackground01.png')
            if not os.path.exists(flames_path):
                print(f"Warning: Background image not found at {flames_path}")
                return

            self.background_label = QLabel(self)
            self.background_pixmap = QPixmap(flames_path)
            
            if self.background_pixmap.isNull():
                print(f"Warning: Failed to load background image from {flames_path}")
                return

            # Set up the background label
            self.background_label.setAttribute(Qt.WA_TransparentForMouseEvents)
            self.background_label.setParent(self)  # Ensure it's parented to the main window
            self.background_label.lower()  # Keep it behind other widgets
            self.update_background()
        except Exception as e:
            print(f"Error setting up background: {str(e)}")

    def update_background(self):
        """Update the background size and position"""
        try:
            if not hasattr(self, 'background_label') or not self.background_label:
                return

            if not self.background_label.parent() is self:
                # If parent is wrong, recreate the background
                self.setup_background()
                return

            if not hasattr(self, 'background_pixmap') or self.background_pixmap.isNull():
                return

            # Get dimensions, ensuring they're not zero
            pixmap_width = max(1, self.background_pixmap.width())
            pixmap_height = max(1, self.background_pixmap.height())
            window_width = max(1, self.width())
            window_height = max(1, self.height())

            # Calculate target height (half of window height)
            target_height = window_height // 2
            
            # Calculate the width needed to maintain aspect ratio
            aspect_ratio = pixmap_width / pixmap_height
            target_width = int(target_height * aspect_ratio)
            
            # If target width is less than window width, scale based on width instead
            if target_width < window_width:
                target_width = window_width
                target_height = int(target_width / aspect_ratio)
            
            # Scale the pixmap
            scaled_pixmap = self.background_pixmap.scaled(
                target_width,
                target_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            # Calculate x position to center horizontally if wider than window
            x_position = (window_width - scaled_pixmap.width()) // 2
            
            # Set the pixmap and position
            self.background_label.setPixmap(scaled_pixmap)
            self.background_label.setGeometry(
                x_position,
                window_height - scaled_pixmap.height(),
                scaled_pixmap.width(),
                scaled_pixmap.height()
            )
            
            # Ensure it stays behind other widgets
            self.background_label.lower()
            self.background_label.show()
        except Exception as e:
            print(f"Error updating background: {str(e)}")

    def resizeEvent(self, event):
        """Handle window resize events"""
        super().resizeEvent(event)
        self.update_background()

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

    def showEvent(self, event):
        """Handle window show events"""
        super().showEvent(event)
        if hasattr(self, 'background_label'):
            self.update_background()

    def changeEvent(self, event):
        """Handle window state changes (maximize, minimize, etc.)"""
        super().changeEvent(event)
        if event.type() == QEvent.WindowStateChange and hasattr(self, 'background_label'):
            # Use QTimer to delay the update slightly to ensure proper window dimensions
            QTimer.singleShot(100, self.update_background)

    def show_split_screen(self):
        self.save_window_state()
        if hasattr(self, 'background_label'):
            self.background_label.setParent(self)  # Ensure background stays with main window
        self.split_screen = SplitScreen(self)
        self.setCentralWidget(self.split_screen)
        self.restore_window_state()
        QTimer.singleShot(50, self.update_background)  # Update background after a short delay

    def show_merge_screen(self):
        self.save_window_state()
        if hasattr(self, 'background_label'):
            self.background_label.setParent(self)  # Ensure background stays with main window
        self.merge_screen = MergeScreen(self)
        self.setCentralWidget(self.merge_screen)
        self.restore_window_state()
        QTimer.singleShot(50, self.update_background)

    def show_rotate_screen(self):
        self.save_window_state()
        if hasattr(self, 'background_label'):
            self.background_label.setParent(self)  # Ensure background stays with main window
        self.rotate_screen = RotateScreen(self)
        self.setCentralWidget(self.rotate_screen)
        self.restore_window_state()
        QTimer.singleShot(50, self.update_background)

    def show_main_screen(self):
        """Return to main screen while preserving window state"""
        self.save_window_state()
        if hasattr(self, 'background_label'):
            self.background_label.setParent(self)  # Ensure background stays with main window
        self.init_ui()
        self.restore_window_state()
        QTimer.singleShot(50, self.update_background)

    def closeEvent(self, event):
        """Save window state when closing the application"""
        self.save_window_state()
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    window = HotwheelsPDF()
    window.show()
    sys.exit(app.exec_())
