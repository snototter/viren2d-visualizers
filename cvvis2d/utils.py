import viren2d


def compute_absolute_canvas_position(
        position: viren2d.Vec2d,
        canvas_width: int,
        canvas_height: int) -> viren2d.Vec2d:
    """
    Positions used in several visualizers can be specified by the user either
    as absolute or relative (w.r.t. the canvas size) coordinates.

    For the actual drawing, however, we need to compute the absolute
    coordinates which is performed in this utility function.
    """
    # If position is negative, we compute the position based on the
    # image/canvas dimension (i.e. going "back" from the opposite border).
    # If position is specified as a fraction of the image/canvas size,
    # we compute the absolute values.
    pos = viren2d.Vec2d(position)
    if pos[0] < 0:
        if pos[0] >= -1.0:
            pos[0] = canvas_width + pos[0] * canvas_width
        else:
            pos[0] = canvas_width + pos[0]
    elif pos[0] <= 1.0:
        pos[0] *= canvas_width

    if pos[1] < 0:
        if pos[1] >= -1.0:
            pos[1] = canvas_height + pos[1] * canvas_height
        else:
            pos[1] = canvas_height + pos[1]
    elif pos[1] <= 1.0:
        pos[1] *= canvas_height

    return pos


def compute_absolute_padding(
        padding: viren2d.Vec2d,
        width: int, height: int) -> viren2d.Vec2d:
    """
    Computes the absolute padding values if they were specified as fraction
    of the reference dimensions (width & height).

    To be used for drawing text, as this should not intersect the rounded
    corners of the enclosing text box/bounding box. This could happen if the
    corner radius is specified as fraction of the box size, but the padding
    would be absolute (and the box size would be rather large...)
    """
    pad = viren2d.Vec2d(padding)
    if pad[0] <= 1.0:
        pad[0] *= width

    if pad[1] <= 1.0:
        pad[1] *= height

    return pad
