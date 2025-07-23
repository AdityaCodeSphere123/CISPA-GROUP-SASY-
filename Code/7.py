import math
import matplotlib.pyplot as plt

def calculate_delta_min(n, d):
    x = math.log(2) * 60
    return math.sqrt(x / (d * n))

# Parameters
d_values = [2, 50, 250, 1000]
n_values = range(1, 501, 5)

print("Calculating delta_min and cost function for various d, n values\n")
print(f"{'d':>6} {'n':>8} {'delta_min':>10} {'cost':>12}")

all_costs = {}

# Plot each graph individually
for d in d_values:
    costs = []
    ns = []

    for n in n_values:
        delta_min = calculate_delta_min(n, d)
        cost = ((1 + delta_min) * d * n) / 4

        costs.append(cost)
        ns.append(n)

        print(f"{d:6} {n:8} {delta_min:10.4f} {cost:12.2f}")

    # Save for later
    all_costs[d] = (ns, costs)

    # Individual plot
    plt.figure(figsize=(8, 5))
    plt.plot(ns, costs, label=f'd={d}', color='blue')
    plt.xlabel("n (number of iterations)")
    plt.ylabel("Cost = ((1 + δ_min) × d × n) / 4")
    plt.title(f"Cost vs n for d = {d}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Combined plot
plt.figure(figsize=(10, 6))
for d in d_values:
    ns, costs = all_costs[d]
    plt.plot(ns, costs, label=f'd={d}')

plt.xlabel("n (number of iterations)")
plt.ylabel("Cost = ((1 + δ_min) × d × n) / 4")
plt.title("Cost vs n for different d values (Combined Plot)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
