# S2_G5_Network
Project on Coverage probability in wireless networks with determinantal scheduling

# Stochastic Optimization of Spatial Throughput in Wireless Networks

**Course:** CSE 400: Fundamentals of Probability in Computing  
**Group:** 5 
**Team Members:** Yagnik, Prakshal, Devshree, Hiranshee, Dhruv

---

## 📌 Project Overview
In wireless network design, there is a fundamental trade-off between **Reliability** (probability of successful transmission) and **Capacity** (network throughput). 
* **Standard Aloha protocols** schedule transmissions randomly (Poisson Point Process), leading to clustering, severe interference, and network crashes at high densities.
* **Conservative scheduling** strictly spaces out users, guaranteeing high reliability but resulting in very low overall data throughput.

**Our Objective:** We aim to mathematically find the "sweet spot" by maximizing the **Spatial Throughput ($T$)** function:  
`T(λ) = λ × P_cov(λ)`  
*(Where `λ` is the density of active transmitters and `P_cov` is the probability of coverage/success).*

We achieve this by using **Determinantal Point Processes (DPP)** to introduce probabilistic "Negative Dependence" (geometric repulsion) among active nodes, inherently reducing interference and allowing for a higher optimal network density.

---

## 🚀 Milestone 1: Problem Formulation
In M1, we established the system context and identified the primary sources of uncertainty in a wireless environment:
1. **Physical Uncertainty:** Signal strength fluctuates unpredictably due to multipath propagation (Rayleigh Fading).
2. **Geometric Uncertainty:** The exact locations of active transmitters are random.
3. **Interaction Uncertainty:** Because locations and fading are random, the Aggregate Interference ($I$) acting on any receiver is a highly volatile stochastic process.

---

## 📊 Milestone 2: Mathematical Modeling
In M2, we deconstructed the network into its foundational Random Variables (RVs) and simulated them to build our probabilistic intuition. 

### 1. The Physics (Channel Uncertainty)
* **Random Variable:** Fading Coefficient ($H$)
* **Model:** Exponential Distribution (`μ = 1`)
* **Rationale:** Models Rayleigh Fading in a non-line-of-sight environment. Our simulations confirmed that "deep fades" (signal power near zero) are highly probable, necessitating a robust scheduling algorithm.

### 2. The Geometry (Node Configuration)
* **Random Variable:** Spatial Point Process ($\Phi$)
* **Baseline Model:** Poisson Point Process (PPP) - *Independent, prone to clustering.*
* **Proposed Model:** Determinantal Point Process (DPP) - *Negatively dependent.*
* **Rationale:** We utilize a Kernel Matrix to mathematically penalize close proximity. Our visual simulations prove that DPP enforces "social distancing" among nodes, structuring the randomness.

### 3. The Interaction (Stochastic Interference)
* **Random Variable:** Aggregate Interference ($I$)
* **Model:** Stochastic Shot Noise Process (`I = Σ P_i * H_i * r_i^(-α)`)
* **Rationale:** By plotting the Cumulative Distribution Function (CDF) of $I$, we mathematically proved that DPP geometry significantly reduces the variance and extreme upper bounds of network noise compared to Aloha.

---

## 💻 Codebase & Execution (Milestone 2 Artifacts)

The repository contains the base simulation code provided by B. Błaszczyszyn and H.P. Keeler. For Milestone 2, we extracted specific logic to generate our diagnostic probability plots.

### Generating the M2 Plots
We have created a script to visualize the Random Variables defined in Milestone 2. Run the following Python script to generate the artifacts:

```bash
python milestone2_plots.py
