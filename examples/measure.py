"""
JETI Spectroradiometer Measurement Collection
Collects measurements from a single JETI device and saves raw data to CSV

This script only performs measurements and saves data.
Use analyze_comparison.py to compare two measurement files.
"""

import sys
import csv
import numpy as np
import time
import gc
from pathlib import Path
from datetime import datetime
from typing import Tuple

# Add src directory to path for development mode
_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root / "src"))

from jeti import JetiRadioEx, JetiException

serial_device = ""  # Global variable to hold device serial number for file header
def get_user_inputs(device: JetiRadioEx) -> Tuple[int, str, int, str]:
    """
    Get user inputs for measurement configuration
    
    Args:
        device: JetiRadioEx instance to query available devices
    
    Returns:
        Tuple of (device_index, measurement_type, num_samples, base_filename)
    """
    print("=" * 70)
    print("JETI SPECTRORADIOMETER MEASUREMENT COLLECTION")
    print("=" * 70)
    print()
    print("This script collects measurements from a single JETI device.")
    print()
    
    # Device selection
    num_devices = device.get_num_devices()
    print("DEVICE SELECTION")
    print("-" * 70)
    print(f"Found {num_devices} device(s):")
    print()
    
    if num_devices == 0:
        raise RuntimeError("No devices found. Please connect a JETI device.")
    
    device_info = []
    for i in range(num_devices):
        serial = device.get_serial_device(i)
        device_info.append(serial)
        print(f"  {i + 1}. Device S/N: {serial[2]}")
        serial_device = serial[2]
    
    print()
    
    while True:
        try:
            choice = int(input(f"Select device (1-{num_devices}): ").strip())
            if 1 <= choice <= num_devices:
                device_index = choice - 1
                break
            print(f"Please enter a number between 1 and {num_devices}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    print(f"\n✓ Selected: Device {device_index + 1} (S/N: {device_info[device_index][2]})")
    print()
    # Measurement type
    print("MEASUREMENT TYPE")
    print("-" * 70)
    print("Note: You must physically attach/remove the diffuser between modes.")
    print("Choose ONE measurement type per session:")
    print()
    print("  1. Radiance  (no diffuser)")
    print("  2. Irradiance (with diffuser)")
    print()
    
    while True:
        choice = input("Select measurement type (1 or 2): ").strip()
        if choice == "1":
            measurement_type = "Radiance"
            break
        elif choice == "2":
            measurement_type = "Irradiance"
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    print(f"\n✓ Selected: {measurement_type}")
    print()
    
    # Number of samples
    print("NUMBER OF SAMPLES")
    print("-" * 70)
    print("Recommended: 30-50 for robust statistical analysis")
    print("Minimum: 10 for basic comparison")
    print()
    
    while True:
        try:
            num_samples = int(input("Enter number of samples to collect: ").strip())
            if num_samples > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    print(f"\n✓ Will collect {num_samples} samples")
    print()
    
    # Base filename
    print("OUTPUT FILENAME")
    print("-" * 70)
    print("Enter a base name for the output file.")
    print("Full filename will be: {base_name}_{DD-MM-YYYY}_{HHMMSS}.csv")
    print()
    
    while True:
        base_filename = input("Enter base filename: ").strip()
        if base_filename:
            # Remove invalid characters
            base_filename = "".join(c for c in base_filename if c.isalnum() or c in "._- ")
            if base_filename:
                break
        print("Please enter a valid filename.")
    
    print(f"\n✓ Base filename: {base_filename}")
    print()
    
    return device_index, measurement_type, num_samples, base_filename


def collect_measurement(device: JetiRadioEx, wavelength_start: int = 380, 
                        wavelength_end: int = 780) -> np.ndarray:
    """
    Collect spectral intensity data from a single device
    
    Args:
        device: JetiRadioEx device instance
        wavelength_start: Start wavelength in nm
        wavelength_end: End wavelength in nm
        
    Returns:
        Numpy array of spectral intensity values
    """
    # Perform measurement
    device.measure(integration_time=0.0, average=1, step=1)
    device.wait_for_measurement()
    
    # Get spectral data
    spectral_data = device.get_spectral_radiance(wavelength_start, wavelength_end)
    
    return spectral_data


def save_measurements(measurements: list, filename: str, wavelength_start: int, wavelength_end: int, measurement_type: str):
    """
    Save all measurements to CSV file with each sample as a separate column
    
    Args:
        measurements: List of numpy arrays with spectral data
        filename: Output filename
        wavelength_start: Start wavelength
        wavelength_end: End wavelength
        measurement_type: Type of measurement (Radiance or Irradiance)
    """
    print(f"\nSaving data to {filename}...")
    
    wavelengths = np.arange(wavelength_start, wavelength_end + 1)
    measurements_array = np.array(measurements)
    num_samples = len(measurements)
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header with sample columns
        header = ['Serial {serial_device}'] + ['Wavelength (nm)'] + [f'Sample(s) 1 to {num_samples}'] + [measurement_type]
        writer.writerow(header)
        
        # Write data rows - one row per wavelength with all sample intensities
        for wl_idx, wl in enumerate(wavelengths):
            row = [f"{wl:.2f}"]
            # Add intensity from each sample for this wavelength
            for sample_idx in range(num_samples):
                row.append(f"{measurements_array[sample_idx, wl_idx]:.6e}")
            writer.writerow(row)
    
    print(f"✓ Data saved successfully!")


def main():
    """Main measurement collection workflow"""
    
    print("=" * 70)
    print("DEVICE INITIALIZATION")
    print("=" * 70)
    
    try:
        # Initialize device
        device = JetiRadioEx()
        
        # Get user inputs (includes device selection)
        device_index, measurement_type, num_samples, base_filename = get_user_inputs(device)
        
        # Generate filename
        now = datetime.now()
        date_str = now.strftime('%d-%m-%Y')
        time_str = now.strftime('%H%M%S')
        filename = f"{base_filename}_{date_str}_{time_str}.csv"
        output_path = Path(__file__).parent.parent / "reports" / filename
        output_path.parent.mkdir(exist_ok=True)
        
        # Open selected device
        print()
        print("=" * 70)
        print("OPENING DEVICE")
        print("=" * 70)
        print(f"\nOpening device {device_index+1}...", end="", flush=True)
        device.open_device(device_index)
        serial = device.get_serial_device(device_index)
        device_serial = serial[2]
        print(f" ✓ (S/N: {device_serial})")
        
        print()
        print("=" * 70)
        print("COLLECTING MEASUREMENTS")
        print("=" * 70)
        print(f"Collecting {num_samples} measurements...")
        print()
        
        wavelength_start = 380
        wavelength_end = 780
        measurements = []
        
        # Collect measurements
        for i in range(num_samples):
            print(f"Sample {i+1}/{num_samples}...", end="", flush=True)
            
            try:
                spectral_data = collect_measurement(device, wavelength_start, wavelength_end)
                measurements.append(spectral_data)
                print(f" ✓")
                
                # Add small delay to allow DLL processing
                time.sleep(0.05)
                
                # Force garbage collection every 5 measurements to clean up ctypes references
                if (i + 1) % 5 == 0:
                    gc.collect()
                    
            except Exception as e:
                print(f" ✗ Failed: {e}")
                # Continue with next measurement
                continue
                
        # Close device BEFORE saving to ensure DLL resources are fully released
        print("\nClosing device...", end="", flush=True)
        try:
            device.close_device()
            print(" ✓")
        except Exception as e:
            print(f" Error: {e}")
            import traceback
            traceback.print_exc()
        
        # Save data
        print()
        print("=" * 70)
        print("SAVING DATA")
        print("=" * 70)
        try:
            save_measurements(measurements, output_path, wavelength_start, wavelength_end, measurement_type)
        except Exception as e:
            print(f"Error saving: {e}")
            import traceback
            traceback.print_exc()
        
        print()
        print("=" * 70)
        print("COLLECTION COMPLETE!")
        print("=" * 70)
        print(f"Data saved to: {output_path}")
        print()
        print("Next step: Collect data from second device, then use")
        print("           analyze_comparison.py to compare both files.")
        print()
        
    except JetiException as e:
        print(f"\nJETI Error: {e}")
        return
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    main()
