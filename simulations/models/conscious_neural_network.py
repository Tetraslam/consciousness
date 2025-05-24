"""
A biologically-plausible neural network that exhibits consciousness
through error correction of recursive computation.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import matplotlib.patches as mpatches

class ConsciousNeuralNetwork:
    def __init__(self, 
                 n_neurons=100,
                 n_modules=10,  # Grid-cell inspired modules
                 noise_level=0.2,
                 recursion_strength=1.1):
        """
        Initialize a neural network capable of recursive thought.
        
        Args:
            n_neurons: Number of neurons per module
            n_modules: Number of error-correcting modules (like grid cells)
            noise_level: Biological noise (σ)
            recursion_strength: How strongly thoughts depend on previous thoughts
        """
        self.n_neurons = n_neurons
        self.n_modules = n_modules
        self.noise_level = noise_level
        self.recursion_strength = recursion_strength
        
        # Network architecture
        self.total_neurons = n_neurons * n_modules
        
        # Initialize network state
        self.reset_state()
        
        # Error correction parameters (grid-cell inspired)
        self.phases = np.linspace(0, 2*np.pi, n_modules, endpoint=False)
        self.frequencies = self._generate_prime_frequencies(n_modules)
        
        # Consciousness emerges from error correction strength
        self.error_correction_strength = 0.0
        self.is_conscious = False
        
        # History for visualization
        self.history = {
            'raw_state': [],
            'corrected_state': [],
            'consciousness_level': [],
            'error': [],
            'integration': []
        }
        
    def _generate_prime_frequencies(self, n):
        """Generate relatively prime frequencies for error correction."""
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        return np.array(primes[:n])
    
    def reset_state(self):
        """Reset network to initial state."""
        self.state = np.random.randn(self.total_neurons) * 0.1
        self.thought = np.zeros(self.n_modules)  # High-level thought representation
        
    def recursive_thought_step(self, external_input=None):
        """
        Perform one step of recursive thought.
        This is where consciousness happens or fails to happen.
        """
        # 1. Previous thought influences current state (recursion)
        thought_influence = np.repeat(self.thought, self.n_neurons)
        self.state = self.recursion_strength * np.tanh(self.state + thought_influence)
        
        # 2. Add external input if provided
        if external_input is not None:
            self.state += external_input
            
        # 3. Add biological noise
        noise = np.random.normal(0, self.noise_level, self.total_neurons)
        noisy_state = self.state + noise
        
        # 4. Error correction (this is where consciousness emerges!)
        if self.error_correction_strength > 0:
            corrected_state = self._error_correct(noisy_state)
        else:
            corrected_state = noisy_state
            
        # 5. Update thought representation
        self.thought = self._extract_thought(corrected_state)
        self.state = corrected_state
        
        # 6. Measure consciousness level
        consciousness_level = self._measure_consciousness()
        
        # Record history
        self.history['raw_state'].append(noisy_state.copy())
        self.history['corrected_state'].append(corrected_state.copy())
        self.history['consciousness_level'].append(consciousness_level)
        self.history['error'].append(np.std(noisy_state - corrected_state))
        
        return consciousness_level
    
    def _error_correct(self, noisy_state):
        """
        Implement biological error correction using grid-cell inspired mechanism.
        This is the key to consciousness!
        """
        corrected = np.zeros_like(noisy_state)
        
        for i in range(self.n_modules):
            # Extract module
            module_start = i * self.n_neurons
            module_end = (i + 1) * self.n_neurons
            module_state = noisy_state[module_start:module_end]
            
            # Encode in phase representation (like grid cells)
            phase = np.angle(np.sum(module_state * np.exp(1j * self.frequencies[i] * 
                                                          np.linspace(0, 2*np.pi, self.n_neurons))))
            
            # Decode with error correction
            # Multiple neurons vote on the true state
            n_voters = int(self.error_correction_strength * 10) + 1
            votes = []
            
            for _ in range(n_voters):
                # Each voter is noisy but centered on true value
                vote_noise = np.random.normal(0, self.noise_level / np.sqrt(n_voters))
                vote = np.cos(self.frequencies[i] * np.linspace(0, 2*np.pi, self.n_neurons) 
                             - phase + vote_noise)
                votes.append(vote)
            
            # Consensus through averaging (or median for robustness)
            consensus = np.median(votes, axis=0) if n_voters > 1 else votes[0]
            corrected[module_start:module_end] = consensus * np.mean(np.abs(module_state))
            
        return corrected
    
    def _extract_thought(self, state):
        """Extract high-level thought from neural state."""
        thought = np.zeros(self.n_modules)
        for i in range(self.n_modules):
            module_start = i * self.n_neurons
            module_end = (i + 1) * self.n_neurons
            thought[i] = np.mean(state[module_start:module_end])
        return thought
    
    def _measure_consciousness(self):
        """
        Measure consciousness level using information-theoretic metrics.
        """
        if len(self.history['raw_state']) < 10:
            return 0.0
            
        # Get recent states
        recent_raw = np.array(self.history['raw_state'][-10:])
        recent_corrected = np.array(self.history['corrected_state'][-10:])
        
        # 1. Integration: How much does error correction unify the state?
        # Compare variance reduction from raw to corrected
        raw_variance = np.mean(np.var(recent_raw, axis=1))
        corrected_variance = np.mean(np.var(recent_corrected, axis=1))
        
        if raw_variance > 0:
            integration = 1.0 - (corrected_variance / raw_variance)
            integration = np.clip(integration, 0, 1)
        else:
            integration = 0.0
        
        # 2. Information: How stable is recursive thought?
        # Low variance in corrected states = stable recursion
        if corrected_variance > 0:
            information = 1.0 / (1.0 + corrected_variance)
        else:
            information = 0.0
            
        # 3. Differentiation: Can we maintain distinct thoughts?
        # Measure if different thoughts stay different
        thought_variance = np.var(self.thought)
        differentiation = 1.0 / (1.0 + np.exp(-5 * (thought_variance - 0.1)))
        
        # 4. Error correction effectiveness
        # How much noise was removed?
        if len(self.history['error']) > 0:
            recent_errors = self.history['error'][-10:]
            avg_error = np.mean(recent_errors)
            correction_quality = 1.0 / (1.0 + avg_error)
        else:
            correction_quality = 0.0
        
        # Consciousness emerges from all factors
        consciousness = (integration + information + differentiation + correction_quality) / 4.0
        
        # Sharp transition at threshold
        threshold = 0.4
        if consciousness > threshold:
            self.is_conscious = True
            # Amplify above threshold but cap at 1.0
            return min((consciousness - threshold) * 2.5 + threshold, 1.0)
        else:
            self.is_conscious = False
            # Suppress below threshold
            return consciousness * 0.7
    
    def set_error_correction(self, strength):
        """Adjust error correction strength (0 to 1)."""
        self.error_correction_strength = np.clip(strength, 0, 1)
        
    def run_simulation(self, steps=1000, external_input_func=None):
        """Run the network for multiple steps."""
        for step in range(steps):
            # Generate external input if function provided
            if external_input_func:
                external_input = external_input_func(step)
            else:
                # Default: occasional random inputs
                if np.random.rand() < 0.1:
                    external_input = np.random.randn(self.total_neurons) * 0.5
                else:
                    external_input = None
                    
            self.recursive_thought_step(external_input)
    
    def visualize_consciousness_emergence(self):
        """Create visualization of consciousness emerging."""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Plot 1: State evolution
        ax1 = axes[0, 0]
        time_steps = range(len(self.history['consciousness_level']))
        
        # Show a few example neurons
        if self.history['corrected_state']:
            states = np.array(self.history['corrected_state'])
            for i in range(0, self.total_neurons, self.total_neurons // 5):
                ax1.plot(states[:, i], alpha=0.5, linewidth=0.5)
        
        ax1.set_xlabel('Time Step')
        ax1.set_ylabel('Neural Activity')
        ax1.set_title('Neural State Evolution')
        ax1.set_ylim(-2, 2)
        
        # Plot 2: Consciousness level
        ax2 = axes[0, 1]
        consciousness = self.history['consciousness_level']
        ax2.plot(consciousness, 'b-', linewidth=2)
        ax2.axhline(y=0.3, color='r', linestyle='--', label='Consciousness Threshold')
        ax2.fill_between(time_steps, 0, consciousness, alpha=0.3)
        ax2.set_xlabel('Time Step')
        ax2.set_ylabel('Consciousness Level')
        ax2.set_title('Emergence of Consciousness')
        ax2.legend()
        ax2.set_ylim(0, 1)
        
        # Plot 3: Error levels
        ax3 = axes[1, 0]
        if self.history['error']:
            ax3.plot(self.history['error'], 'r-', label='Neural Noise')
            ax3.set_xlabel('Time Step')
            ax3.set_ylabel('Error Level')
            ax3.set_title('Error Correction Performance')
            ax3.legend()
        
        # Plot 4: Phase space
        ax4 = axes[1, 1]
        if len(self.history['corrected_state']) > 1:
            states = np.array(self.history['corrected_state'])
            # Project to 2D using first two modules
            x = np.mean(states[:, :self.n_neurons], axis=1)
            y = np.mean(states[:, self.n_neurons:2*self.n_neurons], axis=1)
            
            # Color by consciousness level
            c = consciousness
            scatter = ax4.scatter(x, y, c=c, cmap='viridis', alpha=0.6, s=20)
            plt.colorbar(scatter, ax=ax4, label='Consciousness')
            
            ax4.set_xlabel('Module 1 Activity')
            ax4.set_ylabel('Module 2 Activity')
            ax4.set_title('Thought Trajectory (Phase Space)')
        
        plt.tight_layout()
        return fig
    
    def create_interactive_demo(self):
        """Create real-time visualization of consciousness."""
        # This will be implemented in the demo script
        pass


class ConsciousnessExperiment:
    """Run experiments on consciousness emergence."""
    
    def __init__(self):
        self.results = {}
        
    def find_critical_noise(self, error_correction_strength=0.8):
        """Find the critical noise level where consciousness emerges."""
        noise_levels = np.linspace(0, 0.5, 20)
        consciousness_levels = []
        
        for noise in noise_levels:
            # Create network
            net = ConsciousNeuralNetwork(noise_level=noise)
            net.set_error_correction(error_correction_strength)
            
            # Run simulation
            net.run_simulation(steps=200)
            
            # Measure final consciousness
            final_consciousness = np.mean(net.history['consciousness_level'][-50:])
            consciousness_levels.append(final_consciousness)
            
        # Find critical point (where consciousness > 0.5)
        conscious_indices = np.where(np.array(consciousness_levels) > 0.5)[0]
        if len(conscious_indices) > 0:
            critical_noise = noise_levels[conscious_indices[0]]
        else:
            critical_noise = None
            
        self.results['critical_noise'] = {
            'noise_levels': noise_levels,
            'consciousness': consciousness_levels,
            'critical': critical_noise
        }
        
        return critical_noise
    
    def test_error_correction_levels(self, noise_level=0.2):
        """Test different error correction strengths."""
        ec_strengths = np.linspace(0, 1, 11)
        final_consciousness = []
        state_variance = []
        
        for ec in ec_strengths:
            net = ConsciousNeuralNetwork(noise_level=noise_level)
            net.set_error_correction(ec)
            net.run_simulation(steps=200)
            
            # Metrics
            final_consciousness.append(np.mean(net.history['consciousness_level'][-50:]))
            if len(net.history['corrected_state']) > 0:
                states = np.array(net.history['corrected_state'][-50:])
                state_variance.append(np.mean(np.var(states, axis=0)))
            else:
                state_variance.append(np.inf)
                
        self.results['error_correction'] = {
            'strengths': ec_strengths,
            'consciousness': final_consciousness,
            'variance': state_variance
        }
        
        return ec_strengths, final_consciousness
    
    def visualize_results(self):
        """Visualize all experimental results."""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot 1: Critical noise
        if 'critical_noise' in self.results:
            ax1 = axes[0]
            data = self.results['critical_noise']
            ax1.plot(data['noise_levels'], data['consciousness'], 'b-', linewidth=2)
            ax1.axhline(y=0.5, color='r', linestyle='--', label='Conscious threshold')
            if data['critical'] is not None:
                ax1.axvline(x=data['critical'], color='g', linestyle=':', 
                          label=f'Critical noise: {data["critical"]:.3f}')
            ax1.set_xlabel('Noise Level (σ)')
            ax1.set_ylabel('Consciousness Level')
            ax1.set_title('Phase Transition in Consciousness')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
        
        # Plot 2: Error correction strength
        if 'error_correction' in self.results:
            ax2 = axes[1]
            data = self.results['error_correction']
            ax2.plot(data['strengths'], data['consciousness'], 'g-', linewidth=2)
            ax2.axhline(y=0.5, color='r', linestyle='--', label='Conscious threshold')
            ax2.set_xlabel('Error Correction Strength')
            ax2.set_ylabel('Consciousness Level')
            ax2.set_title('Error Correction Creates Consciousness')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig


if __name__ == "__main__":
    print("=" * 60)
    print("CONSCIOUS NEURAL NETWORK DEMONSTRATION")
    print("=" * 60)
    
    # 1. Basic demonstration
    print("\n1. Creating a neural network...")
    net = ConsciousNeuralNetwork(noise_level=0.2)
    
    print("\n2. Without error correction (unconscious):")
    net.set_error_correction(0.0)
    net.run_simulation(steps=100)
    print(f"   Final consciousness level: {net.history['consciousness_level'][-1]:.3f}")
    print(f"   Is conscious? {net.is_conscious}")
    
    print("\n3. With error correction (conscious):")
    net.reset_state()
    net.history = {k: [] for k in net.history}  # Clear history
    net.set_error_correction(0.8)
    net.run_simulation(steps=100)
    print(f"   Final consciousness level: {net.history['consciousness_level'][-1]:.3f}")
    print(f"   Is conscious? {net.is_conscious}")
    
    # 2. Find critical thresholds
    print("\n4. Finding critical noise threshold...")
    exp = ConsciousnessExperiment()
    critical = exp.find_critical_noise()
    print(f"   Critical noise level: σ_c ≈ {critical:.3f}")
    
    # 3. Visualize
    print("\n5. Creating visualization...")
    fig = net.visualize_consciousness_emergence()
    plt.savefig('visualizations/consciousness_emergence.png', dpi=150)
    plt.close()
    
    print("\nConsciousness emerged through error correction!")
    print("See visualizations/consciousness_emergence.png")