from dataclasses import dataclass
from typing import Optional, Tuple

from .point import Point

@dataclass
class Rectangle:
    """Rectangle type."""
    top_left: Point
    bottom_right: Point

    @classmethod
    def from_tuples(cls, top_left: Tuple[float, float], bottom_right: Tuple[float, float]) -> 'Rectangle':
        return cls(Point(*top_left), Point(*bottom_right))

    @classmethod
    def from_tuple(cls, coords: Tuple[float, float, float, float]) -> 'Rectangle':
        return cls(Point(*coords[:2]), Point(*coords[2:]))

    def __post_init__(self):
        tl = self.top_left
        br = self.bottom_right

        if (tl.x == br.x or br.is_to_the_left_of(tl)):
            raise ValueError(f'bottom right point {br} should be to the right of top left {tl}')
        
        if (tl.y == br.y or br.is_higher_than(tl)):
            raise ValueError(f'bottom right point {br} should be lower than top left {tl}')

    def __eq__(self, other: 'Rectangle') -> bool:
        return self.top_left == other.top_left and self.bottom_right  == other.bottom_right

    def intersection(self, other: 'Rectangle') -> Optional['Rectangle']:
        """
        Get a rectangle that is the intersection of the two or 
        None if there is no intersection
        """

        inter_top_left = Point(
            max(self.top_left.x, other.top_left.x),
            min(self.top_left.y, other.top_left.y)
        )

        inter_bottom_right = Point(
            min(self.bottom_right.x, other.bottom_right.x),
            max(self.bottom_right.y, other.bottom_right.y)
        )

        try:
            return Rectangle(inter_top_left, inter_bottom_right)
        except ValueError:
            # invalid rectangle means no intersection
            return None      

    def iou(self, other: 'Rectangle') -> float:
        inter = self.intersection(other)
        inter_area =  (inter.area() if inter else 0)

        return inter_area / (self.area() + other.area() - inter_area)

    def area(self) -> float:
        return (self.top_left.y - self.bottom_right.y) * (self.bottom_right.x - self.top_left.x)
