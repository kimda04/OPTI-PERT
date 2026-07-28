from dataclasses import dataclass, field


@dataclass
class Activity:
    """
    Representa una actividad dentro de un proyecto PERT/CPM.
    """

    name: str
    description: str
    optimistic: float
    most_likely: float
    pessimistic: float

    predecessors: list[str] = field(default_factory=list)

    expected_time: float = 0.0
    variance: float = 0.0

    es: float = 0.0
    ef: float = 0.0

    ls: float = 0.0
    lf: float = 0.0

    slack: float = 0.0