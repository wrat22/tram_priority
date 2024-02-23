from priority_analysis import signal_group_analysis, det_before_cross_analysis, calculate_time_at_stop, calculate_time_arrival
from datetime import datetime

def test_valid_singal_group():
    assert signal_group_analysis(3) == [True, False, False]
    assert signal_group_analysis(1) == [False, True, False]
    assert signal_group_analysis(0) == [False, False, True]
    assert signal_group_analysis(2) == [False, False, True]


def test_valid_before_cross():
    assert det_before_cross_analysis(1, True, False, False) == True
    assert det_before_cross_analysis(1, False, True, False) == False
    assert det_before_cross_analysis(1, False, False, True) == False


def test_calculate_time_at_stop():
    time1 = datetime(2024, 2, 12, 21, 37, 11)
    time2 = datetime(2024, 2, 12, 21, 37, 36)
    assert calculate_time_at_stop(time1, time2) == 25
    time1 = datetime(2024, 2, 12, 21, 37, 1)
    time2 = datetime(2024, 2, 12, 21, 37, 36)
    assert calculate_time_at_stop(time1, time2) == 35
    
    time1 = "21:37:11"
    time2 = "21:37:36"

    time1 = datetime.strptime(time1, "%H:%M:%S")
    time2 = datetime.strptime(time2, "%H:%M:%S")
    assert calculate_time_at_stop(time1, time2) == 25


def test_calculate_time_arrival():
    time1_str = "21:37:11"
    time2_str = "21:37:36"
    time3_str = "21:37:48"

    time1 = datetime.strptime(time1_str, "%H:%M:%S")
    time2 = datetime.strptime(time2_str, "%H:%M:%S")
    time3 = datetime.strptime(time3_str, "%H:%M:%S")

    eta_time, eta_time_updated, substracted_eta_updated = calculate_time_arrival(time1, time2, time3)
    assert eta_time == 37
    assert eta_time_updated == 12
    assert substracted_eta_updated == 25
