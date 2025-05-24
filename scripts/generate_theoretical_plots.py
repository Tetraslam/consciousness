"""
Generates theoretical plots: phase_transition.png and information_analysis.png.

Run:
    uv run scripts/generate_theoretical_plots.py

This script uses the RecursiveErrorAnalysis and InformationTheoreticConsciousness
classes to compute and save the visualizations.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

# from matplotlib.patches import Rectangle # Not actually used in the original code

class RecursiveErrorAnalysis:
    def __init__(self, noise_std=0.1, recursion_func=None):
        self.noise_std = noise_std
        self.recursion_func = recursion_func or (lambda x: 1.1 * np.tanh(x))
        
    def error_growth_rate(self, x, with_correction=False, correction_strength=0):
        h = 1e-6
        df_dx = (self.recursion_func(x + h) - self.recursion_func(x - h)) / (2 * h)
        return df_dx * (1 - correction_strength) if with_correction else df_dx
    
    def find_critical_threshold(self, correction_strengths):
        thresholds = []
        for c in correction_strengths:
            def condition(sigma):
                x_samples = np.random.randn(1000) * sigma
                growth_rates = [self.error_growth_rate(x, True, c) for x in x_samples]
                return np.mean(np.abs(growth_rates)) - 1.0
            try:
                threshold = fsolve(condition, x0=0.1)[0]
                thresholds.append(max(0, threshold))
            except:
                thresholds.append(0)
        return np.array(thresholds)
    
    def simulate_with_error_correction(self, steps=1000, correction_strength=0.5):
        x = np.zeros(steps)
        x_corrected = np.zeros(steps)
        x[0] = x_corrected[0] = 1.0
        
        for t in range(1, steps):
            noise = np.random.normal(0, self.noise_std)
            x[t] = self.recursion_func(x[t-1]) + noise
            if correction_strength > 0:
                num_measurements = int(10 * correction_strength)
                if num_measurements < 1: num_measurements = 1 # Ensure at least one measurement
                measurements = [x[t] + np.random.normal(0, self.noise_std/2) for _ in range(num_measurements)]
                x_corrected[t] = np.median(measurements)
            else:
                x_corrected[t] = x[t]
        return x, x_corrected
    
    def plot_phase_transition(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        noise_levels = np.linspace(0, 0.5, 25) # Reduced for speed
        correction_strengths = np.linspace(0, 1, 25) # Reduced for speed
        stability_matrix = np.zeros((len(noise_levels), len(correction_strengths)))
        
        for i, noise in enumerate(noise_levels):
            self.noise_std = noise
            for j, correction in enumerate(correction_strengths):
                _, x_corrected = self.simulate_with_error_correction(steps=100, correction_strength=correction)
                stability_matrix[i, j] = np.var(x_corrected[50:]) < 10
        
        ax1.imshow(stability_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 0.5], cmap='RdYlBu_r') # Reversed cmap for intuitive stability coloring
        ax1.set_xlabel('Error Correction Strength')
        ax1.set_ylabel('Noise Level (σ)')
        ax1.set_title('Phase Diagram: Stability of Recursive Computation')
        
        phase_boundary = []
        for j in range(len(correction_strengths)):
            stable_indices = np.where(stability_matrix[:, j] == 1)[0]
            phase_boundary.append(noise_levels[stable_indices[-1]] if len(stable_indices) > 0 else 0)
        
        ax1.plot(correction_strengths, phase_boundary, 'k-', linewidth=2, label='Phase Boundary')
        ax1.legend()
        ax1.text(0.2, 0.1, 'STABLE\n(Unconscious-like)', fontsize=10, ha='center', color='white') # Adjusted text for cmap
        ax1.text(0.7, 0.3, 'STABLE\n(Conscious-like)', fontsize=10, ha='center', color='white') # Adjusted text for cmap
        ax1.text(0.2, 0.4, 'UNSTABLE', fontsize=10, ha='center', color='black')
        
        self.noise_std = 0.2
        x_no_corr, _ = self.simulate_with_error_correction(steps=200, correction_strength=0)
        _, x_with_corr = self.simulate_with_error_correction(steps=200, correction_strength=0.8)
        
        ax2.plot(x_no_corr[:100], label='No Error Correction', alpha=0.7)
        ax2.plot(x_with_corr[:100], label='With Error Correction', alpha=0.7)
        ax2.set_xlabel('Time Step'); ax2.set_ylabel('State Value')
        ax2.set_title('Recursive Computation Trajectories'); ax2.legend(); ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('visualizations/phase_transition.png', dpi=150); plt.close()

class InformationTheoreticConsciousness:
    def mutual_information(self, x, y, bins=10): # Reduced bins for speed
        hist_2d, _, _ = np.histogram2d(x, y, bins=bins)
        pxy = hist_2d / np.sum(hist_2d)
        px = np.sum(pxy, axis=1); py = np.sum(pxy, axis=0)
        px_py = px[:, None] * py[None, :] + 1e-10 # Add epsilon before multiplication
        pxy_safe = pxy + 1e-10 # Add epsilon before division
        mi = np.sum(pxy_safe * np.log(pxy_safe / px_py))
        return mi if mi > 0 else 0 # Ensure non-negative MI
    
    def entropy(self, x, bins=10): # Reduced bins for speed
        hist, _ = np.histogram(x, bins=bins)
        px = hist / np.sum(hist) + 1e-10
        return -np.sum(px * np.log(px))

    def consciousness_as_compression(self, neural_states_flat, corrected_states_flat):
        results = {
            'raw_entropy': self.entropy(neural_states_flat),
            'corrected_entropy': self.entropy(corrected_states_flat),
            'compression_ratio': 0,
            'predictive_info': 0,
            'integration': 0 # Placeholder, original logic was more complex and assumed structured input
        }
        if results['raw_entropy'] > 0:
             results['compression_ratio'] = (results['raw_entropy'] - results['corrected_entropy']) / results['raw_entropy']
        
        mid = len(corrected_states_flat) // 2
        if mid > 1:
             results['predictive_info'] = self.mutual_information(corrected_states_flat[:mid], corrected_states_flat[mid:])
        return results

    def plot_information_analysis(self):
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        noise_levels = np.linspace(0.01, 0.5, 10) # Reduced for speed
        metrics = {k: [] for k in ['compression', 'predictive_info', 'integration', 'subjective_valuation']}
        
        for noise in noise_levels:
            rea = RecursiveErrorAnalysis(noise_std=noise)
            # Simulate with a single array output for x_raw and x_corrected for simplicity with current MI
            x_raw_flat, x_corrected_flat = rea.simulate_with_error_correction(steps=500, correction_strength=0.8) # Reduced steps
            x_raw_flat = x_raw_flat[100:]
            x_corrected_flat = x_corrected_flat[100:]
            
            if len(x_raw_flat) == 0 or len(x_corrected_flat) == 0 : continue # Skip if no data

            info_results = self.consciousness_as_compression(x_raw_flat, x_corrected_flat)
            metrics['compression'].append(info_results['compression_ratio'])
            metrics['predictive_info'].append(info_results['predictive_info'])
            metrics['integration'].append(info_results.get('integration', 0.5))
            state_variance = np.var(x_corrected_flat)
            metrics['subjective_valuation'].append(1 / (1 + state_variance) if (1 + state_variance) !=0 else 1)
        
        metric_names = ['compression', 'predictive_info', 'integration', 'subjective_valuation']
        for i, key in enumerate(metric_names):
            ax = axes[i//2, i%2]
            if metrics[key]: # Check if list is not empty
                ax.plot(noise_levels[:len(metrics[key])], metrics[key], 'b-', linewidth=2) # Adjust noise_levels length
            ax.set_xlabel('Noise Level (σ)'); ax.set_ylabel(key.replace('_', ' ').title()); ax.grid(True, alpha=0.3)
            ax.axvline(x=0.15, color='r', linestyle='--', label='Approx. Phase Transition')
            if i == 0: ax.legend()
        
        plt.suptitle('Information-Theoretic Signatures of Consciousness', fontsize=14); plt.tight_layout()
        plt.savefig('visualizations/information_analysis.png', dpi=150); plt.close()

if __name__ == "__main__":
    print("=" * 60)
    print("THEORETICAL PLOT GENERATION")
    print("=" * 60)
    
    print("\n1. Computing phase transition (phase_transition.png)...")
    rea = RecursiveErrorAnalysis()
    rea.plot_phase_transition()
    print(f"   [OK] phase_transition.png saved to visualizations/")
    
    print("\n2. Computing information-theoretic analysis (information_analysis.png)...")
    itc = InformationTheoreticConsciousness()
    itc.plot_information_analysis()
    print(f"   [OK] information_analysis.png saved to visualizations/")

    print("\nAll theoretical plots generated.") 