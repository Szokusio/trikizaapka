import asyncio

from ..device import ButtonTracker, TrikiDevice


async def run(device: TrikiDevice) -> None:
    settings = device.settings
    tracker = ButtonTracker()
    print("\nSENSORY: podglad danych na zywo.")
    print("Przytrzymaj przycisk, aby wrocic do menu.")

    while device.connected:
        now = asyncio.get_running_loop().time()
        values = {
            field: device.read(field)
            for field in ("spin_x", "spin_y", "turn_z", "tilt_x", "tilt_y", "flip_z")
        }
        battery = device.controller.battery_level if device.controller else "?"
        print(
            "\r"
            + " ".join(f"{name}={value:6d}" for name, value in values.items())
            + f" battery={battery}%",
            end="",
            flush=True,
        )
        _, long_press = tracker.update(
            device.read("button_pressed"), now, settings.button_long_press
        )
        if long_press:
            print()
            return
        await asyncio.sleep(0.20)
