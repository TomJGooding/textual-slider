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
        self.max = max
        self.step = step
        if value is not None:
            self.value = value

    def render(self) -> RenderableType:
        scroll_percentage = (self.value / self.max) * 100
        scroll_thumb_size = round(100 / self.max)
        scroll_thumb_pos = scroll_percentage - (scroll_thumb_size / 2)
        return ScrollBarRender(
            virtual_size=100,
            window_size=scroll_thumb_size,
            position=scroll_thumb_pos,
            vertical=False,
        )

    def get_content_width(self, container: Size, viewport: Size) -> int:
        return 32

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        return 1
