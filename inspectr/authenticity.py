#!/usr/bin/env python3
import ast
import pathlib
from typing import List


def main(files: List[pathlib.Path]) -> None:
    todo_count = 0
    empty_try_except_count = 0
    stub_functions = []

    for f in files:
        src = f.read_text(encoding="utf-8")

        todo_count += src.count("TODO")

        try:
            tree = ast.parse(src, filename=str(f))
        except SyntaxError:
            continue  # skip broken files

        for node in ast.walk(tree):
            # Empty try/except blocks
            if isinstance(node, ast.Try):
                try_empty = len(node.body) == 0
                except_empty = all(len(h.body) == 0 or all(isinstance(s, ast.Pass) for s in h.body) for h in node.handlers)
                if try_empty and except_empty:
                    empty_try_except_count += 1

            # Stub functions/methods
            if isinstance(node, ast.FunctionDef):
                # Only consider body statements that are `pass` or empty return
                is_stub = True
                for stmt in node.body:
                    if isinstance(stmt, ast.Pass):
                        continue
                    elif isinstance(stmt, ast.Return) and stmt.value is None:
                        continue
                    else:
                        is_stub = False
                        break
                if is_stub:
                    stub_functions.append(f"{f}:{node.name}")

    print("Analysis results:")
    print(f"  TODO comments: {todo_count}")
    print(f"  Empty try/except blocks: {empty_try_except_count}")
    print(f"  Stub functions/methods: {len(stub_functions)}")
    for stub in stub_functions:
        print(f"    {stub}")
