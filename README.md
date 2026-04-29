# 📂 Automated File Organizer

## 📝 Description
The **Automated File Organizer** is a Python automation script designed to clean up cluttered directories. It scans a specified folder, identifies files by their extensions (e.g., `.py`, `.txt`, `.jpg`), and automatically moves them into categorized subfolders (like "Documents", "Images", "Python_Code"). 

It is built with a focus on safety and transparency, handling edge cases like duplicate filenames and permission errors, while logging all operations.

## ✨ Features
* **Smart Categorization:** Automatically maps file extensions to specific folders. Unrecognized files are moved to an "Other" folder.
* **Conflict Resolution:** If a file with the same name already exists in the destination, it safely renames the new file (e.g., `report.txt` becomes `report(1).txt`) to prevent data loss.
* **Dry-Run Mode:** Includes a safe `--dry-run` flag to preview changes in the terminal without actually moving any files.
* **Detailed Logging:** Uses Python's `logging` module to track all successful moves and errors in an `organizer_log.txt` file.
* **Command-Line Interface (CLI):** Built with `argparse` for a smooth terminal user experience.

## 🛠️ Technologies Used
* **Python 3.x**
* Built-in Libraries: `os`, `pathlib`, `shutil`, `argparse`, `logging` (No external dependencies needed!)

## 🚀 How to Use

**1. Clone the repository:**
```bash
git clone [https://github.com/your-username/Automated-File-Organizer.git](https://github.com/your-username/Automated-File-Organizer.git)
cd Automated-File-Organizer


Run a Dry Run (Preview Changes):
python organizer.py test_folder --dry-run

Run the Organizer:
python organizer.py test_folder


📁 Example Workflow

Before Organizing:

test_folder/
├── Flow-Chart-For-A-Face-Emotion-Detection.png
└── hello.txt

After Organizing:

test_folder/
├── Documents/
│   ├── hello.txt
├── Images/
│   └── Flow-Chart-For-A-Face-Emotion-Detection.png



