from typing import Any, Dict
import numpy as np
import viren2d
import logging

#TODO remove debug timings
from vito import pyutils


class VisualizationPipeline(object):
    """
    Sets up a visualization pipeline which you can apply to simplify
    visualizing a stream of images.

    Example: Overlay timestamps for a video:

    >>> from visualizers.pipeline import VisualizationPipeline
    >>> from visualizers.text_overlay import TextOverlay, frame_label
    >>> # Set up the visualization pipeline:
    >>> visualizer = VisualizationPipeline()
    >>> overlay = TextOverlay()
    >>> visualizer.add('frame-label', overlay)
    >>> # Process video stream
    >>> while True:
    >>>     image = load_next_image()
    >>>     vis = visualizer.visualize(image, {'frame-label': 'Some text'})

    #TODO add tracking-by-detection or camera geometry/calibration example
    """
    def __init__(self):
        # The painter will be passed on to each visualizer
        self._painter = viren2d.Painter()
        # Registered visualizers as list of tuple(identifier, visualizer)
        self._visualizers = list()
        # Used to check for unique identifiers
        self._identifiers = set()
    
    def add(self, identifier: str, visualizer: object) -> None:
        """
        Adds the given visualizer to this pipeline.

        Args:
          identifier: Unique identifier which will be used to look up the
            input parameters for this visualizer in the `visualize` call.
          visualizer: A visualizer must have an `apply` method, which takes the
            `viren2d.Painter` (used for drawing) and its additional parameters.
        """
        if identifier in self._identifiers:
            raise KeyError(
                f'Identifier "{identifier}" has already been registered')

        apply_op = getattr(visualizer, 'apply', None)
        if not callable(apply_op):
            raise ValueError(
                f'Visualizer "{identifier}" does not have an `apply` method.')

        self._identifiers.add(identifier)
        self._visualizers.append((identifier, visualizer))
    
    def visualize(
            self, image: np.ndarray,
            visualizer_args: Dict[str, Any]) -> np.ndarray:
        """
        Applies the configured visualization pipeline on the given image.

        Returns the visualization result as RGB image.

        Args:
          image: Input image.
          visualizer_args: Dictionary holding the input parameters for each
            registered visualizer. The lookup key (type `str`) is the
            identifier used for the corresponding `add` call.
        """
        if image is None:
            return None

        pyutils.tic('painter-setup')
        # Suppress viren2d warnings if we have non-contiguous or non-mutable inputs:
        # copy = True if (not image.flags.c_contiguous) or (not image.flags.writeable) else False
        # buffer = viren2d.ImageBuffer(image, copy)
        # self._painter.set_canvas_image(buffer)
        self._painter.set_canvas_image(image)
        pyutils.toc('painter-setup')

        # pyutils.tic('sanity-check')
        # Warn the user about potential typos
        for k in visualizer_args.keys():
            if k not in self._identifiers:
                logging.warning(
                    f'Visualizer "{k}" has not been registered, but its parameters '
                    'are provided - check calling code for potential typo.')
        # pyutils.toc('sanity-check')

        # Apply all configured visualizers
        for identifier, visualizer in self._visualizers:
            pyutils.tic(identifier)
            if identifier in visualizer_args:
                visualizer.apply(self._painter, visualizer_args[identifier])
            else:
                visualizer.apply(self._painter)
            pyutils.toc(identifier)

        # Return the visualization result (RGBA) as RGB image
        #res = np.array(self._painter.canvas.to_channels(3), copy=True)
        res = np.array(self._painter.canvas, copy=True)
        return res[:, :, :3]
