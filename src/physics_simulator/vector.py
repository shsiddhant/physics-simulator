from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class VectorTwo:
    x: int | float
    y: int | float

    ZERO: ClassVar[VectorTwo]

    def __add__(self, other: VectorTwo) -> VectorTwo:
        return VectorTwo(self.x + other.x, self.y + other.y)

    def __neg__(self) -> VectorTwo:
        return VectorTwo(-self.x, -self.y)

    def __sub__(self, other: VectorTwo) -> VectorTwo:
        return self + (-other)

    def __mul__(self, other: float):
        return VectorTwo(other * self.x, other * self.y)

    def __rmul__(self, other: float):
        return self.__mul__(other)

    def __truediv__(self, other: float):
        if other == 0:
            raise ZeroDivisionError("Cannot divide vector by zero")
        return VectorTwo(self.x / other, self.y / other)

    def dot(self, other: VectorTwo) -> float:
        return self.x * other.x + self.y * other.y

    def norm_squared(self) -> float:
        return self.dot(self)

    def norm_k(self, k: int) -> float:
        return pow(self.norm_squared(), 0.5 * k)

    def norm(self) -> float:
        return self.norm_k(1)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


VectorTwo.ZERO = VectorTwo(0.0, 0.0)
