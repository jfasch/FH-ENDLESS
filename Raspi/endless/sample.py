from dataclasses import dataclass


@dataclass(frozen=True)
class Sample:
    name: str
    timestamp_ms: int
    temperature: float
