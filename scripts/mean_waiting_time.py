import pandas as pd
from datetime import timedelta, datetime


def mean_waiting(data, detector, signal_group):
    if detector:
        mean_waiting_with_detector(data, detector, signal_group)
    else:
        mean_waiting_without_detector(data, signal_group)


def mean_waiting_with_detector(data, detector, signal_group):
    df = pd.DataFrame(data)
    czas_zgloszenia, czas_wzbudzenia, sumaryczny_czas_oczekiwania = 0, 0, 0
    lista_czasow_oczekiwania = []
    oczekiwanie_na_zielony, sygnal_zielony = False, False

    for index, row in df.iterrows():
        if (
            row["Urzadzenie"] in detector
            and row["Stan"] == 1
            and not sygnal_zielony
            and not oczekiwanie_na_zielony
        ):
            oczekiwanie_na_zielony = True
            czas_zgloszenia = row["Czas"]
        elif row["Urzadzenie"] == signal_group and row["Stan"] == 3:
            sygnal_zielony = True
            if oczekiwanie_na_zielony:
                czas_wzbudzenia = row["Czas"]
                oczekiwanie_na_zielony = False
        elif row["Urzadzenie"] == signal_group and (
            row["Stan"] == 1 or row["Stan"] == 2
        ):
            sygnal_zielony = False
        (
            czas_zgloszenia,
            czas_wzbudzenia,
            lista_czasow_oczekiwania,
            sumaryczny_czas_oczekiwania,
        ) = process_time_waiting(
            czas_zgloszenia,
            czas_wzbudzenia,
            lista_czasow_oczekiwania,
            sumaryczny_czas_oczekiwania,
        )

    sredni_czas_oczekiwania = sumaryczny_czas_oczekiwania / len(
        lista_czasow_oczekiwania
    )
    print(lista_czasow_oczekiwania)
    print(
        f"Średni czas oczekiwania na sygnał zielony wynosi: {sredni_czas_oczekiwania}"
    )


def mean_waiting_without_detector(data, signal_group):
    df = pd.DataFrame(data)
    czas_zgloszenia, czas_wzbudzenia, sumaryczny_czas_oczekiwania = 0, 0, 0
    lista_czasow_oczekiwania = []
    oczekiwanie_na_zielony = False

    for index, row in df.iterrows():
        if row["Urzadzenie"] == signal_group:
            if row["Stan"] == 3 and oczekiwanie_na_zielony:
                czas_wzbudzenia = row["Czas"]
                oczekiwanie_na_zielony = False
            elif row["Stan"] == 1:
                czas_zgloszenia = row["Czas"]
                oczekiwanie_na_zielony = True
        (
            czas_zgloszenia,
            czas_wzbudzenia,
            lista_czasow_oczekiwania,
            sumaryczny_czas_oczekiwania,
        ) = process_time_waiting(
            czas_zgloszenia,
            czas_wzbudzenia,
            lista_czasow_oczekiwania,
            sumaryczny_czas_oczekiwania,
        )

    sredni_czas_oczekiwania = sumaryczny_czas_oczekiwania / len(
        lista_czasow_oczekiwania
    )
    print(lista_czasow_oczekiwania)
    print(
        f"Średni czas oczekiwania na sygnał zielony wynosi: {sredni_czas_oczekiwania}"
    )


def process_time_waiting(
    czas_zgloszenia,
    czas_wzbudzenia,
    lista_czasow_oczekiwania,
    sumaryczny_czas_oczekiwania,
):
    if czas_zgloszenia != 0 and czas_wzbudzenia != 0:
        roznica = (
            datetime.combine(datetime.min, czas_wzbudzenia)
            - datetime.combine(datetime.min, czas_zgloszenia)
        ).total_seconds()
        lista_czasow_oczekiwania.append(roznica)
        sumaryczny_czas_oczekiwania += roznica
        czas_zgloszenia, czas_wzbudzenia = 0, 0
    return (
        czas_zgloszenia,
        czas_wzbudzenia,
        lista_czasow_oczekiwania,
        sumaryczny_czas_oczekiwania,
    )
