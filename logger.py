from termcolor import colored
import os
from enum import Enum
from datetime import datetime
import sys

class LEVEL(Enum):
    INFO = "INFO"
    VERBOSE = "VERBOSE"
    WARNING = "WARNING"
    ERROR = "ERROR"

Level_Color_Mapping = {
    LEVEL.INFO: "blue",
    LEVEL.VERBOSE: "green",
    LEVEL.WARNING: "yellow",
    LEVEL.ERROR: "red"
}


class Logger:

    def __init__(self, name, path = os.path.join(os.path.dirname(sys.argv[0]), "./Logs"), ) -> None:
        self.path = path
        self.name = name

    def log(self, level, text):
        now = datetime.now()
        final_text= "[%s] [%s] %s - %s" % (now.strftime("%H:%M:%S.%f"), self.name, str(level).split(".")[1], text)
        self.log_to_console(level, final_text)
        self.log_to_file(level, final_text)


    def log_to_console(self, level, text):
        print(colored(text, Level_Color_Mapping[level]))

    def log_to_file(self, level, text):
        with open(os.path.join(self.path, "./%s_%s.log" % (datetime.now().strftime("%Y%m%d"), str(level).split(".")[1].lower())), "a+") as f:
            f.write("%s\n" % (text))


    def info(self, text):
        self.log(LEVEL.INFO, text=text)

    def verbose(self, text):
        self.log(LEVEL.VERBOSE, text=text)


    def error(self, text):
        self.log(LEVEL.ERROR, text=text)

    def warning(self, text):
        self.log(LEVEL.WARNING, text=text)
