from dataclasses import dataclass
from typing import Callable


@dataclass
class Conversion:
    tag_name: str
    endpoint_name: str
    source_format: str
    target_format: str
    source_extension: str
    target_extension: str
    converter: Callable[[str], str]
