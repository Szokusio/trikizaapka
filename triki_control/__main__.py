import asyncio

from .config import Settings
from .device import TrikiDevice
from .modes import mouse, repetitions, sensors, timer, volume


MODES = {
    "1": ("Myszka", mouse.run),
    "2": ("Glosnosc", volume.run),
    "3": ("Timer", timer.run),
    "4": ("Powtorzenia", repetitions.run),
    "5": ("Podglad sensorow", sensors.run),
}


def print_menu() -> None:
    print("\n=== TRIKI CONTROL CENTER ===")
    for key, (name, _) in MODES.items():
        print(f"{key}. {name}")
    print("q. Zakoncz")


async def main() -> None:
    device = TrikiDevice(Settings())
    try:
        await device.connect()
        print("Przytrzymanie przycisku przez 1.5 s wraca z trybu do menu.")

        while device.connected:
            print_menu()
            choice = input("Wybierz tryb: ").strip().lower()
            if choice == "q":
                break
            selected = MODES.get(choice)
            if selected is None:
                print("Nieprawidlowy wybor.")
                continue

            name, mode = selected
            print(f"Uruchamiam tryb: {name}")
            try:
                await mode(device)
            except Exception as error:
                print(f"Blad trybu {name}: {error}")

    except KeyboardInterrupt:
        print("\nZamykanie...")
    except Exception as error:
        print(f"Blad polaczenia: {error}")
    finally:
        await device.disconnect()
        print("Rozlaczono.")


if __name__ == "__main__":
    asyncio.run(main())
