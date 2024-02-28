import pandas as pd
from datetime import timedelta, datetime


def signal_group_analysis(state):
    if state == 3:
        return [True, False, False]
    elif state == 1:
        return [False, True, False]
    else:
        return [False, False, True]


def det_before_cross_analysis(state, green_signal, red_signal, amber_signal):
    if state == 1:
        if red_signal or amber_signal:
            return False
        elif green_signal:
            return True


def priority_analysis(data, singal_group, det_before_cross):
    df = pd.DataFrame(data)

    count_priority, count_no_priority, count_trams_before_cross = 0, 0, 0
    green_signal, red_signal, amber_signal = False, False, False
    no_priority_list = []

    for _, row in df.iterrows():
        if row["Urzadzenie"] == singal_group:
            (
                green_signal,
                red_signal,
                amber_signal,
            ) = signal_group_analysis(row["Stan"])
        elif row["Urzadzenie"] == det_before_cross and row["Stan"] == 1:
            count_trams_before_cross += 1
            trams_before_cross = True
        if red_signal or amber_signal:
            if trams_before_cross and count_trams_before_cross > 0:
                count_priority += 1
                count_trams_before_cross -= 1
        elif green_signal and trams_before_cross and count_trams_before_cross > 0:
            count_no_priority += 1
            count_trams_before_cross -= 1

    print(f"Tramwaje bez priorytetu: {count_priority}")
    print(f"Tramwaje z priorytetem: {count_no_priority}")


def priority_analysis_with_stop(data, singal_group, det_before_cross, det_logout):
    df = pd.DataFrame(data)

    TIME_FOR_STOP = 30
    login_time, logout_time = 0, 0
    count_priority, count_no_priority = 0, 0

    for _, row in df.iterrows():
        if row["Urzadzenie"] == det_before_cross and row["Stan"] == 1:
            login_time = row["Czas"]
        elif row["Urzadzenie"] == det_logout and row["Stan"] == 1:
            logout_time = row["Czas"]
        if login_time != 0 and logout_time != 0:
            time_at_stop = calculate_time_at_stop(login_time, logout_time)
            if time_at_stop > TIME_FOR_STOP:
                count_priority += 1
            else:
                count_no_priority += 1
            login_time, logout_time = 0, 0

    print(f"Tramwaje bez priorytetu: {count_priority}")
    print(f"Tramwaje z priorytetem: {count_no_priority}")


def calculate_time_at_stop(time1, time2):
    helper_time = timedelta(
        hours=time2.hour, minutes=time2.minute, seconds=time2.second
    ) - timedelta(hours=time1.hour, minutes=time1.minute, seconds=time1.second)
    calculated_time = (timedelta() + helper_time).total_seconds()
    return calculated_time
