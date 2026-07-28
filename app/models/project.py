from dataclasses import dataclass, field

from app.models.activity import Activity


@dataclass
class Project:
    """
    Contiene todas las actividades del proyecto.
    """

    name: str

    activities: list[Activity] = field(default_factory=list)

    total_duration: float = 0.0

    critical_path: list[str] = field(default_factory=list)