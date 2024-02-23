import pandas as pd

def sip_effectiveness(data, sip_det, det_before_cross):
    df = pd.DataFrame(data)

    undetected_list = []
    count_trams_before_cross, count_sip_detected, count_sip_undetected = 0, 0, 0

    for index, row in df.iterrows():
        if row["Urzadzenie"] == sip_det and row["Stan"] == 1:
            count_trams_before_cross += 1
            print(row["Czas"], count_trams_before_cross)
        elif row["Urzadzenie"] == det_before_cross and row["Stan"] == 1:
            if count_trams_before_cross > 0:
                count_sip_detected += 1
                count_trams_before_cross -= 1
            else:
                count_sip_undetected += 1
                undetected_list.append(row["Czas"])
    

    print(f"Liczba wykrytych: {count_sip_detected}")
    print(f"Liczba niewykrytych: {count_sip_undetected}")
    print(undetected_list)