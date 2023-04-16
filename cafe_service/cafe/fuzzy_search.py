from functools import reduce
from operator import index
import re


CHO_HANGUL = [
    "ㄱ",
    "ㄲ",
    "ㄴ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

HANGUL_START_CHARCODE = ord("가")
CHO_PERIOD = int(ord("까") - ord("가"))
JUNG_PERIOD = int(ord("개") - ord("가"))


def combine(cho, jung, jong):
    return chr(HANGUL_START_CHARCODE + cho * CHO_PERIOD + jung * JUNG_PERIOD + jong)


def make_regex_by_cho(search=""):
    regex = reduce(
        lambda acc, cho: acc.replace(
            cho,
            f"[{combine(CHO_HANGUL.index(cho), 0, 0)}-{combine(CHO_HANGUL.index(cho) + 1, 0, -1)}]",
        ),
        CHO_HANGUL,
        search,
    )
    return re.compile(f"({regex})", re.IGNORECASE)
