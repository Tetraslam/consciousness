"""Generate the realistic phase transition diagram.

Run:
    uv run scripts/generate_phase_diagram.py
This uses ConsciousNeuralNetworkV3.test_realistic_transition() to
recompute and save visualizations/realistic_phase_transition.png.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulations.models.conscious_neural_network_v3 import \
    test_realistic_transition

if __name__ == "__main__":
    test_realistic_transition()
    print("\n[OK] realistic_phase_transition.png regenerated under visualizations/\n") 