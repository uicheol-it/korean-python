import unittest

from korean_python import translate


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


if __name__ == "__main__":
    unittest.main()
