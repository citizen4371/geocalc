from dataclasses import dataclass

@dataclass
class Point:
    """Point type."""
    x: float
    y: float

    def is_to_the_left_of(self, other: 'Point') -> bool:
        return self.x < other.x

    def is_higher_than(self, other: 'Point') -> bool:
        return self.y > other.y

    def __str__(self):
        return f'{{x: {self.x}, y: {self.y}}}'
