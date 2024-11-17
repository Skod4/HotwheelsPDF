from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QFileDialog, QMessageBox, QListWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
import PyPDF2
from pathlib import Path
import os

class DropListWidget(QListWidget):
    """List widget that accepts drag and drop of PDF files"""
    dropped = pyqtSignal(list)  # Signal emitted when PDFs are dropped

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QListWidget {
                border: 2px dashed #aaa;
                border-radius: 5px;
                background: #f8f8f8;
            }
            QListWidget:hover {
                background: #f0f0f0;
                border-color: #999;
            }
        """)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if all(url.toLocalFile().lower().endswith('.pdf') for url in urls):
                event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            pdf_paths = [url.toLocalFile() for url in urls 
                        if url.toLocalFile().lower().endswith('.pdf')]
            self.dropped.emit(pdf_paths)

class MergeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.pdf_files = []
        self.export_folder = None  # Store custom export location
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Instructions
        instructions = QLabel('Add PDF files to merge. Drag to reorder.')
        instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(instructions)

        # PDF list with drag and drop support
        self.pdf_list = DropListWidget()
        self.pdf_list.dropped.connect(self.add_pdfs)
        layout.addWidget(self.pdf_list)

        # Buttons for file management
        btn_layout = QHBoxLayout()
        add_btn = QPushButton('Add PDFs')
        add_btn.clicked.connect(self.select_files)
        remove_btn = QPushButton('Remove Selected')
        remove_btn.clicked.connect(self.remove_selected)
        clear_btn = QPushButton('Clear All')
        clear_btn.clicked.connect(self.clear_files)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(remove_btn)
        btn_layout.addWidget(clear_btn)
        layout.addLayout(btn_layout)

        # Export folder selection
        export_layout = QHBoxLayout()
        export_label = QLabel('Export to:')
        self.export_path_label = QLabel('Same as first PDF')
        select_export_btn = QPushButton('Select Export Folder')
        select_export_btn.clicked.connect(self.select_export_folder)
        reset_export_btn = QPushButton('Reset to Default')
        reset_export_btn.clicked.connect(self.reset_export_folder)
        
        export_layout.addWidget(export_label)
        export_layout.addWidget(self.export_path_label, stretch=1)
        export_layout.addWidget(select_export_btn)
        export_layout.addWidget(reset_export_btn)
        layout.addLayout(export_layout)

        # Merge and back buttons
        action_layout = QHBoxLayout()
        merge_btn = QPushButton('Merge PDFs')
        merge_btn.clicked.connect(self.merge_pdfs)
        back_btn = QPushButton('Back')
        back_btn.clicked.connect(self.go_back)
        
        action_layout.addWidget(back_btn)
        action_layout.addWidget(merge_btn)
        layout.addLayout(action_layout)

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
        """Reset export folder to default (same as first input file)"""
        self.export_folder = None
        self.export_path_label.setText('Same as first PDF')
        self.export_path_label.setToolTip('')

    def get_default_export_folder(self):
        """Get the default export folder based on input files.
        Priority:
        1. User-selected export folder
        2. First valid parent folder from input PDFs
        3. Downloads folder as fallback
        """
        if self.export_folder:
            return self.export_folder
            
        # Try to find first valid parent folder from input PDFs
        for pdf_path in self.pdf_files:
            try:
                parent = Path(pdf_path).parent
                # Check if the parent folder exists and is writable
                if parent.exists() and os.access(str(parent), os.W_OK):
                    return str(parent)
            except Exception:
                continue
                
        # Fallback to Downloads folder
        return str(Path.home() / 'Downloads')

    def add_pdfs(self, pdf_paths):
        """Add PDFs to the list (from drag and drop or file dialog)"""
        for path in pdf_paths:
            if path not in self.pdf_files:
                self.pdf_files.append(path)
                self.pdf_list.addItem(Path(path).name)

    def select_files(self):
        """Open file dialog to select PDFs"""
        files, _ = QFileDialog.getOpenFileNames(
            self, 'Select PDF Files', 
            str(Path.home()), 'PDF Files (*.pdf)'
        )
        if files:
            self.add_pdfs(files)

    def remove_selected(self):
        """Remove selected PDFs from the list"""
        for item in self.pdf_list.selectedItems():
            idx = self.pdf_list.row(item)
            self.pdf_list.takeItem(idx)
            self.pdf_files.pop(idx)

    def clear_files(self):
        """Clear all PDFs from the list"""
        self.pdf_list.clear()
        self.pdf_files.clear()

    def get_output_path(self):
        """Generate output path for merged PDF"""
        if not self.pdf_files:
            return None
            
        output_dir = Path(self.get_default_export_folder())
        base_name = 'merged'
        
        # Try to create a meaningful name from input files
        if len(self.pdf_files) <= 3:
            stems = [Path(f).stem for f in self.pdf_files]
            base_name = '_'.join(stems)
        
        output_path = output_dir / f'{base_name}.pdf'
        
        # Handle file name conflicts
        counter = 1
        while output_path.exists():
            output_path = output_dir / f'{base_name}_{counter}.pdf'
            counter += 1
            
        return str(output_path)

    def merge_pdfs(self):
        if len(self.pdf_files) < 2:
            QMessageBox.warning(self, 'Error', 'Please select at least 2 PDF files to merge.')
            return

        output_path = self.get_output_path()
        if not output_path:
            return

        try:
            merger = PyPDF2.PdfMerger()
            
            # Add each PDF to the merger
            for pdf_file in self.pdf_files:
                merger.append(pdf_file)
            
            # Write the merged PDF
            merger.write(output_path)
            merger.close()
            
            QMessageBox.information(self, 'Success', 'PDFs merged successfully!')
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred while merging PDFs: {str(e)}')

    def go_back(self):
        """Return to main screen while preserving window state"""
        self.parent.show_main_screen()
