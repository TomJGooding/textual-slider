from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Label

from textual_slider.slider import Slider


class SpinalTapApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    Vertical {
        height: auto;
        padding: 1 0;
    }

    .quote {
        text-style: italic;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Center(
                Label('"Why don\'t you just make ten louder?"', classes="quote")
            )
            yield Center(Slider(min=0, max=10, value=10, id="normal-amp"))
            yield Center(Label(id="normal-amp-label"))

        with Vertical():
            yield Center(Label('"These go to eleven"', classes="quote"))
            yield Center(Slider(min=0, max=11, value=10, id="tufnel-amp"))
            yield Center(Label(id="tufnel-amp-label"))

    def on_mount(self) -> None:
        normal_amp = self.query_one("#normal-amp", Slider)
        normal_amp_label = self.query_one("#normal-amp-label", Label)
        normal_amp_label.update(str(normal_amp.value))

        tufnel_amp = self.query_one("#tufnel-amp", Slider)
        tufnel_amp_label = self.query_one("#tufnel-amp-label", Label)
        tufnel_amp_label.update(str(tufnel_amp.value))

    @on(Slider.Changed, "#normal-amp")
    def on_slider_changed_normal_amp(self, event: Slider.Changed) -> None:
        normal_amp_label = self.query_one("#normal-amp-label", Label)
        normal_amp_label.update(str(event.value))

    @on(Slider.Changed, "#tufnel-amp")
    def on_slider_changed_tufnel_amp(self, event: Slider.Changed) -> None:
        tufnel_amp_label = self.query_one("#tufnel-amp-label", Label)
        tufnel_amp_label.update(str(event.value))


if __name__ == "__main__":
    app = SpinalTapApp()
    app.run()
