import ast
import os
from collections import defaultdict

def extract_functions(file_path: str):
    """Return a set of top-level functions and class methods from a Python file."""
    functions = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
    except (SyntaxError, FileNotFoundError):
        return functions

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.add(node.name)
        elif isinstance(node, ast.AsyncFunctionDef):
            functions.add(node.name)
    return functions


def compare_functions(dir1: str, dir2: str, rel_files: list[str]):
    # collect function mappings: function_name -> file(s)
    functions_in_dir1 = defaultdict(set)
    functions_in_dir2 = defaultdict(set)

    for rel in rel_files:
        file1 = os.path.join(dir1, rel)
        file2 = os.path.join(dir2, rel)

        funcs1 = extract_functions(file1)
        funcs2 = extract_functions(file2)

        for fn in funcs1:
            functions_in_dir1[fn].add(rel)
        for fn in funcs2:
            functions_in_dir2[fn].add(rel)

        # per-file report: what exists in both versions
        common = funcs1 & funcs2
        if common:
            print(f"\n[{rel}]")
            print("  Common functions/methods:")
            for fn in sorted(common):
                print(f"    - {fn}")
        else:
            print(f"No functions in common between {dir1} and {dir2} in {rel}")

    # cross-file check: moved functions
    moved = []
    for fn, files1 in functions_in_dir1.items():
        files2 = functions_in_dir2.get(fn, set())
        if files2 and files1 != files2:
            moved.append((fn, files1, files2))

    if moved:
        print("\nFunctions/methods that appear to have moved:")
        for fn, f1, f2 in moved:
            print(f"  {fn}: {f1} -> {f2}")
    else:
        print("No functions moved to a different file")


# example usage
if __name__ == "__main__":
    dir1 = "dir1"
    dir2 = "dir2"
    with open("files.txt") as files:
        lines = files.readlines()
    rel_files = [line.rstrip("\n") for line in lines]

    compare_functions(dir1, dir2, rel_files)

