import re
import sys


def repeat(count, *functions):
    for _ in range(count):
        for function in functions:
            function()


def 변환하기(oo):
    문자열표 = {}
    보호된 = []
    위치 = 0

    while 위치 < len(oo):
        if oo[위치] not in ('"', "'"):
            보호된.append(oo[위치])
            위치 += 1
            continue

        따옴표 = oo[위치]
        끝 = 위치 + 1
        while 끝 < len(oo):
            if oo[끝] == "\\":
                끝 += 2
                continue
            if oo[끝] == 따옴표:
                break
            끝 += 1

        if 끝 == len(oo):
            보호된.append(oo[위치:])
            break

        원본문자열 = oo[위치:끝 + 1]
        자리표시자 = f"__OO_STRING_{len(문자열표)}__"
        문자열표[자리표시자] = 원본문자열
        보호된.append(자리표시자)
        위치 = 끝 + 1

    변환된 = "".join(보호된)
    변환된 = re.sub(
        r"(?m)^(\s*)각\s+([가-힣A-Za-z_]\w*)\s+안에서\s+(.+):\s*$",
        r"\1for \2 in \3:",
        변환된,
    )
    치환표 = {
        "아니면 만약": "elif",
        "같지 않다": "!=",
        "보다 크거나 같다": ">=",
        "보다 작거나 같다": "<=",
        "보다 크다": ">",
        "보다 작다": "<",
        "같다": "==",
        "아니면": "else",
        "만약": "if",
        "조건부 반복": "while",
        "함수": "def",
        "출력": "print",
        "입력": "input",
        "반복": "repeat",
        "참": "True",
        "거짓": "False",
        "그리고": "and",
        "또는": "or",
        "아니다": "not",
        "반환": "return",
        "정수": "int",
        "실수": "float",
        "문자열": "str",
        "리스트": "list",
        "사전": "dict",
        "범위": "range",
        "길이": "len",
        "합계": "sum",
        "최대": "max",
        "최소": "min",
        "절댓값": "abs",
        "반올림": "round",
    }

    for 원래말, 바꿀말 in 치환표.items():
        변환된 = 변환된.replace(원래말, 바꿀말)

    for 자리표시자, 원본문자열 in 문자열표.items():
        변환된 = 변환된.replace(자리표시자, 원본문자열)

    return 변환된


def 실행하기(oo, 환경=None):
    파이썬 = 변환하기(oo)
    실행환경 = {"repeat": repeat}
    if 환경 is not None:
        실행환경.update(환경)
    exec(파이썬, 실행환경)


def 파일실행하기(파일경로, 환경=None):
    with open(파일경로, encoding="utf-8") as 파일:
        실행하기(파일.read(), 환경)


if __name__ == "__main__":
    파일경로 = sys.argv[1] if len(sys.argv) > 1 else "main.oo.txt"
    파일실행하기(파일경로)
