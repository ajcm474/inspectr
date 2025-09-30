import ast, pathlib

for f in pathlib.Path.cwd().rglob("*.py"):
    tree = ast.parse(f.read_text(), filename=str(f))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, "id", "")=="open":
            if not any(isinstance(p, ast.With) and node in ast.walk(p) for p in ast.walk(tree)):
                print(f"{f}:{node.lineno}: open() outside with")

