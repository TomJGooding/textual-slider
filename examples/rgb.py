from textual import on
from textual.app import App, ComposeResult
from textual.color import Color
from textual.widgets import Header

from textual_slider import Slider


class RgbSlidersApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    #red-slider .slider--slider {
        color: red;
    }

    #green-slider .slider--slider {
        color: green;
    }

    #blue-slider .slider--slider {
        color: blue;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Slider(min=0, max=255, value=0, id="red-slider")
        yield Slider(min=0, max=255, value=0, id="green-slider")
        yield Slider(min=0, max=255, value=0, id="blue-slider")

    def on_mount(self) -> None:
        red = self.query_one("#red-slider", Slider).value
        green = self.query_one("#green-slider", Slider).value
        blue = self.query_one("#blue-slider", Slider).value

        self.screen.styles.background = Color(red, green, blue)
        self.title = f"RGB {red} {green} {blue}"

    @on(Slider.Changed)
    def update_screen_color(self) -> None:
        red = self.query_one("#red-slider", Slider).value
        green = self.query_one("#green-slider", Slider).value
        blue = self.query_one("#blue-slider", Slider).value

        self.screen.styles.background = Color(red, green, blue)
        self.title = f"RGB {red} {green} {blue}"


if __name__ == "__main__":
    app = RgbSlidersApp()
    app.run()
