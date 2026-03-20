import numpy as np
import matplotlib.pyplot as plt
# Importing YOUR uploaded files
from dependency.funPairsL import funPairsL
from dependency.funSimSimpleDPP import funSimSimpleDPP
from dependency.funLtoK import funLtoK

# --- Setup from FairPairsCompareDetAloha.py ---
lambda0 = 50
windowSize = 1.0
n_sims = 1000  # Number of snapshots

# Lists to store the Random Variable 'I'
Interference_Aloha = []
Interference_DPP = []

print("Running Simulation to extract Interference...")

for _ in range(n_sims):
    # 1. Create Random Points (Aloha)
    n_points = np.random.poisson(lambda0)
    xx = np.random.uniform(0, windowSize, n_points)
    yy = np.random.uniform(0, windowSize, n_points)
    
    if n_points < 2: continue

    # 2. Physics: Create L Matrix (Repulsion Kernel)
    # We use Gaussian kernel (choiceKernel=1) as per DemoDetPoisson
    sigma = 0.1
    # Simple Gaussian Kernel calculation (from funS.py logic)
    xxDiff = np.subtract.outer(xx, xx)
    yyDiff = np.subtract.outer(yy, yy)
    rrSquared = xxDiff**2 + yyDiff**2
    L = np.exp(-rrSquared / sigma**2) 
    
    # 3. Simulate DPP (The "Polite" selection)
    K = funLtoK(L)
    eigenValK, eigenVectK = np.linalg.eigh(K) # Using numpy directly for stability
    # Call your repo function to get active nodes
    # Correct: Passing the 1D vector of eigenvalues (length 55)
    indexDPP = funSimSimpleDPP(eigenVectK, eigenValK)
    
    # 4. Calculate Interference (Sum of Power)
    # We measure interference at the center (0.5, 0.5)
    # Path Loss Model: r^-4
    
    # Aloha Interference (All nodes talk)
    dists_aloha = np.sqrt((xx - 0.5)**2 + (yy - 0.5)**2)
    fading_aloha = np.random.exponential(1.0, len(xx))
    I_aloha = np.sum(fading_aloha * (dists_aloha**-4))
    Interference_Aloha.append(I_aloha)

    # DPP Interference (Only selected nodes talk)
    if len(indexDPP) > 0:
        dists_dpp = np.sqrt((xx[indexDPP] - 0.5)**2 + (yy[indexDPP] - 0.5)**2)
        fading_dpp = np.random.exponential(1.0, len(indexDPP))
        I_dpp = np.sum(fading_dpp * (dists_dpp**-4))
        Interference_DPP.append(I_dpp)

# 5. Plot CDF
plt.figure(figsize=(8,6))
sorted_aloha = np.sort(Interference_Aloha)
sorted_dpp = np.sort(Interference_DPP)
y_vals_aloha = np.arange(len(sorted_aloha))/float(len(sorted_aloha))
y_vals_dpp = np.arange(len(sorted_dpp))/float(len(sorted_dpp))

plt.semilogx(sorted_aloha, y_vals_aloha, 'b--', label='Aloha (High Noise)')
plt.semilogx(sorted_dpp, y_vals_dpp, 'r-', linewidth=2, label='DPP (Controlled Noise)')
plt.title("Visual 3: Stochastic Interference ($I$)", fontsize=14)
plt.xlabel("Interference Power (Log Scale)", fontsize=12)
plt.ylabel("CDF (Probability)", fontsize=12)
plt.legend()
plt.grid(True)
plt.savefig("Visual3_Interference.png")
plt.show()
