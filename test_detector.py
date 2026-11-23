import numpy as np

import detector as det

def test_ab_diff():
    ar_1 = np.zeros((4,4), dtype=np.uint8)
    ar_2 = np.zeros((4,4), dtype=np.uint8)
    ans_ar = np.zeros((4,4), dtype=np.uint8)

    ar_1[2, 1] = 10
    ar_2[2, 1] = 12
    ans_ar[2,1] = 2
    calc_arr = det.ab_diff(ar_1, ar_2)
    
    assert np.array_equal(ans_ar, calc_arr)

def test_moving_true():
    pixel_thrs = 2
    count_thrs = 3
    difference = np.zeros((4,4))
    difference[0] = 3
    assert det.is_moving(difference, pixel_thrs, count_thrs)

def test_not_moving():
    pixel_thrs = 2
    count_thrs = 3
    difference = np.zeros((4,4))
    difference[0] = 1
    assert not det.is_moving(difference, pixel_thrs, count_thrs) 
 
def test_pixel_at_threshold_does_not_count():
    pixel_thrs = 3
    count_thrs = 2
    difference = np.zeros((4,4))
    difference[0] = 3
    assert not det.is_moving(difference, pixel_thrs, count_thrs) 

def test_count_at_threshold_does_not_count():
    pixel_thrs = 2
    count_thrs = 4
    difference = np.zeros((4,4))
    difference[0] = 3
    assert not det.is_moving(difference, pixel_thrs, count_thrs) 