import math
import random
import matplotlib.pyplot as plt
import csv

# Gravitatieconstante
G = 6.67430e-11
dt = 3600  # 1 uur
stappen = 2400000  # 100000 dagen simulatie

# Massa's (kg)
M = 1.898e27      # Jupiter
m_io = 8.93e22
m_europa = 4.8e22

# Halve lange assen (gemiddelde afstand tot Jupiter, meter)
a_io = 4.22e8
a_eu = 6.71e8

# Excentriciteiten
e_io = 0.0041
e_eu = 0.009

# Start bij perihelium (dichtst bij Jupiter)
r_io = a_io * (1 - e_io)
r_eu = a_eu * (1 - e_eu)

# Vis-viva-vergelijking (snelheid bij perihelium)
v_io = math.sqrt(G * M * (2 / r_io - 1 / a_io))
v_eu = math.sqrt(G * M * (2 / r_eu - 1 / a_eu))

# Genereer beginpositie en -snelheid (richting loodrecht op straalvector)
def random_pos_vel(r, v):
    theta = random.uniform(0, 2 * math.pi)
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    vx = -v * math.sin(theta)
    vy = v * math.cos(theta)
    return x, y, vx, vy

# Beginwaarden
Mx, My, vMx, vMy = 0, 0, 0, 0
iox, ioy, viox, vioy = random_pos_vel(r_io, v_io)
eux, euy, veux, veuy = random_pos_vel(r_eu, v_eu)

# Opslaan van posities
pos_io = []
pos_eu = []
pos_jupiter = []
theta_io = []
theta_eu = []

def hoek(x, y):
    return math.atan2(y - My, x - Mx)

# Simulatie
for step in range(stappen):
    dx_io, dy_io = iox - Mx, ioy - My
    dx_eu, dy_eu = eux - Mx, euy - My

    r_io_curr = math.hypot(dx_io, dy_io)
    r_eu_curr = math.hypot(dx_eu, dy_eu)

    F_io = G * M * m_io / r_io_curr**2
    F_eu = G * M * m_europa / r_eu_curr**2

    Fx_io = -F_io * dx_io / r_io_curr
    Fy_io = -F_io * dy_io / r_io_curr
    Fx_eu = -F_eu * dx_eu / r_eu_curr
    Fy_eu = -F_eu * dy_eu / r_eu_curr

    ax_io = Fx_io / m_io
    ay_io = Fy_io / m_io
    ax_eu = Fx_eu / m_europa
    ay_eu = Fy_eu / m_europa

    viox += ax_io * dt
    vioy += ay_io * dt
    veux += ax_eu * dt
    veuy += ay_eu * dt

    iox += viox * dt
    ioy += vioy * dt
    eux += veux * dt
    euy += veuy * dt

    if step % 240 == 0:  # elke 10 dagen
        pos_io.append((iox, ioy))
        pos_eu.append((eux, euy))
        pos_jupiter.append((Mx, My))
        theta_io.append(hoek(iox, ioy))
        theta_eu.append(hoek(eux, euy))

# Omloopdetectie
def tel_omlopen(theta_lijst):
    count = 0
    for i in range(1, len(theta_lijst)):
        if theta_lijst[i-1] < 0 and theta_lijst[i] >= 0:
            count += 1
    return count

n_io = tel_omlopen(theta_io)
n_eu = tel_omlopen(theta_eu)

# Verhouding vereenvoudigen
def vereenvoudig(a, b):
    from math import gcd
    g = gcd(a, b)
    return a // g, b // g

v1, v2 = vereenvoudig(n_io, n_eu)

# 📊 Resultaten printen
print("📈 Omloopverhouding over de simulatie:")
print(f"Io     : {n_io} omlopen")
print(f"Europa : {n_eu} omlopen")
print(f"➤ Verhouding Io : Europa ≈ {v1}:{v2}")

# 💾 Export naar CSV
with open("posities.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["dag", "iox", "ioy", "eux", "euy", "Mx", "My"])
    for i in range(len(pos_io)):
        iox_, ioy_ = pos_io[i]
        eux_, euy_ = pos_eu[i]
        Mx_, My_ = pos_jupiter[i]
        writer.writerow([i * 10, iox_, ioy_, eux_, euy_, Mx_, My_])

print("✅ Posities opgeslagen in 'posities.csv'.")

# 📈 Plot
iox_list, ioy_list = zip(*pos_io)
eux_list, euy_list = zip(*pos_eu)
Mx_list, My_list = zip(*pos_jupiter)

plt.figure(figsize=(10, 10))
plt.plot(iox_list, ioy_list, label="Io", color="orange")
plt.plot(eux_list, euy_list, label="Europa", color="blue")
plt.plot(Mx_list, My_list, 'o', label="Jupiter", color="gray", markersize=4)

plt.xlabel("x (meter)")
plt.ylabel("y (meter)")
plt.title("Banen van Io en Europa met elliptische banen (resonantieonderzoek)")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
