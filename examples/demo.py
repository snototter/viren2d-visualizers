import cv2
import numpy as np
import datetime
import cvvis2d
import viren2d
from vito import pyutils
from typing import List


def _gradient_magnitude(img: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gx = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=3)
    gy = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=3)
    mag = cv2.convertScaleAbs(np.sqrt(gx**2 + gy**2))
    return cv2.merge((mag, mag, mag, 255*np.ones(mag.shape[:2], dtype=np.uint8)))
    # return mag


def _bounding_boxes(img: np.ndarray) -> List[cvvis2d.BoundingBox2d]:
    height, width = img.shape[:2]
    # Randomly sample n boxes
    n = 10
    boxes = np.random.rand(n, 6)
    boxes[:, 0] = np.floor(boxes[:, 0] * 10)
    boxes[:, 1] *= (width * 0.6)
    boxes[:, 2] *= (height * 0.6)
    boxes[:, 3] *= (width / 2)
    boxes[:, 4] *= (height / 2)
    # boxes[:, 3] = 80
    # boxes[:, 4] = 120

    def _class_name(class_id):
        cn = viren2d.Color.object_category_names()
        return cn[int(class_id) % len(cn)]

    return [
        cvvis2d.create_bounding_box(
            _class_name(boxes[i, 0]), *boxes[i, 1:])
        for i in range(boxes.shape[0])]


def demo_webcam_visualizer():
    try:
        cam = cv2.VideoCapture(0)

        if not cam.isOpened():
            raise IOError('Cannot open webcam')
            
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        def next_image():
            retval, frame = cam.read()
            if retval:
                return frame
            else:
                return None
    except IOError:
        print('Cannot open webcam - using dummy image instead')
        def next_image():
            img = np.zeros((1080, 1920, 3), dtype=np.uint8)
            img[:, :, 0] = 180
            return img

    visualizer = cvvis2d.VisualizationPipeline()
    overlay = cvvis2d.text.DynamicTextOverlay()
    visualizer.add('frame-label', overlay)

    overlay = cvvis2d.StaticTextOverlay()
    overlay.text = 'Pipeline Demo'
    visualizer.add('static-text', overlay)

    overlay = cvvis2d.BoundingBox2dOverlay()
    visualizer.add('bbox2d', overlay)

    overlay = cvvis2d.ImageOverlay()
    overlay.scale = (0.3, 0.3)
    overlay.alpha = 1
    visualizer.add('gradient-overlay', overlay)
    
    num_frames = 0
    bbox2d = None
    while True:
        frame = next_image()
        if frame is None:
            break

        # Convert from OpenCV BGR to RGB (used by viren2d)
        rgb = frame[:, :, ::-1]
        # TODO remove
        #     pyutils.tic('np-copy-buffer')
        #     rgb = frame[:, :, ::-1].copy()
        #     # rgb = cv2.merge((frame[:,:,2], frame[:,:,1], frame[:,:,0], 255*np.ones(frame.shape[:2], dtype=np.uint8)))
        #     pyutils.toc('np-copy-buffer')


        # Prepare parameters for the configured visualizers
        text = cvvis2d.frame_label('Webcam', num_frames, datetime.datetime.now())
        mag = _gradient_magnitude(frame)
        if bbox2d is None:
            bbox2d = _bounding_boxes(frame)

        # Apply the visualization pipeline
        print()
        pyutils.tic('visualization')
        vis = visualizer.visualize(
            rgb, {'frame-label': text, 'gradient-overlay': mag, 'bbox2d': bbox2d})
        pyutils.toc('visualization')
        # Convert back to BGR for display
        vis = vis[:, :, ::-1]

        cv2.imshow('Image', vis)
        k = cv2.waitKey(10) & 0xff
        if (k == 27) or (k == ord('q')):
            break
        num_frames += 1
    cv2.destroyAllWindows()


if __name__ == '__main__':
    demo_webcam_visualizer()

