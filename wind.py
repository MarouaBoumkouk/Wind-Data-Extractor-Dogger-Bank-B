import numpy as np
import matplotlib.pyplot as plt
from py_wake import NOJ
from py_wake.site import UniformSite
from py_wake.examples.data.hornsrev1 import V80

# --------------------------
# STEP 1: Manual Turbine Coordinates
# --------------------------
x_coords = [259927, 261371, 256818, 250732, 249284,
            247957, 253940, 267450, 246194, 263322, 253969]
y_coords = [i * 500 for i in range(len(x_coords))]

turbines = np.array(list(zip(x_coords, y_coords)))

# --------------------------
# STEP 2: PyWake Setup
# --------------------------
# Use simple wind conditions: 1 wind direction, low turbulence
site = UniformSite(p_wd=[1], ti=0.1)

# Use built-in V80 turbine model
turbine = V80()

# Use the NOJ wake model
model = NOJ(site, turbine)

# Run the simulation
result = model(x_coords, y_coords)

# Calculate AEP (Annual Energy Production)
total_aep = result.aep().sum()
print(f"Total AEP: {total_aep:.2f} GWh")

# --------------------------
# STEP 3: Visualization
# --------------------------
# Boundary around the wind farm
buffer = 1000
boundary_x = [min(x_coords)-buffer, max(x_coords)+buffer, max(x_coords)+buffer,
              min(x_coords)-buffer, min(x_coords)-buffer]
boundary_y = [min(y_coords)-buffer, min(y_coords)-buffer, max(y_coords)+buffer,
              max(y_coords)+buffer, min(y_coords)-buffer]

# Cable connections
connections = [(i, i+1) for i in range(len(turbines)-1)]

# Plot
plt.figure(figsize=(12, 6))
plt.plot(boundary_x, boundary_y, 'b-', label="Wind Farm Boundary")

# Cable lines
for i, j in connections:
    plt.plot([turbines[i][0], turbines[j][0]],
             [turbines[i][1], turbines[j][1]],
             color='gray', linewidth=1)

# Turbines
plt.scatter(turbines[:, 0], turbines[:, 1], color='orange', label="Turbines", zorder=5)

# Labels
for i, (x, y) in enumerate(turbines):
    plt.text(x, y + 150, f"T{i+1}", ha='center', fontsize=8)

# Final touches
plt.xlabel("Distance to Shore (m)")
plt.ylabel("Y Position (arbitrary)")
plt.title("Dogger Bank B – Turbine Layout with PyWake AEP Simulation")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
