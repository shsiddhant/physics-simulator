from abc import ABC, abstractmethod
from dataclasses import dataclass

from .system_state import System, SystemState
from .vector import VectorTwo


class ForceLaw(ABC):
    @abstractmethod
    def __call__(self, system: System, time: float) -> SystemState: ...

    def __add__(self, other: "ForceLaw"):
        return NetForceLaw(self, other)


class NetForceLaw(ForceLaw):
    def __init__(self, *forces: ForceLaw) -> None:
        self.forces: tuple[ForceLaw, ...] = forces

    def __call__(self, system: System, time: float) -> SystemState:
        particles = system.particles
        states = [force(system, time) for force in self.forces]
        forces = {
            id: sum(
                (state.forces[id] for state in states),
                start=VectorTwo.ZERO,
            )
            for id in particles
        }
        return SystemState(particles, forces)

    def __add__(self, other):
        if isinstance(other, NetForceLaw):
            return NetForceLaw(*self.forces, *other.forces)
        elif isinstance(other, ForceLaw):
            return NetForceLaw(*self.forces, other)
        return NotImplemented


@dataclass(frozen=True)
class ConstantForce(ForceLaw):
    value: VectorTwo

    def __call__(self, system: System, time: float) -> SystemState:
        particles = system.particles
        return SystemState(
            particles=particles,
            forces={id: self.value for id, p in particles.items()},
        )


@dataclass(frozen=True)
class ConstantGravity(ForceLaw):
    g: VectorTwo

    def __call__(self, system: System, time: float) -> SystemState:
        particles = system.particles
        return SystemState(
            particles=particles,
            forces={id: p.mass * self.g for id, p in particles.items()},
        )


@dataclass(frozen=True)
class LinearDrag(ForceLaw):
    k: float

    def __post_init__(self) -> None:
        if self.k < 0:
            raise ValueError("Drag coefficient must be non-negative")

    def __call__(self, system: System, time: float) -> SystemState:
        particles = system.particles
        return SystemState(
            particles=particles,
            forces={id: -self.k * p.velocity for id, p in particles.items()},
        )


@dataclass(frozen=True)
class HookeLaw(ForceLaw):
    k: float

    def __post_init__(self) -> None:
        if self.k < 0:
            raise ValueError("Spring constant must be non-negative")

    def __call__(self, system: System, time: float) -> SystemState:
        particles = system.particles
        return SystemState(
            particles=particles,
            forces={id: -self.k * p.position for id, p in particles.items()},
        )


@dataclass(frozen=True)
class CentralInverseSquare(ForceLaw):
    C: float

    def __call__(self, system: System, time: float) -> SystemState:
        particles = system.particles
        return SystemState(
            particles=particles,
            forces={
                id: self.C * p.position / (p.position).norm_k(3)
                for id, p in particles.items()
            },
        )
