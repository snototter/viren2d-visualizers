# import numpy as np
import viren2d
from cvvis2d.utils import compute_absolute_padding
from typing import List, Tuple, Union


def _to_str_list(label: Union[str, List[str]]) -> List[str]:
    if label is None:
        return []
    elif isinstance(label, str):
        return [label]
    else:
        return label


class BoundingBox2d(object):
    """
    Encapsulates a bounding box for visualization, *i.e.* box coordinates and
    corresponding label(s).
    """
    def __init__(
            self, left: float, top: float, width: float, height: float,
            color: viren2d.Color, label_top: str, label_bottom: str,
            label_left: str, label_right: str):
        self._left = left
        self._top = top
        self._width = width
        self._height = height
        self._color = color
        self._label_top = label_top
        self._label_bottom = label_bottom
        self._label_left = label_left
        self._label_right = label_right
    
    def to_rect(self, corner_radius: float):
        return viren2d.Rect.from_ltwh(
            self._left, self._top, self._width, self._height, corner_radius)

    @property
    def color(self):
        return self._color

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def label_top(self):
        return _to_str_list(self._label_top)

    @property
    def label_bottom(self):
        return _to_str_list(self._label_bottom)

    @property
    def label_left(self):
        return _to_str_list(self._label_left)

    @property
    def label_right(self):
        return _to_str_list(self._label_right)
    
    @classmethod
    def from_ltwh(
            cls, left: float, top: float, width: float, height: float,
            color: viren2d.Color, label_top: str = None,
            label_bottom: str = None, label_left: str = None,
            label_right: str = None):
        return cls(
            left, top, width, height, color, label_top, label_bottom,
            label_left, label_right)


def create_bounding_box(
        class_id: Union[str, int], left: float, top: float,
        width: float, height: float, score: float) -> BoundingBox2d:
    """TODO document (default bounding box/label from id, l, t, w, h & score"""
    if isinstance(class_id, str):
        label_top = class_id
        color = viren2d.Color.from_object_category(str(class_id))
    else:
        class_id = int(class_id)
        label_top = f'Class #{class_id:d}'
        color = viren2d.Color.from_object_id(class_id)
    label_bottom = f'C: {score:.2f}'
    label_left = None
    label_right = None
    return BoundingBox2d.from_ltwh(
        left, top, width, height, color, label_top, label_bottom,
        label_left, label_right)


class BoundingBox2dOverlay(object):
    """
    Draws bounding boxes (rectangles + corresponding labels).

    TODO doc parametrization
    TODO label padding can be specified relative (w.r.t. bounding box dimension)
    """
    def __init__(self):
        self.text_style = viren2d.TextStyle(
            family='sans-serif', size=14, color='navy-blue',
            bold=False, italic=False, halign='left')
        self.line_style = viren2d.LineStyle(
            width=3)
        self.box_fill_color = 'same!30'
        self.text_fill_color = 'white!70'
        self.corner_radius = 0.1
        self.label_padding = viren2d.Vec2d(0.05, 0.05)
        self.clip_label = False
        self.label_left_t2b = False
        self.label_right_t2b = True

    def apply(
            self, painter: viren2d.Painter,
            detections: List[BoundingBox2d]) -> bool:
        box_style = viren2d.BoundingBox2DStyle(
            line_style=self.line_style, text_style=self.text_style,
            box_fill_color=self.box_fill_color,
            text_fill_color=self.text_fill_color,
            label_padding=self.label_padding,
            clip_label=self.clip_label)

        success = True
        for box in detections:
            box_style.label_padding = compute_absolute_padding(
                self.label_padding, box.width, box.height)
            box_style.line_style.color = box.color
            res = painter.draw_bounding_box_2d(
                rect=box.to_rect(self.corner_radius), box_style=box_style,
                label_top=box.label_top, label_bottom=box.label_bottom,
                label_left=box.label_left, left_t2b=self.label_left_t2b,
                label_right=box.label_right, right_t2b=self.label_right_t2b)
            success = success and res

        return success
