## Example: Falling under Gravity and Linear Drag

from physics_simulator.forces import ConstantGravity, LinearDrag
from physics_simulator.integrator import SemiImplicitEuler
from physics_simulator.system_state import Particle, ParticleId, System
from physics_simulator.trajectory import trajectory
from physics_simulator.vector import VectorTwo

# Setup initial system.
initial_position = VectorTwo(0.0, 100.0)
initial_velocity = VectorTwo.ZERO
particle_id = ParticleId(1)
mass = 1
initial_system = System(
    particles={particle_id: Particle(mass, initial_position, initial_velocity)}
)

print("Initial System:", initial_system.to_dict())

# Setup force law and integrator
g = VectorTwo(0.0, -10.0)
k = 2  # Drag coefficient
force_law = ConstantGravity(g) + LinearDrag(k)
print("Forces:", force_law.forces)
integrator = SemiImplicitEuler()
print("Integrator:", integrator)
dt = 0.1

# Expected terminal velocity
v_y_term = mass * g.y / k
print(f"Expected terminal velocity: {v_y_term}")

# Run trajectory generator
for i, system in enumerate(
    trajectory(initial_system, force_law, integrator, dt=dt, duration=3.0)
):
    t = i * dt
    v_y = system.particles[particle_id].velocity.y
    print(f"t={i * 0.1:.1f}, v_y={v_y:.3f}")
