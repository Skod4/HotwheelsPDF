import PyInstaller.__main__
import os
import platform
from PIL import Image
import tempfile
import shutil

def convert_to_icns(png_path, workpath):
    """Convert PNG to ICNS for macOS."""
    if not os.path.exists(png_path):
        return None
    
    # Create iconset in the build directory
    iconset_name = os.path.join(workpath, "icon.iconset")
    os.makedirs(iconset_name, exist_ok=True)
    
    sizes = [(16,16), (32,32), (64,64), (128,128), (256,256), (512,512), (1024,1024)]
    
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
    icns_path = os.path.join(workpath, "icon.icns")
    os.system(f"iconutil -c icns {iconset_name} -o {icns_path}")
    
    if os.path.exists(icns_path):
        return icns_path
    return None

def convert_to_ico(png_path, workpath):
    """Convert PNG to ICO for Windows."""
    if not os.path.exists(png_path):
        return None
    
    # Save ICO directly in the build directory
    ico_path = os.path.join(workpath, "icon.ico")
    
    # Load the image and convert to RGBA
    img = Image.open(png_path).convert('RGBA')
    
    # Create ICO file with multiple sizes
    sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
    img.save(ico_path, format='ICO', sizes=sizes)
    
    if os.path.exists(ico_path):
        return ico_path
    return None

def build():
    # Get the directory containing images
    images_dir = os.path.join('hotwheelspdf', 'images')
    icon_path = os.path.join('hotwheelspdf', 'images', 'LogoBackground01.png')
    
    # Create a work directory that won't be deleted
    work_dir = os.path.join(os.getcwd(), 'build', 'icon_work')
    os.makedirs(work_dir, exist_ok=True)
    
    # Platform-specific settings
    path_sep = ';' if platform.system() == 'Windows' else ':'
    
    # Convert icon based on platform
    if platform.system() == 'Darwin':
        converted_icon = convert_to_icns(icon_path, work_dir)
    elif platform.system() == 'Windows':
        converted_icon = convert_to_ico(icon_path, work_dir)
    else:
        converted_icon = None
    
    # Use converted icon if available, otherwise use original
    icon_arg = converted_icon if converted_icon else icon_path
    
    PyInstaller.__main__.run([
        'run.py',
        '--name=HotwheelsPDF',
        '--onefile',
        '--windowed',
        f'--add-data={images_dir}{path_sep}images',
        f'--icon={icon_arg}',
        '--clean',
        f'--workpath={work_dir}'
    ])

if __name__ == '__main__':
    build()
