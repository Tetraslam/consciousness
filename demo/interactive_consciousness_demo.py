"""
Interactive demo for consciousness emergence through error correction.
Perfect for the Discovery AI Agent Hackathon presentation.
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulations.models.conscious_neural_network_v3 import \
    ConsciousNeuralNetworkV3


class InteractiveConsciousnessDemo:
    def __init__(self):
        self.net = ConsciousNeuralNetworkV3(noise_level=0.3)
        self.is_running = False
        self.setup_figure()
        
    def setup_figure(self):
        """Create the interactive figure with controls."""
        self.fig = plt.figure(figsize=(18, 11))
        self.fig.suptitle('Consciousness as Error Correction: Interactive Demo', fontsize=18, weight='bold')
        
        # Create grid layout with better spacing
        gs = self.fig.add_gridspec(3, 3, height_ratios=[2, 2, 1], width_ratios=[2, 2, 1.2],
                                  hspace=0.3, wspace=0.3)
        
        # Main visualization axes
        self.ax_brain = self.fig.add_subplot(gs[0, 0])
        self.ax_consciousness = self.fig.add_subplot(gs[0, 1])
        self.ax_phase = self.fig.add_subplot(gs[1, 0])
        self.ax_metrics = self.fig.add_subplot(gs[1, 1])
        
        # Control panel
        self.ax_controls = self.fig.add_subplot(gs[2, :2])
        self.ax_info = self.fig.add_subplot(gs[:2, 2])
        
        # Initialize plots
        self.setup_brain_view()
        self.setup_consciousness_plot()
        self.setup_phase_plot()
        self.setup_metrics_plot()
        self.setup_controls()
        self.setup_info_panel()
        
    def setup_brain_view(self):
        """Visual representation of neural activity."""
        self.ax_brain.set_title('Neural Activity (10 Modules)')
        self.ax_brain.set_xlabel('Neurons per Module')
        self.ax_brain.set_ylabel('Module')
        
        # Initialize brain state image
        self.brain_img = self.ax_brain.imshow(
            np.zeros((10, 100)), 
            cmap='RdBu_r', 
            vmin=-2, 
            vmax=2,
            aspect='auto'
        )
        
    def setup_consciousness_plot(self):
        """Real-time consciousness level."""
        self.ax_consciousness.set_title('Consciousness Level Over Time')
        self.ax_consciousness.set_xlabel('Time Steps')
        self.ax_consciousness.set_ylabel('Consciousness Level')
        self.ax_consciousness.set_ylim(0, 1.1)
        
        # Initialize lines
        self.consciousness_line, = self.ax_consciousness.plot([], [], 'b-', linewidth=2)
        self.threshold_line = self.ax_consciousness.axhline(
            y=0.35, color='r', linestyle='--', label='Consciousness Threshold'
        )
        self.ax_consciousness.legend()
        
    def setup_phase_plot(self):
        """Phase space visualization."""
        self.ax_phase.set_title('Thought Trajectory (Phase Space)')
        self.ax_phase.set_xlabel('Module 1 Activity')
        self.ax_phase.set_ylabel('Module 2 Activity')
        self.ax_phase.set_xlim(-1.5, 1.5)
        self.ax_phase.set_ylim(-1.5, 1.5)
        
        # Initialize scatter plot
        self.phase_scatter = self.ax_phase.scatter([], [], c=[], cmap='viridis', s=20)
        
    def setup_metrics_plot(self):
        """Key metrics visualization."""
        self.ax_metrics.set_title('Key Metrics')
        
        # Create bars for metrics
        metrics = ['Noise\nSuppression', 'Temporal\nCoherence', 
                  'Recursive\nStability', 'Integration']
        self.metric_bars = self.ax_metrics.bar(metrics, [0, 0, 0, 0], color='gray')
        self.ax_metrics.set_ylim(0, 1)
        self.ax_metrics.set_ylabel('Level')
        
    def setup_controls(self):
        """Interactive controls."""
        self.ax_controls.axis('off')
        
        # Adjust positions to prevent overlap
        # Noise level slider
        self.ax_noise = plt.axes([0.12, 0.18, 0.35, 0.04])
        self.slider_noise = Slider(
            self.ax_noise, 'Noise Level (σ)', 0.0, 0.6, 
            valinit=self.net.noise_level, valstep=0.05,
            color='lightblue'
        )
        self.slider_noise.on_changed(self.update_noise)
        
        # Error correction slider  
        self.ax_ec = plt.axes([0.12, 0.10, 0.35, 0.04])
        self.slider_ec = Slider(
            self.ax_ec, 'Error Correction', 0.0, 1.0,
            valinit=self.net.error_correction_strength, valstep=0.1,
            color='lightgreen'
        )
        self.slider_ec.on_changed(self.update_error_correction)
        
        # Buttons with better spacing
        self.ax_start = plt.axes([0.52, 0.14, 0.08, 0.05])
        self.btn_start = Button(self.ax_start, 'Start', color='lightgray')
        self.btn_start.on_clicked(self.toggle_simulation)
        
        self.ax_reset = plt.axes([0.62, 0.14, 0.08, 0.05])
        self.btn_reset = Button(self.ax_reset, 'Reset', color='lightcoral')
        self.btn_reset.on_clicked(self.reset_simulation)
        
    def setup_info_panel(self):
        """Information panel."""
        self.ax_info.axis('off')
        self.ax_info.set_xlim(0, 1)
        self.ax_info.set_ylim(0, 1)
        
        # Current state section
        self.ax_info.text(0.05, 0.95, 'Current State:', fontsize=14, weight='bold', 
                         transform=self.ax_info.transAxes)
        
        self.info_texts = {
            'state': self.ax_info.text(0.05, 0.88, 'UNCONSCIOUS', fontsize=16, 
                                      color='red', weight='bold', transform=self.ax_info.transAxes),
            'noise': self.ax_info.text(0.05, 0.80, f'Noise: {self.net.noise_level:.2f}', 
                                      fontsize=11, transform=self.ax_info.transAxes),
            'ec': self.ax_info.text(0.05, 0.74, f'EC: {self.net.error_correction_strength:.1f}', 
                                   fontsize=11, transform=self.ax_info.transAxes),
            'level': self.ax_info.text(0.05, 0.68, 'Level: 0.000', fontsize=11, 
                                      transform=self.ax_info.transAxes),
        }
        
        # Key insights section - moved down and spaced better
        self.ax_info.text(0.05, 0.55, 'Key Insights:', fontsize=13, weight='bold',
                         transform=self.ax_info.transAxes)
        
        insights = [
            '• Without EC:\n  Thoughts chaotic',
            '• With EC:\n  Stable recursion',
            '• Phase transition\n  at EC > 0.3',
            '• Consciousness =\n  Error correction\n  for recursion'
        ]
        
        y_pos = 0.45
        for insight in insights:
            self.ax_info.text(0.05, y_pos, insight, fontsize=10, 
                             transform=self.ax_info.transAxes, va='top')
            y_pos -= 0.10
            
    def update_noise(self, val):
        """Update noise level."""
        self.net.noise_level = val
        self.info_texts['noise'].set_text(f'Noise: {val:.2f}')
        
    def update_error_correction(self, val):
        """Update error correction strength."""
        self.net.set_error_correction(val)
        self.info_texts['ec'].set_text(f'EC: {val:.1f}')
        
    def toggle_simulation(self, event):
        """Start/stop simulation."""
        self.is_running = not self.is_running
        if self.is_running:
            self.btn_start.label.set_text('Stop')
            self.animate()
        else:
            self.btn_start.label.set_text('Start')
            
    def reset_simulation(self, event):
        """Reset the simulation."""
        self.net.reset_state()
        self.net.history = {k: [] for k in self.net.history}
        self.update_plots()
        
    def animate(self):
        """Animation loop."""
        if not self.is_running:
            return
            
        # Run one step
        self.net.recursive_thought_step()
        
        # Update plots
        self.update_plots()
        
        # Schedule next frame
        self.fig.canvas.draw_idle()
        self.fig.canvas.start_event_loop(0.05)  # 50ms delay
        
        # Continue animation
        if self.is_running:
            self.fig.canvas.get_tk_widget().after(50, self.animate)
            
    def update_plots(self):
        """Update all visualizations."""
        # 1. Brain activity
        if len(self.net.history['corrected_state']) > 0:
            state = self.net.history['corrected_state'][-1]
            brain_matrix = state.reshape(self.net.n_modules, self.net.n_neurons)
            self.brain_img.set_data(brain_matrix)
            
        # 2. Consciousness level
        if len(self.net.history['consciousness_level']) > 0:
            steps = range(len(self.net.history['consciousness_level']))
            self.consciousness_line.set_data(steps, self.net.history['consciousness_level'])
            self.ax_consciousness.set_xlim(0, max(10, len(steps)))
            
            # Update state text
            current_level = self.net.history['consciousness_level'][-1]
            self.info_texts['level'].set_text(f'Level: {current_level:.3f}')
            
            if self.net.is_conscious:
                self.info_texts['state'].set_text('CONSCIOUS')
                self.info_texts['state'].set_color('green')
            else:
                self.info_texts['state'].set_text('UNCONSCIOUS')
                self.info_texts['state'].set_color('red')
                
        # 3. Phase space
        if len(self.net.history['corrected_state']) > 20:
            states = np.array(self.net.history['corrected_state'][-100:])
            x = np.mean(states[:, :self.net.n_neurons], axis=1)
            y = np.mean(states[:, self.net.n_neurons:2*self.net.n_neurons], axis=1)
            c = self.net.history['consciousness_level'][-100:]
            
            # Update scatter plot
            self.phase_scatter.set_offsets(np.c_[x, y])
            self.phase_scatter.set_array(np.array(c))
            
        # 4. Metrics
        if len(self.net.history['raw_state']) > 20:
            # Calculate current metrics
            metrics = self.calculate_metrics()
            
            # Update bars
            for bar, value in zip(self.metric_bars, metrics):
                bar.set_height(value)
                # Color based on value
                if value > 0.7:
                    bar.set_color('green')
                elif value > 0.3:
                    bar.set_color('yellow')
                else:
                    bar.set_color('red')
                    
    def calculate_metrics(self):
        """Calculate current metrics."""
        # Simplified version for demo
        recent_raw = np.array(self.net.history['raw_state'][-20:])
        recent_corrected = np.array(self.net.history['corrected_state'][-20:])
        
        # Noise suppression
        raw_noise = np.mean([np.std(s) for s in recent_raw])
        corrected_noise = np.mean([np.std(s) for s in recent_corrected])
        noise_suppression = max(0, (raw_noise - corrected_noise) / raw_noise) if raw_noise > 0 else 0
        
        # Temporal coherence (simplified)
        coherence = 1.0 / (1.0 + np.std(recent_corrected))
        
        # Recursive stability (simplified)
        if len(self.net.history['prediction_error']) > 10:
            stability = 1.0 / (1.0 + np.mean(self.net.history['prediction_error'][-10:]))
        else:
            stability = 0
            
        # Integration (simplified)
        integration = 0.5 if self.net.error_correction_strength > 0 else 0.1
        
        return [noise_suppression, coherence, stability, integration]
        
    def run(self):
        """Run the interactive demo."""
        plt.show()


def create_presentation_slides():
    """Generate key slides for the 3-minute presentation."""
    print("\n" + "=" * 60)
    print("CREATING PRESENTATION SLIDES")
    print("=" * 60)
    
    # Slide 1: The Problem
    fig1, ax1 = plt.subplots(figsize=(10, 7))
    ax1.text(0.5, 0.8, 'Why Does Consciousness Exist?', 
             fontsize=28, weight='bold', ha='center', transform=ax1.transAxes)
    
    points = [
        '• Brains are noisy (neural spike variability)',
        '• Yet we have stable, unified experiences',
        '• Evolution doesn\'t create complexity without reason',
        '',
        'What computational problem does consciousness solve?'
    ]
    
    y_pos = 0.6
    for point in points:
        if point == '':
            y_pos -= 0.05
            continue
        ax1.text(0.1, y_pos, point, fontsize=16, transform=ax1.transAxes)
        y_pos -= 0.08
        
    ax1.axis('off')
    plt.tight_layout()
    plt.savefig('demo/slide_1_problem.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Slide 2: The Insight
    fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(14, 7))
    
    # Left: Recursive thought diagram
    ax2a.text(0.5, 0.9, 'Recursive Thought', fontsize=20, weight='bold', 
              ha='center', transform=ax2a.transAxes)
    
    # Draw recursion loop
    circle = plt.Circle((0.5, 0.5), 0.3, fill=False, linewidth=3, color='blue')
    ax2a.add_patch(circle)
    ax2a.arrow(0.8, 0.5, 0, 0.3, head_width=0.05, head_length=0.05, 
               fc='blue', ec='blue', transform=ax2a.transAxes)
    ax2a.text(0.5, 0.5, 'Thought(t)', fontsize=14, ha='center', 
              va='center', transform=ax2a.transAxes)
    ax2a.text(0.85, 0.65, 'Thought(t+1)', fontsize=12, transform=ax2a.transAxes)
    ax2a.text(0.5, 0.2, 'Problem: Noise accumulates\nexponentially!', 
              fontsize=14, ha='center', color='red', transform=ax2a.transAxes)
    ax2a.axis('off')
    
    # Right: Solution
    ax2b.text(0.5, 0.9, 'Consciousness = Error Correction', 
              fontsize=20, weight='bold', ha='center', transform=ax2b.transAxes)
    
    solution_points = [
        '* Multiple measurements',
        '* Vote on true state',
        '* Maintain stable recursion',
        '* Enable planning & metacognition'
    ]
    
    y_pos = 0.7
    for point in solution_points:
        ax2b.text(0.2, y_pos, point, fontsize=14, transform=ax2b.transAxes)
        y_pos -= 0.1
        
    ax2b.text(0.5, 0.2, 'Consciousness is what error\ncorrection feels like!', 
              fontsize=16, ha='center', weight='bold', color='green', 
              transform=ax2b.transAxes)
    ax2b.axis('off')
    
    plt.tight_layout()
    plt.savefig('demo/slide_2_insight.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("[DONE] Presentation slides created in demo/")
    print("[DONE] Ready for interactive demo!")


if __name__ == "__main__":
    # Create presentation materials
    create_presentation_slides()
    
    # Launch interactive demo
    print("\nLaunching interactive demo...")
    print("Use sliders to adjust noise and error correction")
    print("Watch consciousness emerge at the phase transition!")
    
    demo = InteractiveConsciousnessDemo()
    demo.run() 