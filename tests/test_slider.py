from textual.app import App, ComposeResult

from textual_slider import Slider


class SliderApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    Slider {
        width: 18;
    }
    """

    def compose(self) -> ComposeResult:
        yield Slider(0, 9, step=3)


async def test_clicking_slider_updates_position_and_value() -> None:
    app = SliderApp()
    async with app.run_test() as pilot:
        slider = pilot.app.query_one(Slider)

        await pilot.click(Slider, offset=(13, 1))
        assert slider.value == 9
        assert slider._slider_position == 75.0

        await pilot.click(Slider, offset=(10, 1))
        assert slider.value == 6
        assert slider._slider_position == 50.0

        await pilot.click(Slider, offset=(7, 1))
        assert slider.value == 3
        assert slider._slider_position == 25.0

        await pilot.click(Slider, offset=(4, 1))
        assert slider.value == 0
        assert slider._slider_position == 0.0
