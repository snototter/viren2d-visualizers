import numpy as np
import viren2d
from typing import List, Tuple

#TODO ground plane overlay


class CameraPoseOverlay(object):
    """TODO documentation
    params: (K, R, t, label)
    """
    def __init__(self):
        self.origin = viren2d.Vec3d(0, 0, 0)
        self.arrow_lengths = viren2d.Vec3d(1e3, 1e3, 1e3)
        self.arrow_style = viren2d.ArrowStyle(
            width=5, tip_length=0.3, tip_angle=20,
            tip_closed=True, double_headed=False,
            dash_pattern=[], dash_offset=0.0,
            cap='round', join='miter')
        self.color_x = viren2d.axis_color('x')
        self.color_y = viren2d.axis_color('y')
        self.color_z = viren2d.axis_color('z')

        self.text_anchor = viren2d.Anchor.Top
        self.text_style = viren2d.TextStyle(
            family='sans-serif', size=14, color='navy-blue',
            bold=False, italic=False)
        self.text_box_line_style = viren2d.LineStyle.Invalid
        self.text_box_fill_color = viren2d.Color(1, 1, 1, 0.8)
        self.text_padding = viren2d.Vec2d(5, 5)
        self.text_box_radius = 0.2

    def apply(
            self, painter: viren2d.Painter,
            pose: Tuple[np.ndarray, np.ndarray, np.ndarray, str]) -> bool:
        K, R, t, label = pose

        success, origin, tip_x, tip_y, tip_z = painter.draw_xyz_axes(
            K=K, R=R, t=t, origin=self.origin, lengths=self.arrow_lengths,
            arrow_style=self.arrow_style, color_x=self.color_x,
            color_y=self.color_y, color_z=self.color_z)
        
        if (label is not None) and (len(label) > 0):
            res = painter.draw_text_box(
                text=[label], position=origin, anchor=self.text_anchor,
                text_style=self.text_style, padding=self.text_padding,
                rotation=0, line_style=self.text_box_line_style,
                fill_color=self.text_box_fill_color,
                radius=self.text_box_radius)
            success = success and res

        return success


class TagPoseOverlay(CameraPoseOverlay):
    """TODO params: K, List of R,t,label"""
    def __init__(self):
        super().__init__()
    
    def apply(
            self, painter: viren2d.Painter,
            params: Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray, str]]) -> bool:
        K, poses = params
        success = True
        for R, t, label in poses:
            res = super().apply(painter, (K, R, t, label))
            success = success and res
        return success
