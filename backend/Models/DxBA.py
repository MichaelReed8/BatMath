from dataclasses import dataclass


@dataclass(frozen=True)
class DxBARequest:
    launch_angle: float
    exit_velocity: float
    spray_angle: float
    angle_forgiveness: float
    velocity_forgiveness: float
    launch_forgiveness: float


@dataclass(frozen=True)
class DxBAResult:
    batting_average: float
    slugging: float
    samples: int


@dataclass(frozen=True)
class DataOperationResult:
    success: bool
    message: str
    rows_affected: int = 0
