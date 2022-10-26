#__all__ = ['detection', 'image', 'text']
# The core visualization pipeline
from cvvis2d.pipeline import VisualizationPipeline

# Load version
import os
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'version.py')) as _vf:
    exec(_vf.read())

# Text overlays & utils
from cvvis2d.text import frame_label, DynamicTextOverlay, StaticTextOverlay
# Image overlays
from cvvis2d.image import ImageOverlay

# from cvvis2d.pinhole import
from cvvis2d.detection import BoundingBox2d, BoundingBox2dOverlay, create_bounding_box