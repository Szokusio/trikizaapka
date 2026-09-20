# Triki Control Center

Jedna aplikacja do obslugi kapselka Triki. Stare, dzialajace skrypty pozostaja w folderze `dzialajace skrypt`.

## Tryby

1. Myszka: przechylenie steruje kursorem, klik robi lewy klik, obrot przewija.
2. Glośność: obrot zmienia glosnosc, klik wlacza lub wylacza mute.
3. Timer: obrot ustawia minuty, klik uruchamia lub zatrzymuje odliczanie.
4. Powtorzenia: pelny ruch gora-dol nalicza jedno powtorzenie.
5. Podglad sensorow: pokazuje wartosci zyroskopu, przechylow i baterii.

## Uruchomienie

Uzyj interpretera, w ktorym zainstalowane sa `triki`, `pyautogui` i `pycaw`:

```powershell
C:/Users/pwasi/AppData/Local/Programs/Python/Python314/python.exe -m triki_control
```

Po polaczeniu wybierz numer trybu. Przytrzymanie przycisku kapselka przez 1.5 sekundy wraca do menu.

## Kalibracja

Przed kazdym trybem trzymaj kapsel nieruchomo przez 1.5 sekundy. Program ustawia wtedy wartosci spoczynkowe sensorow.

## Awaryjne zatrzymanie myszki

W trybie myszki przesuniecie kursora do lewego gornego rogu ekranu zatrzymuje `pyautogui`.
"# trikizaapka" 
