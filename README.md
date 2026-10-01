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

파일을 변환해 표준 출력으로 보냅니다.

```sh
python korean_python.py input.kpy
```

출력 파일을 지정하거나 표준 입력을 사용할 수도 있습니다.

```sh
python korean_python.py input.kpy --output output.py
python korean_python.py < input.kpy
```

표준 입력과 출력은 UTF-8입니다. 변환은 Python 토큰 단위로 수행하므로 문자열, 주석, 다른 식별자 안의 한글은 그대로 유지됩니다. 지원하는 예약어는 `korean_python.py`의 `KEYWORD_TRANSLATIONS`에서 확인할 수 있습니다.
