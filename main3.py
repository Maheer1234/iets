import math
import random
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11
dt = 3600  # 1 hour
stappen = 240000  # 10000 dagen

# Masses
M = 1.898e27      # Jupiter
m_io = 8.93e22
m_eu = 4.8e22

# Halve lange assen en excentriciteit
a_io = 4.22e8
e_io = 0.0041

a_eu = 6.71e8
e_eu = 0.009

# Functie: willekeurige positie en snelheid op elliptische baan
def init_pos_vel(a, e, M_mass):
    theta = random.uniform(0, 2 * math.pi)
    r = a * (1 - e**2) / (1 + e * math.cos(theta))
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    mu = G * M_mass
    v = math.sqrt(mu * (2 / r - 1 / a))
    vx = -v * math.sin(theta)
    vy = v * math.cos(theta)
    return x, y, vx, vy

# Startposities en snelheden
iox, ioy, viox, vioy = init_pos_vel(a_io, e_io, M)
eux, euy, veux, veuy = init_pos_vel(a_eu, e_eu, M)

# Jupiter
Mx, My = 0.0, 0.0

# Lijsten
pos_io = []
pos_eu = []
theta_io = []
theta_eu = []

def hoek(x, y):
    return math.atan2(y - My, x - Mx)

# Simulatie
for step in range(stappen):
    # Io → alleen zwaartekracht van Jupiter
    dx_io = iox - Mx
    dy_io = ioy - My
    r_io = math.hypot(dx_io, dy_io)
    F_io = G * M * m_io / r_io**2
    a_iox = -F_io * dx_io / r_io / m_io
    a_ioy = -F_io * dy_io / r_io / m_io

    # Europa → alleen zwaartekracht van Jupiter
    dx_eu = eux - Mx
    dy_eu = euy - My
    r_eu = math.hypot(dx_eu, dy_eu)
    F_eu = G * M * m_eu / r_eu**2
    a_eux = -F_eu * dx_eu / r_eu / m_eu
    a_euy = -F_eu * dy_eu / r_eu / m_eu

    # Snelheden bijwerken
    viox += a_iox * dt
    vioy += a_ioy * dt
    veux += a_eux * dt
    veuy += a_euy * dt

    # Posities bijwerken
    iox += viox * dt
    ioy += vioy * dt
    eux += veux * dt
    euy += veuy * dt

    # Hoeken en posities opslaan
    if step % 240 == 0:
        pos_io.append((iox, ioy))
        pos_eu.append((eux, euy))
        theta_io.append(hoek(iox, ioy))
        theta_eu.append(hoek(eux, euy))

# Omlooptelling (aan hand van 0-passage in hoek)
def tel_omlopen(theta_lijst):
    count = 0
    for i in range(1, len(theta_lijst)):
        if theta_lijst[i-1] < 0 <= theta_lijst[i]:
            count += 1
    return count

n_io = tel_omlopen(theta_io)
n_eu = tel_omlopen(theta_eu)

from math import gcd
def vereenvoudig(a, b):
    g = gcd(a, b)
    return a // g, b // g

v1, v2 = vereenvoudig(n_io, n_eu)

print("\n🧪 Simulatie zonder onderlinge gravitatie")
print(f"Io omlopen: {n_io}")
print(f"Europa omlopen: {n_eu}")
print(f"Verhouding Io : Europa ≈ {v1}:{v2} ({n_io/n_eu:.4f})")
# Verhouding van omwentelingen over tijd
verhouding_tijd = []
omlopen_io = 0
omlopen_eu = 0

for i in range(1, len(theta_io)):
    if theta_io[i-1] < 0 <= theta_io[i]:
        omlopen_io += 1
    if theta_eu[i-1] < 0 <= theta_eu[i]:
        omlopen_eu += 1
    if omlopen_eu > 0:
        verhouding_tijd.append(omlopen_io / omlopen_eu)
    else:
        verhouding_tijd.append(None)  # Voorkom deling door 0

# Tijden in dagen
tijden = [i * 10 for i in range(len(verhouding_tijd))]

# Plot verhouding in de tijd
plt.figure(figsize=(10, 5))
plt.plot(tijden, verhouding_tijd, label="Io / Europa omloopverhouding", color="purple")
plt.axhline(2.0, color="gray", linestyle="--", label="2:1 resonantie")
plt.xlabel("Tijd (dagen)")
plt.ylabel("Omloopverhouding")
plt.title("Verhouding Io : Europa omwentelingen in de tijd")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Plot banen
iox_list, ioy_list = zip(*pos_io)
eux_list, euy_list = zip(*pos_eu)

plt.figure(figsize=(10, 10))
plt.plot(iox_list, ioy_list, label="Io", color="orange")
plt.plot(eux_list, euy_list, label="Europa", color="blue")
plt.plot([0], [0], 'o', color="gray", markersize=6, label="Jupiter")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Io en Europa zonder onderlinge zwaartekracht (geen resonantie mogelijk)")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.show()

# Verhouding van omwentelingen over tijd
...
plt.show()
