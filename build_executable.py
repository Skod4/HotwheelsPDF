import PyInstaller.__main__
import os
import sys

def build():
    # Get the directory containing images
    images_dir = os.path.join('hotwheelspdf', 'images')
    
    PyInstaller.__main__.run([
        'run.py',
        '--name=HotwheelsPDF',
        '--onefile',
        '--windowed',
        f'--add-data={images_dir}{os.pathsep}images',
        '--icon=hotwheelspdf/images/LogoBackground01.png',
        '--clean',
    ])

if __name__ == '__main__':
    build()
