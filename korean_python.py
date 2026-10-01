"""Translate Korean Python keywords into standard Python source."""

import argparse
import io
from pathlib import Path
import sys
import tokenize


KEYWORD_TRANSLATIONS = {
    "만약": "if",
    "아니면만약": "elif",
    "아니면": "else",
    "반복": "for",
    "동안": "while",
    "정의": "def",
    "반환": "return",
    "클래스": "class",
    "가져오기": "import",
    "에서": "from",
    "별칭": "as",
    "시도": "try",
    "예외": "except",
    "마지막으로": "finally",
    "발생": "raise",
    "주장": "assert",
    "함께": "with",
    "통과": "pass",
    "중단": "break",
    "계속": "continue",
    "전역": "global",
    "비지역": "nonlocal",
    "삭제": "del",
    "비동기": "async",
    "기다리기": "await",
    "생성": "yield",
    "람다": "lambda",
    "그리고": "and",
    "또는": "or",
    "아니다": "not",
    "안에": "in",
    "동일": "is",
    "참": "True",
    "거짓": "False",
    "없음": "None",
}


def translate(source: str) -> str:
    """Translate Korean keyword tokens while leaving strings and comments intact."""
    line_offsets = [0]
    for line in source.splitlines(keepends=True):
        line_offsets.append(line_offsets[-1] + len(line))

    replacements = []
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    for token in tokens:
        if token.type != tokenize.NAME:
            continue
        translated = KEYWORD_TRANSLATIONS.get(token.string)
        if translated is None:
            continue
        start = line_offsets[token.start[0] - 1] + token.start[1]
        end = line_offsets[token.end[0] - 1] + token.end[1]
        replacements.append((start, end, translated))

    for start, end, translated in reversed(replacements):
        source = source[:start] + translated + source[end:]
    return source


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Translate Korean Python keywords into standard Python."
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="source file to translate (reads stdin when omitted)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="write translated source to this file instead of stdout",
    )
    args = parser.parse_args(argv)

    try:
        source = (
            Path(args.input).read_text(encoding="utf-8")
            if args.input
            else sys.stdin.buffer.read().decode("utf-8")
        )
        translated = translate(source)
    except UnicodeDecodeError as error:
        parser.error(f"stdin must be UTF-8: {error}")
    except (IndentationError, tokenize.TokenError) as error:
        parser.error(f"cannot tokenize source: {error}")

    if args.output:
        Path(args.output).write_text(translated, encoding="utf-8")
    else:
        sys.stdout.buffer.write(translated.encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
