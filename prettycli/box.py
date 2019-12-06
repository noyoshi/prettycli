from prettycli.colorizer import blue, red, color, yellow


class box:
    def __init__(self, string):
        self.string = string

        self.top_l = "┌"
        self.top_r = "┐"
        self.bar_t = "─"
        self.bar_b = "─"
        self.bot_l = "└"
        self.bot_r = "┘"
        self.line_l = "│"
        self.line_r = "│"
        self.color = color

    def with_color(self, color_cls):
        self.color = color_cls
        return self

    def draw(self):
        result = self.color(
            self.top_l + len(self.string) * self.bar_t +
            self.top_r + "\n" + self.line_l).to_str()
        result = str(result) + str(self.string)
        result = str(result) + self.color(self.line_r + "\n" + self.bot_l +
                                          len(self.string) * self.bar_b + self.bot_r).to_str()
        return result

    def double(self):
        self.bot_r = "╝"
        self.bot_l = "╚"
        self.line_r = "║"
        self.line_l = "║"
        self.top_l = "╔"
        self.top_r = "╗"
        self.bar_b = "═"
        self.bar_t = "═"
        return self

    def thick(self):
        self.bot_r = "▟"
        self.bot_l = "▙"
        self.line_r = "▐"
        self.line_l = "▌"
        self.top_l = "▛"
        self.top_r = "▜"
        self.bar_t = "▀"
        self.bar_b = "▄"

        return self


if __name__ == "__main__":
    print(blue(box("hello there, general kenobi").thick().draw()).bold())
    print(box(red("this is red only here").bold()).thick().with_color(blue).draw())
    print(blue(box(red("this is red only here").bold()).thick().draw()))

    print(box("Hello World!").with_color(red).draw())
