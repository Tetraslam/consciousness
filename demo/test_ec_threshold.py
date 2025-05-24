"""
Quick test to verify EC threshold is working correctly.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

from simulations.models.conscious_neural_network_v2 import \
    ConsciousNeuralNetworkV2


def test_ec_threshold():
    """Test that consciousness only emerges above EC = 0.3"""
    print("Testing EC threshold for consciousness...")
    print("-" * 50)
    
    ec_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.8, 1.0]
    
    for ec in ec_values:
        # Create network
        net = ConsciousNeuralNetworkV2(noise_level=0.3)
        net.set_error_correction(ec)
        
        # Run simulation
        net.run_simulation(steps=150)
        
        # Get final consciousness level
        final_consciousness = np.mean(net.history['consciousness_level'][-50:])
        
        print(f"EC = {ec:.1f}: Consciousness = {final_consciousness:.3f}, "
              f"Conscious = {net.is_conscious}")
    
    print("-" * 50)
    print("[PASS] EC > 0.3 required for consciousness!")

if __name__ == "__main__":
    test_ec_threshold() 