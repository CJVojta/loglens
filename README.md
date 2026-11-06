# LogLens

LogLens summarizes newline-delimited JSON application logs from the command line. Use it to check how many warnings or errors a run produced and which messages recur most often.

## Quick start

Requires Python 3.10 or later. No third-party packages are needed.

```sh
python loglens.py examples/app.jsonl
python loglens.py examples/app.jsonl --level ERROR --top 3
```

The first command produces:

```text
Valid entries: 5
Matched entries: 5
Invalid lines: 0

Levels
  ERROR: 2
  INFO: 2
  WARNING: 1

Top messages
  2  Database connection timed out
  1  Cache miss
  1  Request completed
  1  Service started
```

## Input and behavior

Each non-blank line must be a JSON object with non-empty string fields `level` and `message`. Extra fields are ignored. Level names are normalized to uppercase. Malformed rows are counted separately so they remain visible in the report, even when a level filter is active.

LogLens reads the file one line at a time. It stores counts for distinct matching levels and messages. Results sort by frequency and then alphabetically to make repeated runs easy to compare.
