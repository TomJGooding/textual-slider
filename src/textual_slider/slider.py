from rich.console import RenderableType
from textual.geometry import Size
from textual.reactive import reactive
from textual.scrollbar import ScrollBarRender
from textual.widget import Widget


class Slider(Widget, can_focus=True):
    DEFAULT_CSS = """
    Slider {
        border: tall transparent;
        background: $panel;
        height: auto;
        width: auto;
        padding: 0 2;
    }
    """

    value = reactive(0, init=False)
    grabbed = reactive(None)

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

    def render(self) -> RenderableType:
        num_steps = ((self.max - self.min) / self.step) + 1
        thumb_size = round(100 / num_steps)
        slider_percent = (self.value / num_steps) * 100

        return ScrollBarRender(
            virtual_size=100,
            window_size=thumb_size,
            position=slider_percent,
            vertical=False,
        )

    def get_content_width(self, container: Size, viewport: Size) -> int:
        return 32

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        return 1
