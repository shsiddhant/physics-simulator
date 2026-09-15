import math

from physics_simulator.forces import ForceLaw
from physics_simulator.integrator import Integrator
from physics_simulator.system_state import System


def trajectory(
    system: System,
    force_law: ForceLaw,
    integrator: Integrator,
    dt: float,
    duration: float,
):
    steps = math.floor(duration / dt) + 1

    for i in range(steps):
        yield system
        t = i * dt
        state = force_law(system, t)
        system = integrator.step(state, dt)
