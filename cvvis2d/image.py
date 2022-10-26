import viren2d
import numpy as np
from cvvis2d.utils import compute_absolute_canvas_position


class ImageOverlay(object):
    """
    Draws an image at a predefined location within the canvas.

    Can be used to overlay depth maps, etc.

    Args:
      position: Absolute (coordinates > 1 or < -1) or
        relative (-1 <= coordinates <= 1) position of the
        anchor point within the canvas.
      anchor: How to align the image w.r.t. the anchor point. Can be either
        a viren2d.Anchor enum value or its string representation, e.g. 'top'.
      scale: Scaling factor for the x and y directions.
      rotation: Rotation angle in degrees.
      alpha: Opacity value from 0 (fully transparent) to 1 (fully opaque).
      line_style: If valid, a border will be drawn around the overlay.
      clip_factor: If > 0, the corners will be rounded.
    """

    def __init__(self):
        self.position = viren2d.Vec2d(-5, -5)
        self.anchor = viren2d.Anchor.BottomRight
        self.scale = viren2d.Vec2d(1, 1)
        self.rotation = 0
        self.alpha = 0.8
        self.line_style = viren2d.LineStyle.Invalid
        self.clip_factor = 0.2

    def apply(
            self, painter: viren2d.Painter,
            image: np.ndarray) -> bool:
        position = compute_absolute_canvas_position(
            self.position, painter.width, painter.height)

        return painter.draw_image(
            image=image, position=position, anchor=self.anchor,
            alpha=self.alpha, scale_x=self.scale[0], scale_y=self.scale[1],
            rotation=self.rotation, clip_factor=self.clip_factor,
            line_style=self.line_style)
