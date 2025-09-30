import ast
import pathlib
import sys
from typing import List


def main(files: List[pathlib.Path]) -> None:
    if not files:
        print("Usage: inspectr with_open <file1> [file2 ...]")
        sys.exit(1)

    for filepath in files:
        tree = ast.parse(filepath.read_text(), filename=str(filepath))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, "id", "")=="open":
                if not any(isinstance(p, ast.With) and node in ast.walk(p) for p in ast.walk(tree)):
                    print(f"{filepath}:{node.lineno}: open() outside with")

