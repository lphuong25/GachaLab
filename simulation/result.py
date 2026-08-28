from dataclasses import dataclass

@dataclass
class PullResult:
    pull_number: int
    is_ssr: bool
    is_featured: bool