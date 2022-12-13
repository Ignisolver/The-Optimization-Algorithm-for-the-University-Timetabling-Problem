from dataclasses import dataclass


@dataclass
class AlgResult:
    successes: int = 0
    failures: int = 0
    failures_time: int = 0
    successes_time: int = 0
    time: float = 0

    def __repr__(self):
        return (30 * "-" + "\n" +
                f"ASSIGNED  : " +
                f"{self.successes} / {self.successes + self.failures}" +
                f" CLASSES " +
                f"({round(100 * self.successes / (self.successes + self.failures), 2 )} %)\n" +
                f"FAILURES  : {self.failures}\n"+
                30 * "-")
