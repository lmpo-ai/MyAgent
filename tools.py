from pathlib import Path

# Base directory for file operations
base_dir = Path("test")

def read_file(name: str) -> str:
    """Read the content of a file in the test directory."""
    print(f"(read_file {name})")
    file_path = base_dir / name
    if not file_path.is_file():
        return f"Error: '{name}' is not a valid file."
    try:
        return file_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading '{name}': {e}"

def list_files() -> list[str]:
    """List all files in the test directory and subdirectories."""
    print("(list_files)")
    try:
        return [str(p.relative_to(base_dir)) for p in base_dir.rglob("*") if p.is_file()]
    except Exception as e:
        return [f"Error listing files: {e}"]

def rename_file(name: str, new_name: str) -> str:
    """Rename a file within the test directory."""
    print(f"(rename_file {name} -> {new_name})")
    old_path = base_dir / name
    new_path = base_dir / new_name

    if not old_path.is_file():
        return f"Error: '{name}' does not exist or is not a file."
    if new_path.exists():
        return f"Error: '{new_name}' already exists."

    try:
        new_path.parent.mkdir(parents=True, exist_ok=True)
        old_path.rename(new_path)
        return f"'{name}' successfully renamed to '{new_name}'."
    except Exception as e:
        return f"Error renaming '{name}': {e}"
        
