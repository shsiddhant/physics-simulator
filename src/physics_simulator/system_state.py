from dataclasses import asdict, dataclass

from .vector import VectorTwo


@dataclass
class Particle:
    mass: float
    position: VectorTwo
    velocity: VectorTwo

    def __post_init__(self):
        if self.mass <= 0:
            raise ValueError("Particle mass must be bigger than zero.")


@dataclass(frozen=True)
class ParticleId:
    value: int


@dataclass
class System:
    particles: dict[ParticleId, Particle]

    def to_dict(self):
        return {id.value: asdict(p) for id, p in self.particles.items()}


@dataclass
class SystemState:
    particles: dict[ParticleId, Particle]
    forces: dict[ParticleId, VectorTwo]
