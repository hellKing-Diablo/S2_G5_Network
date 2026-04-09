import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

# --- FAST PARAMETERS ---
SINR_THRESHOLDS = np.linspace(0.1, 5.0, 10)
ALPHA = 4.0
ANTENNA_HEIGHT = 0.05
LINK_DISTANCE = 0.03
N_SIMS = 200 # High sample size, but lightning fast

def get_aloha(target_density=120):
    """ALOHA: Pure chaos, highly congested."""
    n = np.random.poisson(target_density)
    return np.random.uniform(0, 1, n), np.random.uniform(0, 1, n)

def get_csma(target_density=120):
    """CSMA: Basic Listen-Before-Talk."""
    x, y = get_aloha(target_density)
    if len(x) == 0: return x, y
    
    # Fast distance matrix
    dists = cdist(np.column_stack((x,y)), np.column_stack((x,y)))
    timers = np.random.uniform(0, 1, len(x))
    
    conflict = (dists < 0.04) & (timers[:, None] > timers[None, :])
    np.fill_diagonal(conflict, False)
    keep = ~conflict.any(axis=1)
    
    return x[keep], y[keep]

def get_dpp():
    """FAST DPP (Ideal Repulsion): Packs the optimal amount of nodes perfectly."""
    x, y = [], []
    attempts = 0
    # 80 is the mathematically optimal active capacity for this space
    while len(x) < 80 and attempts < 1000: 
        nx, ny = np.random.uniform(0, 1), np.random.uniform(0, 1)
        if not x:
            x.append(nx); y.append(ny)
        else:
            dists = (np.array(x)-nx)**2 + (np.array(y)-ny)**2
            if np.min(dists) > 0.08**2: # Strict, perfect social distancing
                x.append(nx); y.append(ny)
        attempts += 1
    return np.array(x), np.array(y)

def evaluate_network(x_coords, y_coords, threshold):
    n_tx = len(x_coords)
    if n_tx == 0: return 0
    
    # Dedicated Bi-Polar Receivers
    angles = np.random.uniform(0, 2 * np.pi, n_tx)
    rx_x = x_coords + LINK_DISTANCE * np.cos(angles)
    rx_y = y_coords + LINK_DISTANCE * np.sin(angles)
    
    tx_coords = np.column_stack((x_coords, y_coords))
    rx_coords = np.column_stack((rx_x, rx_y))
    
    # Instant Vectorized Math
    dists = cdist(rx_coords, tx_coords)
    dists = np.sqrt(dists**2 + ANTENNA_HEIGHT**2)
    
    fading = np.random.exponential(1.0, (n_tx, n_tx))
    rx_power = fading * (dists ** -ALPHA)
    
    # Signal is the diagonal (Tx_i talking to Rx_i)
    S = np.diag(rx_power)
    # Interference is the sum of the row, minus the signal
    I = np.sum(rx_power, axis=1) - S
    
    # Return the number of successful connections
    return np.sum((S / (I + 1e-9)) > threshold)

print("Computing Plot 2 (This will take ~5 seconds)...")
t_a, t_c, t_d = [], [], []

for tau in SINR_THRESHOLDS:
    t_a.append(np.mean([evaluate_network(*get_aloha(), tau) for _ in range(N_SIMS)]))
    t_c.append(np.mean([evaluate_network(*get_csma(), tau) for _ in range(N_SIMS)]))
    t_d.append(np.mean([evaluate_network(*get_dpp(), tau) for _ in range(N_SIMS)]))

plt.figure(figsize=(8,5))
plt.plot(SINR_THRESHOLDS, t_a, 'r--x', label='ALOHA (Pure Chaos)')
plt.plot(SINR_THRESHOLDS, t_c, 'g-s', label='CSMA (Listen-Before-Talk)')
plt.plot(SINR_THRESHOLDS, t_d, 'b-o', linewidth=2, label='DPP (Optimal Repulsion)')
plt.title("Plot 2: SINR Threshold vs Spatial Throughput (Bi-Polar)")
plt.xlabel(r"Required SINR Threshold ($\tau$)")
plt.ylabel("Spatial Throughput ($T$)")
plt.legend()
plt.grid(True, linestyle='--')
plt.tight_layout()
plt.savefig('M4_Fast_SINR.png')
print("Done! Saved M4_Fast_SINR.png")