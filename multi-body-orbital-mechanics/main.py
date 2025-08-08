import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

# --- Physics constants ---
G = 6.67430e-11  # gravitational constant
dt = 60 * 60 * 6  # time step (6 hours)
frame_count = 0   # to animate glow pulsing

# --- Planet data ---
planets = [
    {
        "pos": [0.39 * 1.496e11, 0],  # Mercury
        "vel": [0, 47360],
        "mass": 3.285e23,
        "x_path": [],
        "y_path": [],
        "color": "gray"
    },
    {
        "pos": [0.72 * 1.496e11, 0],  # Venus
        "vel": [0, 35020],
        "mass": 4.867e24,
        "x_path": [],
        "y_path": [],
        "color": "orange"
    },
    {
        "pos": [1.496e11, 0],  # Earth
        "vel": [0, 29780],
        "mass": 5.972e24,
        "x_path": [],
        "y_path": [],
        "color": "blue"
    },
    {
        "pos": [1.52 * 1.496e11, 0],  # Mars
        "vel": [0, 24077],
        "mass": 6.417e23,
        "x_path": [],
        "y_path": [],
        "color": "red"
    }
]

# --- Setup figure ---
fig, ax = plt.subplots()
ax.set_facecolor("black")
ax.set_aspect('equal', adjustable='box')

def update_positions():
    for i, p1 in enumerate(planets):
        fx = fy = 0
        for j, p2 in enumerate(planets):
            if i != j:
                dx = p2["pos"][0] - p1["pos"][0]
                dy = p2["pos"][1] - p1["pos"][1]
                dist = math.sqrt(dx**2 + dy**2)
                F = G * p1["mass"] * p2["mass"] / dist**2
                fx += F * dx / dist
                fy += F * dy / dist

        # Add Sun gravity
        dx = 0 - p1["pos"][0]
        dy = 0 - p1["pos"][1]
        dist = math.sqrt(dx**2 + dy**2)
        F = G * p1["mass"] * 1.989e30 / dist**2
        fx += F * dx / dist
        fy += F * dy / dist

        # Update velocity & position
        p1["vel"][0] += fx / p1["mass"] * dt
        p1["vel"][1] += fy / p1["mass"] * dt
        p1["pos"][0] += p1["vel"][0] * dt
        p1["pos"][1] += p1["vel"][1] * dt

        # Save path
        p1["x_path"].append(p1["pos"][0])
        p1["y_path"].append(p1["pos"][1])

def animate(frame):
    global frame_count
    frame_count += 1
    ax.clear()
    ax.set_facecolor("black")
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-2.5e11, 2.5e11)
    ax.set_ylim(-2.5e11, 2.5e11)
    ax.axis('off')

    update_positions()

    # --- Sun breathing glow ---
    glow_alpha = 0.3 + 0.25 * (math.sin(frame_count * 0.05) + 1) / 2
    ax.scatter(0, 0, color='yellow', s=200, zorder=3)
    ax.scatter(0, 0, color='yellow', s=900, alpha=glow_alpha, zorder=1)

    # --- Planets ---
    for p in planets:
        # Orbit path
        ax.plot(p["x_path"], p["y_path"], color=p["color"], lw=1)

        # Planet
        ax.scatter(p["pos"][0], p["pos"][1], color=p["color"], s=30, zorder=3)

        # Glow halo
        planet_alpha = 0.3 + 0.25 * (math.sin(frame_count * 0.1) + 1) / 2
        ax.scatter(p["pos"][0], p["pos"][1],
                   color=p["color"], s=200, alpha=planet_alpha, zorder=1)

ani = animation.FuncAnimation(fig, animate, frames=360, interval=20)
plt.show()
