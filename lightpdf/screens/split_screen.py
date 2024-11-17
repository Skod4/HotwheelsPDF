from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QFileDialog, QLineEdit, QMessageBox, QSpinBox,
                           QCheckBox, QScrollArea, QFrame, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QDragEnterEvent, QDropEvent
import PyPDF2
from pathlib import Path
import fitz  # PyMuPDF for PDF preview
import re
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

class PageCheckBox(QCheckBox):
    """Custom checkbox that stores page information"""
    def __init__(self, page_num, label_text, parent=None):
        super().__init__(label_text, parent)
        self.page_num = page_num

class SplitScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_pdf = None
        self.current_page = 1
        self.total_pages = 0
        self.preview_enabled = True
        self.page_checkboxes = []  # List to store page checkboxes
        self.updating_ui = False  # Flag to prevent recursive updates
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

        # Preview and page selection area
        preview_select_layout = QHBoxLayout()
        
        # Left side: Preview
        preview_layout = QVBoxLayout()
        
        # Preview checkbox
        self.preview_checkbox = QCheckBox('Enable Preview')
        self.preview_checkbox.setChecked(self.preview_enabled)
        self.preview_checkbox.stateChanged.connect(self.on_preview_changed)
        preview_layout.addWidget(self.preview_checkbox)

        # Page navigation
        nav_layout = QHBoxLayout()
        prev_btn = QPushButton('Previous')
        next_btn = QPushButton('Next')
        self.page_spin = QSpinBox()
        self.page_spin.setMinimum(1)
        self.page_spin.valueChanged.connect(self.page_changed)
        prev_btn.clicked.connect(self.prev_page)
        next_btn.clicked.connect(self.next_page)

        nav_layout.addWidget(prev_btn)
        nav_layout.addWidget(self.page_spin)
        nav_layout.addWidget(next_btn)
        preview_layout.addLayout(nav_layout)

        # Preview area
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.preview_label)
        
        preview_select_layout.addLayout(preview_layout, stretch=2)

        # Right side: Page selection
        page_select_layout = QVBoxLayout()
        page_select_layout.addWidget(QLabel('Select Pages:'))
        
        # Scroll area for page checkboxes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Container for checkboxes
        self.checkbox_container = QFrame()
        self.checkbox_layout = QGridLayout()
        self.checkbox_container.setLayout(self.checkbox_layout)
        scroll_area.setWidget(self.checkbox_container)
        
        page_select_layout.addWidget(scroll_area)
        preview_select_layout.addLayout(page_select_layout, stretch=1)
        
        layout.addLayout(preview_select_layout)

        # Page range input
        range_layout = QHBoxLayout()
        range_label = QLabel('Page Range:')
        self.range_input = QLineEdit()
        self.range_input.setPlaceholderText('e.g., 1,3-5')
        self.range_input.textChanged.connect(self.on_range_input_changed)
        range_layout.addWidget(range_label)
        range_layout.addWidget(self.range_input)
        layout.addLayout(range_layout)

        # Action buttons
        button_layout = QHBoxLayout()
        back_btn = QPushButton('Back')
        split_btn = QPushButton('Split PDF')
        back_btn.clicked.connect(self.go_back)
        split_btn.clicked.connect(self.split_pdf)
        button_layout.addWidget(back_btn)
        button_layout.addWidget(split_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def create_page_checkboxes(self):
        """Create checkboxes for all pages with their labels"""
        # Clear existing checkboxes
        for i in reversed(range(self.checkbox_layout.count())): 
            self.checkbox_layout.itemAt(i).widget().setParent(None)
        self.page_checkboxes = []

        try:
            doc = fitz.open(self.current_pdf)
            for page_num in range(1, self.total_pages + 1):
                # Get page label if available
                page = doc[page_num - 1]
                page_label = page.get_label()
                if page_label and page_label != str(page_num):
                    label_text = f"Page {page_num} (Label: {page_label})"
                else:
                    label_text = f"Page {page_num}"

                # Create checkbox
                checkbox = PageCheckBox(page_num, label_text)
                checkbox.stateChanged.connect(lambda state, num=page_num: self.on_checkbox_state_changed(num, state))
                self.page_checkboxes.append(checkbox)
                
                # Add to grid layout (2 columns)
                row = (page_num - 1) // 2
                col = (page_num - 1) % 2
                self.checkbox_layout.addWidget(checkbox, row, col)
            
            doc.close()
        except Exception as e:
            print(f"Error creating page checkboxes: {str(e)}")

    def on_checkbox_state_changed(self, page_num, state):
        """Handle checkbox state changes and update the range input"""
        if self.updating_ui:
            return

        try:
            # Get all selected pages
            selected_pages = sorted([cb.page_num for cb in self.page_checkboxes if cb.isChecked()])
            
            # Convert to range string
            range_str = self.pages_to_range_str(selected_pages)
            
            # Update range input
            self.updating_ui = True
            self.range_input.setText(range_str)
            self.updating_ui = False
            
        except Exception as e:
            print(f"Error updating range input: {str(e)}")

    def pages_to_range_str(self, pages):
        """Convert a list of page numbers to a range string"""
        if not pages:
            return ""

        ranges = []
        start = end = pages[0]
        
        for page in pages[1:]:
            if page == end + 1:
                end = page
            else:
                # Add the previous range
                if start == end:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}-{end}")
                start = end = page
        
        # Add the last range
        if start == end:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}-{end}")
        
        return ",".join(ranges)

    def on_range_input_changed(self, text):
        """Update checkboxes when range input changes"""
        if self.updating_ui:
            return

        try:
            selected_pages = self.parse_page_range(text)
            
            # Update checkboxes
            self.updating_ui = True
            for checkbox in self.page_checkboxes:
                checkbox.setChecked(checkbox.page_num in selected_pages)
            self.updating_ui = False
            
        except ValueError:
            # Invalid input - don't update checkboxes
            pass

    def load_pdf(self, file_path):
        self.file_label.setText(file_path)
        self.current_pdf = file_path
        
        # Set total pages and update UI
        with open(file_path, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            self.total_pages = len(pdf.pages)
            self.page_spin.setMaximum(self.total_pages)
        
        # Create page checkboxes
        self.create_page_checkboxes()
        
        self.update_preview()

    def on_preview_changed(self, state):
        self.preview_enabled = state == Qt.Checked
        self.update_preview()

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select PDF file', '', 'PDF files (*.pdf)')
        if file_path:
            self.load_pdf(file_path)

    def page_changed(self, value):
        self.current_page = value
        self.update_preview()

    def prev_page(self):
        if self.current_page > 1:
            self.page_spin.setValue(self.current_page - 1)

    def next_page(self):
        if self.current_page < self.total_pages:
            self.page_spin.setValue(self.current_page + 1)

    def update_preview(self):
        if not self.current_pdf or not self.preview_enabled:
            self.preview_label.clear()
            return

        try:
            # Open the PDF with PyMuPDF
            doc = fitz.open(self.current_pdf)
            if 0 <= self.current_page - 1 < doc.page_count:
                page = doc[self.current_page - 1]
                
                # Render page to image
                matrix = fitz.Matrix(2, 2)  # 2x zoom for better quality
                pix = page.get_pixmap(matrix=matrix)
                img_data = pix.tobytes("ppm")
                
                # Create QPixmap from image data
                pixmap = QPixmap()
                pixmap.loadFromData(img_data)
                
                # Scale pixmap to fit the preview label while maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    self.preview_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                
                self.preview_label.setPixmap(scaled_pixmap)
            doc.close()
            
        except Exception as e:
            self.preview_label.setText('Preview not available')
            print(f'Preview error: {str(e)}')

    def parse_page_range(self, range_str):
        """Parse a page range string into a list of page numbers.
        Examples:
            "1,3-5" -> [1, 3, 4, 5]
            "1-3,5" -> [1, 2, 3, 5]
        """
        if not range_str.strip():
            return []

        pages = set()
        parts = range_str.split(',')
        
        for part in parts:
            part = part.strip()
            if '-' in part:
                try:
                    start, end = map(int, part.split('-'))
                    if start > end:
                        start, end = end, start
                    pages.update(range(start, end + 1))
                except ValueError:
                    raise ValueError(f"Invalid range format: {part}")
            else:
                try:
                    pages.add(int(part))
                except ValueError:
                    raise ValueError(f"Invalid page number: {part}")

        # Validate page numbers
        if not all(1 <= page <= self.total_pages for page in pages):
            raise ValueError(f"Page numbers must be between 1 and {self.total_pages}")

        return sorted(list(pages))

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

    def get_output_path(self, input_path, pages):
        """Generate output path based on selected export folder"""
        input_path = Path(input_path)
        output_dir = Path(self.get_default_export_folder())
        
        # Create a concise page range string for the filename
        page_str = '_'.join(str(p) for p in pages)
        if len(page_str) > 30:  # If too long, use first and last page
            page_str = f'{pages[0]}-{pages[-1]}'
            
        output_name = f'{input_path.stem}_pages_{page_str}{input_path.suffix}'
        output_path = output_dir / output_name
        
        # Handle file name conflicts
        counter = 1
        while output_path.exists():
            output_name = f'{input_path.stem}_pages_{page_str}_{counter}{input_path.suffix}'
            output_path = output_dir / output_name
            counter += 1
            
        return str(output_path)

    def split_pdf(self):
        if not self.current_pdf:
            QMessageBox.warning(self, 'Error', 'Please select a PDF file first.')
            return

        # Get selected pages from checkboxes
        selected_pages = sorted([cb.page_num for cb in self.page_checkboxes if cb.isChecked()])
        
        if not selected_pages:
            QMessageBox.warning(self, 'Error', 'Please select at least one page to split.')
            return

        try:
            # Create output PDF with selected pages
            pdf_writer = PyPDF2.PdfWriter()
            with open(self.current_pdf, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Add selected pages to the output PDF
                for page_num in selected_pages:
                    pdf_writer.add_page(pdf_reader.pages[page_num - 1])
                
                # Generate output filename
                output_path = self.get_output_path(self.current_pdf, selected_pages)
                
                # Write the output PDF
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)

            QMessageBox.information(self, 'Success', 'PDF split successfully!')
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred while splitting the PDF: {str(e)}')

    def go_back(self):
        """Return to main screen while preserving window state"""
        self.parent.show_main_screen()
