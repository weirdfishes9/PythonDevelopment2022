from pyfiglet import Figlet
from time import strftime

def date(format="%Y %d %b, %A", font="graceful"):
    return Figlet(font=font).renderText(strftime(format))