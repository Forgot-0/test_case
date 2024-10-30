from dataclasses import dataclass, field


@dataclass(eq=False)
class ApplicationException(Exception):
    error_code: int = field(default=400, init=False)

    @property
    def message(self):
        return 'App error'