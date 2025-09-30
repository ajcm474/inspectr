# inspectr
A collection of python tools to inspect code quality.

## Installation
```bash
python -m venv .venv/
source .venv/bin/activate
pip install inspectr
```

## Usage
Generally, the syntax goes:
```bash
inspectr <subtool> [files...]
```
where `<subtool>` is one of the following:

- `authenticity`: looks for TODO comments, empty try/except blocks, and stub functions
- `bare_ratio`: checks for the ratio of bare excepts to meaningful exception usage
- `count_exceptions`: counts how many of each type of exception there are (including bare except)
- `size_counts`: various linecount-related code complexity checks
- `with_open`: checks for `open` in the absense of `with` and manual calls to `close()`

**Please note:** this project is in the early alpha stage, so don't expect the above subtool names 
to be stable between versions. I might even merge/split them at some point.