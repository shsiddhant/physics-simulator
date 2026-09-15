# Physics Simulator

A lightweight, extensible 2D particle physics simulation engine built in Python. Designed around composable force laws and clean numerical integration.

## Features

- **Composable Force Laws:** Combine forces naturally using operator overloading (e.g., `ConstantGravity(g) + LinearDrag(k)`).
- **Immutable State:** Built with frozen dataclasses to prevent unintended side effects during simulation steps.
- **Efficient Trajectory Generation:** Stream simulation steps lazily via generators rather than bloating memory.
- **Built-in Laws:** Supports constant forces, gravity, linear drag, Hooke's law, and central inverse-square fields (orbital mechanics).
- **ExtensibleL** Due to the use of abstract classes, it's easier to add new force laws and integrator methods.

## Installation

Requires Python 3.13+

```bash
pip install git+https://github.com/shsiddhant/physics-simulator.git
```

## Example: Falling under Gravity and Linear Drag

```py
from physics_simulator.forces import ConstantGravity, LinearDrag
from physics_simulator.integrator import SemiImplicitEuler
from physics_simulator.system_state import Particle, ParticleId, System
from physics_simulator.trajectory import trajectory
from physics_simulator.vector import VectorTwo

# Initial system: 1kg particle dropped from y=100m
particle_id = ParticleId(1)
initial_system = System(
    particles={
        particle_id: Particle(
            mass=1.0, position=VectorTwo(0.0, 100.0), velocity=VectorTwo.ZERO
        )
    }
)

# Combine gravity and linear drag to get net force law
force_law = ConstantGravity(VectorTwo(0.0, -10.0)) + LinearDrag(k=2.0)
integrator = SemiImplicitEuler()

# Stream trajectory steps
for i, system in enumerate(
    trajectory(initial_system, force_law, integrator, dt=0.1, duration=3.0)
):
    v_y = system.particles[particle_id].velocity.y
    print(f"t={i * 0.1:.1f}, v_y={v_y:.2f}")
```

## License
This project is licensed under the [MIT License](LICENSE).