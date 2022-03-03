import sys
import urllib.request as request

from typing import List
from bullscows import gameplay

def ask(prompt: str, valid: List[str] = None) -> str:
    if valid is None:
        guess = input(prompt)
    else:
        while True:
            guess = input(prompt)
            if guess in valid:
                break
            else:
                print("Слово отсутствует в словаре.")
    return guess

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))

if __name__ == '__main__':
    argv = sys.argv

    if len(argv) < 2 or len(argv) > 3:
        raise ValueError("Wrong number of arguments")

    dict = argv[1]
    try:
        f = open(dict, "r", encoding="utf-8")
        words = f.read().split()
    except:
        f = request.urlopen(dict)
        words = f.read().decode('utf-8').split()

    word_len = int(argv[2]) if len(argv) == 3 else 5
    words = [word for word in words if len(word) == word_len]
    print(gameplay(ask, inform, words))
