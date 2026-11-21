import numpy as np

def is_moving(difference, pixel_thrs, count_thrs):
    return (difference > pixel_thrs).sum() > count_thrs

def ab_diff(frame_1, frame_2):
    return np.maximum(frame_1, frame_2) - np.minimum(frame_1, frame_2)