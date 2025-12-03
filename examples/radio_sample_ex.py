"""
Python version of RadioSampleEx.c
Demonstrates radiometric measurements with extended control using JETI SDK
"""

import sys
from pathlib import Path

# Add src directory to path for development mode
_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root / "src"))

from jeti import JetiRadioEx, JetiException
import numpy as np


class RadioExMeasurementApp:
    """Application for performing radiometric measurements with extended parameters"""
    
    def __init__(self):
        self.device = None
        
    def initialize_device(self):
        """Initialize and open the JETI device"""
        print("\nSearching for JETI devices...")
        
        self.device = JetiRadioEx()
        
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
            
            # Display DLL version
            major, minor, build = self.device.get_dll_version()
            print(f"DLL Version: {major}.{minor}.{build}")
            
            return True
            
        except JetiException as e:
            print(f"Error initializing device: {e}")
            return False
    
    def perform_measurement(self, integration_time: float = 0.0, 
                          average: int = 1, step: int = 1):
        """
        Perform a complete radiometric measurement
        
        Args:
            integration_time: Integration time in ms (0 for automatic)
            average: Number of averages
            step: Step width in nm
        """
        print("\n" + "=" * 60)
        print("Performing radiometric measurement...")
        print(f"Parameters: Tint={integration_time}ms, Avg={average}, Step={step}nm")
        print("=" * 60)
        
        try:
            # Start measurement
            print("Starting measurement...")
            self.device.measure(integration_time, average, step)
            
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
    
    def display_results(self, wavelength_start: int = 380, wavelength_end: int = 780):
        """Display all measurement results"""
        try:
            print("\n" + "-" * 60)
            print("MEASUREMENT RESULTS")
            print("-" * 60)
            
            # Radiometric value
            radio = self.device.get_radiometric_value(wavelength_start, wavelength_end)
            print(f"Radiometric value ({wavelength_start}-{wavelength_end}nm): {radio:.3E} W/m²")
            
            # Photometric value
            photo = self.device.get_photometric_value()
            print(f"Photometric value:                         {photo:.3E} lx")
            
            # Chromaticity coordinates
            x, y = self.device.get_chromaticity_xy()
            print(f"\nCIE 1931 Chromaticity:")
            print(f"  x: {x:.4f}")
            print(f"  y: {y:.4f}")
            
            # Correlated Color Temperature
            cct = self.device.get_cct()
            print(f"\nCorrelated Color Temperature: {cct:.1f} K")
            
            # Color Rendering Index
            cri = self.device.get_cri(cct)
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
    
    def get_spectrum(self, wavelength_start: int = 380, wavelength_end: int = 780):
        """Get and display spectral radiance"""
        try:
            print(f"\nGetting spectral radiance ({wavelength_start}-{wavelength_end}nm)...")
            spectrum = self.device.get_spectral_radiance(wavelength_start, wavelength_end)
            
            print(f"Spectrum shape: {spectrum.shape}")
            print(f"Wavelength range: {wavelength_start}nm to {wavelength_end}nm")
            print(f"Number of points: {len(spectrum)}")
            print(f"\nFirst 10 values:")
            for i in range(min(10, len(spectrum))):
                wavelength = wavelength_start + i
                print(f"  {wavelength}nm: {spectrum[i]:.3E}")
            
            return spectrum
            
        except JetiException as e:
            print(f"Error getting spectrum: {e}")
            return None
    
    def run_interactive_measurement(self):
        """Run an interactive measurement with user-specified parameters"""
        print("\n" + "=" * 60)
        print("INTERACTIVE MEASUREMENT")
        print("=" * 60)
        
        try:
            # Get parameters from user
            print("\nMeasurement parameters:")
            tint = float(input("  Integration time in ms (0 for automatic): "))
            avg = int(input("  Number of averages: "))
            step = int(input("  Step width in nm (1, 5, or 10): "))
            
            # Perform measurement
            results = self.perform_measurement(tint, avg, step)
            
            if results is not None:
                # Ask if user wants to see spectrum
                show_spectrum = input("\nShow spectral radiance? (y/n): ").strip().lower()
                if show_spectrum == 'y':
                    wl_start = int(input("  Start wavelength (nm): "))
                    wl_end = int(input("  End wavelength (nm): "))
                    self.get_spectrum(wl_start, wl_end)
            
        except ValueError as e:
            print(f"Invalid input: {e}")
        except JetiException as e:
            print(f"Error: {e}")
    
    def run_menu(self):
        """Run the interactive menu"""
        while True:
            print("\n" + "=" * 60)
            print("JETI RADIO EX MEASUREMENT - MAIN MENU")
            print("=" * 60)
            print("1) Perform radiometric measurement (default parameters)")
            print("2) Interactive measurement (custom parameters)")
            print("3) Get spectral radiance")
            print("\n0) Exit")
            print("=" * 60)
            
            choice = input("\nYour choice: ").strip()
            
            if choice == '1':
                # Default: automatic integration time, 1 average, 1nm step
                self.perform_measurement(0.0, 1, 1)
                input("\nPress Enter to continue...")
                
            elif choice == '2':
                self.run_interactive_measurement()
                input("\nPress Enter to continue...")
                
            elif choice == '3':
                try:
                    wl_start = int(input("Start wavelength (nm): "))
                    wl_end = int(input("End wavelength (nm): "))
                    spectrum = self.get_spectrum(wl_start, wl_end)
                    
                    if spectrum is not None:
                        # Ask if user wants to save
                        save = input("\nSave spectrum to file? (y/n): ").strip().lower()
                        if save == 'y':
                            filename = input("Filename: ").strip()
                            wavelengths = np.arange(wl_start, wl_end + 1)
                            data = np.column_stack((wavelengths, spectrum))
                            np.savetxt(filename, data, fmt='%.6e', 
                                     header='Wavelength(nm)\tSpectralRadiance')
                            print(f"Spectrum saved to {filename}")
                except ValueError as e:
                    print(f"Invalid input: {e}")
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
    app = RadioExMeasurementApp()
    
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
