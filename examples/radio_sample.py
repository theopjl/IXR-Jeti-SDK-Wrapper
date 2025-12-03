"""
Python version of RadioSample.c
Demonstrates basic radiometric measurements using JETI SDK
"""

import sys
from pathlib import Path

# Add src directory to path for development mode
_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root / "src"))

from jeti import JetiRadio, JetiException
import numpy as np


class RadioMeasurementApp:
    """Application for performing radiometric measurements"""
    
    def __init__(self):
        self.device = None
        
    def initialize_device(self):
        """Initialize and open the JETI device"""
        print("\nSearching for JETI devices...")
        
        self.device = JetiRadio()
        
        try:
            num_devices = self.device.get_num_devices()
            
            if num_devices == 0:
                print("No matching device found!")
                return False
            
            if num_devices > 1:
                print(f"\nFound {num_devices} devices:")
                for i in range(num_devices):
                    board_sn, spec_sn, device_sn = self.device.get_serial_device(i)
                    print(f"Device {i}: Board S/N: {board_sn}, Spec S/N: {spec_sn}, Device S/N: {device_sn}")
                
                device_num = int(input("\nEnter device number to open: "))
                if device_num >= num_devices:
                    print("Invalid device number!")
                    return False
            else:
                device_num = 0
            
            # Open the device
            self.device.open_device(device_num)
            print(f"Device {device_num} opened successfully!")
            return True
            
        except JetiException as e:
            print(f"Error initializing device: {e}")
            return False
    
    def perform_measurement(self):
        """Perform a complete radiometric measurement"""
        print("\n" + "=" * 60)
        print("Performing radiometric measurement...")
        print("=" * 60)
        
        
        try:
            # Start measurement with automatic integration time
            print("Starting measurement (automatic integration time)...")
            self.device.measure()
            
            # Wait for measurement to complete
            print("Measuring", end="", flush=True)
            while self.device.get_measure_status():
                print(".", end="", flush=True)
                import time
                time.sleep(0.1)
            print(" Done!\n")
            
            # Get all measurement results
            results = self.display_results()
            
            return results
            
        except JetiException as e:
            print(f"Error during measurement: {e}")
            return None
    
    def display_results(self):
        """Display all measurement results"""
        try:
            print("\n" + "-" * 60)
            print("MEASUREMENT RESULTS")
            print("-" * 60)
            
            # Radiometric value
            radio = self.device.get_radiometric_value()
            print(f"Radiometric value:        {radio:.3E} W/m²")
            
            # Photometric value
            photo = self.device.get_photometric_value()
            print(f"Photometric value:        {photo:.3E} lx")
            
            # Chromaticity coordinates
            x, y = self.device.get_chromaticity_xy()
            print(f"\nCIE 1931 Chromaticity:")
            print(f"  x: {x:.4f}")
            print(f"  y: {y:.4f}")
            
            # Correlated Color Temperature
            cct = self.device.get_cct()
            print(f"\nCorrelated Color Temperature: {cct:.1f} K")
            
            # Color Rendering Index
            cri = self.device.get_cri()
            print(f"\nColor Rendering Indices (CRI):")
            print(f"  Ra (General):  {cri[0]:.2f}")
            for i in range(1, 15):
                print(f"  R{i:2d}:           {cri[i]:.2f}")
            
            print("-" * 60 + "\n")
            
            return {
                'radiometric': radio,
                'photometric': photo,
                'chromaticity_x': x,
                'chromaticity_y': y,
                'cct': cct,
                'cri': cri
            }
            
        except JetiException as e:
            print(f"Error reading results: {e}")
            return None
    
    def run_menu(self):
        """Run the interactive menu"""
        while True:
            print("\n" + "=" * 60)
            print("JETI RADIO MEASUREMENT - MAIN MENU")
            print("=" * 60)
            print("1) Perform radiometric measurement")
            print("\n--- Single Operations ---")
            print("a) Start radiometric measurement")
            print("b) Break measurement")
            print("c) Get measurement status")
            print("d) Get radiometric value")
            print("e) Get photometric value")
            print("f) Get chromaticity coordinates x and y")
            print("g) Get correlated color temperature CCT")
            print("h) Get color rendering index CRI")
            print("\n0) Exit")
            print("=" * 60)
            
            choice = input("\nYour choice: ").strip().lower()
            
            if choice == '1':
                self.perform_measurement()
                input("\nPress Enter to continue...")
                
            elif choice == 'a':
                try:
                    print("Starting measurement...")
                    self.device.measure()
                    print("Measurement started!")
                except JetiException as e:
                    print(f"Error: {e}")
                input("\nPress Enter to continue...")
                
            elif choice == 'b':
                try:
                    self.device.break_measurement()
                    print("Measurement cancelled!")
                except JetiException as e:
                    print(f"Error: {e}")
                input("\nPress Enter to continue...")
                
            elif choice == 'c':
                try:
                    status = self.device.get_measure_status()
                    if status:
                        print("Measurement is running...")
                    else:
                        print("Measurement finished!")
                except JetiException as e:
                    print(f"Error: {e}")
                input("\nPress Enter to continue...")
                
            elif choice == 'd':
                try:
                    radio = self.device.get_radiometric_value()
                    print(f"Radiometric value: {radio:.3E} W/m²")
                except JetiException as e:
                    print(f"Error: {e}")
                input("\nPress Enter to continue...")
                
            elif choice == 'e':
                try:
                    photo = self.device.get_photometric_value()
                    print(f"Photometric value: {photo:.3E} lx")
                except JetiException as e:
                    print(f"Error: {e}")
                input("\nPress Enter to continue...")
                
            elif choice == 'f':
                try:
                    x, y = self.device.get_chromaticity_xy()
                    print(f"Chromaticity coordinates:")
                    print(f"  x: {x:.4f}")
                    print(f"  y: {y:.4f}")
                except JetiException as e:
                    print(f"Error: {e}")
                input("\nPress Enter to continue...")
                
            elif choice == 'g':
                try:
                    cct = self.device.get_cct()
                    print(f"Correlated Color Temperature: {cct:.1f} K")
                except JetiException as e:
                    print(f"Error: {e}")
                input("\nPress Enter to continue...")
                
            elif choice == 'h':
                try:
                    cri = self.device.get_cri()
                    print("Color Rendering Indices:")
                    print(f"  Ra (General):  {cri[0]:.2f}")
                    for i in range(1, 15):
                        print(f"  R{i:2d}:           {cri[i]:.2f}")
                except JetiException as e:
                    print(f"Error: {e}")
                input("\nPress Enter to continue...")
                
            elif choice == '0':
                break
            else:
                print("Invalid choice!")
                input("\nPress Enter to continue...")
    
    def cleanup(self):
        """Clean up resources"""
        if self.device is not None:
            try:
                self.device.close_device()
                print("Device closed successfully!")
            except JetiException as e:
                print(f"Error closing device: {e}")


def main():
    """Main application entry point"""
    app = RadioMeasurementApp()
    
    try:
        if app.initialize_device():
            app.run_menu()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user!")
    finally:
        app.cleanup()
    
    print("\nGoodbye!")


if __name__ == "__main__":
    main()
