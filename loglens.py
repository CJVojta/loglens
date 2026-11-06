"""Summarize application logs stored as JSON Lines."""

import argparse
from collections import Counter
import json
from pathlib import Path


def parse_entry(line: str) -> tuple[str, str]:
    entry = json.loads(line)
    if not isinstance(entry, dict):
        raise ValueError("Expected a JSON object")

    level = entry.get("level")
    message = entry.get("message")
    if not isinstance(level, str) or not level.strip():
        raise ValueError("Expected a non-empty level")
    if not isinstance(message, str) or not message.strip():
        raise ValueError("Expected a non-empty message")
    return level.strip().upper(), message.strip()


def summarize(path: Path, selected_level: str | None, top: int) -> None:
    levels: Counter[str] = Counter()
    messages: Counter[str] = Counter()
    valid = invalid = 0
    with path.open(encoding="utf-8-sig") as source:
        for line in source:
            if not line.strip():
                continue
            try:
                level, message = parse_entry(line)
            except ValueError:
                invalid += 1
                continue

            valid += 1
            if selected_level is None or level == selected_level:
                levels[level] += 1
                messages[message] += 1

    print(f"Valid entries: {valid}")
    print(f"Matched entries: {sum(levels.values())}")
    print(f"Invalid lines: {invalid}")

    print("\nLevels")
    for level, count in sorted(levels.items(), key=lambda item: (-item[1], item[0])):
        print(f"  {level}: {count}")

    print("\nTop messages")
    ranked = sorted(messages.items(), key=lambda item: (-item[1], item[0]))
    for message, count in ranked[:top]:
        escaped_message = json.dumps(message, ensure_ascii=False)[1:-1]
        print(f"  {count}  {escaped_message}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to a UTF-8 JSON Lines file")
    parser.add_argument("--level", type=lambda value: value.strip().upper(), help="Filter by level")
    parser.add_argument("--top", type=int, default=5, help="Maximum messages to show (default: 5)")
    args = parser.parse_args()
    if args.top < 1:
        parser.error("--top must be at least 1")
    if args.level == "":
        parser.error("--level must not be empty")

    try:
        summarize(args.path, args.level, args.top)
    except (OSError, UnicodeError) as error:
        parser.exit(1, f"LogLens: {error}\n")


if __name__ == "__main__":
    main()
