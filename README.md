# korean-python

한글로 작성한 Python 예약어를 표준 Python 코드로 바꾸는 변환기입니다.

## 사용법

```python
정의 인사(이름):
    만약 이름:
        반환 f"안녕, {이름}"
    아니면:
        반환 "안녕하세요"
```

## 명령줄에서 사용하기

파일을 변환해 표준 출력으로 보냅니다.

```sh
python korean_python.py input.kpy
```

출력 파일을 지정하거나 표준 입력을 사용할 수도 있습니다.

```sh
python korean_python.py input.kpy --output output.py
python korean_python.py < input.kpy
```

Windows에서는 저장소 폴더에서 `korean-python.bat`을 인자 없이 실행하면 한글 코드를 바로 입력할 수 있는 대화형 인터프리터가 열립니다. Python이 설치되어 있고 `python` 명령을 사용할 수 있어야 합니다.

```bat
korean-python.bat
```

화면에 `한글>>>` 프롬프트가 나타나면 한글 키워드로 코드를 입력합니다. 여러 줄 블록은 들여쓴 코드를 입력한 다음 빈 줄을 입력해 실행하고, `종료` 또는 Ctrl+Z로 끝냅니다.

```text
한글>>> 정의 더하기(a, b):
...     반환 a + b
...
한글>>> 더하기(2, 3)
5
한글>>> 종료
```

파일 변환도 기존처럼 배치 파일에 입력 파일을 지정해 사용할 수 있습니다.

```bat
korean-python.bat input.kpy
korean-python.bat input.kpy --output output.py
```

## 다른 Python 파일에서 import하기

`korean_python.py`를 사용하는 Python 파일과 같은 폴더에 두고 변환 함수를 import할 수 있습니다. 입력 파일과 출력 파일은 UTF-8로 읽고 씁니다.

```python
from korean_python import translate_file

translate_file("input.kpy", "output.py")
```

문자열을 직접 변환하려면 `translate()`을 사용합니다.

```python
from korean_python import translate

source = "만약 참:\n    print('안녕')\n"
python_source = translate(source)
print(python_source)
```

표준 입력과 출력은 UTF-8입니다. 변환은 Python 토큰 단위로 수행하므로 문자열, 주석, 다른 식별자 안의 한글은 그대로 유지됩니다. 지원하는 예약어는 `korean_python.py`의 `KEYWORD_TRANSLATIONS`에서 확인할 수 있습니다.
