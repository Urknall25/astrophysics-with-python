import numpy as np
import matplotlib.pyplot as plt

# ========== Constants ==========
mu = 3.986e14         # gravitational constant × Earth’s mass
R_earth = 6371e3      # Earth's radius (m)

# ========== Orbit altitudes (from 200 km to 36,000 km) ==========
h = np.linspace(200e3, 36000e3, 200)
r = R_earth + h

# ========== Orbital velocity at that altitude ==========
v_orbit = np.sqrt(mu / r)

# ========== Approximate Δv to reach that orbit from Earth ==========
v_surface = np.sqrt(mu / R_earth)
print(v_surface)
delta_v = v_orbit - v_surface  # not realistic, but only for comparison
delta_v = np.abs(delta_v)

# ========== Plot ==========
plt.figure(figsize=(8, 5))
plt.plot(h/1000, delta_v/1000, color='royalblue', linewidth=2)
plt.title("Δv vs Orbit Altitude", fontsize=14)
plt.xlabel("Orbit altitude (km)")
plt.ylabel("Δv (km/s)")
plt.grid(True)
plt.show()
