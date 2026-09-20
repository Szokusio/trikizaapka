import asyncio

from ..device import ButtonTracker, TrikiDevice


async def run(device: TrikiDevice) -> None:
    settings = device.settings
    await device.calibrate()
    count = 0
    movement_started_at: float | None = None
    tracker = ButtonTracker()
    led_pulse_until = 0.0
    last_led = None

    print("\nPOWTORZENIA: wykonuj ruch gora-dol.")
    print("Klik zeruje licznik, przytrzymanie wraca do menu.")

    try:
        while device.connected:
            now = asyncio.get_running_loop().time()
            position = abs(device.relative("tilt_y"))

            if movement_started_at is None and position >= settings.motion_threshold:
                movement_started_at = now
            elif movement_started_at is not None and position <= settings.motion_deadzone:
                if now - movement_started_at >= settings.minimum_rep_duration:
                    count += 1
                    led_pulse_until = now + 0.15
                    print(f"\nPowtorzenia: {count}")
                movement_started_at = None

            short_press, long_press = tracker.update(
                device.read("button_pressed"), now, settings.button_long_press
            )
            if long_press:
                return
            if short_press:
                count = 0
                movement_started_at = None
                print("\nLicznik wyzerowany.")

            led = now >= led_pulse_until
            if led != last_led:
                await device.led(led)
                last_led = led
            await asyncio.sleep(settings.loop_delay)
    finally:
        await device.led(True)
