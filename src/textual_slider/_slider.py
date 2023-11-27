from __future__ import annotations

from math import ceil
from typing import Optional

from rich.console import RenderableType
from textual import events
from textual.binding import Binding
from textual.geometry import Offset, clamp
from textual.message import Message
from textual.reactive import reactive, var
from textual.scrollbar import ScrollBarRender
from textual.widget import Widget


class Slider(Widget, can_focus=True):
    """A simple slider widget."""

    BINDINGS = [
        Binding("right", "slide_right", "Slide Right", show=False),
        Binding("left", "slide_left", "Slide Left", show=False),
    ]

    COMPONENT_CLASSES = {"slider--slider"}

    DEFAULT_CSS = """
    Slider {
        width: 32;
        height: 3;
        min-height: 3;
        border: tall transparent;
        background: $boost;
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

    value = reactive(0, init=False)
    """The value of the slider."""

    _slider_position = reactive(0.0)
    _grabbed: var[Offset | None] = var[Optional[Offset]](None)
    _grabbed_position: var[float] = var(0.0)

    class Changed(Message):
        """Posted when the value of the slider changes.

        This message can be handled using an `on_slider_changed` method.
        """

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
        """Create a slider widget.

        Args:
            min: The minimum value of the slider.
            max: The maximum value of the slider.
            step: The step size of the slider.
            value: The initial value of the slider.
            name: The name of the slider.
            id: The ID of the slider in the DOM.
            classes: The CSS classes of the slider.
            disabled: Whether the slider is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.min = min
        self.max = max
        self.step = step
        self.value = value if value is not None else min
        self._slider_position = (
            (self.value - self.min) / (self.number_of_steps / 100)
        ) / self.step

    @property
    def number_of_steps(self) -> int:
        return int((self.max - self.min) / self.step) + 1

    def validate_value(self, value: int) -> int:
        return clamp(value, self.min, self.max)

    def validate__slider_position(self, slider_position: float) -> float:
        max_position = (
            (self.max - self.min) / (self.number_of_steps / 100)
        ) / self.step
        return clamp(slider_position, 0, max_position)

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

    def action_slide_right(self) -> None:
        self.value = self.value + self.step

    def action_slide_left(self) -> None:
        self.value = self.value - self.step

    def action_grab(self) -> None:
        self.capture_mouse()

        # Workaround for unexpected mouse grab and drag behaviour
        # depending on the currently focused widget.
        # Stolen from https://github.com/1j01/textual-paint
        self.can_focus = False

    async def _on_mouse_up(self, event: events.MouseUp) -> None:
        if self._grabbed:
            self.release_mouse()
            self._grabbed = None

            # Workaround for unexpected mouse behaviour mentioned above
            self.can_focus = True

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
            self._slider_position = self.grabbed_position + (
                mouse_move * (100 / self.content_size.width)
            )
            self.value = (
                self.step * round(self._slider_position * (self.number_of_steps / 100))
                + self.min
            )

        event.stop()

    async def _on_click(self, event: events.Click) -> None:
        event.stop()
