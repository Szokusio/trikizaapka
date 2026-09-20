import asyncio

from ..device import ButtonTracker, TrikiDevice


async def run(device: TrikiDevice) -> None:
    from pycaw.pycaw import AudioUtilities

    settings = device.settings
    volume = AudioUtilities.GetSpeakers().EndpointVolume
    await device.calibrate()
    tracker = ButtonTracker()
    last_change = 0.0
    print("\nGLOSNOSC: obrot w prawo glosniej, w lewo ciszej.")
    print("Klik wycisza, przytrzymanie wraca do menu.")

    while device.connected:
        now = asyncio.get_running_loop().time()
        short_press, long_press = tracker.update(
            device.read("button_pressed"), now, settings.button_long_press
        )
        if long_press:
            return
        if short_press:
            volume.SetMute(not bool(volume.GetMute()), None)
            print("\nMute: " + ("wlaczony" if volume.GetMute() else "wylaczony"))

        rotation = device.relative("turn_z")
        if abs(rotation) > settings.volume_deadzone and now - last_change >= settings.volume_cooldown:
            step = max(-settings.volume_step_limit, min(settings.volume_step_limit, rotation / settings.volume_sensitivity))
            current = volume.GetMasterVolumeLevelScalar()
            new_volume = max(0.0, min(1.0, current + step))
            volume.SetMasterVolumeLevelScalar(new_volume, None)
            print(f"\rGlośność: {round(new_volume * 100):3d}%   ", end="", flush=True)
            last_change = now
        await asyncio.sleep(settings.loop_delay)
