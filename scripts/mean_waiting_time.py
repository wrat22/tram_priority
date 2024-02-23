import pandas as pd
from datetime import datetime


def mean_waiting(data, detector, signal_group):
    if detector:
        mean_waiting_with_detector(data, detector, signal_group)
    else:
        mean_waiting_without_detector(data, signal_group)


def mean_waiting_with_detector(data, detector, signal_group):
    df = pd.DataFrame(data)
    registration_time, green_on_time, total_time_waiting = 0, 0, 0
    time_waiting_list = []
    waiting_for_green, green_signal = False, False

    for index, row in df.iterrows():
        if (
            row["Urzadzenie"] in detector
            and row["Stan"] == 1
            and not green_signal
            and not waiting_for_green
        ):
            waiting_for_green = True
            registration_time = row["Czas"]
        elif row["Urzadzenie"] == signal_group and row["Stan"] == 3:
            green_signal = True
            if waiting_for_green:
                green_on_time = row["Czas"]
                waiting_for_green = False
        elif row["Urzadzenie"] == signal_group and (
            row["Stan"] == 1 or row["Stan"] == 2
        ):
            green_signal = False
        (
            registration_time,
            green_on_time,
            time_waiting_list,
            total_time_waiting,
        ) = process_time_waiting(
            registration_time,
            green_on_time,
            time_waiting_list,
            total_time_waiting,
        )

    mean_time_waiting = total_time_waiting / len(
        time_waiting_list
    )
    print(time_waiting_list)
    print(
        f"Średni czas oczekiwania na sygnał zielony wynosi: {mean_time_waiting}"
    )


def mean_waiting_without_detector(data, signal_group):
    df = pd.DataFrame(data)
    registration_time, green_on_time, total_time_waiting = 0, 0, 0
    time_waiting_list = []
    waiting_for_green = False

    for index, row in df.iterrows():
        if row["Urzadzenie"] == signal_group:
            if row["Stan"] == 3 and waiting_for_green:
                green_on_time = row["Czas"]
                waiting_for_green = False
            elif row["Stan"] == 1:
                registration_time = row["Czas"]
                waiting_for_green = True
        (
            registration_time,
            green_on_time,
            time_waiting_list,
            total_time_waiting,
        ) = process_time_waiting(
            registration_time,
            green_on_time,
            time_waiting_list,
            total_time_waiting,
        )

    mean_time_waiting = total_time_waiting / len(
        time_waiting_list
    )
    print(time_waiting_list)
    print(
        f"Średni czas oczekiwania na sygnał zielony wynosi: {mean_time_waiting}"
    )


def process_time_waiting(
    registration_time,
    green_on_time,
    time_waiting_list,
    total_time_waiting,
):
    if registration_time != 0 and green_on_time != 0:
        time_distinction = (
            datetime.combine(datetime.min, green_on_time)
            - datetime.combine(datetime.min, registration_time)
        ).total_seconds()
        time_waiting_list.append(time_distinction)
        total_time_waiting += time_distinction
        registration_time, green_on_time = 0, 0
    return (
        registration_time,
        green_on_time,
        time_waiting_list,
        total_time_waiting,
    )
