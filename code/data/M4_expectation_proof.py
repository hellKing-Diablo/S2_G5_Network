import numpy as np

ALPHA = 4.0
ANTENNA_HEIGHT = 0.05
N_SNAPSHOTS = 500 # Large sample size for statistical accuracy

def get_aloha_ppp(density):
    n_points = np.random.poisson(density)
    return np.random.uniform(0.05, 0.95, n_points), np.random.uniform(0.05, 0.95, n_points)

def get_successes(x_coords, y_coords):
    n_tx = len(x_coords)
    if n_tx == 0: return 0
    rx_x, rx_y = np.meshgrid(np.linspace(0.1, 0.9, 10), np.linspace(0.1, 0.9, 10))
    successes = 0
    for i in range(100):
        dists = np.sqrt((x_coords - rx_x.flatten()[i])**2 + (y_coords - rx_y.flatten()[i])**2 + ANTENNA_HEIGHT**2)
        rx_power = np.random.exponential(1.0, n_tx) * (dists ** -ALPHA)
        S = np.max(rx_power)
        I = np.sum(rx_power) - S
        if (S / (I + 1e-9)) > 1.0: # SINR Threshold
            successes += 1
    return successes

print("Running Monte Carlo Simulation to calculate E[XY]...")
X_active_tx = []
Y_successes = []

# Simulate varying network loads over time
for _ in range(N_SNAPSHOTS):
    # Random fluctuating density between 50 and 150
    current_density = np.random.uniform(50, 150) 
    x, y = get_aloha_ppp(current_density)
    
    X_active_tx.append(len(x))
    Y_successes.append(get_successes(x, y))

# Calculate Expectations and Covariance
E_X = np.mean(X_active_tx)
E_Y = np.mean(Y_successes)
E_XY = np.mean(np.multiply(X_active_tx, Y_successes))
Cov_XY = np.cov(X_active_tx, Y_successes)[0][1]

print("\n" + "="*45)
print("PROFESSOR'S EXPECTATION OPERATOR PROOF")
print("="*45)
print(f"E[X]  (Avg Active Transmitters) = {E_X:.2f}")
print(f"E[Y]  (Avg Successful Links)    = {E_Y:.2f}")
print(f"E[XY] (Joint Expectation)       = {E_XY:.2f}")
print("-" * 45)
print(f"Covariance Cov(X, Y)            = {Cov_XY:.2f}")
print("="*45)

if Cov_XY < 0:
    print("\nCONCLUSION: Negative Correlation Confirmed.")
    print("As the number of active transmitters (X) increases, the")
    print("resulting interference causes successful transmissions (Y) to drop.")
else:
    print("\nCONCLUSION: Positive Correlation.")