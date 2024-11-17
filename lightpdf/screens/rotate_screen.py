from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QFileDialog, QMessageBox, QSpinBox, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QDragEnterEvent, QDropEvent
import PyPDF2
from pathlib import Path
import fitz  # PyMuPDF for PDF preview
import os

class DropLabel(QLabel):
    """Label that accepts drag and drop of PDF files"""
    dropped = pyqtSignal(str)  # Signal emitted when PDF is dropped

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
                padding: 10px;
                background: #f8f8f8;
            }
            QLabel:hover {
                background: #f0f0f0;
                border-color: #999;
            }
        """)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1 and urls[0].toLocalFile().lower().endswith('.pdf'):
                event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            pdf_path = urls[0].toLocalFile()
            self.dropped.emit(pdf_path)

class RotateScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_pdf = None
        self.current_page = 1
        self.total_pages = 0
        self.preview_enabled = True
        self.export_folder = None  # Store custom export location
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # File selection area
        file_layout = QVBoxLayout()
        
        # Drag and drop area
        self.drop_label = DropLabel('Drag and drop PDF here\nor click Select PDF')
        self.drop_label.dropped.connect(self.load_pdf)
        file_layout.addWidget(self.drop_label)
        
        # File selection button
        select_file_btn = QPushButton('Select PDF')
        select_file_btn.clicked.connect(self.select_file)
        file_layout.addWidget(select_file_btn)
        
        # Selected file label
        self.file_label = QLabel('No file selected')
        file_layout.addWidget(self.file_label)
        
        layout.addLayout(file_layout)

        # Export folder selection
        export_layout = QHBoxLayout()
        export_label = QLabel('Export to:')
        self.export_path_label = QLabel('Same as input file')
        select_export_btn = QPushButton('Select Export Folder')
        select_export_btn.clicked.connect(self.select_export_folder)
        reset_export_btn = QPushButton('Reset to Default')
        reset_export_btn.clicked.connect(self.reset_export_folder)
        
        export_layout.addWidget(export_label)
        export_layout.addWidget(self.export_path_label, stretch=1)
        export_layout.addWidget(select_export_btn)
        export_layout.addWidget(reset_export_btn)
        layout.addLayout(export_layout)

        # Preview and rotation controls
        preview_controls = QHBoxLayout()
        
        # Left side: Preview
        preview_layout = QVBoxLayout()
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.preview_label)
        
        # Page navigation
        page_nav = QHBoxLayout()
        prev_btn = QPushButton('Previous')
        next_btn = QPushButton('Next')
        self.page_spin = QSpinBox()
        self.page_spin.setMinimum(1)
        self.total_pages_label = QLabel('/ 1')
        
        prev_btn.clicked.connect(self.prev_page)
        next_btn.clicked.connect(self.next_page)
        self.page_spin.valueChanged.connect(self.page_changed)
        
        page_nav.addWidget(prev_btn)
        page_nav.addWidget(self.page_spin)
        page_nav.addWidget(self.total_pages_label)
        page_nav.addWidget(next_btn)
        preview_layout.addLayout(page_nav)
        
        # Right side: Rotation controls
        rotation_layout = QVBoxLayout()
        rotate_left_btn = QPushButton('Rotate Left')
        rotate_right_btn = QPushButton('Rotate Right')
        self.preview_checkbox = QCheckBox('Show Preview')
        self.preview_checkbox.setChecked(True)
        
        rotate_left_btn.clicked.connect(lambda: self.rotate_page(-90))
        rotate_right_btn.clicked.connect(lambda: self.rotate_page(90))
        self.preview_checkbox.stateChanged.connect(self.toggle_preview)
        
        rotation_layout.addWidget(rotate_left_btn)
        rotation_layout.addWidget(rotate_right_btn)
        rotation_layout.addWidget(self.preview_checkbox)
        rotation_layout.addStretch()
        
        preview_controls.addLayout(preview_layout)
        preview_controls.addLayout(rotation_layout)
        layout.addLayout(preview_controls)

        # Action buttons
        button_layout = QHBoxLayout()
        back_btn = QPushButton('Back')
        save_btn = QPushButton('Save PDF')
        
        back_btn.clicked.connect(self.go_back)
        save_btn.clicked.connect(self.save_pdf)
        
        button_layout.addWidget(back_btn)
        button_layout.addWidget(save_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def select_export_folder(self):
        """Let user select a custom export folder"""
        folder = QFileDialog.getExistingDirectory(
            self, 'Select Export Folder', 
            self.export_folder or str(Path.home() / 'Downloads')
        )
        if folder:
            self.export_folder = folder
            self.export_path_label.setText(folder)
            self.export_path_label.setToolTip(folder)

    def reset_export_folder(self):
        """Reset export folder to default (same as input file)"""
        self.export_folder = None
        self.export_path_label.setText('Same as input file')
        self.export_path_label.setToolTip('')

    def get_default_export_folder(self):
        """Get the default export folder based on input file.
        Priority:
        1. User-selected export folder
        2. Parent folder of input PDF (if exists and writable)
        3. Downloads folder as fallback
        """
        if self.export_folder:
            return self.export_folder
            
        # Try to use parent folder of input PDF
        if self.current_pdf:
            try:
                parent = Path(self.current_pdf).parent
                # Check if the parent folder exists and is writable
                if parent.exists() and os.access(str(parent), os.W_OK):
                    return str(parent)
            except Exception:
                pass
                
        # Fallback to Downloads folder
        return str(Path.home() / 'Downloads')

    def get_output_path(self):
        """Generate output path for rotated PDF"""
        if not self.current_pdf:
            return None
            
        input_path = Path(self.current_pdf)
        output_dir = Path(self.get_default_export_folder())
        output_name = f'{input_path.stem}_rotated{input_path.suffix}'
        output_path = output_dir / output_name
        
        # Handle file name conflicts
        counter = 1
        while output_path.exists():
            output_name = f'{input_path.stem}_rotated_{counter}{input_path.suffix}'
            output_path = output_dir / output_name
            counter += 1
            
        return str(output_path)

    def load_pdf(self, pdf_path):
        """Load a PDF file (from drag and drop or file dialog)"""
        try:
            # Open the PDF
            self.doc = fitz.open(pdf_path)
            self.current_pdf = pdf_path
            self.total_pages = len(self.doc)
            
            # Update UI
            self.file_label.setText(Path(pdf_path).name)
            self.page_spin.setMaximum(self.total_pages)
            self.total_pages_label.setText(f'/ {self.total_pages}')
            
            # Show first page
            self.current_page = 1
            self.page_spin.setValue(1)
            self.update_preview()
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load PDF: {str(e)}')

    def select_file(self):
        """Open file dialog to select a PDF"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select PDF File',
            str(Path.home()), 'PDF Files (*.pdf)'
        )
        if file_path:
            self.load_pdf(file_path)

    def prev_page(self):
        """Show previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.page_spin.setValue(self.current_page)
            self.update_preview()

    def next_page(self):
        """Show next page"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.page_spin.setValue(self.current_page)
            self.update_preview()

    def page_changed(self, value):
        """Handle manual page number change"""
        self.current_page = value
        self.update_preview()

    def toggle_preview(self, state):
        """Toggle preview on/off"""
        self.preview_enabled = bool(state)
        if self.preview_enabled:
            self.update_preview()
        else:
            self.preview_label.clear()

    def rotate_page(self, angle):
        """Rotate current page by specified angle"""
        if not self.current_pdf:
            return
            
        try:
            # Get the current page
            page = self.doc[self.current_page - 1]
            
            # Calculate new rotation
            current_rotation = page.rotation
            new_rotation = (current_rotation + angle) % 360
            
            # Apply rotation
            page.set_rotation(new_rotation)
            
            # Update preview
            if self.preview_enabled:
                self.update_preview()
                
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to rotate page: {str(e)}')

    def update_preview(self):
        """Update the preview image"""
        if not self.current_pdf or not self.preview_enabled:
            return
            
        try:
            # Get the current page
            page = self.doc[self.current_page - 1]
            
            # Render page to image
            pix = page.get_pixmap()
            img = QPixmap.fromImage(pix.tobytes("ppm"))
            
            # Scale image to fit label while maintaining aspect ratio
            scaled_img = img.scaled(
                self.preview_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            self.preview_label.setPixmap(scaled_img)
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to update preview: {str(e)}')

    def save_pdf(self):
        """Save the rotated PDF"""
        if not self.current_pdf:
            QMessageBox.warning(self, 'Error', 'Please select a PDF file first.')
            return

        output_path = self.get_output_path()
        if not output_path:
            return

        try:
            # Save the modified PDF
            self.doc.save(output_path)
            QMessageBox.information(self, 'Success', 'PDF saved successfully!')
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save PDF: {str(e)}')

    def go_back(self):
        """Return to main screen while preserving window state"""
        if hasattr(self, 'doc'):
            self.doc.close()
        self.parent.show_main_screen()
