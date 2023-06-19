from textual.app import App, ComposeResult
from textual.containers import Center
from textual.widgets import Label

from textual_slider.slider import Slider


class SliderWithStepApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Center(Label("0 to 100 slider with step of 25"))
        yield Center(Slider(max=100, step=25, value=0))
        yield Center(Label(id="slider-value"))

    def on_slider_changed(self, event: Slider.Changed) -> None:
        value_label = self.query_one("#slider-value", Label)
        value_label.update(str(event.value))


if __name__ == "__main__":
    app = SliderWithStepApp()
    app.run()
