import math
import matplotlib.pyplot as plt
import csv

# Constantes
G = 6.67430e-11     # Gravitatieconstante in m^3/kg/s^2
dt = 100000          # Tijdsinterval: 1 uur (in seconden)
stappen = 5_000_000 # Simuleer 5 miljoen uur (~570 jaar)

# Massa's (in kg)
M = 0.37 * 1.9885e30      # Gliese 876 (ster)
m1 = 0.7142 * 1.898e27     # Gliese 876 c (binnenste)
m2 = 2.275 * 1.898e27     # Gliese 876 b (buitenste)

# Gemiddelde afstand tot ster (in meter)
r1 = 0.130 * 1.496e11     # Gliese 876 c
r2 = 0.208 * 1.496e11     # Gliese 876 b

# Excentriciteiten
e1 = 0.256                # Gliese 876 c
e2 = 0.032                # Gliese 876 b

# Cirkelsnelheden
v1_circ = math.sqrt(G * M / r1)
v2_circ = math.sqrt(G * M / r2)

# Beginsnelheden aangepast voor elliptische baan (op apoapsis)
v1 = v1_circ * math.sqrt((1 - e1) / (1 + e1))
v2 = v2_circ * math.sqrt((1 - e2) / (1 + e2))

# Beginposities (op apoapsis)
Mx, My = 0, 0
m1x, m1y = r1 * (1 + e1), 0       # Gliese 876 c
m2x, m2y = 0, r2 * (1 + e2)       # Gliese 876 b

# Beginsnelheden (loodrecht op straalvector)
vMx, vMy = 0, 0
vm1x, vm1y = 0, -v1               # Gliese 876 c
vm2x, vm2y = v2, 0                # Gliese 876 b

# Positielijsten
uren = []
posities_m1 = []
posities_m2 = []
posities_M = []

# Simulatie
for step in range(stappen):
    # Afstanden
    dxMm1 = m1x - Mx
    dyMm1 = m1y - My
    dxMm2 = m2x - Mx
    dyMm2 = m2y - My
    dxm1m2 = m2x - m1x
    dym1m2 = m2y - m1y

    rMm1 = math.hypot(dxMm1, dyMm1)
    rMm2 = math.hypot(dxMm2, dyMm2)
    rm1m2 = math.hypot(dxm1m2, dym1m2)

    # Gravitatiekrachten
    FzMm1 = G * M * m1 / rMm1**2
    FzMm2 = G * M * m2 / rMm2**2
    Fzm1m2 = G * m1 * m2 / rm1m2**2

    # Richtingen van krachten
    FzMm1x = FzMm1 * dxMm1 / rMm1
    FzMm1y = FzMm1 * dyMm1 / rMm1

    FzMm2x = FzMm2 * dxMm2 / rMm2
    FzMm2y = FzMm2 * dyMm2 / rMm2

    Fzm1m2x = Fzm1m2 * dxm1m2 / rm1m2
    Fzm1m2y = Fzm1m2 * dym1m2 / rm1m2

    # Totale krachten
    FMx = FzMm1x + FzMm2x
    FMy = FzMm1y + FzMm2y

    Fm1x = -FzMm1x + Fzm1m2x
    Fm1y = -FzMm1y + Fzm1m2y

    Fm2x = -FzMm2x - Fzm1m2x
    Fm2y = -FzMm2y - Fzm1m2y

    # Versnellingen
    aMx = FMx / M
    aMy = FMy / M

    am1x = Fm1x / m1
    am1y = Fm1y / m1

    am2x = Fm2x / m2
    am2y = Fm2y / m2

    # Snelheden bijwerken
    vMx += aMx * dt
    vMy += aMy * dt

    vm1x += am1x * dt
    vm1y += am1y * dt

    vm2x += am2x * dt
    vm2y += am2y * dt

    # Posities bijwerken
    Mx += vMx * dt
    My += vMy * dt

    m1x += vm1x * dt
    m1y += vm1y * dt

    m2x += vm2x * dt
    m2y += vm2y * dt

    # Opslaan van eerste 1000 en laatste 1000 uur
    if step < 10000 :
        uren.append(step)
        posities_m1.append((m1x, m1y))
        posities_m2.append((m2x, m2y))
        posities_M.append((Mx, My))

print("✅ Simulatie voltooid. Eerste en laatste 1000 uurposities opgeslagen.")

# CSV-export
with open("posities_gliese876_bc.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["uur", "c_x", "c_y", "b_x", "b_y", "ster_x", "ster_y"])
    for i in range(len(uren)):
        m1x_i, m1y_i = posities_m1[i]
        m2x_i, m2y_i = posities_m2[i]
        Mx_i, My_i = posities_M[i]
        writer.writerow([uren[i], m1x_i, m1y_i, m2x_i, m2y_i, Mx_i, My_i])

print("✅ Posities opgeslagen in 'posities_gliese876_bc.csv'.")

# Visualisatie
m1x_list, m1y_list = zip(*posities_m1)
m2x_list, m2y_list = zip(*posities_m2)
Mx_list, My_list = zip(*posities_M)

plt.figure(figsize=(10, 10))
plt.plot(m1x_list, m1y_list, label="Gliese 876 c (e ≈ 0.255)", color="blue")
plt.plot(m2x_list, m2y_list, label="Gliese 876 b (e ≈ 0.032)", color="green")
plt.plot(Mx_list, My_list, 'o', color="orange", label="Gliese 876 (ster)", markersize=3)

plt.xlabel("x (meter)")
plt.ylabel("y (meter)")
plt.title("Begin- en eindbanen van Gliese 876 b en c (Laplace-resonantie, dt = 1 uur)")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()