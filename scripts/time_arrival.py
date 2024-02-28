import pandas as pd
from datetime import datetime


def time_arrival_analysis(data, det_login, det_update, det_before_cross):
    if det_update:
        time_arrival_with_update(data, det_login, det_update, det_before_cross)
    else:
        time_arrival_without_update(data, det_login, det_before_cross)


def time_arrival_with_update(data, det_login, det_update, det_before_cross):
    df = pd.DataFrame(data)
    time1_1, time1_2, time1_3, time2_1, time2_2, time2_3 = 0, 0, 0, 0, 0, 0
    time_arrival_dict = {
        "Czas dojazdu": [],
        "Zaktualizowany czas dojazdu": [],
        "Różnica TD - TDupdate": []
    }

    for _, row in df.iterrows():
        if row["Urzadzenie"] == det_login and row["Stan"] == 1:
            if time1_1 == 0:
                time1_1 = datetime.strptime(row["Czas"], "%H:%M:%S")
            elif time2_1 == 0:
                time2_1 = datetime.strptime(row["Czas"], "%H:%M:%S")
        elif row["Urzadzenie"] == det_update and row["Stan"] == 1:
            if time1_2 == 0 and time1_1 != 0:
                time1_2 = datetime.strptime(row["Czas"], "%H:%M:%S")
            elif time2_2 == 0 and time2_1 != 0:
                time2_2 = datetime.strptime(row["Czas"], "%H:%M:%S")
        elif row["Urzadzenie"] == det_before_cross and row["Stan"] == 1:
            if time1_3 == 0 and time1_2 != 0 and time1_1 != 0:
                time1_3 = datetime.strptime(row["Czas"], "%H:%M:%S")
            elif time2_3 == 0 and time2_2 != 0 and time2_1 != 0:
                time2_3 = datetime.strptime(row["Czas"], "%H:%M:%S")
        if time1_1 != 0 and time1_2 != 0 and time1_3 != 0:
            (
                eta,
                updated_eta,
                subtracted_eta,
            ) = calculate_time_arrival(time1_1, time1_2, time1_3)
            time_arrival_dict["Czas dojazdu"].append(eta)
            time_arrival_dict["Zaktualizowany czas dojazdu"].append(updated_eta)
            time_arrival_dict["Różnica TD - TDupdate"].append(subtracted_eta)
            time1_1, time1_2, time1_3 = 0, 0, 0
        elif time2_1 != 0 and time2_2 != 0 and time2_3 != 0:
            (
                eta,
                updated_eta,
                subtracted_eta,
            ) = calculate_time_arrival(time2_1, time2_2, time2_3)
            time_arrival_dict["Czas dojazdu"].append(eta)
            time_arrival_dict["Zaktualizowany czas dojazdu"].append(updated_eta)
            time_arrival_dict["Różnica TD - TDupdate"].append(subtracted_eta)
            time2_1, time2_2, time2_3 = 0, 0, 0

    print(time_arrival_dict)


def calculate_time_arrival(time1, time2, time3):
    eta = (time3 - time1).total_seconds()
    eta_updated = (time3 - time2).total_seconds()
    eta_subtracted = (time2 - time1).total_seconds()

    return eta, eta_updated, eta_subtracted


def time_arrival_without_update(data, det_login, det_before_cross):
    df = pd.DataFrame(data)
    time1_1, time1_2, time2_1, time2_2 = 0, 0, 0, 0
    time_arrival_list = []

    for _, row in df.iterrows():
        if row["Urzadzenie"] == det_login and row["Stan"] == 1:
            if time1_1 == 0:
                time1_1 = datetime.strptime(row["Czas"], "%H:%M:%S")
            elif time2_1 == 0:
                time2_1 = datetime.strptime(row["Czas"], "%H:%M:%S")
        elif row["Urzadzenie"] == det_before_cross and row["Stan"] == 1:
            if time1_2 == 0 and time1_1 != 0:
                time1_2 = datetime.strptime(row["Czas"], "%H:%M:%S")
            elif time2_2 == 0 and time2_1 != 0:
                time2_2 = datetime.strptime(row["Czas"], "%H:%M:%S")
        if time1_1 != 0 and time1_2 != 0:
            time_arrival_list.append(calculate_time_arrival_no_update(time1_1, time1_2))
            time1_1, time1_2 = 0, 0
        elif time2_1 != 0 and time2_2 != 0:
            time_arrival_list.append(calculate_time_arrival_no_update(time2_1, time2_2))
            time2_1, time2_2 = 0, 0

    print(time_arrival_list)


def calculate_time_arrival_no_update(time1, time2):
    eta_time = (time2 - time1).total_seconds()
    return eta_time
