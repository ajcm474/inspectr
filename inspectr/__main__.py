import sys
import pathlib
import importlib

def main():
    if len(sys.argv) < 2:
        print("Usage: inspectr <subtool> [files...]")
        sys.exit(1)

    subtool = sys.argv[1]
    args = [pathlib.Path(arg) for arg in sys.argv[2:]]

    try:
        mod = importlib.import_module(f"inspectr.{subtool}")
    except ModuleNotFoundError:
        print(f"Unknown subtool: {subtool}")
        sys.exit(1)

    # Each subtool should define a `main(args)` function
    if not hasattr(mod, "main"):
        print(f"Subtool '{subtool}' does not define a main(args) function")
        sys.exit(1)

    mod.main(args)

if __name__ == "__main__":
    main()
