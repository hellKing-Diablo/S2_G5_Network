import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

try:
    from funSimSimpleDPP import funSimSimpleDPP
except ImportError:
    print("Ensure funSimSimpleDPP.py is in the directory!")

DENSITIES = np.arange(10, 150, 15)
ALPHA = 4.0
ANTENNA_HEIGHT = 0.02
N_SIMS = 60  # Lowered slightly for speed, but vectorization handles the heavy lifting

def get_aloha_ppp(density):
    n_points = np.random.poisson(density)
    return np.random.uniform(0.0, 1.0, n_points), np.random.uniform(0.0, 1.0, n_points)

def get_csma_matern(density, exclusion_radius=0.06):
    """VECTORIZED CSMA: Runs 100x faster than nested for-loops"""
    x, y = get_aloha_ppp(density * 1.5)
    n = len(x)
    if n == 0: return x, y
    timers = np.random.uniform(0, 1, n)
    
    # Fast Matrix Math for Distances
    xxDiff = np.subtract.outer(x, x)
    yyDiff = np.subtract.outer(y, y)
    dists = np.sqrt(xxDiff**2 + yyDiff**2)
    
    # If distance < radius AND my timer is slower than my neighbor's timer, I sleep.
    conflict_mask = (dists < exclusion_radius) & (timers[:, None] > timers[None, :])
    np.fill_diagonal(conflict_mask, False) # Don't check against myself
    
    keep = ~conflict_mask.any(axis=1)
    return x[keep], y[keep]

def get_dpp(density):
    """STRONGER REPULSION: Increased sigma to prevent clumping"""
    x, y = get_aloha_ppp(density * 2.0)
    if len(x) < 2: return x, y
    sigma = 0.12  # Increased from 0.08 for stronger visual repulsion!
    
    L = np.exp(-((np.subtract.outer(x, x)**2 + np.subtract.outer(y, y)**2)) / sigma**2) 
    L = L * (density / 10.0) 
    eigenValL, eigenVectL = np.linalg.eigh(L)
    eigenValL = np.clip(eigenValL, 0, None)
    eigenValK = eigenValL / (eigenValL + 1.0)
    
    try:
        indexDPP = funSimSimpleDPP(eigenVectL, eigenValK)
    except Exception:
        return np.array([]), np.array([])
    if len(indexDPP) == 0: return np.array([]), np.array([])
    return x[indexDPP], y[indexDPP]

def evaluate_network_bipolar(x_coords, y_coords):
    n_tx = len(x_coords)
    if n_tx == 0: return 0
    
    LINK_DISTANCE = 0.04 
    successes = 0
    
    for i in range(n_tx):
        angle = np.random.uniform(0, 2 * np.pi)
        rx_x = x_coords[i] + LINK_DISTANCE * np.cos(angle)
        rx_y = y_coords[i] + LINK_DISTANCE * np.sin(angle)
        
        dists = np.sqrt((x_coords - rx_x)**2 + (y_coords - rx_y)**2 + ANTENNA_HEIGHT**2)
        rx_power = np.random.exponential(1.0, n_tx) * (dists ** -ALPHA)
        
        S = rx_power[i] 
        I = np.sum(rx_power) - S 
        
        if (S / (I + 1e-9)) > 1.0: 
            successes += 1
            
    return successes

# ==========================================
# 1. GENERATE THE SPATIAL MAPS
# ==========================================
print("Generating Spatial Maps...")
x_aloha, y_aloha = get_aloha_ppp(80)
x_dpp, y_dpp = get_dpp(80)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.scatter(x_aloha, y_aloha, c='red', s=50, alpha=0.7, edgecolors='black')
ax1.set_title("ALOHA (Random Chaos)\nNotice the tight clumping")
ax1.set_xlim(0, 1); ax1.set_ylim(0, 1); ax1.grid(True, linestyle='--', alpha=0.5)

ax2.scatter(x_dpp, y_dpp, c='blue', s=50, alpha=0.7, edgecolors='black')
ax2.set_title("DPP (Controlled Repulsion)\nNotice the 'social distancing'")
ax2.set_xlim(0, 1); ax2.set_ylim(0, 1); ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('M4_Spatial_Maps.png')
print("Saved M4_Spatial_Maps.png")

# ==========================================
# 2. GENERATE THE ULTIMATE BELL CURVE
# ==========================================
print("Generating The Ultimate Bell Curve (Should take ~15 seconds now)...")
t_aloha, t_csma, t_dpp = [], [], []

for d in DENSITIES:
    t_aloha.append(np.mean([evaluate_network_bipolar(*get_aloha_ppp(d)) for _ in range(N_SIMS)]))
    t_csma.append(np.mean([evaluate_network_bipolar(*get_csma_matern(d)) for _ in range(N_SIMS)]))
    t_dpp.append(np.mean([evaluate_network_bipolar(*get_dpp(d)) for _ in range(N_SIMS)]))

plt.figure(figsize=(8,5))
plt.plot(DENSITIES, t_aloha, 'r--x', label='ALOHA (Pure Randomness)')
plt.plot(DENSITIES, t_csma, 'g-s', label='CSMA (Listen-Before-Talk)')
plt.plot(DENSITIES, t_dpp, 'b-o', linewidth=2, label='DPP (Mathematical Repulsion)')
plt.title(r"The Ultimate Bell Curve (Bi-Polar Model)")
plt.xlabel(r"Target Network Density ($\lambda$)")
plt.ylabel(r"Spatial Throughput ($T$)")
plt.legend()
plt.grid(True, linestyle='--')
plt.tight_layout()
plt.savefig('M4_Ultimate_Bell_Curve.png')
print("Saved M4_Ultimate_Bell_Curve.png")