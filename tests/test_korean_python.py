from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import keyword
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from korean_python import KEYWORD_TRANSLATIONS, run_repl, translate, translate_file


class TranslateTests(unittest.TestCase):
    def test_translation_table_covers_python_keywords(self):
        translated_keywords = set(KEYWORD_TRANSLATIONS.values())
        self.assertLessEqual(
            set(keyword.kwlist) | set(keyword.softkwlist),
            translated_keywords,
        )

    def test_translates_korean_keywords(self):
        source = "만약 값 안에 자료 그리고 참:\n    반환 없음\n"
        self.assertEqual(
            translate(source),
            "if 값 in 자료 and True:\n    return None\n",
        )

    def test_translates_common_builtin_names(self):
        source = (
            "출력(길이(목록(범위(3))))\n"
            "출력(합계(묶음(정수('2'), 정수('3'))))\n"
            "출력(최댓값(1, 2), 최솟값(1, 2), 절대값(-3))\n"
            "출력(정렬([3, 1]), 반올림(2.6), 거듭제곱(2, 3))\n"
            "출력(문자열(실수('1.5')), 튜플([1]), 집합([1]), 사전())\n"
            "출력(입력.__name__, 열거.__name__)\n"
        )
        translated = translate(source)
        self.assertEqual(
            translated,
            "print(len(list(range(3))))\n"
            "print(sum(zip(int('2'), int('3'))))\n"
            "print(max(1, 2), min(1, 2), abs(-3))\n"
            "print(sorted([3, 1]), round(2.6), pow(2, 3))\n"
            "print(str(float('1.5')), tuple([1]), set([1]), dict())\n"
            "print(input.__name__, enumerate.__name__)\n",
        )

    def test_leaves_strings_comments_and_identifiers_unchanged(self):
        source = '메시지 = "만약 참"\n# 아니면\n만약조건 = 거짓\n'
        self.assertEqual(
            translate(source),
            '메시지 = "만약 참"\n# 아니면\n만약조건 = False\n',
        )

    def test_preserves_formatting(self):
        source = "\t만약(값):  # 조건\n\t\t통과\n"
        self.assertEqual(translate(source), "\tif(값):  # 조건\n\t\tpass\n")

    def test_translated_source_is_valid_python(self):
        source = "정의 인사(이름):\n    반환 f'안녕, {이름}'\n"
        compile(translate(source), "<translated>", "exec")

    def test_translates_pattern_matching_and_type_alias_syntax(self):
        source = (
            "형식 응답 = int\n"
            "선택 값:\n"
            "    경우 0:\n"
            "        결과 = '영'\n"
            "    경우 무엇이든:\n"
            "        결과 = '기타'\n"
        )
        translated = translate(source)
        self.assertEqual(
            translated,
            "type 응답 = int\n"
            "match 값:\n"
            "    case 0:\n"
            "        결과 = '영'\n"
            "    case _:\n"
            "        결과 = '기타'\n",
        )
        namespace = {"값": 5}
        exec(compile(translated, "<translated>", "exec"), namespace)
        self.assertEqual(namespace["결과"], "기타")

    def test_translate_file_reads_and_writes_utf8(self):
        with TemporaryDirectory() as directory:
            source_path = Path(directory) / "input.kpy"
            output_path = Path(directory) / "output.py"
            source_path.write_text("만약 참:\n    통과\n", encoding="utf-8")

            translate_file(source_path, output_path)

            self.assertEqual(
                output_path.read_text(encoding="utf-8"),
                "if True:\n    pass\n",
            )

    def test_repl_executes_korean_statements_and_multiline_functions(self):
        commands = iter(
            [
                "정의 더하기(a, b):",
                "    반환 a + b",
                "",
                "더하기(2, 3)",
                "종료",
            ]
        )
        output = StringIO()

        with patch("builtins.input", side_effect=lambda _prompt: next(commands)):
            with redirect_stdout(output):
                run_repl()

        self.assertIn("5", output.getvalue())

    def test_repl_waits_for_open_parentheses_to_be_closed(self):
        commands = iter(["출력(", "    1 + 2", ")", "종료"])
        output = StringIO()

        with patch("builtins.input", side_effect=lambda _prompt: next(commands)):
            with redirect_stdout(output):
                run_repl()

        self.assertIn("3", output.getvalue())
        self.assertNotIn("Traceback", output.getvalue())

    def test_repl_allows_else_after_entering_if_body(self):
        commands = iter(
            [
                "a = 4",
                "만약 a % 2 == 0:",
                "    출력('짝수')",
                "아니면:",
                "    출력('홀수')",
                "",
                "종료",
            ]
        )
        output = StringIO()
        errors = StringIO()

        with patch("builtins.input", side_effect=lambda _prompt: next(commands)):
            with redirect_stdout(output):
                with redirect_stderr(errors):
                    run_repl()

        self.assertIn("짝수", output.getvalue())
        self.assertNotIn("홀수", output.getvalue())
        self.assertNotIn("Traceback", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
