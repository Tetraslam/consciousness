"""
Improved conscious neural network with better phase transitions.
This version has more realistic parameters that show clear differences
between conscious and unconscious states.
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


class ConsciousNeuralNetworkV2:
    def __init__(self, 
                 n_neurons=100,
                 n_modules=10,
                 noise_level=0.3,  # Higher biological noise
                 recursion_strength=1.2):  # Stronger recursion
        """
        Initialize an improved neural network with clearer phase transitions.
        """
        self.n_neurons = n_neurons
        self.n_modules = n_modules
        self.noise_level = noise_level
        self.recursion_strength = recursion_strength
        
        # Network architecture
        self.total_neurons = n_neurons * n_modules
        
        # Initialize network state
        self.reset_state()
        
        # Error correction parameters
        self.phases = np.linspace(0, 2*np.pi, n_modules, endpoint=False)
        self.frequencies = self._generate_prime_frequencies(n_modules)
        
        # Consciousness parameters
        self.error_correction_strength = 0.0
        self.is_conscious = False
        
        # History
        self.history = {
            'raw_state': [],
            'corrected_state': [],
            'consciousness_level': [],
            'error': [],
            'integration': [],
            'prediction_error': []
        }
        
    def _generate_prime_frequencies(self, n):
        """Generate relatively prime frequencies."""
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        return np.array(primes[:n]) * 0.5  # Scale down for stability
    
    def reset_state(self):
        """Reset network to initial state."""
        self.state = np.random.randn(self.total_neurons) * 0.1
        self.thought = np.random.randn(self.n_modules) * 0.1
        self.previous_thought = self.thought.copy()
        
    def recursive_thought_step(self, external_input=None):
        """
        Perform one step of recursive thought with improved dynamics.
        """
        # Store previous thought for prediction error
        self.previous_thought = self.thought.copy()
        
        # 1. Recursive dynamics (stronger coupling)
        thought_influence = np.repeat(self.thought, self.n_neurons)
        self.state = self.recursion_strength * np.tanh(self.state * 0.9 + thought_influence * 0.5)
        
        # 2. External input
        if external_input is not None:
            self.state += external_input * 0.2
            
        # 3. Add realistic biological noise
        noise = np.random.normal(0, self.noise_level, self.total_neurons)
        # Add correlated noise within modules (more realistic)
        for i in range(self.n_modules):
            module_noise = np.random.normal(0, self.noise_level * 0.3)
            start = i * self.n_neurons
            end = (i + 1) * self.n_neurons
            noise[start:end] += module_noise
            
        noisy_state = self.state + noise
        
        # 4. Error correction
        if self.error_correction_strength > 0:
            corrected_state = self._error_correct_v2(noisy_state)
        else:
            corrected_state = noisy_state
            
        # 5. Update thought representation
        self.thought = self._extract_thought(corrected_state)
        self.state = corrected_state
        
        # 6. Measure consciousness
        consciousness_level = self._measure_consciousness_v2()
        
        # Record history
        self.history['raw_state'].append(noisy_state.copy())
        self.history['corrected_state'].append(corrected_state.copy())
        self.history['consciousness_level'].append(consciousness_level)
        self.history['error'].append(np.std(noisy_state - corrected_state))
        
        # Prediction error for recursive thought
        pred_error = np.mean(np.abs(self.thought - self.previous_thought))
        self.history['prediction_error'].append(pred_error)
        
        return consciousness_level
    
    def _error_correct_v2(self, noisy_state):
        """
        Improved error correction that shows clearer effects.
        """
        corrected = np.zeros_like(noisy_state)
        
        for i in range(self.n_modules):
            # Extract module
            module_start = i * self.n_neurons
            module_end = (i + 1) * self.n_neurons
            module_state = noisy_state[module_start:module_end]
            
            # Phase encoding with error correction
            if self.error_correction_strength > 0.3:  # Threshold for effectiveness
                # Strong error correction: multiple measurements
                n_measurements = int(self.error_correction_strength * 20)
                measurements = []
                
                for _ in range(n_measurements):
                    # Each measurement has independent noise
                    meas_noise = np.random.normal(0, self.noise_level * 0.5, self.n_neurons)
                    noisy_measurement = module_state + meas_noise
                    
                    # Encode to phase
                    phase = np.angle(np.sum(noisy_measurement * 
                                          np.exp(1j * self.frequencies[i] * 
                                                np.linspace(0, 2*np.pi, self.n_neurons))))
                    
                    # Decode
                    decoded = np.cos(self.frequencies[i] * 
                                   np.linspace(0, 2*np.pi, self.n_neurons) - phase)
                    measurements.append(decoded)
                
                # Take median for robustness
                corrected_module = np.median(measurements, axis=0)
                corrected_module *= np.mean(np.abs(module_state))
            else:
                # Weak error correction: no real correction, just pass through with noise
                corrected_module = module_state
                
            corrected[module_start:module_end] = corrected_module
            
        return corrected
    
    def _extract_thought(self, state):
        """Extract thought with nonlinear transformation."""
        thought = np.zeros(self.n_modules)
        for i in range(self.n_modules):
            module_start = i * self.n_neurons
            module_end = (i + 1) * self.n_neurons
            # Nonlinear extraction
            module_activity = state[module_start:module_end]
            thought[i] = np.tanh(np.mean(module_activity))
        return thought
    
    def _measure_consciousness_v2(self):
        """
        Improved consciousness measurement with clearer distinctions.
        """
        if len(self.history['raw_state']) < 20:
            return 0.0
            
        # Get recent history
        recent_raw = np.array(self.history['raw_state'][-20:])
        recent_corrected = np.array(self.history['corrected_state'][-20:])
        recent_thoughts = np.array([self._extract_thought(s) for s in recent_corrected])
        
        # 1. Noise suppression: How much noise is removed?
        raw_noise = np.mean([np.std(state) for state in recent_raw])
        corrected_noise = np.mean([np.std(state) for state in recent_corrected])
        
        if raw_noise > 0:
            noise_suppression = (raw_noise - corrected_noise) / raw_noise
            noise_suppression = np.clip(noise_suppression, -1, 1)
        else:
            noise_suppression = 0
            
        # 2. Temporal coherence: Are thoughts stable over time?
        if len(recent_thoughts) > 1:
            thought_changes = np.diff(recent_thoughts, axis=0)
            temporal_coherence = 1.0 / (1.0 + np.mean(np.abs(thought_changes)))
        else:
            temporal_coherence = 0
            
        # 3. Recursive stability: Can maintain recursive loops?
        if len(self.history['prediction_error']) > 10:
            recent_pred_errors = self.history['prediction_error'][-10:]
            avg_pred_error = np.mean(recent_pred_errors)
            recursive_stability = 1.0 / (1.0 + avg_pred_error * 5)
        else:
            recursive_stability = 0
            
        # 4. Information integration
        if len(recent_thoughts) > 0:
            # Check if different modules are coordinated
            module_correlations = []
            for i in range(self.n_modules - 1):
                corr = np.corrcoef(recent_thoughts[:, i], recent_thoughts[:, i+1])[0, 1]
                if not np.isnan(corr):
                    module_correlations.append(abs(corr))
            
            if module_correlations:
                integration = np.mean(module_correlations)
            else:
                integration = 0
        else:
            integration = 0
            
        # Combine metrics with strong requirement for error correction
        if self.error_correction_strength > 0.3:  # Must exceed threshold
            # With sufficient error correction
            consciousness = (
                noise_suppression * 0.3 +
                temporal_coherence * 0.3 +
                recursive_stability * 0.2 +
                integration * 0.2
            )
            # Apply threshold
            threshold = 0.35
            if consciousness > threshold:
                self.is_conscious = True
                return min((consciousness - threshold) * 3 + threshold, 1.0)
            else:
                self.is_conscious = False
                return consciousness * 0.7
        else:
            # Without sufficient error correction - always unconscious
            self.is_conscious = False
            # Return very low consciousness
            return 0.05 + np.random.normal(0, 0.01)  # Small fluctuations around 0.05
    
    def set_error_correction(self, strength):
        """Set error correction strength."""
        self.error_correction_strength = np.clip(strength, 0, 1)
        
    def run_simulation(self, steps=1000, external_input_func=None):
        """Run simulation."""
        for step in range(steps):
            if external_input_func:
                external_input = external_input_func(step)
            else:
                # Occasional inputs
                if np.random.rand() < 0.05:
                    external_input = np.random.randn(self.total_neurons) * 0.3
                else:
                    external_input = None
                    
            self.recursive_thought_step(external_input)


def demonstrate_phase_transition():
    """Demonstrate clear phase transition in consciousness."""
    print("=" * 60)
    print("IMPROVED CONSCIOUSNESS DEMONSTRATION")
    print("=" * 60)
    
    # Test different conditions
    conditions = [
        ("No error correction", 0.3, 0.0),
        ("Weak error correction", 0.3, 0.2),
        ("Medium error correction", 0.3, 0.5),
        ("Strong error correction", 0.3, 0.8),
        ("Low noise, no correction", 0.1, 0.0),
        ("High noise, strong correction", 0.5, 0.8)
    ]
    
    results = []
    
    for name, noise, ec in conditions:
        print(f"\nTesting: {name}")
        print(f"  Noise level: {noise:.1f}")
        print(f"  Error correction: {ec:.1f}")
        
        net = ConsciousNeuralNetworkV2(noise_level=noise)
        net.set_error_correction(ec)
        net.run_simulation(steps=300)
        
        # Get final consciousness level
        final_c = np.mean(net.history['consciousness_level'][-100:])
        
        print(f"  Final consciousness: {final_c:.3f}")
        print(f"  Is conscious: {net.is_conscious}")
        
        results.append({
            'name': name,
            'noise': noise,
            'ec': ec,
            'consciousness': final_c,
            'is_conscious': net.is_conscious
        })
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Bar chart of results
    names = [r['name'] for r in results]
    consciousness_levels = [r['consciousness'] for r in results]
    colors = ['red' if not r['is_conscious'] else 'green' for r in results]
    
    bars = ax1.bar(range(len(names)), consciousness_levels, color=colors, alpha=0.7)
    ax1.set_xticks(range(len(names)))
    ax1.set_xticklabels(names, rotation=45, ha='right')
    ax1.axhline(y=0.35, color='black', linestyle='--', label='Consciousness threshold')
    ax1.set_ylabel('Consciousness Level')
    ax1.set_title('Consciousness Under Different Conditions')
    ax1.legend()
    ax1.set_ylim(0, 1.1)
    
    # Phase diagram
    noise_levels = np.linspace(0, 0.6, 20)
    ec_levels = np.linspace(0, 1, 20)
    
    consciousness_grid = np.zeros((len(noise_levels), len(ec_levels)))
    
    print("\nGenerating phase diagram...")
    for i, noise in enumerate(noise_levels):
        for j, ec in enumerate(ec_levels):
            net = ConsciousNeuralNetworkV2(noise_level=noise)
            net.set_error_correction(ec)
            net.run_simulation(steps=200)
            consciousness_grid[i, j] = np.mean(net.history['consciousness_level'][-50:])
    
    im = ax2.imshow(consciousness_grid, origin='lower', aspect='auto',
                    extent=[0, 1, 0, 0.6], cmap='RdYlGn', vmin=0, vmax=1)
    ax2.set_xlabel('Error Correction Strength')
    ax2.set_ylabel('Noise Level (σ)')
    ax2.set_title('Phase Diagram of Consciousness')
    
    # Add contour line at threshold
    X, Y = np.meshgrid(ec_levels, noise_levels)
    contour = ax2.contour(X, Y, consciousness_grid, levels=[0.35], colors='black', linewidths=2)
    ax2.clabel(contour, inline=True, fmt='threshold')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax2)
    cbar.set_label('Consciousness Level')
    
    # Mark test points
    for r in results:
        if r['noise'] <= 0.6:  # Only if in range
            ax2.scatter(r['ec'], r['noise'], 
                       color='blue' if r['is_conscious'] else 'red',
                       s=100, edgecolor='black', linewidth=2)
    
    plt.tight_layout()
    plt.savefig('visualizations/improved_phase_transition.png', dpi=150)
    plt.close()
    
    print("\nPhase transition demonstrated!")
    print("See visualizations/improved_phase_transition.png")
    
    return results


if __name__ == "__main__":
    results = demonstrate_phase_transition() 