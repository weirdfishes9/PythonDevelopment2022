import locale
import sys
from .date import date

if __name__=="__main__":
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    argv = sys.argv
    if (len(argv) == 1):
        print(date())
    elif (len(argv) == 2):
        print(date(argv[1]))
    elif (len(argv) == 3):
        print(date(argv[1], argv[2]))
    else:
        raise ValueError("Wrong number of arguments")