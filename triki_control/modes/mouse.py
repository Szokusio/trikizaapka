import asyncio

from ..device import ButtonTracker, TrikiDevice


async def run(device: TrikiDevice) -> None:
    import pyautogui

    settings = device.settings
    tracker = ButtonTracker()
    last_scroll = 0.0
    pyautogui.PAUSE = 0.01
    pyautogui.FAILSAFE = True
    print("\nMYSZ: przechylenie rusza kursorem, klik robi lewy klik.")
    print("Obrot przewija, przytrzymanie wraca do menu.")

    while device.connected:
        now = asyncio.get_running_loop().time()
        x = device.relative("tilt_x")
        y = device.relative("tilt_y")
        move_x = 0 if abs(x) < settings.motion_deadzone else int(x / settings.mouse_sensitivity)
        move_y = 0 if abs(y) < settings.motion_deadzone else int(y / settings.mouse_sensitivity)
        move_x = max(-settings.max_mouse_step, min(settings.max_mouse_step, move_x))
        move_y = max(-settings.max_mouse_step, min(settings.max_mouse_step, move_y))
        if move_x or move_y:
            pyautogui.moveRel(move_x, move_y, duration=0)

        turn = device.relative("turn_z")
        if abs(turn) >= settings.scroll_threshold and now - last_scroll >= settings.scroll_cooldown:
            pyautogui.scroll(1 if turn > 0 else -1)
            last_scroll = now

        short_press, long_press = tracker.update(
            device.read("button_pressed"), now, settings.button_long_press
        )
        if long_press:
            return
        if short_press:
            pyautogui.click()
        await asyncio.sleep(settings.loop_delay)
