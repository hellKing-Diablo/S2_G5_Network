import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Milestone3App:
    def __init__(self, root):
        self.root = root
        self.root.title("Milestone 3: Deterministic Baseline Simulator")
        self.root.geometry("1100x700")

        # --- Variables ---
        self.density_var = tk.IntVar(value=25)
        self.alpha_var = tk.DoubleVar(value=4.0)
        self.rx_x_var = tk.DoubleVar(value=0.55) # Offset to avoid exact overlap
        self.rx_y_var = tk.DoubleVar(value=0.55)
        self.fading_var = tk.DoubleVar(value=1.0)

        # --- Layout ---
        self.create_sidebar()
        self.create_main_area()
        self.update_plots() # Initial plot

    def create_sidebar(self):
        sidebar = tk.Frame(self.root, width=250, bg="#f0f0f0", padx=10, pady=10)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(sidebar, text="Network Controls", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

        # Density
        tk.Label(sidebar, text="Grid Density (Towers):", bg="#f0f0f0").pack(anchor="w")
        tk.Scale(sidebar, variable=self.density_var, from_=9, to=100, orient=tk.HORIZONTAL, command=self.on_slider_change, bg="#f0f0f0").pack(fill=tk.X)

        # Alpha
        tk.Label(sidebar, text="Path Loss Exponent (Alpha):", bg="#f0f0f0").pack(anchor="w", pady=(10,0))
        tk.Scale(sidebar, variable=self.alpha_var, from_=2.0, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.on_slider_change, bg="#f0f0f0").pack(fill=tk.X)

        # Receiver X
        tk.Label(sidebar, text="Receiver X Position:", bg="#f0f0f0").pack(anchor="w", pady=(10,0))
        tk.Scale(sidebar, variable=self.rx_x_var, from_=0.0, to=1.0, resolution=0.05, orient=tk.HORIZONTAL, command=self.on_slider_change, bg="#f0f0f0").pack(fill=tk.X)

        # Receiver Y
        tk.Label(sidebar, text="Receiver Y Position:", bg="#f0f0f0").pack(anchor="w", pady=(10,0))
        tk.Scale(sidebar, variable=self.rx_y_var, from_=0.0, to=1.0, resolution=0.05, orient=tk.HORIZONTAL, command=self.on_slider_change, bg="#f0f0f0").pack(fill=tk.X)

        # Fading
        tk.Label(sidebar, text="Fading Multiplier:", bg="#f0f0f0").pack(anchor="w", pady=(10,0))
        tk.Scale(sidebar, variable=self.fading_var, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.on_slider_change, bg="#f0f0f0").pack(fill=tk.X)

        # Reset Fading Button
        tk.Button(sidebar, text="Reset Fading to 1.0", command=self.reset_fading).pack(pady=10, fill=tk.X)

    def create_main_area(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Square
        self.tab_sq = tk.Frame(self.notebook)
        self.notebook.add(self.tab_sq, text="Square Grid")
        self.fig_sq, self.ax_sq = plt.subplots(figsize=(6, 5))
        self.canvas_sq = FigureCanvasTkAgg(self.fig_sq, master=self.tab_sq)
        self.canvas_sq.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.stats_sq = tk.Label(self.tab_sq, text="", font=("Arial", 12), justify=tk.LEFT)
        self.stats_sq.pack(side=tk.BOTTOM, pady=10)

        # Tab 2: Hex
        self.tab_hex = tk.Frame(self.notebook)
        self.notebook.add(self.tab_hex, text="Hexagonal Grid")
        self.fig_hex, self.ax_hex = plt.subplots(figsize=(6, 5))
        self.canvas_hex = FigureCanvasTkAgg(self.fig_hex, master=self.tab_hex)
        self.canvas_hex.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.stats_hex = tk.Label(self.tab_hex, text="", font=("Arial", 12), justify=tk.LEFT)
        self.stats_hex.pack(side=tk.BOTTOM, pady=10)

        # Tab 3: Explanation
        self.tab_exp = tk.Frame(self.notebook, padx=20, pady=20)
        self.notebook.add(self.tab_exp, text="Understanding the Math")
        explanation = (
            "HOW THE NETWORK IS CALCULATED:\n\n"
            "1. The Grid (Transmitters): Blue dots represent fixed cell towers. They never move.\n"
            "2. The Receiver (You): The Red 'X' represents a mobile phone. You can move it using the sliders.\n"
            "3. The Signal: The app automatically finds the closest tower (Green Star) and connects to it.\n"
            "4. Interference: Every other tower in the city is broadcasting on the same frequency, creating background noise.\n\n"
            "WHAT IS THROUGHPUT?\n"
            "Throughput = Density x Success Rate.\n"
            "If your Signal is stronger than the Interference (SINR > 1.0), your specific connection succeeds.\n"
            "If this happens across the whole grid, the total Spatial Throughput equals the Density of the grid.\n\n"
            "SQUARE vs HEXAGONAL:\n"
            "Hexagonal grids pack towers more efficiently. By staggering the rows, the distance to the 'first ring' "
            "of interfering towers is uniformly spread out. This prevents severe interference spikes and makes Hexagonal "
            "grids the standard for real-world cellular networks."
        )
        tk.Label(self.tab_exp, text=explanation, font=("Arial", 12), justify=tk.LEFT, wraplength=700).pack(anchor="w")

    def reset_fading(self):
        self.fading_var.set(1.0)
        self.update_plots()

    def on_slider_change(self, event):
        self.update_plots()

    # --- MATH ENGINE ---
    def create_square_grid(self, density):
        points = int(np.sqrt(density))
        x = np.linspace(0.1, 0.9, points)
        y = np.linspace(0.1, 0.9, points)
        X, Y = np.meshgrid(x, y)
        return X.flatten(), Y.flatten()

    def create_hex_grid(self, density):
        points = int(np.sqrt(density))
        x_coords, y_coords = [], []
        spacing = 0.8 / points
        for row in range(points):
            for col in range(points):
                x = 0.1 + col * spacing
                y = 0.1 + row * spacing * np.sqrt(3)/2
                if row % 2 != 0:
                    x += spacing / 2
                if x <= 0.95 and y <= 0.95:
                    x_coords.append(x)
                    y_coords.append(y)
        return np.array(x_coords), np.array(y_coords)

    def calculate_network(self, x_tx, y_tx, rx_x, rx_y, alpha, fading_base):
        distances = np.sqrt((x_tx - rx_x)**2 + (y_tx - rx_y)**2)
        
        # Ensure receiver is physically separated from transmitters (min distance 0.02)
        distances = np.where(distances < 0.02, 0.02, distances) 
        
        np.random.seed(42) # Keep fading stable while moving receiver
        fading = np.random.exponential(1.0, len(distances)) * fading_base
        
        path_loss = distances ** (-alpha)
        received_power = fading * path_loss
        
        closest_idx = np.argmin(distances)
        signal_power = received_power[closest_idx]
        
        interference_power = np.sum(received_power) - signal_power
        sinr = signal_power / (interference_power + 1e-9)
        
        success = "YES" if sinr > 1.0 else "NO (Failed)"
        throughput = len(x_tx) if sinr > 1.0 else 0
        
        return closest_idx, signal_power, interference_power, sinr, success, throughput

    def update_plots(self):
        density = self.density_var.get()
        alpha = self.alpha_var.get()
        rx_x = self.rx_x_var.get()
        rx_y = self.rx_y_var.get()
        fading = self.fading_var.get()

        # Generate Grids
        sq_x, sq_y = self.create_square_grid(density)
        hex_x, hex_y = self.create_hex_grid(density)

        # Calculate
        sq_idx, sq_s, sq_i, sq_sinr, sq_succ, sq_t = self.calculate_network(sq_x, sq_y, rx_x, rx_y, alpha, fading)
        hex_idx, hex_s, hex_i, hex_sinr, hex_succ, hex_t = self.calculate_network(hex_x, hex_y, rx_x, rx_y, alpha, fading)

        # Plot Square
        self.ax_sq.clear()
        self.ax_sq.scatter(sq_x, sq_y, c='blue', s=50, label="Interfering Tower")
        self.ax_sq.scatter(sq_x[sq_idx], sq_y[sq_idx], c='green', s=150, marker='*', label="Signal Tower")
        self.ax_sq.scatter(rx_x, rx_y, c='red', s=100, marker='X', label="Receiver (You)")
        self.ax_sq.plot([sq_x[sq_idx], rx_x], [sq_y[sq_idx], rx_y], 'g--', label="Active Link")
        self.ax_sq.set_xlim(0, 1)
        self.ax_sq.set_ylim(0, 1)
        self.ax_sq.legend(loc="upper right")
        self.canvas_sq.draw()
        
        self.stats_sq.config(text=f"Signal (S): {sq_s:.4f}  |  Interference (I): {sq_i:.4f}\n"
                                  f"SINR: {sq_sinr:.4f}  |  Link Success: {sq_succ}\n"
                                  f"Expected Network Throughput: {sq_t} active links")

        # Plot Hex
        self.ax_hex.clear()
        self.ax_hex.scatter(hex_x, hex_y, c='blue', s=50, label="Interfering Tower")
        self.ax_hex.scatter(hex_x[hex_idx], hex_y[hex_idx], c='green', s=150, marker='*', label="Signal Tower")
        self.ax_hex.scatter(rx_x, rx_y, c='red', s=100, marker='X', label="Receiver (You)")
        self.ax_hex.plot([hex_x[hex_idx], rx_x], [hex_y[hex_idx], rx_y], 'g--', label="Active Link")
        self.ax_hex.set_xlim(0, 1)
        self.ax_hex.set_ylim(0, 1)
        self.ax_hex.legend(loc="upper right")
        self.canvas_hex.draw()

        self.stats_hex.config(text=f"Signal (S): {hex_s:.4f}  |  Interference (I): {hex_i:.4f}\n"
                                   f"SINR: {hex_sinr:.4f}  |  Link Success: {hex_succ}\n"
                                   f"Expected Network Throughput: {hex_t} active links")

if __name__ == "__main__":
    root = tk.Tk()
    app = Milestone3App(root)
    root.mainloop()
