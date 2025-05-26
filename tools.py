from pathlib import Path
import os

# Define the base directory for file operations
base_dir = Path("./test")

def read_file(name: str) -> str:
    """Reads and returns the content of a file in the test directory.
    
    Args:
        name (str): The name of the file to read (relative to test directory).
    
    Returns:
        str: The file's content or an error message if the file cannot be read.
    """
    print(f"(read_file {name})")
    try:
        file_path = base_dir / name
        if not file_path.is_file():
            return f"Error: '{name}' is not a file or does not exist."
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error: Failed to read '{name}' - {e}"

def list_files() -> list[str]:
    """Lists all files in the test directory and its subdirectories.
    
    Returns:
        list[str]: A list of file names relative to the test directory.
    """
    print("(list_files)")
    try:
        return [str(item.relative_to(base_dir)) for item in base_dir.rglob("*") if item.is_file()]
    except Exception as e:
        return [f"Error: Failed to list files - {e}"]

def rename_file(name: str, new_name: str) -> str:
    """Renames a file in the test directory.
    
    Args:
        name (str): The current name of the file (relative to test directory).
        new_name (str): The new name for the file (relative to test directory).
    
    Returns:
        str: A success message or an error message if the operation fails.
    """
    print(f"(rename_file {name} -> {new_name})")
    try:
        old_path = base_dir / name
        new_path = base_dir / new_name
        if not old_path.is_file():
            return f"Error: '{name}' does not exist or is not a file."
        if not str(new_path).startswith(str(base_dir)):
            return "Error: New path is outside the test directory."
        os.makedirs(new_path.parent, exist_ok=True)
        os.rename(old_path, new_path)
        return f"File '{name}' successfully renamed to '{new_name}'."
    except Exception as e:
        return f"Error: Failed to rename '{name}' to '{new_name}' - {e}"