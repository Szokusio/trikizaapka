# Triki Control Center

Program zamienia kapsel Triki w uniwersalny kontroler Bluetooth dla komputera.
Wykorzystuje jego przycisk, żyroskop, czujniki przechyłu oraz zieloną diodę LED.

Projekt jest napisany w Pythonie i działa obecnie na Windows.

## Możliwości

| Tryb | Działanie |
| --- | --- |
| **Myszka** | Przechylenie steruje kursorem, przycisk wykonuje lewy klik, a obrót przewija stronę. |
| **Głośność** | Obrót zwiększa lub zmniejsza głośność, a przycisk przełącza wyciszenie. |
| **Timer** | Obrót ustawia czas, przycisk uruchamia lub zatrzymuje odliczanie, a LED pokazuje stan. |
| **Powtórzenia** | Ruch kapselka góra-dół wykrywa pełne powtórzenia i ignoruje szybkie drgania. |
| **Podgląd sensorów** | Pokazuje na żywo wartości osi żyroskopu, przechyłu i poziom baterii. |

## Wymagania

- Windows 10 lub nowszy
- Python 3.10 lub nowszy
- Kapsel Triki z włączonym Bluetooth
- zainstalowane zależności z pliku `requirements.txt`

## Instalacja

Sklonuj repozytorium i przejdź do jego katalogu:

```powershell
git clone https://github.com/Szokusio/trikizaapka.git
cd trikizaapka
```

Utwórz środowisko wirtualne:

```powershell
py -m venv .venv
```

Aktywuj je w PowerShellu:

```powershell
.\.venv\Scripts\Activate.ps1
```

Zainstaluj zależności:

```powershell
python -m pip install -r requirements.txt
```

> Jeśli biblioteka `triki` jest dostępna tylko w głównym interpreterze Python,
> uruchom program tym interpreterem zamiast `.venv`.

## Uruchomienie

Uruchom aplikację jako moduł:

```powershell
python -m triki_control
```

Możesz też użyć pliku startowego:

```powershell
python run_triki.py
```

Po połączeniu wybierz numer trybu w menu.

## Sterowanie

### Wspólne

- **krótki klik** - akcja aktualnego trybu,
- **przytrzymanie przycisku przez 1,5 sekundy** - powrót do menu,
- **zielona LED** - sygnalizuje stan aktualnego trybu.

### Kalibracja

Przed uruchomieniem każdego trybu program wykonuje kalibrację przez około 1,5 sekundy.
W tym czasie połóż kapsel w pozycji neutralnej i trzymaj go nieruchomo.

### Myszka

- przechylenie w lewo/prawo - ruch kursora poziomo,
- przechylenie przód/tył - ruch kursora pionowo,
- klik przyciskiem kapselka - lewy przycisk myszy,
- obrót kapselka - przewijanie.

Awaryjne zatrzymanie `pyautogui`: przesuń kursor do lewego górnego rogu ekranu.

### Timer

- obrót - dodaje lub odejmuje minutę,
- klik - start/pauza,
- klik po zakończeniu - reset do 5 minut,
- szybkie miganie LED - zakończenie odliczania.

### Powtórzenia

Program zalicza powtórzenie dopiero po wykonaniu pełnego ruchu i powrocie do pozycji
startowej. Ruch musi trwać co najmniej 0,5 sekundy. Klik zeruje licznik.

## Struktura projektu

```text
triki-control-center/
├── triki_control/
│   ├── __main__.py          # menu główne i uruchamianie trybów
│   ├── config.py             # ustawienia czułości i progów
│   ├── device.py             # Bluetooth, kalibracja i LED
│   └── modes/
│       ├── mouse.py          # sterowanie myszką
│       ├── repetitions.py    # licznik powtórzeń
│       ├── sensors.py        # podgląd sensorów
│       ├── timer.py          # timer
│       └── volume.py         # sterowanie głośnością
├── dzialajace skrypt/        # wcześniejsze, samodzielne wersje skryptów
├── requirements.txt
├── run_triki.py
└── README.md
```

## Dostosowanie czułości

Najważniejsze ustawienia znajdują się w [triki_control/config.py](triki_control/config.py):

- `motion_deadzone` - ignorowanie drobnych drgań,
- `mouse_sensitivity` - czułość ruchu kursora,
- `volume_sensitivity` - czułość zmiany głośności,
- `minimum_rep_duration` - minimalny czas powtórzenia,
- `button_long_press` - czas przytrzymania przycisku.

## Status projektu

Projekt jest rozwijany eksperymentalnie. Połączenie Bluetooth, kalibracja sensorów,
tryby sterowania oraz obsługa LED są już zaimplementowane.

## Licencja

Projekt nie ma jeszcze wybranej licencji.
