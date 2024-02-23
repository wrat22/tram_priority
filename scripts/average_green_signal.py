import pandas as pd
from datetime import datetime


def mean_green(data, signal_group):
    df = pd.DataFrame(data)
    amber_time, green_time = 0, 0
    green_signal = False
    time_waiting_list = []

    for index, row in df.iterrows():
        if row["Urzadzenie"] == signal_group:
            if row["Stan"] == 3:
                green_time = row["Czas"]
                green_signal = True
            elif row["Stan"] == 0 and green_signal == True:
                amber_time = row["Czas"]
                green_signal = False
        if green_time != 0 and amber_time != 0:
            time_distinction = (
                datetime.combine(datetime.min, amber_time)
                - datetime.combine(datetime.min, green_time)
            ).total_seconds()
            time_waiting_list.append(time_distinction)
            green_time, amber_time = 0, 0

    print(time_waiting_list)
    average_time_waiting = round(sum(time_waiting_list) / len(time_waiting_list), 0)
    print(f"Średnia długość sygnału zielonego wynosi: {average_time_waiting}")
