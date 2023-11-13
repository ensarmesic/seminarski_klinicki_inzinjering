import random
import time
from enum import Enum
from contextlib import contextmanager

class Dogadjaj(Enum):
    UKLJUCENO = "UKLJUCENO"
    ISKLJUCENO = "ISKJUCENO"
    INTERFERENCIJA = "INTERFERENCIJA"
    SIMULACIJA_VREMENA = "SIMULACIJA_VREMENA"
    SIMULACIJA_VREMENA_U_IZOLIRANOJ_SOBI = "SIMULACIJA_VREMENA_U_IZOLIRANOJ_SOBI"

class MedicinskaOprema:
    def __init__(self, naziv, logger=None):
        self.naziv = naziv
        self.ukljucena = False
        self.logger = logger

    def ukljuci(self):
        self.ukljucena = True
        self.logiraj_dogadjaj(Dogadjaj.UKLJUCENO)

    def iskljuci(self):
        self.ukljucena = False
        self.logiraj_dogadjaj(Dogadjaj.ISKLJUCENO)

    def provjeri_interferenciju(self):
        return random.choice([True, False])

    def logiraj_dogadjaj(self, dogadjaj):
        if self.logger:
            self.logger.write(f"{self.naziv}: {dogadjaj.value}\n")
        else:
            print(f"{self.naziv}: {dogadjaj.value}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

class StanjeIzoliraneSobe(Enum):
    ISKLJUCENA = "ISKLJUCENA"
    UKLJUCENA = "UKLJUCENA"

class ElektromagnetskiIzoliranaSoba:
    def __init__(self, logger=None):
        self.stanje = StanjeIzoliraneSobe.ISKLJUCENA
        self.logger = logger

    def __enter__(self):
        self.ukljuci_izolaciju()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.iskljuci_izolaciju()

    def ukljuci_izolaciju(self):
        if self.stanje == StanjeIzoliraneSobe.ISKLJUCENA:
            self.stanje = StanjeIzoliraneSobe.UKLJUCENA
            self.logiraj_dogadjaj(Dogadjaj.UKLJUCENO)

    def iskljuci_izolaciju(self):
        if self.stanje == StanjeIzoliraneSobe.UKLJUCENA:
            self.stanje = StanjeIzoliraneSobe.ISKLJUCENA
            self.logiraj_dogadjaj(Dogadjaj.ISKLJUCENO)

    def logiraj_dogadjaj(self, dogadjaj):
        if self.logger:
            self.logger.write(f"Izolirana soba: {dogadjaj.value}\n")
        else:
            print(f"Izolirana soba: {dogadjaj.value}")

class ElektromagnetskiIzvor:
    def __init__(self, naziv, logger=None):
        self.naziv = naziv
        self.ukljucen = False
        self.vrijeme_upotrebe = 0
        self.logger = logger

    def __enter__(self):
        self.ukljuci()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.iskljuci()

    def ukljuci(self):
        if not self.ukljucen:
            self.ukljucen = True
            self.logiraj_dogadjaj(Dogadjaj.UKLJUCENO)

    def iskljuci(self):
        if self.ukljucen:
            self.ukljucen = False
            self.logiraj_dogadjaj(Dogadjaj.ISKLJUCENO)

    def logiraj_dogadjaj(self, dogadjaj):
        if self.logger:
            self.logger.write(f"{self.naziv}: {dogadjaj.value}\n")
        else:
            print(f"{self.naziv}: {dogadjaj.value}")

    def zapisi_trajanje_upotrebe(self, trajanje):
        self.vrijeme_upotrebe += trajanje

    def prikazi_trajanje_upotrebe(self):
        print(f"{self.naziv}: Ukupno vrijeme upotrebe - {self.vrijeme_upotrebe} sekundi")

class BolnickiSistem:
    def __init__(self):
        self.medicinska_oprema_lista = []
        self.elektromagnetski_izvori = []
        self.logger = Logiranje()

    def dodaj_medicinsku_opremu(self, oprema):
        self.medicinska_oprema_lista.append(oprema)

    def dodaj_elektromagnetski_izvor(self, izvor):
        self.elektromagnetski_izvori.append(izvor)

    def simuliraj_vrijeme(self, trajanje):
        self.logiraj_dogadjaj(Dogadjaj.SIMULACIJA_VREMENA)
        time.sleep(trajanje)

    def simuliraj_vrijeme_u_izoliranoj_sobi(self, trajanje):
        with ElektromagnetskiIzoliranaSoba(logger=self.logger):
            self.simuliraj_vrijeme(trajanje)
            self.logiraj_dogadjaj(Dogadjaj.SIMULACIJA_VREMENA_U_IZOLIRANOJ_SOBI)

    def prikazi_trajanje_upotrebe(self):
        for izvor in self.elektromagnetski_izvori:
            izvor.prikazi_trajanje_upotrebe()

    def logiraj_dogadjaj(self, dogadjaj):
        self.logger.write(f"Sistem: {dogadjaj.value}\n")

class Logiranje:
    def __init__(self):
        self.log_datoteka = "log.txt"

    def write(self, text):
        with open(self.log_datoteka, "a", encoding="utf-8") as f:
            f.write(text)

# Primjer koda za upravljanje elektromagnetskim izvorima i praćenje medicinske opreme u bolnici
bolnicki_sistem = BolnickiSistem()

wifi_router = ElektromagnetskiIzvor("WiFi router", logger=bolnicki_sistem.logger)
mobilni_telefon = ElektromagnetskiIzvor("Mobilni telefon", logger=bolnicki_sistem.logger)
racunar = ElektromagnetskiIzvor("Računar", logger=bolnicki_sistem.logger)

bolnicki_sistem.dodaj_elektromagnetski_izvor(wifi_router)
bolnicki_sistem.dodaj_elektromagnetski_izvor(mobilni_telefon)
bolnicki_sistem.dodaj_elektromagnetski_izvor(racunar)

# Generiranje nasumičnog broja između 1 i 10
nasumicno_trajanje = random.randint(1, 10)

# Simulacija korištenja elektromagnetskih izvora s nasumičnim trajanjem
with wifi_router, mobilni_telefon, racunar:
    bolnicki_sistem.simuliraj_vrijeme(nasumicno_trajanje)

wifi_router.zapisi_trajanje_upotrebe(nasumicno_trajanje)
mobilni_telefon.zapisi_trajanje_upotrebe(nasumicno_trajanje + 2)
racunar.zapisi_trajanje_upotrebe(nasumicno_trajanje + 4)

# Simulacija praćenja medicinske opreme
ekg = MedicinskaOprema("EKG", logger=bolnicki_sistem.logger)
ct_skener = MedicinskaOprema("CT skener", logger=bolnicki_sistem.logger)
infuzijska_pumpa = MedicinskaOprema("Infuzijska pumpa", logger=bolnicki_sistem.logger)
defibrilator = MedicinskaOprema("Defibrilator", logger=bolnicki_sistem.logger)
rendgenski_aparat = MedicinskaOprema("Rendgenski aparat", logger=bolnicki_sistem.logger)
ultrazvuk = MedicinskaOprema("Ultrazvuk", logger=bolnicki_sistem.logger)
laboratorijski_analizator = MedicinskaOprema("Laboratorijski analizator", logger=bolnicki_sistem.logger)
monitor_vitalnih_znakova = MedicinskaOprema("Monitor vitalnih znakova", logger=bolnicki_sistem.logger)
anestezioloski_aparat = MedicinskaOprema("Anesteziološki aparat", logger=bolnicki_sistem.logger)
ekg_holter_monitor = MedicinskaOprema("EKG Holter monitor", logger=bolnicki_sistem.logger)

bolnicki_sistem.dodaj_medicinsku_opremu(ekg)
bolnicki_sistem.dodaj_medicinsku_opremu(ct_skener)
bolnicki_sistem.dodaj_medicinsku_opremu(infuzijska_pumpa)
bolnicki_sistem.dodaj_medicinsku_opremu(defibrilator)
bolnicki_sistem.dodaj_medicinsku_opremu(rendgenski_aparat)
bolnicki_sistem.dodaj_medicinsku_opremu(ultrazvuk)
bolnicki_sistem.dodaj_medicinsku_opremu(laboratorijski_analizator)
bolnicki_sistem.dodaj_medicinsku_opremu(monitor_vitalnih_znakova)
bolnicki_sistem.dodaj_medicinsku_opremu(anestezioloski_aparat)
bolnicki_sistem.dodaj_medicinsku_opremu(ekg_holter_monitor)

for oprema in bolnicki_sistem.medicinska_oprema_lista:
    with oprema:
        if oprema.provjeri_interferenciju():
            print(f"Upozorenje: {oprema.naziv} je osjetljiv na elektromagnetsku interferenciju.")

# Simulacija vremena provedenog u izoliranoj sobi
bolnicki_sistem.simuliraj_vrijeme_u_izoliranoj_sobi(5)

# Prikaz trajanja upotrebe izvora
bolnicki_sistem.prikazi_trajanje_upotrebe()
