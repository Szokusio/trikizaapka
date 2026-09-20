import asyncio
from dataclasses import dataclass
from typing import Any

from triki import TRIKIScanner, TRIKIController

from .config import Settings


@dataclass
class Calibration:
    spin_x: float = 0.0
    spin_y: float = 0.0
    turn_z: float = 0.0
    tilt_x: float = 0.0
    tilt_y: float = 0.0
    flip_z: float = 0.0


class ButtonTracker:
    def __init__(self) -> None:
        self.previous = False
        self.pressed_at: float | None = None

    def update(self, pressed: bool, now: float, long_press_after: float) -> tuple[bool, bool]:
        short_press = pressed and not self.previous
        long_press = False

        if pressed and not self.previous:
            self.pressed_at = now
        elif not pressed and self.previous:
            self.pressed_at = None
        elif pressed and self.pressed_at is not None:
            long_press = now - self.pressed_at >= long_press_after

        self.previous = pressed
        return short_press, long_press


class TrikiDevice:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        self.controller: TRIKIController | None = None
        self.name = ""
        self.address = ""
        self.calibration = Calibration()

    @property
    def connected(self) -> bool:
        return self.controller is not None and self.controller.is_connected

    async def connect(self) -> None:
        scanner = TRIKIScanner()
        print("Szukam kapselka Triki...")
        await scanner.scan()
        if not scanner.scanned_devices:
            raise RuntimeError("Nie znaleziono kapselka.")

        device = scanner.scanned_devices[0]
        self.name = device.name
        self.address = device.address
        self.controller = TRIKIController(device.address)
        await self.controller.connect()
        print(f"Polaczono z: {self.name}")

    async def disconnect(self) -> None:
        if self.connected and self.controller is not None:
            await self.controller.disconnect()
        self.controller = None

    async def calibrate(self) -> Calibration:
        if not self.connected or self.controller is None:
            raise RuntimeError("Kapsel nie jest polaczony.")

        print("Kalibracja: trzymaj kapsel nieruchomo przez 1.5 sekundy")
        values: dict[str, list[int]] = {
            field: [] for field in Calibration.__dataclass_fields__
        }
        for _ in range(self.settings.calibration_samples):
            for field in values:
                values[field].append(getattr(self.controller, field))
            await asyncio.sleep(self.settings.calibration_delay)

        self.calibration = Calibration(
            **{field: sum(samples) / len(samples) for field, samples in values.items()}
        )
        return self.calibration

    def read(self, field: str) -> int:
        if not self.connected or self.controller is None:
            raise RuntimeError("Kapsel nie jest polaczony.")
        return int(getattr(self.controller, field))

    def relative(self, field: str) -> float:
        return self.read(field) - getattr(self.calibration, field)

    async def led(self, is_on: bool) -> None:
        if self.connected and self.controller is not None:
            await self.controller.toggle_led(is_on)
