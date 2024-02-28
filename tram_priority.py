from scripts.menu import (
    get_option,
    validate_tram_priority,
    validate_time_arrival,
    validate_sip_effectiveness,
    validate_mean_time_waiting,
)
from scripts.read_csv_file import read_csv_file
from scripts.priority_analysis import (
    priority_analysis_with_stop,
    priority_analysis,
)
from scripts.time_arrival import time_arrival_analysis
from scripts.sip_effectiveness_analysis import sip_effectiveness
from scripts.mean_waiting_time import mean_waiting
from scripts.average_green_signal import mean_green
import sys

sys.path.insert(0, "C:/Users/gural/tram_priority/modules")


def main():
    option = get_option()
    if option == "1":
        priority_research()
    elif option == "2":
        time_arrival()
    elif option == "3":
        sip_research()
    elif option == "4":
        analyse_mean_time_waiting()
    elif option == "5":
        analyse_average_green()


def priority_research():
    data = read_csv_file()
    signal_group, det_before_cross, det_logout, tram_stop = validate_tram_priority()
    if tram_stop:
        priority_analysis_with_stop(data, signal_group, det_before_cross, det_logout)
    else:
        priority_analysis(data, signal_group, det_before_cross)


def time_arrival():
    data = read_csv_file()
    det_login, det_update, det_before_cross = validate_time_arrival()
    time_arrival_analysis(data, det_login, det_update, det_before_cross)


def sip_research():
    data = read_csv_file()
    sip_det, det_before_cross = validate_sip_effectiveness()
    sip_effectiveness(data, sip_det, det_before_cross)


def analyse_mean_time_waiting():
    data = read_csv_file()
    signal_group, detector = validate_mean_time_waiting()
    mean_waiting(data, detector, signal_group)


def analyse_average_green():
    data = read_csv_file()
    signal_group = input("Jak nazywa się badana grupa sygnałowa? ").upper()
    mean_green(data, signal_group)


if __name__ == "__main__":
    main()
