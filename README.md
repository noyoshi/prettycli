<h1 align="center">🎨 prettycli 🌟</h1>
<h5 align="center">
<i align="center">Dependency free pretty CLI printing in Python (colors, unicode boxes, etc). More to come!</i></h5>

### Color module example
![Demo Gif](docs/demo.gif)
_Made with asciinema_

```py
from colorizer import red, blue, yellow, color

# You can print a basic color by passing a string into the color object
print(red("this is red"))

# You can add other attributed to what you print by calling methods on the
# color objects
print(red("this is red and bold").bold())

# You can set the background by passing in a color object to the bg method
print(red("this is red, with a blue background").bg(blue))

# We even support true colors! You can use the base object 'color' and modify
# the foreground with the rgb method
print(color("This was made with true color rgb").rgb(60, 100, 120))
```

#### TODO
- [ ] Performance checks - this should be as lightweight as possible
- [ ] Unit tests
- [x] No more dynamic variable definitions, as that messes with linters
- [ ] `box.py` demo + better abstractions

