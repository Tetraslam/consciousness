"""
Generates the error_accumulation.png visualization.

Run:
    uv run scripts/generate_error_accumulation_plot.py

This script demonstrates how errors accumulate exponentially in a noisy
recursive system without error correction, for various recursion strengths.
"""

import matplotlib.pyplot as plt
import numpy as np


def recursive_computation_no_correction(steps=100, noise_std=0.1, recursion_strength=1.1):
    """
    Simulate recursive computation without error correction.
    x(t) = recursion_strength * x(t-1) + noise
    """
    x = np.zeros(steps)
    x[0] = 1.0  # Initial state
    errors = np.zeros(steps)
    
    true_x = np.zeros(steps)
    true_x[0] = 1.0
    
    for t in range(1, steps):
        true_x[t] = recursion_strength * true_x[t-1]
        noise_val = np.random.normal(0, noise_std)
        x[t] = recursion_strength * x[t-1] + noise_val
        errors[t] = abs(x[t] - true_x[t])
    
    return x, true_x, errors

def plot_error_accumulation():
    """Demonstrate exponential error growth."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Error Accumulation in Noisy Recursive Systems without Correction", fontsize=16)

    recursion_strengths_to_test = [0.9, 1.0, 1.1, 1.2]
    
    for i, rec_strength in enumerate(recursion_strengths_to_test):
        ax = axes[i//2, i%2]
        for _ in range(5): # Number of trials to overlay
            _, _, errors_run = recursive_computation_no_correction(
                steps=100, 
                noise_std=0.01,
                recursion_strength=rec_strength
            )
            ax.semilogy(errors_run, alpha=0.6, linewidth=1.5)
        
        ax.set_title(f'Recursion Strength (a) = {rec_strength}')
        ax.set_xlabel('Time Step')
        ax.set_ylabel('Absolute Error (log scale)')
        ax.grid(True, which="both", linestyle='--', linewidth=0.5)
        ax.set_ylim(bottom=1e-4) # Ensure consistent y-axis start if errors are very small
    
    plt.tight_layout(rect=[0, 0, 1, 0.96]) # Adjust for suptitle
    plt.savefig('visualizations/error_accumulation.png', dpi=150)
    plt.close(fig)

if __name__ == "__main__":
    plot_error_accumulation()
    print("\n[OK] error_accumulation.png saved to visualizations/")
    print("Error accumulation analysis complete. See visualizations/error_accumulation.png") # Original print 