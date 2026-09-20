import asyncio

from ..device import ButtonTracker, TrikiDevice


async def run(device: TrikiDevice) -> None:
    settings = device.settings
    await device.calibrate()
    seconds = 5 * 60
    running = False
    finished = False
    tracker = ButtonTracker()
    last_tick = asyncio.get_running_loop().time()
    last_rotation = 0.0
    last_display = None
    last_led = None

    print("\nTIMER: obrot ustawia minuty, klik start/pauza.")
    print("Przytrzymaj przycisk, aby wyjsc do menu.")

    try:
        while device.connected:
            now = asyncio.get_running_loop().time()
            elapsed = now - last_tick
            last_tick = now

            if running:
                seconds = max(0.0, seconds - elapsed)
                if seconds == 0:
                    running = False
                    finished = True
                    print("\nCzas skonczony!")

            short_press, long_press = tracker.update(
                device.read("button_pressed"), now, settings.button_long_press
            )
            if long_press:
                return
            if short_press:
                if finished:
                    seconds = 5 * 60
                    finished = False
                elif seconds > 0:
                    running = not running

            rotation = device.relative("turn_z")
            if not running and abs(rotation) > settings.volume_deadzone:
                if now - last_rotation >= settings.volume_cooldown:
                    seconds = max(60, min(99 * 60, seconds + (60 if rotation > 0 else -60)))
                    finished = False
                    last_rotation = now

            display = (int(seconds) // 60, int(seconds) % 60, running)
            if display != last_display:
                state = "ODLICZANIE" if running else "PAUZA"
                print(f"\r[{state}] {display[0]:02d}:{display[1]:02d}   ", end="", flush=True)
                last_display = display

            if finished:
                led = int(now * 5) % 2 == 0
            elif running:
                led = int(now * 2) % 2 == 0
            else:
                led = True
            if led != last_led:
                await device.led(led)
                last_led = led
            await asyncio.sleep(settings.loop_delay)
    finally:
        await device.led(True)
        print()
