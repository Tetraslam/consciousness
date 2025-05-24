"""
Discovery AI Agent Hackathon Demo
=================================

Consciousness as Error Correction
github.com/tetraslam/consciousness
"""

import os
import subprocess
import sys
import time
import webbrowser


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print the demo header."""
    clear_screen()
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         CONSCIOUSNESS AS ERROR CORRECTION                 ║
    ║           Discovery AI Agent Hackathon 2024               ║
    ║                                                           ║
    ║         github.com/tetraslam/consciousness                ║
    ╚═══════════════════════════════════════════════════════════╝
    """)


def run_presenterm():
    """Run the presenterm presentation."""
    print("\nStarting presentation mode...")
    print("Controls: Arrow keys to navigate, 'q' to quit\n")
    time.sleep(2)
    
    # Ensure presenterm is available in PATH
    try:
        subprocess.run(["presenterm", "--version"], capture_output=True, check=True)
    except FileNotFoundError:
        print("Error: 'presenterm' command not found. Install it (e.g., cargo install presenterm) and ensure it's in your PATH.")
        input("Press Enter to return to menu...")
        return

    # Run the presentation
    subprocess.run(["presenterm", "-X", "demo/presentation.md"])


def run_interactive_demo():
    """Run the interactive visualization."""
    print_header()
    print("\nLaunching interactive consciousness visualization...")
    print("\nInstructions:")
    print("1. Adjust the Error Correction slider from 0 to 0.4")
    print("2. Watch consciousness emerge at EC > 0.3!")
    print("3. Try different noise levels")
    print("4. Observe the phase space trajectories\n")
    
    input("Press Enter to launch...")
    
    # Run the interactive demo
    subprocess.run(['uv', 'run', 'demo/interactive_consciousness_demo.py'])


def show_results():
    """Open the visualization results."""
    print_header()
    print("\nOpening visualization results...")
    
    visualizations = [
        'visualizations/realistic_phase_transition.png',
        'visualizations/consciousness_emergence.png',
        'visualizations/psychedelic_test.png',
        'visualizations/development_test.png',
        'visualizations/anesthesia_test.png'
    ]
    
    for viz in visualizations:
        if os.path.exists(viz):
            print(f"Opening {viz}...")
            webbrowser.open(f'file://{os.path.abspath(viz)}')
            time.sleep(0.5)


def run_quick_test():
    """Run a quick consciousness test."""
    print_header()
    print("\nRunning quick consciousness test...\n")
    
    subprocess.run(['uv', 'run', 'demo/test_ec_threshold.py'])
    
    print("\nConsciousness is what error correction feels like.")
    input("\nPress Enter to continue...")


def main_menu():
    """Main demo menu."""
    while True:
        print_header()
        print("""
    Select Demo Mode:
    
    1. Full Presentation (presenterm)
    2. Interactive Visualization
    3. Quick Consciousness Test
    4. View Results Gallery
    5. Open GitHub Repository
    
    0. Exit
        """)
        
        choice = input("\nEnter your choice (0-5): ")
        
        if choice == '1':
            run_presenterm()
        elif choice == '2':
            run_interactive_demo()
        elif choice == '3':
            run_quick_test()
        elif choice == '4':
            show_results()
        elif choice == '5':
            print("\nOpening GitHub repository...")
            webbrowser.open('https://github.com/tetraslam/consciousness')
            input("\nPress Enter to continue...")
        elif choice == '0':
            print("\nConsciousness is what error correction feels like.")
            print("Thank you!")
            break
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(1)


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nConsciousness is what error correction feels like.")
        print("Thank you!") 