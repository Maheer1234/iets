import math

# Constantes
G = 6.67430e-11       # Gravitatieconstante (m³/kg/s²)
dt = 86400            # Tijdsinterval (1 dag in seconden)
dagen = 10000         # Aantal iteraties (bijv. 10.000 dagen)

# Massa's
M = 1.989e30          # Zon
m1 = 5.972e24         # Aarde
m2 = 6.417e23         # Mars

# Beginposities (x, y)
Mx, My = 0, 0
m1x, m1y = 1.496e11, 0
m2x, m2y = 0, 2.279e11

# Beginsnelheden (x, y)
vMx, vMy = 0, 0
vm1x, vm1y = 0, 29780
vm2x, vm2y = 24070, 0

# (Optioneel) Posities bijhouden om te plotten
posities_m1 = []
posities_m2 = []
posities_M  = []

for step in range(dagen):
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

    # Krachten (schaalwaarden)
    FzMm1 = G * M * m1 / rMm1**2
    FzMm2 = G * M * m2 / rMm2**2
    Fzm1m2 = G * m1 * m2 / rm1m2**2

    # Richtingscomponenten krachten
    FzMm1x = FzMm1 * dxMm1 / rMm1
    FzMm1y = FzMm1 * dyMm1 / rMm1

    FzMm2x = FzMm2 * dxMm2 / rMm2
    FzMm2y = FzMm2 * dyMm2 / rMm2

    Fzm1m2x = Fzm1m2 * dxm1m2 / rm1m2
    Fzm1m2y = Fzm1m2 * dym1m2 / rm1m2

    # Resultante krachten
    FMx = FzMm1x + FzMm2x
    FMy = FzMm1y + FzMm2y

    Fm1x = -FzMm1x + Fzm1m2x
    Fm1y = -FzMm1y + Fzm1m2y

    Fm2x = -FzMm2x - Fzm1m2x
    Fm2y = -FzMm2y - Fzm1m2y

    # Versnellingen (a = F/m) * dt
    vMx += (FMx / M) * dt
    vMy += (FMy / M) * dt

    vm1x += (Fm1x / m1) * dt
    vm1y += (Fm1y / m1) * dt

    vm2x += (Fm2x / m2) * dt
    vm2y += (Fm2y / m2) * dt

    # Positie updates
    Mx += vMx * dt
    My += vMy * dt

    m1x += vm1x * dt
    m1y += vm1y * dt

    m2x += vm2x * dt
    m2y += vm2y * dt

    # Posities opslaan (elke 10 stappen)
    if step % 10 == 0:
        posities_m1.append((m1x, m1y))
        posities_m2.append((m2x, m2y))
        posities_M.append((Mx, My))
    import matplotlib.pyplot as plt

    # Posities splitsen in x- en y-lijsten
    m1x_list, m1y_list = zip(*posities_m1)
    m2x_list, m2y_list = zip(*posities_m2)
    Mx_list, My_list = zip(*posities_M)

    plt.figure(figsize=(8, 8))
    plt.plot(m1x_list, m1y_list, label="Aarde", color="blue")
    plt.plot(m2x_list, m2y_list, label="Mars", color="red")
    plt.plot(Mx_list, My_list, label="Zon", color="orange")

    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Banen van Aarde en Mars rond de Zon")
    plt.axis("equal")
    plt.legend()
    plt.grid(True)
    plt.show()
