import pandas as pd
from datetime import timedelta, datetime


def signal_group_analysis(stan):
    if stan == 3:
        return [True, False, False]
    if stan == 1:
        return [False, True, False]
    if stan == 0 or stan == 2:
        return [False, False, True]


def det_before_cross_analysis(
    stan, sygnal_zezwalajacy, sygnal_zabraniajacy, sygnal_kocie
):
    if stan == 1:
        if sygnal_zabraniajacy or sygnal_kocie:
            return False
        elif sygnal_zezwalajacy:
            return True


def priority_analysis_2(data, singal_group, det_before_cross, det_logout):
    # data = data.head(50)
    df = pd.DataFrame(data)

    licznik_bez_priorytetu, licznik_z_priorytetem = 0, 0
    licznik_tramwajow_przed_skrzyzowaniem = 0
    tramwaj_przed_skrzyzowaniem = False

    for _, row in df.iterrows():
        if row["Urzadzenie"] == singal_group:
            (
                sygnal_zezwalajacy,
                sygnal_zabraniajacy,
                sygnal_kocie,
            ) = signal_group_analysis(row["Stan"])
        elif row["Urzadzenie"] == det_before_cross and row["Stan"] == 1:
            licznik_tramwajow_przed_skrzyzowaniem += 1
            tramwaj_przed_skrzyzowaniem = True
        if sygnal_zabraniajacy or sygnal_kocie:
            if (
                tramwaj_przed_skrzyzowaniem
                and licznik_tramwajow_przed_skrzyzowaniem > 0
            ):
                licznik_bez_priorytetu += 1
                licznik_tramwajow_przed_skrzyzowaniem -= 1
        elif (
            sygnal_zezwalajacy
            and tramwaj_przed_skrzyzowaniem
            and licznik_tramwajow_przed_skrzyzowaniem > 0
        ):
            licznik_z_priorytetem += 1
            licznik_tramwajow_przed_skrzyzowaniem -= 1

    print(f"Tramwaje bez priorytetu: {licznik_bez_priorytetu}")
    print(f"Tramwaje z priorytetem: {licznik_z_priorytetem}")


def priority_analysis_with_stop(data, singal_group, det_before_cross, det_logout):
    df = pd.DataFrame(data)

    TIME_FOR_STOP = 30
    time1, time2 = 0, 0
    licznik_bez_priorytetu, licznik_z_priorytetem = 0, 0

    for _, row in df.iterrows():
        if row["Urzadzenie"] == det_before_cross and row["Stan"] == 1:
            time1 = row["Czas"]
        elif row["Urzadzenie"] == det_logout and row["Stan"] == 1:
            time2 = row["Czas"]
        if time1 != 0 and time2 != 0:
            time_at_stop = calculate_time_at_stop(time1, time2)
            if time_at_stop > TIME_FOR_STOP:
                licznik_bez_priorytetu += 1
            else:
                licznik_z_priorytetem += 1
            time1, time2 = 0, 0

    print(f"Tramwaje bez priorytetu: {licznik_bez_priorytetu}")
    print(f"Tramwaje z priorytetem: {licznik_z_priorytetem}")


def calculate_time_at_stop(time1, time2):
    delta_czasu = timedelta(
        hours=time2.hour, minutes=time2.minute, seconds=time2.second
    ) - timedelta(hours=time1.hour, minutes=time1.minute, seconds=time1.second)
    nowy_czas = (timedelta() + delta_czasu).total_seconds()
    return nowy_czas


def time_arrival_analysis(data, det_login, det_update, det_before_cross):
    if det_update:
        time_arrival_with_update(data, det_login, det_update, det_before_cross)
    else:
        time_arrival_without_update(data, det_login, det_before_cross)


def time_arrival_with_update(data, det_login, det_update, det_before_cross):
    df = pd.DataFrame(data)
    czas1_1, czas1_2, czas1_3, czas2_1, czas2_2, czas2_3 = 0, 0, 0, 0, 0, 0
    time_arrival = {}

    for _, row in df.iterrows():
        if row["Urzadzenie"] == det_login and row["Stan"] == 1:
            if czas1_1 == 0:
                czas1_1 = datetime.strptime(row["Czas"], "%H:%M:%S")
            elif czas2_1 == 0:
                czas2_1 = datetime.strptime(row["Czas"], "%H:%M:%S")
        elif row["Urzadzenie"] == det_update and row["Stan"] == 1:
            if czas1_2 == 0 and czas1_1 != 0:
                czas1_2 = datetime.strptime(row["Czas"], "%H:%M:%S")
            elif czas2_2 == 0 and czas2_1 != 0:
                czas2_2 = datetime.strptime(row["Czas"], "%H:%M:%S")
        elif row["Urzadzenie"] == det_before_cross and row["Stan"] == 1:
            if czas1_3 == 0 and czas1_2 != 0 and czas1_1 != 0:
                czas1_3 = datetime.strptime(row["Czas"], "%H:%M:%S")
            elif czas2_3 == 0 and czas2_2 != 0 and czas2_1 != 0:
                czas2_3 = datetime.strptime(row["Czas"], "%H:%M:%S")
        if czas1_1 != 0 and czas1_2 != 0 and czas1_3 != 0:
            (
                czas_dojazdu,
                zaktualizowany_czas_dojazdu,
                roznica_td_tdupdate,
            ) = calculate_time_arrival(czas1_1, czas1_2, czas1_3)
            time_arrival["Czas dojazdu"].append(czas_dojazdu)
            time_arrival["Zaktualizowany czas dojazdu"].append(
                zaktualizowany_czas_dojazdu
            )
            time_arrival["Różnica TD - TDupdate"].append(roznica_td_tdupdate)
            czas1_1, czas1_2, czas1_3 = 0, 0, 0
        elif czas2_1 != 0 and czas2_2 != 0 and czas2_3 != 0:
            (
                czas_dojazdu,
                zaktualizowany_czas_dojazdu,
                roznica_td_tdupdate,
            ) = calculate_time_arrival(czas2_1, czas2_2, czas2_3)
            time_arrival["Czas dojazdu"].append(czas_dojazdu)
            time_arrival["Zaktualizowany czas dojazdu"].append(
                zaktualizowany_czas_dojazdu
            )
            time_arrival["Różnica TD - TDupdate"].append(roznica_td_tdupdate)
            czas2_1, czas2_2, czas2_3 = 0, 0, 0

    print(time_arrival)


def calculate_time_arrival(time1, time2, time3):
    eta_time = (time3 - time1).total_seconds()
    eta_time_updated = (time3 - time2).total_seconds()
    substracted_eta_updated = (time2 - time1).total_seconds()

    return eta_time, eta_time_updated, substracted_eta_updated


def time_arrival_without_update(data, det_login, det_before_cross):
    df = pd.DataFrame(data)
    czas1_1, czas1_2, czas2_1, czas2_2 = 0, 0, 0, 0
    time_arrival = []

    for _, row in df.iterrows():
        if row["Urzadzenie"] == det_login and row["Stan"] == 1:
            if czas1_1 == 0:
                czas1_1 = datetime.strptime(row["Czas"], "%H:%M:%S")
            elif czas2_1 == 0:
                czas2_1 = datetime.strptime(row["Czas"], "%H:%M:%S")
        elif row["Urzadzenie"] == det_before_cross and row["Stan"] == 1:
            if czas1_2 == 0 and czas1_1 != 0:
                czas1_2 = datetime.strptime(row["Czas"], "%H:%M:%S")
            elif czas2_2 == 0 and czas2_1 != 0:
                czas2_2 = datetime.strptime(row["Czas"], "%H:%M:%S")
        if czas1_1 != 0 and czas1_2 != 0:
            time_arrival.append(calculate_time_arrival_without_update(czas1_1, czas1_2))
            czas1_1, czas1_2 = 0, 0
        elif czas2_1 != 0 and czas2_2 != 0:
            time_arrival.append(calculate_time_arrival_without_update(czas2_1, czas2_2))
            czas2_1, czas2_2 = 0, 0

    print(time_arrival)


def calculate_time_arrival_without_update(time1, time2):
    eta_time = (time2 - time1).total_seconds()
    return eta_time


if __name__ == "__main__":
    main()
