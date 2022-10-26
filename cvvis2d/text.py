from typing import Any, List, Union
import viren2d
import datetime
from cvvis2d.utils import compute_absolute_canvas_position


def frame_label(
      cam_label: str, frame_number: int = None,
      timestamp: datetime.datetime = None,
      num_digits: int = 5,
      include_date: bool = True) -> str:
    """
    Returns a default string representation to tag/label an image based on
    the current frame number (if not None) and timestamp (if not None).
    """
    lbl = cam_label
    if frame_number is not None:
        lbl += f' #{frame_number:0{num_digits}d}'

    if timestamp is not None:
        lbl += ', {:s}.{:03d}'.format(
            timestamp.strftime("%Y-%m-%d %H:%M:%S" if include_date else "%H:%M:%S"),
            int(timestamp.microsecond / 1e3))
    return lbl


class DynamicTextOverlay(object):
    """
    Draws text/a text box at a predefined location within the image.

    The text has to be provided for each image separately. Thus, this
    visualizer can be used to overlay time, frame number, camera label, etc.
    To overlay a static text (text that will never change), use
    `StaticTextOverlay` instead.

    Args:
      position: Absolute (coordinates > 1 or < -1) or
        relative (-1 <= coordinates <= 1) position of the
        anchor point within the canvas.
      anchor: How to align the text w.r.t. the anchor point. Can be either
        a viren2d.Anchor enum value or its string representation, e.g. 'top'.
      text_style: How to render the glyphs.
      line_style: If valid, a border will be drawn around the text.
      fill_color: If valid, the background behind the text will be colored.
      padding: Distance between the text box edge and the glyphs.
      rotation: Rotation angle in degrees.
      corner_radius: If > 0 (and < 0.5), the text box will be drawn with
        rounded corners.
    """
    def __init__(self):
        self.position = viren2d.Vec2d(0.5, 10)
        self.anchor = viren2d.Anchor.Top
        self.text_style = viren2d.TextStyle(
            family='monospace', size=14, color='navy-blue',
            bold=False, italic=False)
        self.line_style = viren2d.LineStyle.Invalid
        self.fill_color = viren2d.Color(1, 1, 1, 0.8)
        self.padding = viren2d.Vec2d(5, 5)
        self.rotation = 0
        self.corner_radius = 0.2
    
    def apply(
            self, painter: viren2d.Painter,
            text: Union[str, List[str]]) -> bool:
        position = compute_absolute_canvas_position(
            self.position, painter.width, painter.height)

        return painter.draw_text_box(
            text=[text] if isinstance(text, str) else text,
            position=position, anchor=self.anchor,
            text_style=self.text_style, padding=self.padding,
            rotation=self.rotation, line_style=self.line_style,
            fill_color=self.fill_color, radius=self.corner_radius)


class StaticTextOverlay(DynamicTextOverlay):
    """
    Draws a static (never changing) text/a text box at a predefined
    location within the image.

    Useful to overlay camera labels, sequence names, etc.

    See `DynamicTextOverlay` for the general parametrization (text style,
    positioning, etc.).
    In addition, this class simply provides a `text` attribute which
    holds the text to be displayed.
    """

    def __init__(self):
        super().__init__()
        self.position = viren2d.Vec2d(-10, 10)
        self.anchor = viren2d.Anchor.TopRight
        self.text = 'Static Text'
    
    def apply(self, painter: viren2d.Painter) -> bool:
        return super().apply(painter, self.text)
