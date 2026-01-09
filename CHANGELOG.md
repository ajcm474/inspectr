## Version 0.1.2
- Move input validation outside of main functions

## Version 0.1.1
- Fix `complexity` tool to properly preserve all terms
  - Bugs remain in combining constant terms
- Add more robust tests for `complexity` tool 

## Version 0.1.0
- Add `complexity` tool to command line interface with support for analyzing multiple files
- Add `compare_funcs` tool to command line interface for comparing functions across directories
- Flexible CLI option parsing: any `--option` is passed as keyword arg to subtool main function
- All tools now verify inputs up front
- `authenticity` now correctly detects all stub functions, including those with only docstrings
- Major overhaul of `duplicates` tool, which now
  - reports matches with >80% similarity instead of requiring exact matches
  - accepts `--block-size` and `--min-occur` command line options
  - reports occurrences in improved format showing line ranges and similarity percentages
  - merges overlapping duplicate ranges (>50% overlap)
- Add unit tests for all subtools
- Add `pytest` to test dependencies

## Version 0.0.5
- Add `duplicates` to README
- Bugfix: `authenticity` now considers docstring-only functions as empty
- Add FIXME and Placeholder counts to `authenticity`

## Version 0.0.4
- Change default values in `duplicates` to be 10 lines, 3 occurrences

## Version 0.0.3
- Add `duplicates` tool to count occurrences of duplicate code

## Version 0.0.2
- Bugfix: `size_counts` no longer ignores the files passed into it
