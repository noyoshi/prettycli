from os import isatty
from sys import stdout

def tty_brancher(function):
    """
    function MUST RETURN A LIST OF STRINGS OF SIZE 3
    """
    def f(*args, **kwargs):
        if isatty(stdout.fileno()):
            # print("is a tty")
            return ''.join(function(*args, **kwargs))
        # print("not a tty")
        return_data = function(*args, **kwargs)
        return return_data[1]
    return f

class BaseColorClass:
    """
    This should more or less only be used when you are at the final stage of emiting something
    with print
    """

    END_CODE = "\033[0m"
    START_CODE_FORMATTER = "\033[{}m" # insert the specific stuff in here
    RGB_FORMATTER = "38;2;{};{};{};"
    def __init__(self, bg="", fg="", color_code=None, string=""):
        self.bg = bg
        self.fg = fg

        # Should be set by the call
        self.string = string

        # Should be set by the rgb method?
        self.color_code = color_code
        self.codes = []

    def fore_ground(self, code):
        self.fg = code
        self.codes.append(code)
        return self

    def background(self, cls):
        self.bg = cls.fg + 10
        self.codes.append(self.bg)
        return self

    def rgb(self, r, g, b):
        self.codes += [38, 2, r, g, b]
        return self

    def rgb_bg(self, r, g, b):
        self.codes += [48, 2, r, g, b]
        return self

    def code(self, code):
        self.codes.append(str(code))
        return self

    def make_color_code(self):
        basic_codes = ';'.join(list(map(str, self.codes)))

        # partials = [self.rgb_string]
        # partials = [x for x in partials if x]
        return self.START_CODE_FORMATTER.format(basic_codes)

    def __call__(self, string=None):
        if string is not None:
            self.string = string
        return self.copy()

    def build(self):
        return self.copy()

    @tty_brancher
    def __str__(self):
        self.color_code = self.make_color_code()

        return "{}#{}#{}".format(self.color_code, self.string, self.END_CODE).split("#")

    def __len__(self):
        return len(self.string)
    
    def __add__(self, x):
        return self.string + x

    @tty_brancher
    def to_str(self):
        """To make it a bit easier to convert"""
        return str(self)

    def as_func(self):
        return self.__call__

    def copy(self):
        # TODO refactor this
        n = BaseColorClass(self.bg, self.fg, self.color_code, self.string)
        n.codes = list(self.codes)
        return n


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
    # ("framed", 51),
    # ("encircled", 52),
    # ("blink", 5)
]

def wrapped(code):
    def add_atrribute(self, string=""):
        x = self.copy()
        x.codes.append(code)
        x.string += string
        return x 
    return add_atrribute

for c, code in colors:
    locals()[c] = BaseColorClass().fore_ground(code)

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

    print(normal("whacky stuff!"))
