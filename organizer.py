import argparse
import shutil
import logging
from pathlib import Path

# ==========================================
# 1. CATEGORY DICTIONARY
# ==========================================
# This dictionary maps file extensions to folder names.
# You can easily add more extensions here later!
CATEGORIES = {
    # Documents
    ".txt": "Documents", ".pdf": "Documents", ".docx": "Documents",
    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
    # Code
    ".py": "Python_Code", ".html": "Web_Code", ".js": "Web_Code",
    # Data
    ".csv": "Data", ".json": "Data"
}

# ==========================================
# 2. SETUP LOGGING
# ==========================================
def setup_logging():
    """Configures the logging file to track successes and errors."""
    logging.basicConfig(
        filename='organizer_log.txt', # Creates a text file for logs
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# ==========================================
# 3. CONFLICT RESOLUTION (Duplicate Names)
# ==========================================
def get_unique_path(target_path):
    """
    If a file already exists (e.g., report.txt), 
    this safely renames it to report(1).txt, report(2).txt, etc.
    """
    # If the file doesn't exist yet, the path is safe to use
    if not target_path.exists():
        return target_path

    counter = 1
    # .stem gets the name ("report"), .suffix gets the extension (".txt")
    while True:
        new_name = f"{target_path.stem}({counter}){target_path.suffix}"
        new_path = target_path.parent / new_name
        
        # Check if the new name is finally unique
        if not new_path.exists():
            return new_path
        counter += 1

# ==========================================
# 4. MAIN ORGANIZER LOGIC
# ==========================================
def organize_directory(source_dir, dry_run=False):
    """Scans the directory and moves files into categorized folders."""
    source = Path(source_dir)
    
    # Counters for our final summary report
    files_moved = 0
    errors_encountered = 0

    # Safety check: Does the folder actually exist?
    if not source.exists() or not source.is_dir():
        print(f"Error: The directory '{source}' does not exist.")
        return

    print(f"Scanning directory: {source}")
    if dry_run:
        print("--- DRY RUN MODE: No files will actually be moved ---")

    # Loop through everything inside the source folder
    for item in source.iterdir():
        
        # We only want to move files, skip folders/directories
        if item.is_file():
            # Get the extension in lowercase (e.g., .JPG becomes .jpg)
            ext = item.suffix.lower()
            
            # Find the matching folder, or default to "Other"
            category_folder = CATEGORIES.get(ext, "Other")
            
            # Build the path for the new folder
            target_dir = source / category_folder
            
            # Create the folder if it doesn't exist (and we aren't in dry-run mode)
            if not target_dir.exists() and not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                logging.info(f"Created directory: {target_dir}")

            # Build the full path for where the file will go
            target_path = target_dir / item.name
            
            # Check for duplicates and rename if necessary
            target_path = get_unique_path(target_path)

            # Safely try to move the file
            try:
                if dry_run:
                    print(f"[Dry Run] Would move: {item.name} -> {category_folder}/")
                else:
                    # shutil.move physically moves the file
                    shutil.move(str(item), str(target_path))
                    logging.info(f"Successfully moved {item.name} -> {target_path}")
                    files_moved += 1
                    print(f"Moved: {item.name} -> {category_folder}/")

            except PermissionError:
                # Handle locked files or permission issues
                logging.error(f"Permission denied: Cannot move {item.name}")
                errors_encountered += 1
                print(f"Error: Permission denied for {item.name}")
            except Exception as e:
                # Handle any other unexpected errors safely
                logging.error(f"Unexpected error moving {item.name}: {e}")
                errors_encountered += 1
                print(f"Error moving {item.name}")

    # Print Summary Report
    print("\n--- Summary Report ---")
    print(f"Total Files Moved: {files_moved}")
    print(f"Total Errors: {errors_encountered}")
    if not dry_run:
        print("Check 'organizer_log.txt' for detailed logs.")

# ==========================================
# 5. COMMAND LINE INTERFACE (CLI)
# ==========================================
if __name__ == "__main__":
    setup_logging()

    # Setup argparse so users can run the script from the terminal
    parser = argparse.ArgumentParser(description="Automated File Organizer")
    
    # Required argument: The folder to organize
    parser.add_argument("source", help="The path of the directory you want to organize")
    
    # Optional argument: --dry-run (preview changes only)
    parser.add_argument("--dry-run", action="store_true", help="Preview what will happen without actually moving files")

    # Parse the commands typed by the user
    args = parser.parse_args()

    # Start the program with the user's inputs
    organize_directory(args.source, args.dry_run)