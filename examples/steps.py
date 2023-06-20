from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Label

from textual_slider.slider import Slider


class SliderWithStepApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    Vertical {
        height: auto;
        padding: 1 0;
        content-align: center middle;
    }

    .title {
        text-style: bold;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Center(Label("0 to 100 slider with step of 25", classes="title"))
            yield Center(Slider(min=0, max=100, step=25, value=0, id="slider1"))
            yield Center(Label(id="slider1-value"))

        with Vertical():
            yield Center(Label("-20 to 20 slider with step of 4", classes="title"))
            yield Center(Slider(min=-20, max=20, step=4, value=0, id="slider2"))
            yield Center(Label(id="slider2-value"))

        with Vertical():
            yield Center(Label("200 to 500 slider with step of 100", classes="title"))
            yield Center(Slider(min=200, max=500, step=100, value=200, id="slider3"))
            yield Center(Label(id="slider3-value"))

    def on_mount(self) -> None:
        slider1 = self.query_one("#slider1", Slider)
        slider1_value_label = self.query_one("#slider1-value", Label)
        slider1_value_label.update(str(slider1.value))

        slider2 = self.query_one("#slider2", Slider)
        slider2_value_label = self.query_one("#slider2-value", Label)
        slider2_value_label.update(str(slider2.value))

        slider3 = self.query_one("#slider3", Slider)
        slider3_value_label = self.query_one("#slider3-value", Label)
        slider3_value_label.update(str(slider3.value))

    @on(Slider.Changed, "#slider1")
    def on_slider_changed_slider1(self, event: Slider.Changed) -> None:
        value_label = self.query_one("#slider1-value", Label)
        value_label.update(str(event.value))

    @on(Slider.Changed, "#slider2")
    def on_slider_changed_slider2(self, event: Slider.Changed) -> None:
        value_label = self.query_one("#slider2-value", Label)
        value_label.update(str(event.value))

    @on(Slider.Changed, "#slider3")
    def on_slider_changed_slider3(self, event: Slider.Changed) -> None:
        value_label = self.query_one("#slider3-value", Label)
        value_label.update(str(event.value))


if __name__ == "__main__":
    app = SliderWithStepApp()
    app.run()
