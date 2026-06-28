from dataclasses import dataclass
from typing import Callable


@dataclass
class Conversion:
    name: str
    source_format: str
    target_format: str
    source_extension: str
    target_extension: str
    converter: Callable[[str], str]
