from dataclasses import dataclass
from typing import Literal

InstallationMode = Literal["light", "dark"]


@dataclass
class InstallationColor:
    hue: int
    saturation: int | None
    modes: list[InstallationMode]