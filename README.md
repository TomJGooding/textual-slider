# textual-slider

A Textual widget for a simple slider.

![screenshot](https://raw.githubusercontent.com/TomJGooding/textual-slider/main/assets/screenshot.png)

## Installation

Install textual-slider using pip:

```
pip install textual-slider
```

## Usage

textual-slider provides a simple `Slider` widget for use in
[Textual](https://github.com/Textualize/textual), that allows selecting an
**integer** value within a given range.

The initial value of the slider if not specified is the minimum value.
You can also optionally specify a step size between valid values.

```python
yield Slider(0, 10)

yield Slider(min=200, max=500, step=100, value=300)
```

You can find more complete usage examples of the `Slider` widget in the
`/examples/` directory of this repo.

## Limitations

Textual apps run in the terminal, which work in terms of character cells rather
than pixels. This means you obviously can't have the same fine-grained control
for this slider as usual, depending on the size of the slider range and the
styled width.

Currently this slider widget only works with **integer** values. Any suggestions
for how to work with floating point values would be welcome!

## Contributing

I created this simple slider widget as a learning exercise to better
understand Textual and it is still a work in progress.

I'd really appreciate any feedback or suggestions, but I'm afraid I
probably won't be accepting any PRs at the moment.

## Licence

Licensed under the [GNU General Public License v3.0](LICENSE).
