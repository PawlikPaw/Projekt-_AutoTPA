import math

def oblicz_kat_tpa(p1_skokowy, p2_kolanowy, p3_plateau_przod, p4_plateau_tyl):
    """
    Oblicza kąt TPA (Tibial Plateau Angle) w stopniach na podstawie 4 punktów (X, Y).
    
    p1_skokowy: (x, y) - środek stawu skokowego (dół kości)
    p2_kolanowy: (x, y) - wzniesienie międzykłykciowe (góra kości)
    p3_plateau_przod: (x, y) - przednia krawędź powierzchni stawowej
    p4_plateau_tyl: (x, y) - tylna krawędź powierzchni stawowej
    """
    # 1. Wektor osi mechanicznej piszczeli (od stawu skokowego do kolana)
    vx_mech = p2_kolanowy[0] - p1_skokowy[0]
    vy_mech = p2_kolanowy[1] - p1_skokowy[1]

    # 2. Wektor linii plateau (nachylenie powierzchni stawowej)
    vx_plat = p4_plateau_tyl[0] - p3_plateau_przod[0]
    vy_plat = p4_plateau_tyl[1] - p3_plateau_przod[1]

    # 3. Długości obu wektorów (twierdzenie Pitagorasa)
    dlugosc_mech = math.hypot(vx_mech, vy_mech)
    dlugosc_plat = math.hypot(vx_plat, vy_plat)

    if dlugosc_mech == 0 or dlugosc_plat == 0:
        raise ValueError("Punkty nachodzą na siebie - nie można zbudować linii.")

    # 4. Iloczyn skalarny wektorów i wyliczenie kąta między obiema liniami
    iloczyn_skalarny = abs(vx_mech * vx_plat + vy_mech * vy_plat)
    cos_kata = max(min(iloczyn_skalarny / (dlugosc_mech * dlugosc_plat), 1.0), -1.0)
    kat_miedzy_osiami = math.degrees(math.acos(cos_kata))

    # 5. Kąt TPA to kąt między linią plateau a prostą PROSTOPADŁĄ (90°) do osi mechanicznej
    tpa = 90.0 - kat_miedzy_osiami

    return round(tpa, 2)


# --- SZYBKI TEST  ---
if __name__ == "__main__":
    # Przykładowe piksele (X, Y) zwrócone przez YOLO
    staw_skokowy = (250, 600)
    staw_kolanowy = (250, 150)
    plateau_przod = (210, 140)
    plateau_tyl = (290, 175)

    wynik = oblicz_kat_tpa(staw_skokowy, staw_kolanowy, plateau_przod, plateau_tyl)
    print(f"Wyliczony kąt TPA: {wynik}°")  # Wyliczony kąt TPA: 23.63°