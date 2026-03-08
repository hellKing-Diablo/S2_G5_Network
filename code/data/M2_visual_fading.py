import numpy as np
import matplotlib.pyplot as plt

# 1. This mimics the logic in 'funProbCovPairsDetSamp.py' (Line 67)
muFading = 1.0  # Standard mean from your settings
samples = np.random.exponential(muFading, 10000)

# 2. Plotting (Visualization for M2)
plt.figure(figsize=(8, 6))
plt.hist(samples, bins=50, density=True, color='skyblue', edgecolor='black', alpha=0.7)
plt.title("Visual 1: Physics Model (Rayleigh Fading Variable $H$)", fontsize=14)
plt.xlabel("Signal Strength", fontsize=12)
plt.ylabel("Probability", fontsize=12)
plt.grid(True, alpha=0.3)
plt.savefig("Visual1_Fading.png")
plt.show()
