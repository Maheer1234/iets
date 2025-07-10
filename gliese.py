import math
import matplotlib.pyplot as plt
import csv

# Constantes
G = 6.67430e-11
dt = 100000
stappen = 5_000_000

# Massa's
M = 0.37 * 1.9885e30
m1 = 0.7142 * 1.898e27
m2 = 2.275 * 1.898e27

# Afstanden
r1 = 0.130 * 1.496e11
r2 = 0.208 * 1.496e11

# Excentriciteiten
e1 = 0.256
e2 = 0.032

# Beginsnelheden (apoapsis)
v1_circ = math.sqrt(G * M / r1)
v2_circ = math.sqrt(G * M / r2)
v1 = v1_circ * math.sqrt((1 - e1) / (1 + e1))
v2 = v2_circ * math.sqrt((1 - e2) / (1 + e2))

# Beginposities
Mx, My = 0, 0
m1x, m1y = r1 * (1 + e1), 0
m2x, m2y = 0, r2 * (1 + e2)

# Beginsnelheden
vMx, vMy = 0, 0
vm1x, vm1y = 0, -v1
vm2x, vm2y = v2, 0

# Opslag
uren = []
vx_m1, vx_m2, vx_M = [], [], []
pos_m1, pos_m2, pos_M = [], [], []

# Simulatie
for step in range(stappen):
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

    FzMm1x = FzMm1 * dxMm1 / rMm1
    FzMm1y = FzMm1 * dyMm1 / rMm1
    FzMm2x = FzMm2 * dxMm2 / rMm2
    FzMm2y = FzMm2 * dyMm2 / rMm2
    Fzm1m2x = Fzm1m2 * dxm1m2 / rm1m2
    Fzm1m2y = Fzm1m2 * dym1m2 / rm1m2

    FMx = FzMm1x + FzMm2x
    FMy = FzMm1y + FzMm2y
    Fm1x = -FzMm1x + Fzm1m2x
    Fm1y = -FzMm1y + Fzm1m2y
    Fm2x = -FzMm2x - Fzm1m2x
    Fm2y = -FzMm2y - Fzm1m2y

    aMx = FMx / M
    aMy = FMy / M
    am1x = Fm1x / m1
    am1y = Fm1y / m1
    am2x = Fm2x / m2
    am2y = Fm2y / m2

    vMx += aMx * dt
    vMy += aMy * dt
    vm1x += am1x * dt
    vm1y += am1y * dt
    vm2x += am2x * dt
    vm2y += am2y * dt

    Mx += vMx * dt
    My += vMy * dt
    m1x += vm1x * dt
    m1y += vm1y * dt
    m2x += vm2x * dt
    m2y += vm2y * dt

    # Alleen eerste 1000 uur (stap 990001 t/m 1.000.000)
    if 990000 < step <= 1000000:
        uren.append(step)
        vx_m1.append(vm1x)
        vx_m2.append(vm2x)
        vx_M.append(vMx)
        pos_m1.append((m1x, m1y))
        pos_m2.append((m2x, m2y))
        pos_M.append((Mx, My))

print("✅ Simulatie voltooid. Snelheden en coördinaten opgeslagen.")

# CSV-export
with open("gliese876_snelheden_coordinaten.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["uur", "vx_c", "x_c", "y_c", "vx_b", "x_b", "y_b", "vx_ster", "x_ster", "y_ster"])
    for i in range(len(uren)):
        m1x_i, m1y_i = pos_m1[i]
        m2x_i, m2y_i = pos_m2[i]
        Mx_i, My_i = pos_M[i]
        writer.writerow([uren[i], vx_m1[i], m1x_i, m1y_i, vx_m2[i], m2x_i, m2y_i, vx_M[i], Mx_i, My_i])

print("✅ Data opgeslagen in 'gliese876_snelheden_coordinaten.csv'.")

# Plot 1: x-snelheden
plt.figure(figsize=(10, 6))
plt.plot(uren, vx_m1, label="vx Gliese 876 c", color="blue")
plt.plot(uren, vx_m2, label="vx Gliese 876 b", color="green")
plt.plot(uren, vx_M, label="vx ster", color="orange")
plt.xlabel("Tijd (uur)")
plt.ylabel("x-snelheid (m/s)")
plt.title("x-snelheid over tijd (laatste 1000 uur)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot 2: banen in x-y
m1x_list, m1y_list = zip(*pos_m1)
m2x_list, m2y_list = zip(*pos_m2)
Mx_list, My_list = zip(*pos_M)

plt.figure(figsize=(8, 8))
plt.plot(m1x_list, m1y_list, label="baan Gliese 876 c", color="blue")
plt.plot(m2x_list, m2y_list, label="baan Gliese 876 b", color="green")
plt.plot(Mx_list, My_list, 'o', label="baan ster", color="orange", markersize=3)
plt.xlabel("x (meter)")
plt.ylabel("y (meter)")
plt.title("Banen van Gliese 876 b, c en ster (laatste 1000 uur)")
plt.legend()
plt.axis("equal")
plt.grid(True)
plt.tight_layout()
plt.show()
