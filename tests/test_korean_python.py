from contextlib import redirect_stdout
from io import StringIO
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from korean_python import run_repl, translate, translate_file


class TranslateTests(unittest.TestCase):
    def test_translates_korean_keywords(self):
        source = "만약 값 안에 목록 그리고 참:\n    반환 없음\n"
        self.assertEqual(
            translate(source),
            "if 값 in 목록 and True:\n    return None\n",
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


if __name__ == "__main__":
    unittest.main()
