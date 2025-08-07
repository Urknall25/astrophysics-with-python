import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
G = 6.674e-11  # Gravitational constant
dt = 3600*24  # Time step (seconds)

# Inputs
mass_star = 1.989e30  # Mass of the star (e.g. the Sun)
mass_planet = 5.972e24  # Mass of the planet (e.g. the Earth)
num_steps = 2000  # Number of simulation steps

# Initial Conditions
planet_position = [1.5e11, 0]     # Start at 1 AU (same as Earth)
velocity = [3000, 25000]   # Initial velocity (m/s)
star_position = [0, 0]  # Star is at the origin

# Lists to store the path for plotting
x_positions = []
y_positions = []
trail_positions = []
trail_lines = []

# Create the figure
fig, ax = plt.subplots()
planet_dot, = ax.plot([], [], 'bo')  # Planet as blue dot
star_dot, = ax.plot(0, 0, 'yo', label='Star')  # Star as yellow dot
orbit_path, = ax.plot([], [], 'b-', linewidth=0.5)  # Planet's full path
ax.set_xlim(-3e11, 3e11)
ax.set_ylim(-3e11, 3e11)
ax.set_aspect('equal')
ax.grid(True)
ax.set_title("Orbital Animation")
ax.set_xlabel("X position (m)")
ax.set_ylabel("Y position (m)")
ax.legend()

def update(frame):
    global planet_position, velocity, trail_lines

    # Compute distance components
    dx = star_position[0] - planet_position[0]
    dy = star_position[1] - planet_position[1]
    magnitude = math.sqrt(dx**2 + dy**2)

    # Compute gravitational force
    force = G * mass_star * mass_planet / magnitude**2

    # Unit vector from planet to star
    unit_vector = [dx / magnitude, dy / magnitude]

    # Force vector
    force_vector = [force * unit_vector[0], force * unit_vector[1]]

    # Acceleration = F / m
    acceleration = [force_vector[0] / mass_planet, force_vector[1] / mass_planet]

    # Update velocity
    velocity[0] += acceleration[0] * dt
    velocity[1] += acceleration[1] * dt

    # Update position
    planet_position[0] += velocity[0] * dt
    planet_position[1] += velocity[1] * dt

    # Store position for full orbit
    x_positions.append(planet_position[0])
    y_positions.append(planet_position[1])

    # Store position for fading trail
    trail_positions.append(planet_position.copy())
    max_trail_length = 100
    if len(trail_positions) > max_trail_length:
        trail_positions.pop(0)

    # Remove previous trail lines
    for line in trail_lines:
        line.remove()
    trail_lines = []

    # Draw fading trail
    for i in range(1, len(trail_positions)):
        alpha = i / len(trail_positions)
        line, = ax.plot(
            [trail_positions[i-1][0], trail_positions[i][0]],
            [trail_positions[i-1][1], trail_positions[i][1]],
            color='blue',
            alpha=alpha,
            linewidth=2
        )
        trail_lines.append(line)

    # Update planet and orbit
    planet_dot.set_data([planet_position[0]], [planet_position[1]])
    orbit_path.set_data(x_positions, y_positions)

    return planet_dot, orbit_path, *trail_lines

# Animate!
ani = FuncAnimation(fig, update, frames=num_steps, interval=10, blit=False)
plt.show()
