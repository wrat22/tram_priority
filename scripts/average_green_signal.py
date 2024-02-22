import pandas as pd
from datetime import datetime


def mean_green(data, signal_group):
    df = pd.DataFrame(data)
    czas_zoltego, czas_zielonego = 0, 0
    green_light = False
    time_waiting_list = []

    for index, row in df.iterrows():
        if row["Urzadzenie"] == signal_group:
            if row["Stan"] == 3:
                czas_zielonego = row["Czas"]
                green_light = True
            elif row["Stan"] == 0 and green_light == True:
                czas_zoltego = row["Czas"]
                green_light = False
        if czas_zielonego != 0 and czas_zoltego != 0:
            roznica = (
                datetime.combine(datetime.min, czas_zoltego)
                - datetime.combine(datetime.min, czas_zielonego)
            ).total_seconds()
            time_waiting_list.append(roznica)
            czas_zielonego, czas_zoltego = 0, 0

    print(time_waiting_list)
    average_time_waiting = round(sum(time_waiting_list) / len(time_waiting_list), 0)
    print(f"Średnia długość sygnału zielonego wynosi: {average_time_waiting}")
