import PyInstaller.__main__
import os
import platform
from PIL import Image
import tempfile

def convert_to_icns(png_path):
    """Convert PNG to ICNS for macOS."""
    if not os.path.exists(png_path):
        return None
    
    # Create a temporary directory for the iconset
    with tempfile.TemporaryDirectory() as iconset_path:
        sizes = [(16,16), (32,32), (64,64), (128,128), (256,256), (512,512), (1024,1024)]
        iconset_name = os.path.join(iconset_path, "icon.iconset")
        os.mkdir(iconset_name)
        
        # Load and resize image for different sizes
        img = Image.open(png_path)
        for size in sizes:
            icon_size = f"{size[0]}x{size[1]}"
            icon_path = os.path.join(iconset_name, f"icon_{icon_size}.png")
            resized = img.resize(size, Image.Resampling.LANCZOS)
            resized.save(icon_path)
            
            # Also create @2x version
            icon_path = os.path.join(iconset_name, f"icon_{size[0]//2}x{size[1]//2}@2x.png")
            resized.save(icon_path)
        
        # Convert iconset to icns
        icns_path = os.path.join(iconset_path, "icon.icns")
        os.system(f"iconutil -c icns {iconset_name} -o {icns_path}")
        
        if os.path.exists(icns_path):
            with open(icns_path, 'rb') as f:
                return icns_path
    return None

def build():
    # Get the directory containing images
    images_dir = os.path.join('hotwheelspdf', 'images')
    icon_path = os.path.join('hotwheelspdf', 'images', 'LogoBackground01.png')
    
    # Platform-specific settings
    path_sep = ';' if platform.system() == 'Windows' else ':'
    
    # Convert icon for macOS if needed
    if platform.system() == 'Darwin':
        icns_path = convert_to_icns(icon_path)
        if icns_path:
            icon_path = icns_path
    
    PyInstaller.__main__.run([
        'run.py',
        '--name=HotwheelsPDF',
        '--onefile',
        '--windowed',
        f'--add-data={images_dir}{path_sep}images',
        f'--icon={icon_path}',
        '--clean',
    ])

if __name__ == '__main__':
    build()
