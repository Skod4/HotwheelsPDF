import PyInstaller.__main__
import os
import platform

def build():
    # Get the directory containing images
    images_dir = os.path.join('hotwheelspdf', 'images')
    
    # Platform-specific path separator
    path_sep = ';' if platform.system() == 'Windows' else ':'
    
    PyInstaller.__main__.run([
        'run.py',
        '--name=HotwheelsPDF',
        '--onefile',
        '--windowed',
        f'--add-data={images_dir}{path_sep}images',
        '--icon=hotwheelspdf/images/LogoBackground01.png',
        '--clean',
    ])

if __name__ == '__main__':
    build()
