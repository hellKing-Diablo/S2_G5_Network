import numpy as np
import matplotlib.pyplot as plt

# --- SIMULATION PARAMETERS ---
N_FADING_SIMS = 50          # Fading "dice rolls" per test point
ALPHA = 4.0                 # Path loss exponent
THRESHOLD = 1.0             # SINR threshold (0 dB)
ANTENNA_HEIGHT = 0.05       # THE FIX: Prevents infinite signal strength (Bounded Path Loss)
DENSITIES = np.arange(10, 420, 20) # Pushing density extremely high to force the crash

# 1. CONSTANT GRID AREA (The City)
# Generate a fixed mesh of 400 deterministic test points to evaluate the city
rx_test_x, rx_test_y = np.meshgrid(np.linspace(0.1, 0.9, 20), np.linspace(0.1, 0.9, 20))
rx_test_x = rx_test_x.flatten()
rx_test_y = rx_test_y.flatten()

def create_square_grid(density):
    points = int(np.sqrt(density))
    if points < 1: points = 1
    x = np.linspace(0.05, 0.95, points)
    y = np.linspace(0.05, 0.95, points)
    X, Y = np.meshgrid(x, y)
    return X.flatten(), Y.flatten()

def create_hex_grid(density):
    points = int(np.sqrt(density))
    if points < 1: points = 1
    x_coords, y_coords = [], []
    spacing = 0.9 / points
    for row in range(points):
        for col in range(points):
            x = 0.05 + col * spacing
            y = 0.05 + row * spacing * np.sqrt(3)/2
            if row % 2 != 0: x += spacing / 2
            if x <= 0.95 and y <= 0.95:
                x_coords.append(x)
                y_coords.append(y)
    return np.array(x_coords), np.array(y_coords)

throughput_square = []
throughput_hex = []

print("Running Bounded Path Loss Monte Carlo Simulation...")

for density in DENSITIES:
    # Generate the locked grids
    sq_x, sq_y = create_square_grid(density)
    hex_x, hex_y = create_hex_grid(density)
    
    success_sq = 0
    success_hex = 0
    total_tests = len(rx_test_x) * N_FADING_SIMS
    
    for i in range(len(rx_test_x)):
        rx_x, rx_y = rx_test_x[i], rx_test_y[i]
        
        # Calculate 2D Distances
        dists_2d_sq = np.sqrt((sq_x - rx_x)**2 + (sq_y - rx_y)**2)
        dists_2d_hex = np.sqrt((hex_x - rx_x)**2 + (hex_y - rx_y)**2)
        
        # APPLY ANTENNA HEIGHT (Real 3D distance: d = sqrt(r^2 + h^2))
        dists_3d_sq = np.sqrt(dists_2d_sq**2 + ANTENNA_HEIGHT**2)
        dists_3d_hex = np.sqrt(dists_2d_hex**2 + ANTENNA_HEIGHT**2)
        
        path_loss_sq = dists_3d_sq ** (-ALPHA)
        path_loss_hex = dists_3d_hex ** (-ALPHA)
        
        for _ in range(N_FADING_SIMS):
            # Evaluate Square
            fading_sq = np.random.exponential(1.0, len(dists_3d_sq))
            rx_power_sq = fading_sq * path_loss_sq
            signal_idx_sq = np.argmax(rx_power_sq) # Phone locks to the STRONGEST signal, not just physically closest
            S_sq = rx_power_sq[signal_idx_sq]
            I_sq = np.sum(rx_power_sq) - S_sq
            if (S_sq / (I_sq + 1e-9)) > THRESHOLD:
                success_sq += 1
                
            # Evaluate Hexagonal
            fading_hex = np.random.exponential(1.0, len(dists_3d_hex))
            rx_power_hex = fading_hex * path_loss_hex
            signal_idx_hex = np.argmax(rx_power_hex)
            S_hex = rx_power_hex[signal_idx_hex]
            I_hex = np.sum(rx_power_hex) - S_hex
            if (S_hex / (I_hex + 1e-9)) > THRESHOLD:
                success_hex += 1

    # Calculate actual number of nodes generated
    actual_density_sq = len(sq_x)
    actual_density_hex = len(hex_x)
    
    prob_cov_sq = success_sq / total_tests
    prob_cov_hex = success_hex / total_tests
    
    throughput_square.append(actual_density_sq * prob_cov_sq)
    throughput_hex.append(actual_density_hex * prob_cov_hex)
    print(f"Target Density {density} processed. (Actual Sq: {actual_density_sq}, Hex: {actual_density_hex})")

# PLOT THE BELL CURVE
plt.figure(figsize=(10, 6))
plt.plot(DENSITIES, throughput_square, 'b-o', linewidth=2, label='Square Grid Baseline')
plt.plot(DENSITIES, throughput_hex, 'r-s', linewidth=2, label='Hexagonal Grid Baseline')

plt.title('Milestone 3: Deterministic Throughput (Bounded Path Loss)', fontsize=14)
plt.xlabel(r'Network Density ($\lambda$)', fontsize=12)
plt.ylabel('Spatial Throughput ($T$)', fontsize=12)

# Highlight the Peak (Optimal Density)
max_t_hex = max(throughput_hex)
optimal_lambda_hex = DENSITIES[throughput_hex.index(max_t_hex)]
plt.axvline(x=optimal_lambda_hex, color='g', linestyle='--', alpha=0.7, label=fr'Optimal Hex Peak ($\lambda^* \approx {optimal_lambda_hex}$)')

plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('M3_Bell_Curve_Throughput.png')
plt.show()

print("Simulation Complete. Look at 'M3_Bell_Curve_Throughput.png' for the bell curve!")
