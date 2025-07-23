import numpy as np
import matplotlib.pyplot as plt

V = 1000 
d_values = [2, 10, 50, 100, 250]

x = np.linspace(V/2, V - 1e-6, 500)

# Plot individual graphs for each d value
for d in d_values:
    plt.figure(figsize=(10, 6))
    y = ((V * (d - 1) / 2) - x) / (V - x)
    plt.plot(x, y, label=f'((V(d-1)/2) - x)/(V - x), d = {d}', linewidth=2)
    plt.axhline(y=d, color='red', linestyle='--', label=f'y = {d}', linewidth=2)
    
    plt.title(f'Plot for d = {d}')
    plt.xlabel('x')
    plt.ylabel('Expression value')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Plot all d values in a single graph
plt.figure(figsize=(12, 8))

for d in d_values:
    y = ((V * (d - 1) / 2) - x) / (V - x)
    plt.plot(x, y, label=f'd = {d}', linewidth=2)

plt.title('Plot of ((V(d - 1)/2) - x)/(V - x) for various d')
plt.xlabel('x')
plt.ylabel('Expression value')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
