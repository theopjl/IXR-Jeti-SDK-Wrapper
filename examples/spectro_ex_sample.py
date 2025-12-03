"""
Python version of SpectroExSample.c
Demonstrates light measurements using JETI Spectro Ex SDK
"""

import sys
from pathlib import Path

# Add src directory to path for development mode
_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root / "src"))

from jeti import JetiSpectroEx, JetiException
import numpy as np


class SpectroExMeasurementApp:
    """Application for performing spectroscopic light measurements"""
    
    def __init__(self):
        self.device = None
        
    def initialize_device(self):
        """Initialize and open the JETI device"""
        print("\nSearching for JETI Spectro devices...")
        
        self.device = JetiSpectroEx()
        
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
            
            # Display pixel count
            pixel_count = self.device.get_pixel_count()
            print(f"Pixel count: {pixel_count}")
            
            return True
            
        except JetiException as e:
            print(f"Error initializing device: {e}")
            return False
    
    def perform_light_measurement(self, integration_time: float = 100.0, 
                                 average: int = 1,
                                 wavelength_start: int = 380,
                                 wavelength_end: int = 780,
                                 step: float = 5.0):
        """
        Perform a complete light measurement
        
        Args:
            integration_time: Integration time in ms (0 for automatic)
            average: Number of averages
            wavelength_start: Start wavelength in nm
            wavelength_end: End wavelength in nm
            step: Step width in nm
        """
        print("\n" + "=" * 60)
        print("Performing light measurement...")
        print(f"Parameters: Tint={integration_time}ms, Avg={average}")
        print(f"Wavelength: {wavelength_start}-{wavelength_end}nm (step={step}nm)")
        print("=" * 60)
        
        try:
            # Start measurement
            print("\nStarting measurement...")
            self.device.start_light_measurement(integration_time, average)
            
            # Wait for measurement to complete
            print("Measuring", end="", flush=True)
            while self.device.get_status():
                print(".", end="", flush=True)
                import time
                time.sleep(0.1)
            print(" Done!\n")
            
            # Get light spectrum
            print("Reading light spectrum...")
            spectrum = self.device.get_light_spectrum_wavelength(
                wavelength_start, wavelength_end, step
            )
            
            # Display results
            self.display_spectrum_info(spectrum, wavelength_start, wavelength_end, step)
            
            return spectrum
            
        except JetiException as e:
            print(f"Error during measurement: {e}")
            return None
    
    def display_spectrum_info(self, spectrum: np.ndarray, 
                             wavelength_start: int,
                             wavelength_end: int,
                             step: float):
        """Display spectrum information"""
        print("\n" + "-" * 60)
        print("LIGHT SPECTRUM")
        print("-" * 60)
        print(f"Wavelength range: {wavelength_start}nm to {wavelength_end}nm")
        print(f"Step width: {step}nm")
        print(f"Number of points: {len(spectrum)}")
        print(f"\nStatistics:")
        print(f"  Min value:  {np.min(spectrum):.3E}")
        print(f"  Max value:  {np.max(spectrum):.3E}")
        print(f"  Mean value: {np.mean(spectrum):.3E}")
        print(f"  Std dev:    {np.std(spectrum):.3E}")
        
        print(f"\nFirst 10 values:")
        for i in range(min(10, len(spectrum))):
            wavelength = wavelength_start + i * step
            print(f"  {wavelength:.1f}nm: {spectrum[i]:.3E}")
        
        print("-" * 60 + "\n")
    
    def get_pixel_spectrum(self):
        """Get and display raw pixel spectrum"""
        try:
            print("\nGetting raw pixel spectrum...")
            
            pixel_count = self.device.get_pixel_count()
            print(f"Reading {pixel_count} pixels...")
            
            pixel_spectrum = self.device.get_light_spectrum_pixel()
            
            print(f"\nPixel spectrum shape: {pixel_spectrum.shape}")
            print(f"Data type: {pixel_spectrum.dtype}")
            print(f"\nStatistics:")
            print(f"  Min value:  {np.min(pixel_spectrum)}")
            print(f"  Max value:  {np.max(pixel_spectrum)}")
            print(f"  Mean value: {np.mean(pixel_spectrum):.2f}")
            
            print(f"\nFirst 10 pixels:")
            for i in range(min(10, len(pixel_spectrum))):
                print(f"  Pixel {i}: {pixel_spectrum[i]}")
            
            return pixel_spectrum
            
        except JetiException as e:
            print(f"Error getting pixel spectrum: {e}")
            return None
    
    def run_interactive_measurement(self):
        """Run an interactive measurement with user-specified parameters"""
        print("\n" + "=" * 60)
        print("INTERACTIVE LIGHT MEASUREMENT")
        print("=" * 60)
        
        try:
            # Get parameters from user
            print("\nMeasurement parameters:")
            tint = float(input("  Integration time in ms (0 for automatic): "))
            avg = int(input("  Number of averages: "))
            
            print("\nWavelength parameters:")
            wl_start = int(input("  Start wavelength (nm): "))
            wl_end = int(input("  End wavelength (nm): "))
            step = float(input("  Step width (nm): "))
            
            # Perform measurement
            spectrum = self.perform_light_measurement(tint, avg, wl_start, wl_end, step)
            
            if spectrum is not None:
                # Ask if user wants to save
                save = input("\nSave spectrum to file? (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("Filename: ").strip()
                    wavelengths = np.arange(wl_start, wl_end + step, step)
                    # Ensure arrays have same length
                    min_len = min(len(wavelengths), len(spectrum))
                    data = np.column_stack((wavelengths[:min_len], spectrum[:min_len]))
                    np.savetxt(filename, data, fmt='%.6e', 
                             header='Wavelength(nm)\tLightIntensity')
                    print(f"Spectrum saved to {filename}")
            
        except ValueError as e:
            print(f"Invalid input: {e}")
        except JetiException as e:
            print(f"Error: {e}")
    
    def run_menu(self):
        """Run the interactive menu"""
        while True:
            print("\n" + "=" * 60)
            print("JETI SPECTRO EX - MAIN MENU")
            print("=" * 60)
            print("1) Perform light measurement (default parameters)")
            print("2) Interactive measurement (custom parameters)")
            print("\n--- Single Operations ---")
            print("a) Start light measurement")
            print("b) Break measurement")
            print("c) Get measurement status")
            print("d) Get light spectrum (wavelength based)")
            print("e) Get light spectrum (pixel based)")
            print("\n0) Exit")
            print("=" * 60)
            
            choice = input("\nYour choice: ").strip().lower()
            
            if choice == '1':
                # Default: 100ms integration, 1 average, 380-780nm, 5nm step
                self.perform_light_measurement(100.0, 1, 380, 780, 5.0)
                input("\nPress Enter to continue...")
                
            elif choice == '2':
                self.run_interactive_measurement()
                input("\nPress Enter to continue...")
                
            elif choice == 'a':
                try:
                    tint = float(input("Integration time in ms (0 for automatic): "))
                    avg = int(input("Number of averages: "))
                    print("Starting measurement...")
                    self.device.start_light_measurement(tint, avg)
                    print("Measurement started!")
                except ValueError as e:
                    print(f"Invalid input: {e}")
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
                    status = self.device.get_status()
                    if status:
                        print("Measurement is running...")
                    else:
                        print("Measurement finished!")
                except JetiException as e:
                    print(f"Error: {e}")
                input("\nPress Enter to continue...")
                
            elif choice == 'd':
                try:
                    wl_start = int(input("Start wavelength (nm): "))
                    wl_end = int(input("End wavelength (nm): "))
                    step = float(input("Step width (nm): "))
                    spectrum = self.device.get_light_spectrum_wavelength(
                        wl_start, wl_end, step
                    )
                    self.display_spectrum_info(spectrum, wl_start, wl_end, step)
                except ValueError as e:
                    print(f"Invalid input: {e}")
                except JetiException as e:
                    print(f"Error: {e}")
                input("\nPress Enter to continue...")
                
            elif choice == 'e':
                self.get_pixel_spectrum()
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
    app = SpectroExMeasurementApp()
    
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
