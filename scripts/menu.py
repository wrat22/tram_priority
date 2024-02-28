<<<<<<< HEAD
def get_option():
    options = [
        "1. Sprawdź priorytet dla tramwaju",
        "2. Sprawdź czas dojazdu tramwaju",
        "3. Sprawdź skuteczność działania SIP",
        "4. Zbadaj średni czas oczekiwania",
        "5. Sprawdź średnią długość sygnału zielonego",
    ]
    for option in options:
        print(option)
    return validate_option(options)


def validate_option(options):
    NUMBER_OF_TRIES = 5
    for _ in range(NUMBER_OF_TRIES):
        opcja = input("Którą opcję wybierasz? ")
        if opcja == "1":
            return opcja
        elif opcja == "2":
            return opcja
        elif opcja == "3":
            return opcja
        elif opcja == "4":
            return opcja
        elif opcja == "5":
            return opcja
        else:
            print(
                f"Niepoprawna odpowiedź, proszę wprowadzić liczbę z zakresu [1-{len(options)}]"
            )


def validate_tram_priority():
    print("Podaj informacje dla kierunku jazdy")
    singal_group = input("Jak nazywa się grupa sygnałowa? ").upper()
    det_before_cross = input(
        "Jak nazywa się detektor przed skrzyżowaniem? "
    ).upper()
    det_logout = input(
        "Jak nazywa się detektor za skrzyżowaniem / do wylogowania? "
    ).upper()
    tram_stop = validate_tram_stop()
    return singal_group, det_before_cross, det_logout, tram_stop


def validate_tram_stop():
    NUMBER_OF_TRIES = 5
    for _ in range(NUMBER_OF_TRIES):
        stop = input("Czy przystanek jest przed skrzyżowaniem?(T/N) ").upper()
        if stop in ["T", "TAK"]:
            return True
        elif stop in ["N", "NIE"]:
            return False
        else:
            print("Niepoprawna odpowiedź, proszę wprowadzić 'T' lub 'N'")


def validate_time_arrival():
    print("Podaj informacje dla badanego kierunku")
    det_login = input("Jak nazywa się detektor do logowania? ").upper()
    det_update = validate_update_detector()
    det_before_cross = input(
        "Jak nazywa się detektor przed skrzyżowaniem? "
    ).upper()
    return det_login, det_update, det_before_cross


def validate_update_detector():
    for _ in range(5):
        update = input("Czy wykorzystujemy aktualizację?(T/N) ").upper()
        if update in ["T", "TAK"]:
            det_update = input(
                "Jak nazywa się detektor do aktualizacji logowania? "
            ).upper()
            return det_update
        elif update in ["N", "NIE"]:
            det_update = None
            return det_update
        else:
            print("Niepoprawna odpowiedź, proszę wprowadzić 'T' lub 'N'.")


def validate_sip_effectiveness():
    print("Podaj informacje dla badanego detektora SIP")
    det_sip = input("Jak nazywa się detektor SIP? ").upper()
    det_before_cross = input(
        "Jak nazywa się detektor przed skrzyżowaniem? "
    ).upper()
    return det_sip, det_before_cross


def validate_mean_time_waiting():
    print("Podaj informacje dla badanej grupy kierunkowej")
    singal_group = input("Jak nazywa się grupa sygnałowa? ").upper()
    detector = validate_detector_for_time_waiting()
    return singal_group, detector


def validate_detector_for_time_waiting():
    for _ in range(5):
        update = input("Czy wykorzystujemy detektor?(T/N) ").upper()
        if update in ["T", "TAK"]:
            liczba_detektorow = int(input("Ile detektorów używamy? "))
            lista_detektorow = []
            if liczba_detektorow > 1:
                for _ in range(liczba_detektorow):
                    detector = input("Jak nazywa się detektor do badania zajętości? "
                ).upper()
                    lista_detektorow.append(detector)
                return lista_detektorow
            elif liczba_detektorow == 1:
                det_update = input(
                    "Jak nazywa się detektor do badania zajętości? "
                ).upper()
                return det_update
        elif update in ["N", "NIE"]:
            return None
        else:
            print("Niepoprawna odpowiedź, proszę wprowadzić 'T' lub 'N'.")

def menu():
    print("Podaj informacje dla kierunku jazdy")
    singal_group = input("Jak nazywa się grupa sygnałowa? ")
    det_before_cross = input("Jak nazywa się detektor przed skrzyżowaniem? ")
    det_logout = input("Jak nazywa się detektor za skrzyżowaniem / do wylogowania? ")
    return singal_group, det_before_cross, det_logout

