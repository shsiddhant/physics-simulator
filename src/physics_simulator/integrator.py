from abc import ABC, abstractmethod

from physics_simulator.system_state import Particle, ParticleId, System, SystemState


class Integrator(ABC):
    @abstractmethod
    def step(self, state: SystemState, dt: float) -> System: ...


class SemiImplicitEuler(Integrator):
    def step(self, state: SystemState, dt: float) -> System:

        new_particles: dict[ParticleId, Particle] = {}
        for id, p in state.particles.items():
            acceleration = state.forces[id] / p.mass
            velocity = p.velocity + acceleration * dt
            position = p.position + velocity * dt
            new_particles[id] = Particle(p.mass, position, velocity)

        return System(new_particles)

    def __str__(self) -> str:
        return "SemiImplicitEuler"
