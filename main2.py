import math
import random
import matplotlib.pyplot as plt

# Constantes
G = 6.67430e-11
dt = 3600  # 1 uur
stappen = 240000  # 10000 dagen

# Massa's (kg)
M = 1.898e27
m_io = 8.93e22
m_eu = 4.8e22

# Gemiddelde halve lange assen (m)
a_io = 4.22e8
a_eu = 6.71e8

# Excentriciteiten
e_io = 0.0041
e_eu = 0.009

# Functie om startpositie en snelheid te genereren op een elliptische baan,
# maar met een willekeurige fase (theta)
def init_pos_vel(a, e, mass, M_mass):
    theta = random.uniform(0, 2 * math.pi)
    r = a * (1 - e**2) / (1 + e * math.cos(theta))
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    # Vis-viva voor snelheid
    mu = G * M_mass
    v = math.sqrt(mu * (2 / r - 1 / a))
    # Snelheidsrichting loodrecht op straalvector (fase + 90 graden)
    vx = -v * math.sin(theta)
    vy = v * math.cos(theta)
    return x, y, vx, vy

# Start Jupiter in het centrum
Mx, My = 0.0, 0.0
vMx, vMy = 0.0, 0.0

# Startwaarden Io en Europa met random fase
iox, ioy, viox, vioy = init_pos_vel(a_io, e_io, m_io, M)
eux, euy, veux, veuy = init_pos_vel(a_eu, e_eu, m_eu, M)

# Posities en hoeken voor omlooptelling
pos_io = []
pos_eu = []
theta_io = []
theta_eu = []

def hoek(x, y):
    return math.atan2(y - My, x - Mx)

# Functie om krachten tussen twee lichamen te berekenen
def kracht(m1, m2, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    r = math.hypot(dx, dy)
    if r == 0:
        return 0, 0
    F = G * m1 * m2 / r**2
    Fx = F * dx / r
    Fy = F * dy / r
    return Fx, Fy

# Simulatie loop
for step in range(stappen):
    # Krachten op Jupiter
    F_Mx, F_My = 0.0, 0.0

    # Krachten op Io
    F_iox, F_ioy = 0.0, 0.0

    # Krachten op Europa
    F_eux, F_euy = 0.0, 0.0

    # Jupiter - Io
    Fx, Fy = kracht(M, m_io, Mx, My, iox, ioy)
    F_Mx += Fx
    F_My += Fy
    F_iox -= Fx
    F_ioy -= Fy

    # Jupiter - Europa
    Fx, Fy = kracht(M, m_eu, Mx, My, eux, euy)
    F_Mx += Fx
    F_My += Fy
    F_eux -= Fx
    F_euy -= Fy

    # Io - Europa
    Fx, Fy = kracht(m_io, m_eu, iox, ioy, eux, euy)
    F_iox += Fx
    F_ioy += Fy
    F_eux -= Fx
    F_euy -= Fy

    # Versnellingen
    a_Mx = F_Mx / M
    a_My = F_My / M

    a_iox = F_iox / m_io
    a_ioy = F_ioy / m_io

    a_eux = F_eux / m_eu
    a_euy = F_euy / m_eu

    # Snelheden updaten
    vMx += a_Mx * dt
    vMy += a_My * dt

    viox += a_iox * dt
    vioy += a_ioy * dt

    veux += a_eux * dt
    veuy += a_euy * dt

    # Posities updaten
    Mx += vMx * dt
    My += vMy * dt

    iox += viox * dt
    ioy += vioy * dt

    eux += veux * dt
    euy += veuy * dt

    # Posities en hoeken opslaan elke 10 dagen (240 stappen)
    if step % 240 == 0:
        pos_io.append((iox, ioy))
        pos_eu.append((eux, euy))
        theta_io.append(hoek(iox, ioy))
        theta_eu.append(hoek(eux, euy))

    # Elke 10000 dagen (1/24 van totale sim) printen we omlooptelling
    if step % (240 * 1000) == 0 and step > 0:
        def tel_omlopen(theta_lijst):
            count = 0
            for i in range(1, len(theta_lijst)):
                if theta_lijst[i-1] < 0 <= theta_lijst[i]:
                    count += 1
            return count
        n_io = tel_omlopen(theta_io)
        n_eu = tel_omlopen(theta_eu)
        print(f"Na {step*dt/86400:.0f} dagen: Io omlopen={n_io}, Europa omlopen={n_eu}, verhouding ≈ {n_io/n_eu:.4f}")

# Definitieve omlooptelling
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

print("\n✅ Simulatie voltooid!")
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

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 10))
plt.plot(iox_list, ioy_list, label="Io", color="orange")
plt.plot(eux_list, euy_list, label="Europa", color="blue")
plt.plot([Mx], [My], 'o', color="gray", markersize=6, label="Jupiter")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Baan Io en Europa met onderlinge gravitatie en willekeurige startposities")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.show()
# Verhouding van omwentelingen over tijd
...
plt.show()
