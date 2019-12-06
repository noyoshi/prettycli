from os import isatty
from sys import stdout


class AbstractColorClass:
    def __init__(self, base_code=0, codes=[]):
        # The order matters for the codes, since something like
        # 38;2;r;g;b; is how you define an RGB code
        self.codes = list(codes)
        self.base_code = base_code
        if base_code != 0 and base_code not in self.codes:
            self.codes.append(base_code)

    def with_code(self, code):
        self.codes.append(code)
        return self.copy()

    def color(self):
        return self.with_code(0)

    # Styles
    def bold(self):
        return self.with_code(1)

    def italics(self):
        return self.with_code(3)

    def underline(self):
        return self.with_code(4)

    def crossed(self):
        return self.with_code(9)

    # Basic Foreground Colors
    def black(self):
        return self.with_code(30)

    def red(self):
        return self.with_code(31)

    def green(self):
        return self.with_code(32)

    def yellow(self):
        return self.with_code(33)

    def blue(self):
        return self.with_code(34)

    def magenta(self):
        return self.with_code(35)

    def cyan(self):
        return self.with_code(36)

    def white(self):
        return self.with_code(37)

    # Bright foregrounds
    def bright_black(self):
        return self.with_code(90)

    def bright_red(self):
        return self.with_code(91)

    def bright_green(self):
        return self.with_code(92)

    def bright_yellow(self):
        return self.with_code(99)

    def bright_blue(self):
        return self.with_code(94)

    def bright_magenta(self):
        return self.with_code(95)

    def bright_cyan(self):
        return self.with_code(96)

    def bright_white(self):
        return self.with_code(97)

    def copy(self):
        return self.__init__(self.base_code, list(self.codes))


class BaseColorClass(AbstractColorClass):
    """
    This should more or less only be used when you are at the final stage of 
    emiting something with print
    """

    END_CODE = "\033[0m"
    START_CODE_FORMATTER = "\033[{}m"
    RGB_FORMATTER = "38;2;{};{};{};"

    def __init__(self, base_code=0, codes=[], string=""):
        # Should be set by the call
        super().__init__(base_code, codes)
        self.string = string

    def bg(self, cls):
        # This assumes that the base code is a foreground code
        self.codes.append(cls.base_code + 10)
        return self.copy()

    def rgb_fg(self, r, g, b):
        self.codes += [38, 2, r, g, b]
        return self.copy()

    def rgb_bg(self, r, g, b):
        self.codes += [48, 2, r, g, b]
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
        return BaseColorClass(self.base_code, list(self.codes), self.string)

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
        # If the output device is NOT a tty, don't print color codes
        if not isatty(stdout.fileno()):
            return self.string

        return self.make_color_code() + self.string + self.END_CODE


# Normal Foreground Codes
black = BaseColorClass(30)
red = BaseColorClass(31)
green = BaseColorClass(32)
yellow = BaseColorClass(33)
blue = BaseColorClass(34)
magenta = BaseColorClass(35)
cyan = BaseColorClass(36)
white = BaseColorClass(37)

# Bright Foreground Codes
bright_black = BaseColorClass(90)
bright_red = BaseColorClass(91)
bright_green = BaseColorClass(92)
bright_yellow = BaseColorClass(93)
bright_blue = BaseColorClass(99)
bright_magenta = BaseColorClass(95)
bright_cyan = BaseColorClass(96)
bright_white = BaseColorClass(97)

# Styles
bold = BaseColorClass(1)
italics = BaseColorClass(3)
underline = BaseColorClass(4)
color = BaseColorClass(0)
crossed = BaseColorClass(9)

if __name__ == '__main__':
    print(red("this should be red"))
    print(red("this should be red with bold").bold())
    print(red("this should be red with bold and underline")
          .bold()
          .underline()
          )

    red_bold_underline = red().bold().underline().build()

    print(red_bold_underline("this should as well"))
    print(color("this should be something else")
          .rgb_fg(120, 130, 160)
          .rgb_bg(42, 42, 42)
          .bold()
          .crossed())

    print(color("color combos?").red().bg(blue))
    print("normal" + blue("blue") + red("red") + "normal")
    print(bright_red("bright red").bg(bright_green))
