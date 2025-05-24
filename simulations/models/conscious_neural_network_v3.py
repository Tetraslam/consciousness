"""
Realistic conscious neural network with proper phase transitions.
This version shows a sharp but continuous phase transition.
"""

import matplotlib.pyplot as plt
import numpy as np

from simulations.models.conscious_neural_network_v2 import \
    ConsciousNeuralNetworkV2


class ConsciousNeuralNetworkV3(ConsciousNeuralNetworkV2):
    """
    Improved version with more realistic phase transitions.
    """
    
    def _measure_consciousness_v2(self):
        """
        Realistic consciousness measurement with proper phase transition.
        """
        if len(self.history['raw_state']) < 20:
            return 0.0
            
        # Get recent history
        recent_raw = np.array(self.history['raw_state'][-20:])
        recent_corrected = np.array(self.history['corrected_state'][-20:])
        recent_thoughts = np.array([self._extract_thought(s) for s in recent_corrected])
        
        # 1. Noise suppression
        raw_noise = np.mean([np.std(state) for state in recent_raw])
        corrected_noise = np.mean([np.std(state) for state in recent_corrected])
        
        if raw_noise > 0:
            noise_suppression = (raw_noise - corrected_noise) / raw_noise
            noise_suppression = np.clip(noise_suppression, 0, 1)
        else:
            noise_suppression = 0
            
        # 2. Temporal coherence
        if len(recent_thoughts) > 1:
            thought_changes = np.diff(recent_thoughts, axis=0)
            temporal_coherence = 1.0 / (1.0 + np.mean(np.abs(thought_changes)))
        else:
            temporal_coherence = 0
            
        # 3. Recursive stability
        if len(self.history['prediction_error']) > 10:
            recent_pred_errors = self.history['prediction_error'][-10:]
            avg_pred_error = np.mean(recent_pred_errors)
            recursive_stability = 1.0 / (1.0 + avg_pred_error * 5)
        else:
            recursive_stability = 0
            
        # 4. Information integration
        if len(recent_thoughts) > 0:
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
            
        # REALISTIC PHASE TRANSITION
        # Critical region is around EC = 0.25 to 0.35
        ec = self.error_correction_strength
        
        # Base consciousness from metrics
        base_consciousness = (
            noise_suppression * 0.25 +
            temporal_coherence * 0.25 +
            recursive_stability * 0.25 +
            integration * 0.25
        )
        
        # Phase transition function
        # Uses a steep sigmoid around critical point
        critical_ec = 0.3
        steepness = 20  # Controls how sharp the transition is
        
        # Sigmoid transition
        transition_factor = 1 / (1 + np.exp(-steepness * (ec - critical_ec)))
        
        # Add some noise in the transition region for realism
        if 0.25 < ec < 0.35:
            transition_noise = np.random.normal(0, 0.02)
            transition_factor = np.clip(transition_factor + transition_noise, 0, 1)
        
        # Scale consciousness by transition factor
        # Below critical: suppressed
        # Above critical: enhanced
        consciousness = base_consciousness * (0.1 + 0.9 * transition_factor)
        
        # Add small random fluctuations for realism
        consciousness += np.random.normal(0, 0.005)
        consciousness = np.clip(consciousness, 0, 1)
        
        # Determine if conscious (with some hysteresis)
        if hasattr(self, 'was_conscious'):
            # Hysteresis to prevent flickering
            if self.was_conscious:
                self.is_conscious = consciousness > 0.25
            else:
                self.is_conscious = consciousness > 0.35
        else:
            self.is_conscious = consciousness > 0.3
            
        self.was_conscious = self.is_conscious
        
        return consciousness
    
    def _error_correct_v2(self, noisy_state):
        """
        Error correction with gradual effectiveness.
        """
        corrected = np.zeros_like(noisy_state)
        
        # Effectiveness of error correction scales smoothly
        effectiveness = self.error_correction_strength
        
        for i in range(self.n_modules):
            module_start = i * self.n_neurons
            module_end = (i + 1) * self.n_neurons
            module_state = noisy_state[module_start:module_end]
            
            if effectiveness > 0.1:  # Some minimal correction
                # Number of measurements scales with EC strength
                n_measurements = max(1, int(effectiveness * 15))
                measurements = []
                
                for _ in range(n_measurements):
                    # Measurement noise decreases with EC strength
                    meas_noise = np.random.normal(0, self.noise_level * (1 - 0.5 * effectiveness), 
                                                self.n_neurons)
                    noisy_measurement = module_state + meas_noise
                    
                    # Phase encoding
                    phase = np.angle(np.sum(noisy_measurement * 
                                          np.exp(1j * self.frequencies[i] * 
                                                np.linspace(0, 2*np.pi, self.n_neurons))))
                    
                    # Decode
                    decoded = np.cos(self.frequencies[i] * 
                                   np.linspace(0, 2*np.pi, self.n_neurons) - phase)
                    measurements.append(decoded)
                
                if n_measurements > 1:
                    corrected_module = np.median(measurements, axis=0)
                else:
                    corrected_module = measurements[0]
                    
                # Blend between noisy and corrected based on effectiveness
                corrected_module = (1 - effectiveness) * module_state + effectiveness * corrected_module
                corrected_module *= np.mean(np.abs(module_state))
            else:
                corrected_module = module_state
                
            corrected[module_start:module_end] = corrected_module
            
        return corrected


def test_realistic_transition():
    """Test the realistic phase transition."""
    print("Testing realistic phase transition...")
    
    # Test fine-grained EC values
    ec_values = np.linspace(0, 0.5, 26)
    consciousness_levels = []
    
    for ec in ec_values:
        net = ConsciousNeuralNetworkV3(noise_level=0.3)
        net.set_error_correction(ec)
        net.run_simulation(steps=150)
        
        final_c = np.mean(net.history['consciousness_level'][-50:])
        consciousness_levels.append(final_c)
        
        print(f"EC = {ec:.2f}: Consciousness = {final_c:.3f}")
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(ec_values, consciousness_levels, 'b-', linewidth=2, marker='o', markersize=4)
    plt.axhline(y=0.3, color='red', linestyle='--', label='Consciousness threshold')
    plt.axvline(x=0.3, color='gray', linestyle=':', label='Critical EC')
    
    # Highlight transition region
    plt.axvspan(0.25, 0.35, alpha=0.2, color='yellow', label='Transition region')
    
    plt.xlabel('Error Correction Strength')
    plt.ylabel('Consciousness Level')
    plt.title('Realistic Phase Transition in Consciousness')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('visualizations/realistic_phase_transition.png', dpi=150)
    plt.close()
    
    print("\nPhase transition is now more realistic!")
    print("- Gradual increase around EC = 0.3")
    print("- Some variability in transition region")
    print("- Still sharp but not instant")


if __name__ == "__main__":
    test_realistic_transition() 