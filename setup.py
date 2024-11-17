from setuptools import setup, find_packages

setup(
    name="hotwheelspdf",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15.0",
        "PyMuPDF>=1.18.0",
        "PyPDF2>=2.0.0"
    ],
    entry_points={
        'console_scripts': [
            'hotwheelspdf=hotwheelspdf.main:main',
        ],
    },
    package_data={
        'hotwheelspdf': ['images/*.png'],
    },
    author="Nicolas",
    description="A Hot Rod themed PDF manipulation tool with a flame-inspired interface",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="pdf, merge, split, rotate, hot rod, flames",
    url="https://github.com/yourusername/HotwheelsPDF",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.6",
)
