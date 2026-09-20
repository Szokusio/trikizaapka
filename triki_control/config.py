from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    calibration_samples: int = 30
    calibration_delay: float = 0.05
    loop_delay: float = 0.05
    button_long_press: float = 1.5
    motion_deadzone: int = 100
    motion_threshold: int = 250
    minimum_rep_duration: float = 0.5
    max_mouse_step: int = 15
    mouse_sensitivity: int = 120
    scroll_threshold: int = 250
    scroll_cooldown: float = 0.25
    volume_deadzone: int = 90
    volume_sensitivity: int = 18000
    volume_cooldown: float = 0.30
    volume_step_limit: float = 0.018
