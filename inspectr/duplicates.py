import sys
import hashlib
from collections import defaultdict

def find_duplicates(files, block_size=10, min_occur=3):
    """
    Find duplicate blocks of code across files.

    Args:
        files: list of file paths
        block_size: number of consecutive lines in a block
        min_occur: minimum number of occurrences to report

    Yields:
        (filename, line_number, count)
    """
    blocks = defaultdict(list)  # hash -> list of (file, line)

    for fname in files:
        try:
            with open(fname, encoding="utf-8") as f:
                lines = f.readlines()
        except OSError as e:
            print(f"Could not read {fname}: {e}", file=sys.stderr)
            continue

        for i in range(len(lines) - block_size + 1):
            # join block of lines
            block = "".join(lines[i:i + block_size])
            # stable hash
            h = hashlib.sha1(block.encode("utf-8")).hexdigest()
            blocks[h].append((fname, i + 1))

    for locs in blocks.values():
        if len(locs) >= min_occur:
            for fname, lnum in locs:
                yield fname, lnum, len(locs)


def main(args=None) -> None:
    if args is None:
        args = sys.argv[1:]

    if not args:
        print("Usage: inspectr duplicates file1.py [file2.py ...]")
        return

    for fname, lnum, count in find_duplicates(args, block_size=10, min_occur=3):
        print(f"{fname}:{lnum}  (occurs {count} times)")

