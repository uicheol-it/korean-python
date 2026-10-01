"""Translate Korean Python keywords into standard Python source."""

import argparse
import codeop
import io
from pathlib import Path
import sys
import tokenize
import traceback
from typing import Union


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
    "선택": "match",
    "경우": "case",
    "형식": "type",
    "무엇이든": "_",
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
    "출력": "print",
    "입력": "input",
    "범위": "range",
    "길이": "len",
    "정수": "int",
    "실수": "float",
    "문자열": "str",
    "목록": "list",
    "튜플": "tuple",
    "집합": "set",
    "사전": "dict",
    "최댓값": "max",
    "최솟값": "min",
    "합계": "sum",
    "정렬": "sorted",
    "열거": "enumerate",
    "묶음": "zip",
    "절대값": "abs",
    "반올림": "round",
    "거듭제곱": "pow",
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


def translate_file(
    input_path: Union[str, Path], output_path: Union[str, Path]
) -> None:
    """Translate a UTF-8 source file and write the result as UTF-8."""
    source = Path(input_path).read_text(encoding="utf-8")
    Path(output_path).write_text(translate(source), encoding="utf-8")


def _first_token(source: str) -> str:
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT):
            return token.string
    return ""


def run_repl() -> None:
    """Run an interactive shell that translates and executes Korean Python."""
    compiler = codeop.CommandCompiler()
    namespace = {"__name__": "__main__"}
    source_lines = []
    pending_code = None
    compound_statements = {
        "if",
        "for",
        "while",
        "try",
        "with",
        "def",
        "class",
        "match",
        "async",
    }
    continuation_clauses = {
        "아니면",
        "아니면만약",
        "예외",
        "마지막으로",
        "경우",
        "else",
        "elif",
        "except",
        "finally",
        "case",
    }

    print("한글 Python 인터프리터입니다. 종료하려면 '종료' 또는 Ctrl+Z를 입력하세요.")
    while True:
        prompt = "... " if source_lines or pending_code is not None else "한글>>> "
        try:
            line = input(prompt)
        except EOFError:
            print()
            return
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            source_lines.clear()
            continue

        if not source_lines and pending_code is None and line.strip() == "종료":
            return

        if pending_code is not None:
            first_word = line.strip().split(None, 1)[0].rstrip(":") if line.strip() else ""
            if line.strip() and first_word in continuation_clauses:
                pending_code = None
            else:
                compiled_to_run = pending_code
                pending_code = None
                source_lines.clear()
                try:
                    exec(compiled_to_run, namespace)
                except SystemExit:
                    raise
                except Exception:
                    traceback.print_exc()
                if not line.strip():
                    continue

        source_lines.append(line)
        source = "\n".join(source_lines) + "\n"
        try:
            translated = translate(source)
            compiled = compiler(translated, "<한글 입력>", "single")
        except tokenize.TokenError as error:
            if error.args and error.args[0] == "unexpected EOF in multi-line statement":
                continue
            traceback.print_exc()
            source_lines.clear()
            continue
        except (IndentationError, SyntaxError, OverflowError, ValueError):
            traceback.print_exc()
            source_lines.clear()
            continue

        if compiled is None:
            continue

        if line.strip() and _first_token(translated) in compound_statements:
            pending_code = compiled
            continue

        source_lines.clear()
        try:
            exec(compiled, namespace)
        except SystemExit:
            raise
        except Exception:
            traceback.print_exc()


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
    parser.add_argument(
        "--repl",
        action="store_true",
        help="run an interactive Korean Python shell",
    )
    args = parser.parse_args(argv)

    if args.repl:
        run_repl()
        return 0

    try:
        if args.input and args.output:
            translate_file(args.input, args.output)
            return 0
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
