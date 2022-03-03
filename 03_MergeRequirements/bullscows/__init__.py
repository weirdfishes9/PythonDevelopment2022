import textdistance
import random

from typing import Tuple, List

def bullscows(guess: str, secret: str) -> Tuple[int, int]:
    bulls = textdistance.hamming.similarity(guess, secret)
    cows = textdistance.bag.similarity(guess, secret) - bulls
    return bulls, cows

def gameplay(ask: callable, inform: callable, words: List[str]) -> int:
    secret = random.choice(words)
    attempts = 0
    guess = None

    while guess != secret:
        guess = ask("Введите слово: ", words)
        attempts += 1
        b, c = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)
    
    return attempts