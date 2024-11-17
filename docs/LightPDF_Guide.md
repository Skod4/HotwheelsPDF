

LightPDF Software Documentation
Table of Contents
Introduction
Overview
Functional Requirements
General Features
Split Functionality
Merge Functionality
Rotate Functionality
Non-Functional Requirements
User Interface Design
Main Screen
Split Screen
Merge Screen
Rotate Screen
Common Elements
Technical Specifications
Technology Stack
Performance Optimization
Error Handling
Additional Considerations
File Handling
User Preferences
Internationalization
Development Plan
Milestones
Testing
Conclusion
Introduction
This document provides a comprehensive guide for the development of LightPDF, a lightweight, fast, and user-friendly PDF manipulation tool written in Python. The software includes functionalities to split, merge, and rotate PDF files with an intuitive graphical user interface (GUI).

Overview
LightPDF aims to offer users a seamless experience in handling PDF files by providing essential features in a streamlined application. The software focuses on simplicity, speed, and usability, ensuring that users can perform tasks efficiently without unnecessary complexity.

Functional Requirements
General Features
Platform: Desktop application for Windows, macOS, and Linux.
Language: Python 3.x.
GUI Framework: PyQt5 or Tkinter for cross-platform compatibility.
Drag and Drop Support: Users can drag and drop PDF files into the application.
File Selection: Users can select files via a file dialog.
Default Output Directory: The default output directory is the original PDF's location or a user-defined directory.
Memory Persistence: The application remembers user settings and preferences between sessions.
Preview Option: Users can enable or disable a preview of the PDF pages.
Graceful Handling of Duplicates: Output files are named uniquely to prevent overwriting.
Split Functionality
Multiple PDF Support: Users can select or drag and drop multiple PDF files for splitting.
Page Specification: Users can specify pages to split using a text box with a specific format (e.g., 1-3,4,~4).
Format Guidelines: Greyed-out instructional text in the input box guides users on formatting.
Separate Exports: The ~ symbol denotes pages to be exported as separate files.
Default Naming Convention: Output files are named with the original filename appended with _split_X.
Merge Functionality
File Selection: Users can select or drag and drop multiple PDF files to merge.
Order Adjustment: Users can reorder the selected PDF files.
Default Naming Convention: Output files are named with the original filename appended with _merged_X.
Rotate Functionality
Single or Multiple PDFs: Users can select or drag and drop one or multiple PDF files.
Page Selection: Users can navigate through pages using arrow buttons or input a page number directly.
Rotation Options: Users can rotate pages clockwise or counterclockwise.
Preview: A preview of the current page is displayed.
Settings Memory: Rotation settings persist when switching between pages and PDFs.
Default Naming Convention: Output files are named with the original filename appended with _rotated_X.
Limitation: Page rotation works on one PDF file at a time; the rotate option is disabled if multiple files are selected.
Non-Functional Requirements
Performance: The application should be lightweight and perform operations quickly.
Usability: The interface should be intuitive and user-friendly.
Reliability: The software should handle errors gracefully without crashes.
Portability: The application should run on major operating systems (Windows, macOS, Linux).
Scalability: Capable of handling large PDF files efficiently.
Security: The application should not store or transmit user data externally.
User Interface Design
Main Screen
Upon launching the application, the main screen presents three primary buttons:

Split
Merge
Rotate
Each button leads to a different screen corresponding to the selected functionality.

Preview Checkbox: A checkbox labeled "Enable Preview" is present. It's unchecked by default for Split and Merge functions (except for Rotate, where it's checked). The application remembers this setting between sessions.
Settings Button: An icon/button to access application settings (e.g., default output directory).
Split Screen
File Selection Area: An area where users can drag and drop files or click to open a file dialog.
Selected Files List: Displays the list of selected PDF files.
Page Specification Input: A text box with greyed-out instructional text (e.g., "Enter pages like 1-3,4,~5").
Preview Pane (if enabled): Shows a preview of the selected PDF. Users can navigate pages using arrows or by entering a page number.
Output Directory Selection: Option to change the output directory.
Start Button: Initiates the splitting process.
Merge Screen
File Selection Area: Similar to the Split screen.
Selected Files List: Displays selected PDFs with options to reorder them.
Preview Pane (if enabled): Shows a preview of the selected PDF.
Output Directory Selection: Option to change the output directory.
Merge Button: Initiates the merging process.
Rotate Screen
File Selection Area: Users select or drag and drop PDFs.
PDF Dropdown: A dropdown menu to select among the uploaded PDFs.
Preview Pane: Displays the current page of the selected PDF.
Page Navigation: Arrow buttons and page number input to navigate pages.
Rotation Buttons: Buttons to rotate the page clockwise or counterclockwise.
Output Directory Selection: Option to change the output directory.
Rotate Button: Initiates the rotation process.
Common Elements
Status Bar: Displays messages like "Ready", "Processing...", or error messages.
Progress Indicator: Visual feedback during file operations.
Menu Bar (optional): Includes options like "File", "Edit", "Help".
Technical Specifications
Technology Stack
Programming Language: Python 3.x
GUI Framework: PyQt5 (preferred for better aesthetics and features) or Tkinter
PDF Manipulation Library: PyPDF2 or PDFMiner (ensure compatibility with Python 3 and support for required features)
Installer Packaging: PyInstaller or cx_Freeze for creating executable files for different platforms
Performance Optimization
Efficient File I/O: Read and write files in chunks to handle large PDFs.
Multithreading: Use multithreading for GUI responsiveness during long operations.
Lazy Loading: Load previews on-demand to save memory.
Caching: Cache previews to avoid reprocessing when navigating pages.
Error Handling
File Not Found: Alert the user if a file is not accessible.
Invalid Input: Validate page range inputs and show helpful error messages.
Permission Issues: Handle cases where the application lacks permissions to read/write files.
Unsupported PDFs: Notify users if a PDF is encrypted or unsupported.
Additional Considerations
File Handling
Temporary Files: Clean up any temporary files created during processing.
File Locks: Ensure files are not locked after processing to allow user access.
Multiple Instances: Allow multiple instances of the application if necessary.
User Preferences
Settings Storage: Store user preferences in a configuration file (e.g., JSON) in the user's home directory.
Default Directory: Allow users to set and change the default output directory.
Preview Settings: Remember the state of the preview checkbox between sessions.
Internationalization
Language Support: Design the application to support multiple languages in the future.
Unicode Support: Ensure file paths and PDF content with Unicode characters are handled correctly.
Development Plan
Milestones
Setup Development Environment: Configure Python, GUI framework, and PDF libraries.
Implement Core Functionality:
Split PDFs
Merge PDFs
Rotate PDFs
Develop GUI Screens:
Main Screen
Split Screen
Merge Screen
Rotate Screen
Integrate Drag and Drop: Enable drag and drop functionality across all screens.
Implement Preview Feature: Add optional preview panes with enable/disable functionality.
Add User Preferences Storage: Implement memory persistence for settings.
Testing Phase:
Unit Testing for functions
Integration Testing for workflows
User Acceptance Testing
Performance Optimization: Optimize code for speed and resource usage.
Packaging and Distribution: Prepare installers/executables for different platforms.
Documentation: Create user manuals and help guides.
Testing
Test Cases: Develop test cases covering all functionalities and edge cases.
Automation: Use automated testing tools where applicable.
User Feedback: Incorporate feedback from test users to improve usability.
Conclusion
This document outlines the comprehensive plan for developing LightPDF, a fast and lightweight PDF manipulation tool. By adhering to the specifications and considering the additional details provided, the development team should be able to build the application efficiently. The focus on usability, performance, and robustness ensures that the final product will meet user expectations and provide a valuable tool for PDF management.

Note to the Development Team: Please ensure all dependencies are up-to-date and compatible with the targeted platforms. Regularly update this document with any changes or new considerations that arise during the development process.