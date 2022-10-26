import cv2
import apriltag
import numpy as np
import datetime
import cvvis2d
import viren2d
from typing import List


def _tag_vis_parameter(detector, detector_opts, tag_detections):
    """
    Converts the AprilTag detections to the parameter list needed by the
    TagPoseOverlay visualizer.
    """
    tags = list()
    for detection in tag_detections:
        pose, initial_reprj_err, final_reprj_err = detector.detection_pose(
            detection, detector_opts.camera_params, detector_opts.tag_size)
        R, t = pose[:3, :3], pose[:3, 3]
        # I prefer the tag's z-axis pointing up, thus rotate 180° around
        # the x axis:
        R = np.matmul(R, np.array([
            [1.0,  0.0,  0.0],
            [0.0, -1.0,  0.0],
            [0.0,  0.0, -1.0]], dtype=np.float64))
        tags.append(
            (R, t, f'Tag #{detection.tag_id}, reprj.err: {final_reprj_err:.2f}'))
    return tags


def demo_apriltags_webcam():
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
    

    # AprilTag parameters
    tag_family = 'tag36h11'
    tag_size_mm = 400 # INNER SIZE, i.e. size of the 8x8 (black) square (not the 10x10)!
    tag_refine_edges = True
    tag_refine_decode = True
    tag_refine_pose = True
    tag_quad_decimate = 1.0
    tag_quad_contours = True
    

    # Set up visualization pipeline
    visualizer = cvvis2d.VisualizationPipeline()

    overlay = cvvis2d.StaticTextOverlay()
    overlay.text = 'AprilTag Demo'
    overlay.text_style.size = 24
    visualizer.add('static-text', overlay)

    overlay = cvvis2d.TagPoseOverlay()
    overlay.text_style.size = 24
    overlay.text_padding = (10, 10)
    overlay.arrow_lengths = 3 * (tag_size_mm, )
    visualizer.add('tags', overlay)

    
    tag_detector = None
    while True:
        frame = next_image()
        if frame is None:
            break

        # Set up AprilTag detector upon receiving the first frame
        if tag_detector is None:
            # Set up dummy intrinsics
            height, width = frame.shape[:2]
            fl = width
            K = np.array(
                [[fl, 0, width / 2], [0, fl, height / 2], [0, 0, 1]],
                dtype=np.float64)
            detector_opts = apriltag.DetectorOptions(
                families=tag_family, refine_edges=tag_refine_edges,
                refine_decode=tag_refine_decode, refine_pose=tag_refine_pose,
                debug=False, quad_decimate=tag_quad_decimate,
                quad_contours=tag_quad_contours)
            detector_opts.camera_params = (K[0,0], K[1,1], K[0,2], K[1,2])
            detector_opts.tag_size = tag_size_mm

            tag_detector = apriltag.Detector(detector_opts)

        # Detect tags
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        tag_detections = tag_detector.detect(gray, False)

        # Convert tag detections to visualization parameters
        tag_params = (K, _tag_vis_parameter(
            tag_detector, detector_opts, tag_detections))
        # Convert from OpenCV BGR to RGB (used by viren2d)
        rgb = frame[:, :, ::-1]
        # Apply the visualization pipeline
        vis = visualizer.visualize(rgb, {'tags': tag_params})
        # Convert back to BGR for display
        vis = vis[:, :, ::-1]

        cv2.imshow('Image', vis)
        k = cv2.waitKey(10) & 0xff
        if (k == 27) or (k == ord('q')):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    demo_apriltags_webcam()

