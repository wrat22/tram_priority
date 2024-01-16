def menu():
    print("Podaj informacje dla kierunku jazdy")
    singal_group = input("Jak nazywa się grupa sygnałowa? ")
    det_before_cross = input("Jak nazywa się detektor przed skrzyżowaniem? ")
    det_logout = input("Jak nazywa się detektor za skrzyżowaniem / do wylogowania? ")
    return singal_group, det_before_cross, det_logout
