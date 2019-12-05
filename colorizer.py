from os import isatty
from sys import stdout

class BaseColorClass:
    """
    This should more or less only be used when you are at the final stage of emiting something
    with print
    """

    END_CODE = "\033[0m"
    START_CODE_FORMATTER = "\033[{}m" # insert the specific stuff in here
    RGB_FORMATTER = "38;2;{};{};{};"
    def __init__(self, bg="", fg="", color_code=None, string=""):
        self._bg = bg
        self._fg = fg

        # Should be set by the call
        self.string = string

        # Should be set by the rgb method?
        self.color_code = color_code
        self.codes = []

    def fg(self, code):
        self._fg = code
        self.codes.append(code)
        return self.copy()

    def bg(self, cls):
        self._bg = cls._fg + 10
        self.codes.append(self._bg)
        return self.copy()

    def rgb(self, r, g, b):
        self.codes += [38, 2, r, g, b]
        return self.copy()

    def rgb_bg(self, r, g, b):
        self.codes += [48, 2, r, g, b]
        return self.copy()

    def with_code(self, code):
        self.codes.append(str(code))
        return self.copy()

    def make_color_code(self):
        basic_codes = ';'.join(list(map(str, self.codes)))
        return self.START_CODE_FORMATTER.format(basic_codes)

    def build(self):
        return self.copy()

    def to_str(self):
        """To make it a bit easier to convert"""
        return str(self)

    def as_func(self):
        return self.__call__

    def copy(self):
        # TODO refactor this
        n = BaseColorClass(self._bg, self._fg, self.color_code, self.string)
        n.codes = list(self.codes)
        return n

    def __len__(self):
        return len(self.string)

    def __add__(self, x):
        return str(self) + x

    def __radd__(self, x):
        return x + str(self)

    def __call__(self, string=None):
        if string is not None:
            self.string = string
        return self.copy()

    def __str__(self):
        self.color_code = self.make_color_code()

        # If the output device is NOT a tty, don't print color codes
        if not isatty(stdout.fileno()):
            return self.string

        return self.color_code + self.string + self.END_CODE




colors = [
    ("black", 30),
    ("red", 31),
    ("green", 32),
    ("yellow", 33),
    ("blue", 34),
    ("magenta", 35),
    ("cyan", 36),
    ("white", 37),
    ("bold", 1),
    ("italics", 3),
    ("underline", 4),
    ("normal", 0),
    ("crossed", 9)
]

black = BaseColorClass().fg(30)
red = BaseColorClass().fg(31)
green = BaseColorClass().fg(32)
yellow = BaseColorClass().fg(33)
blue = BaseColorClass().fg(34)
magenta = BaseColorClass().fg(35)
cyan = BaseColorClass().fg(36)
white = BaseColorClass().fg(37)
bold = BaseColorClass().fg(1)
italics = BaseColorClass().fg(3)
underline = BaseColorClass().fg(4)
normal = BaseColorClass().fg(0)
crossed = BaseColorClass().fg(9)


def wrapped(code):
    def add_atrribute(self, string=""):
        x = self.copy()
        x.codes.append(code)
        x.string += string
        return x
    return add_atrribute

for c, code in colors:
    setattr(BaseColorClass, c, wrapped(code))

if __name__ == '__main__':
    print(red("this should be red"))
    print(red("this should be red with bold").bold())
    print(
        red("this should be red with bold and underline")
            .bold()
            .underline()
    )

    red_bold_underline = red().bold().underline().build()
    print(red_bold_underline("this should as well"))
    print(normal("this should be something else")
            .rgb(120, 130, 160)
            .rgb_bg(42, 42, 42)
            .bold()
            .crossed())

    print(normal("color combos?").red().bg(blue))
    print("normal" + blue("blue") + red("red") + "normal")
