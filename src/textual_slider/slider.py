from __future__ import annotations

from math import ceil

from rich.console import RenderableType
from textual.binding import Binding
from textual.geometry import Size
from textual.message import Message
from textual.reactive import reactive
from textual.scrollbar import ScrollBarRender
from textual.widget import Widget


class Slider(Widget, can_focus=True):
    BINDINGS = [
        Binding("right", "slide_right", "Slide Right", show=False),
        Binding("left", "slide_left", "Slide Left", show=False),
    ]

    COMPONENT_CLASSES = {"slider--slider"}

    DEFAULT_CSS = """
    Slider {
        border: tall transparent;
        background: $boost;
        height: auto;
        width: auto;
        padding: 0 2;
    }

    Slider > .slider--slider {
        background: $panel-darken-2;
        color: $primary;
    }

    Slider:focus {
        border: tall $accent;
    }
    """

    value = reactive(0)
    slider_percent = reactive(0.0)

    class Changed(Message):
        def __init__(self, slider: Slider, value: int) -> None:
            super().__init__()
            self.value: int = value
            self.slider: Slider = slider

        @property
        def control(self) -> Slider:
            return self.slider

    def __init__(
        self,
        # min: int,
        max: int,
        step: int = 1,
        value: int | None = None,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.min = 0
        self.max = max
        self.step = step
        if value is not None:
            self.value = value

    @property
    def number_of_steps(self) -> int:
        return int((self.max - self.min) / self.step) + 1

    def watch_value(self) -> None:
        self.slider_percent = (self.value / self.number_of_steps) * 100
        self.post_message(self.Changed(self, self.value))

    def render(self) -> RenderableType:
        style = self.get_component_rich_style("slider--slider")
        thumb_size = ceil(100 / self.number_of_steps)
        return ScrollBarRender(
            virtual_size=100,
            window_size=thumb_size,
            position=self.slider_percent,
            style=style,
            vertical=False,
        )

    def get_content_width(self, container: Size, viewport: Size) -> int:
        return 32

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        return 1

    def action_slide_right(self) -> None:
        new_value = self.value + self.step
        if new_value <= self.max:
            self.value = new_value

    def action_slide_left(self) -> None:
        new_value = self.value - self.step
        if new_value >= self.min:
            self.value = new_value
