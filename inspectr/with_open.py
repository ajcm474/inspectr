import ast
import pathlib
import sys
from typing import List


def validate_files(files: List[pathlib.Path]) -> bool:
    """Validate that all files exist and are regular files."""
    for f in files:
        if not f.exists():
            print(f"Error: File does not exist: {f}")
            return False
        if not f.is_file():
            print(f"Error: Not a file: {f}")
            return False
    return True


def main(files: List[pathlib.Path], **kwargs) -> None:
    if not files:
        print("Usage: inspectr with_open <file1> [file2 ...]")
        sys.exit(1)

    if not validate_files(files):
        return

    for filepath in files:
        tree = ast.parse(filepath.read_text(), filename=str(filepath))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "open":
                if not any(isinstance(p, ast.With) and node in ast.walk(p) for p in ast.walk(tree)):
                    print(f"{filepath}:{node.lineno}: open() outside with")
