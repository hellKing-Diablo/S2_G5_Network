import numpy as np
import matplotlib.pyplot as plt

DENSITIES = np.arange(10, 200, 20)
ALPHA = 4.0
ANTENNA_HEIGHT = 0.05
N_SIMS = 500 

def get_deterministic_square(density):
    points = int(np.sqrt(density))
    if points < 1: points = 1
    x, y = np.meshgrid(np.linspace(0.1, 0.9, points), np.linspace(0.1, 0.9, points))
    return x.flatten(), y.flatten()

def get_aloha_ppp(density):
    n_points = np.random.poisson(density)
    return np.random.uniform(0.05, 0.95, n_points), np.random.uniform(0.05, 0.95, n_points)

def evaluate_network(x_coords, y_coords):
    n_tx = len(x_coords)
    if n_tx == 0: return 0
    
    # THE FIX: Randomize the 100 receiver locations to prevent Grid Resonance!
    # Instead of a rigid meshgrid, we scatter the users randomly across the city.
    rx_x = np.random.uniform(0.1, 0.9, 100)
    rx_y = np.random.uniform(0.1, 0.9, 100)
    
    successes = 0
    for i in range(100):
        # Calculate distance to all towers for this specific random user
        dists = np.sqrt((x_coords - rx_x[i])**2 + (y_coords - rx_y[i])**2 + ANTENNA_HEIGHT**2)
        rx_power = np.random.exponential(1.0, n_tx) * (dists ** -ALPHA)
        
        S = np.max(rx_power)
        I = np.sum(rx_power) - S
        
        if (S / (I + 1e-9)) > 1.0: # SINR Threshold = 1.0
            successes += 1
            
    return n_tx * (successes / 100)

print("Generating Plot 1: Deterministic vs ALOHA...")
t_det, t_aloha = [], []

for d in DENSITIES:
    t_det.append(np.mean([evaluate_network(*get_deterministic_square(d)) for _ in range(N_SIMS)]))
    t_aloha.append(np.mean([evaluate_network(*get_aloha_ppp(d)) for _ in range(N_SIMS)]))

plt.figure(figsize=(8,5))
plt.plot(DENSITIES, t_det, 'b-o', label='M3: Deterministic Grid (Planned)')
plt.plot(DENSITIES, t_aloha, 'r--x', label='M4: ALOHA (Random Chaos)')
plt.title("Plot 1: Impact of Randomness on Spatial Throughput")
plt.xlabel(r"Target Density ($\lambda$)")
plt.ylabel(r"Spatial Throughput ($T$)")
plt.legend()
plt.grid(True, linestyle='--')
plt.tight_layout()
plt.savefig('M4_Plot1_Aloha_vs_Det.png')
print("Saved M4_Plot1_Aloha_vs_Det.png")
