import pandas as pd

def sip_effectiveness(data, sip_det, det_before_cross):
    df = pd.DataFrame(data)

    lista_niewykrytych = []
    licznik_tramwajow_przed_skrzyzowaniem, licznik_wykrytych_przez_sip, licznik_ominietych_przez_sip = 0, 0, 0

    for index, row in df.iterrows():
        if row["Urzadzenie"] == sip_det and row["Stan"] == 1:
            licznik_tramwajow_przed_skrzyzowaniem += 1
            print(row["Czas"], licznik_tramwajow_przed_skrzyzowaniem)
        elif row["Urzadzenie"] == det_before_cross and row["Stan"] == 1:
            if licznik_tramwajow_przed_skrzyzowaniem > 0:
                licznik_wykrytych_przez_sip += 1
                licznik_tramwajow_przed_skrzyzowaniem -= 1
            else:
                licznik_ominietych_przez_sip += 1
                lista_niewykrytych.append(row["Czas"])
    

    print(f"Liczba wykrytych: {licznik_wykrytych_przez_sip}")
    print(f"Liczba niewykrytych: {licznik_ominietych_przez_sip}")
    print(lista_niewykrytych)