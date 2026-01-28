import math
import matplotlib.pyplot as plt
import numpy as np

# ========== Constants ==========
mu_earth = 3.986e14  # gravitational constant × Earth’s mass
r_earth = 6371e3      # Earth radius (m)

# ========== Example orbits ==========
r1 = r_earth + 200e3   # Low Earth Orbit (200 km)
r2 = r_earth + 35786e3 # Geostationary Orbit (35,786 km)

def hohmann_delta_v(r1, r2, mu=mu_earth):
    # ========== Hohmann transfer Δv (two burns) ==========
    v1 = math.sqrt(mu / r1)
    v2 = math.sqrt(mu / r2)
    a_transfer = (r1 + r2) / 2

    v_perigee = math.sqrt(mu * (2/r1 - 1/a_transfer))
    v_apogee = math.sqrt(mu * (2/r2 - 1/a_transfer))

    delta_v1 = abs(v_perigee - v1)
    delta_v2 = abs(v2 - v_apogee)
    return delta_v1, delta_v2, delta_v1 + delta_v2

dv1, dv2, total = hohmann_delta_v(r1, r2)
print(f"Δv1 = {dv1/1000:.2f} km/s")
print(f"Δv2 = {dv2/1000:.2f} km/s")
print(f"Gesamtes Δv = {total/1000:.2f} km/s")

def rocket_equation(delta_v, Isp=320, m0=1000):
    g0 = 9.80665
    mf = m0 * math.exp(-delta_v / (Isp * g0))
    fuel_used = m0 - mf
    return fuel_used, (fuel_used / m0) * 100

fuel, percent = rocket_equation(total)
print(f"Verbrauchtes Treibstoff: {fuel:.2f} kg ({percent:.1f}% von Gesamtmasse)")


isp_values = np.linspace(200, 450, 100)


fuel_list = []
for i in isp_values:
    f, _ = rocket_equation(total, Isp=i)
    fuel_list.append(f)


plt.figure(figsize=(8, 4))
plt.plot(isp_values, fuel_list, color='blue', linewidth=2)
plt.title(f'Treibstoff für LEO -> GEO Transfer ({int(total)} m/s)')
plt.xlabel('Spezifischer Impuls (s)')
plt.ylabel('Treibstoffmasse (kg)')
plt.grid(True, linestyle='--', alpha=0.6)


plt.scatter([320], [fuel], color='red', zorder=5)
plt.text(330, fuel, f'Mein Satellit\n(Isp=320s, Treibstoff={int(fuel)}kg)', color='red')

plt.show()