import pandas as pd


def read_csv_file():
    sciezka_do_pliku = (
        "C:\\Users\\gural\\tram_priority\\static\\karolkowa_oczekiwanie_5k_5_02.csv"
    )

    kolumny = ["Czas", "Wartosc", "Urzadzenie", "Stan"]

    df = pd.read_csv(sciezka_do_pliku, sep=";", names=kolumny)

    df.drop(columns="Wartosc", inplace=True)

    df["Czas"] = pd.to_datetime(df["Czas"])

    df["Czas"] = df["Czas"].dt.time

    df.sort_values(by="Czas", ascending=True, inplace=True)

    return df


read_csv_file()
