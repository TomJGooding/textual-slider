from __future__ import annotations

from math import ceil
from typing import Optional

from rich.console import RenderableType
from textual import events
from textual.binding import Binding
from textual.geometry import Offset, Size, clamp
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
    _slider_position = reactive(0.0)
    _grabbed: reactive[Offset | None] = reactive[Optional[Offset]](None)
    _grabbed_position = reactive(0.0)

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
        min: int,
        max: int,
        step: int = 1,
        value: int | None = None,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.min = min
        self.max = max
        self.step = step
        if value is not None:
            self.value = value

    @property
    def number_of_steps(self) -> int:
        return int((self.max - self.min) / self.step) + 1

    def watch_value(self) -> None:
        if not self._grabbed:
            self._slider_position = (
                (self.value - self.min) / (self.number_of_steps / 100)
            ) / self.step
        self.post_message(self.Changed(self, self.value))

    def render(self) -> RenderableType:
        style = self.get_component_rich_style("slider--slider")
        thumb_size = ceil(100 / self.number_of_steps)
        return ScrollBarRender(
            virtual_size=100,
            window_size=thumb_size,
            position=self._slider_position,
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

    def action_grab(self) -> None:
        self.capture_mouse()

    async def _on_mouse_up(self, event: events.MouseUp) -> None:
        if self._grabbed:
            self.release_mouse()
            self._grabbed = None
        event.stop()

    def _on_mouse_capture(self, event: events.MouseCapture) -> None:
        self._grabbed = event.mouse_position
        self.grabbed_position = self._slider_position

    def _on_mouse_release(self, event: events.MouseRelease) -> None:
        self._grabbed = None
        event.stop()

    async def _on_mouse_move(self, event: events.MouseMove) -> None:
        if self._grabbed:
            mouse_move = event.screen_x - self._grabbed.x
            new_slider_position = self.grabbed_position + (
                mouse_move * (100 / self.content_size.width)
            )
            max_position = (
                (self.max - self.min) / (self.number_of_steps / 100)
            ) / self.step
            self._slider_position = clamp(new_slider_position, 0, max_position)
            self.value = (
                self.step * round(self._slider_position * (self.number_of_steps / 100))
                + self.min
            )

        event.stop()

    async def _on_click(self, event: events.Click) -> None:
        event.stop()
