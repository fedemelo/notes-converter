from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


@dataclass
class ConversionOption:
    """A configurable query parameter exposed on a conversion's endpoints."""

    name: str
    default: str
    description: str
    choices: type[Enum] | None = None


@dataclass
class Conversion:
    tag_name: str
    endpoint_name: str
    source_format: str
    target_format: str
    source_extension: str
    target_extension: str
    converter: Callable[..., str]
    options: list[ConversionOption] = field(default_factory=list)
