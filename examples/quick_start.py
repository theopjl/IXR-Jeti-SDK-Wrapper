"""
Quick start example for JETI SDK Python wrapper
Demonstrates the simplest way to perform a measurement
"""

import sys
from pathlib import Path

# Add src directory to path for development mode
_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root / "src"))

from jeti import JetiRadioEx, JetiException


def quick_measurement():
    """Perform a quick radiometric measurement"""
    
    print("JETI Quick Start Example")
    print("=" * 60)
    
    try:
        # Create device instance
        device = JetiRadioEx()
        
        # Find devices
        num_devices = device.get_num_devices()
        print(f"\nFound {num_devices} device(s)")
        
        if num_devices == 0:
            print("No devices found. Please check connection.")
            return
        
        # Open first device
        print("Opening device...")
        device.open_device(0)
        print("Device opened successfully!")
        
        # Perform measurement with automatic settings
        print("\nPerforming measurement...")
        device.measure(integration_time=0.0, average=1, step=1)
        
        # Wait for completion
        device.wait_for_measurement()
        print("Measurement complete!")
        
        # Get results
        print("\n" + "=" * 60)
        print("RESULTS")
        print("=" * 60)
        
        radiometric = device.get_radiometric_value(380, 780)
        print(f"Radiometric value: {radiometric:.3E} W/m²")
        
        photometric = device.get_photometric_value()
        print(f"Photometric value: {photometric:.3E} lx")
        
        x, y = device.get_chromaticity_xy()
        print(f"Chromaticity x,y:  {x:.4f}, {y:.4f}")
        
        cct = device.get_cct()
        print(f"CCT:               {cct:.1f} K")
        
        cri = device.get_cri()
        print(f"CRI (Ra):          {cri[0]:.2f}")
        
        print("=" * 60)
        
        # Close device
        device.close_device()
        print("\nDevice closed.")
        
    except JetiException as e:
        print(f"\nError: {e}")
        return


if __name__ == "__main__":
    quick_measurement()
