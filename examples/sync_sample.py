"""
Python version of SyncSample.c
Demonstrates synchronized measurements with optical trigger and cycle mode
Requires jeti_core and jeti_radio modules
"""

import sys
import time
from pathlib import Path

# Add src directory to path for development mode
_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root / "src"))

from jeti import JetiRadio, JetiException, _get_dll_path
import numpy as np
import ctypes
from ctypes import c_float, c_uint32, c_bool, c_uint8, POINTER


class SyncMeasurementApp:
    """Application for performing synchronized radiometric measurements"""
    
    def __init__(self):
        self.device = None
        self._setup_core_functions()
        
    def _setup_core_functions(self):
        """Setup additional core functions needed for sync mode"""
        # We need to load jeti_core64.dll for sync functions
        dll_path = str(_get_dll_path("jeti_core64.dll"))
        self._core_dll = ctypes.WinDLL(dll_path)
        
        # Setup sync mode functions
        self._core_dll.JETI_GetFlickerFreq.argtypes = [ctypes.c_void_p, POINTER(c_float), POINTER(c_uint32)]
        self._core_dll.JETI_GetFlickerFreq.restype = c_uint32
        
        self._core_dll.JETI_SetSyncMode.argtypes = [ctypes.c_void_p, c_uint8]
        self._core_dll.JETI_SetSyncMode.restype = c_uint32
        
        self._core_dll.JETI_SetSyncFreq.argtypes = [ctypes.c_void_p, c_float]
        self._core_dll.JETI_SetSyncFreq.restype = c_uint32
        
        self._core_dll.JETI_GetSyncFreq.argtypes = [ctypes.c_void_p, POINTER(c_float)]
        self._core_dll.JETI_GetSyncFreq.restype = c_uint32
        
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
    
    def get_flicker_frequency(self) -> float:
        """
        Try to determine flicker frequency automatically
        
        Returns:
            Flicker frequency in Hz (0.0 if could not be determined)
        """
        flicker_freq = c_float()
        warning = c_uint32()
        
        error = self._core_dll.JETI_GetFlickerFreq(
            self.device._device_handle,
            ctypes.byref(flicker_freq),
            ctypes.byref(warning)
        )
        
        if error != 0 or flicker_freq.value == 0.0:
            return 0.0
        
        return flicker_freq.value
    
    def set_sync_mode(self, enable: bool):
        """
        Enable or disable sync mode
        
        Args:
            enable: True to enable sync mode, False to use integration time
        """
        error = self._core_dll.JETI_SetSyncMode(
            self.device._device_handle,
            1 if enable else 0
        )
        if error != 0:
            raise JetiException(error, "JETI_SetSyncMode")
    
    def set_sync_frequency(self, frequency: float):
        """
        Set synchronization frequency
        
        Args:
            frequency: Sync frequency in Hz
        """
        error = self._core_dll.JETI_SetSyncFreq(
            self.device._device_handle,
            frequency
        )
        if error != 0:
            raise JetiException(error, "JETI_SetSyncFreq")
    
    def get_sync_frequency(self) -> float:
        """Get current sync frequency in Hz"""
        sync_freq = c_float()
        error = self._core_dll.JETI_GetSyncFreq(
            self.device._device_handle,
            ctypes.byref(sync_freq)
        )
        if error != 0:
            raise JetiException(error, "JETI_GetSyncFreq")
        return sync_freq.value
    
    def perform_sync_measurement(self):
        """Perform a synchronized radiometric measurement"""
        print("\n" + "=" * 60)
        print("SYNCHRONIZED RADIOMETRIC MEASUREMENT")
        print("=" * 60)
        
        try:
            # Try to determine flicker frequency automatically
            print("\nAttempting to determine flicker frequency automatically...")
            flicker_freq = self.get_flicker_frequency()
            
            if flicker_freq == 0.0:
                print("Could not determine flicker frequency automatically.")
                sync_freq = float(input("Please enter sync frequency in Hz: "))
            else:
                print(f"Detected flicker frequency: {flicker_freq:.2f} Hz")
                use_detected = input("Use detected frequency? (y/n): ").strip().lower()
                if use_detected == 'y':
                    sync_freq = flicker_freq
                else:
                    sync_freq = float(input("Enter sync frequency in Hz: "))
            
            print(f"\nUsing sync frequency: {sync_freq:.2f} Hz")
            
            # Enable sync mode
            print("Enabling sync mode...")
            self.set_sync_mode(True)
            
            # Set sync frequency
            print(f"Setting sync frequency to {sync_freq:.2f} Hz...")
            self.set_sync_frequency(sync_freq)
            
            # Verify sync frequency
            actual_freq = self.get_sync_frequency()
            print(f"Actual sync frequency: {actual_freq:.2f} Hz")
            
            # Start measurement
            print("\nStarting synchronized measurement...")
            self.device.measure()
            
            # Wait for measurement to complete
            print("Measuring", end="", flush=True)
            while self.device.get_measure_status():
                print(".", end="", flush=True)
                time.sleep(0.1)
            print(" Done!\n")
            
            # Get radiometric value
            radio = self.device.get_radiometric_value()
            
            # Display results
            print("\n" + "-" * 60)
            print("MEASUREMENT RESULTS")
            print("-" * 60)
            print(f"Radiometric value:    {radio:.3E} W/m²")
            print(f"Sync frequency:       {sync_freq:.2f} Hz")
            print("-" * 60 + "\n")
            
            # Disable sync mode
            print("Disabling sync mode...")
            self.set_sync_mode(False)
            
            print("Synchronized measurement completed successfully!")
            
            return {
                'radiometric': radio,
                'sync_frequency': sync_freq
            }
            
        except ValueError as e:
            print(f"Invalid input: {e}")
            return None
        except JetiException as e:
            print(f"Error during measurement: {e}")
            # Try to disable sync mode in case of error
            try:
                self.set_sync_mode(False)
            except:
                pass
            return None
    
    def display_sync_info(self):
        """Display current sync mode information"""
        try:
            sync_freq = self.get_sync_frequency()
            print("\n" + "=" * 60)
            print("SYNC MODE INFORMATION")
            print("=" * 60)
            print(f"Current sync frequency: {sync_freq:.2f} Hz")
            print("=" * 60 + "\n")
        except JetiException as e:
            print(f"Error getting sync info: {e}")
    
    def run_menu(self):
        """Run the interactive menu"""
        while True:
            print("\n" + "=" * 60)
            print("JETI SYNCHRONIZED MEASUREMENT - MAIN MENU")
            print("=" * 60)
            print("m) Perform synchronized radiometric measurement")
            print("i) Display sync mode information")
            print("\n0) Exit")
            print("=" * 60)
            
            choice = input("\nYour choice: ").strip().lower()
            
            if choice == 'm':
                self.perform_sync_measurement()
                input("\nPress Enter to continue...")
                
            elif choice == 'i':
                self.display_sync_info()
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
                # Make sure sync mode is disabled
                try:
                    self.set_sync_mode(False)
                except:
                    pass
                
                self.device.close_device()
                print("Device closed successfully!")
            except JetiException as e:
                print(f"Error closing device: {e}")


def main():
    """Main application entry point"""
    print("=" * 60)
    print("JETI SDK - Synchronized Measurement Sample")
    print("=" * 60)
    print("\nThis sample demonstrates synchronized measurements using")
    print("optical trigger and cycle mode.")
    print("\nNote: Requires a light source with periodic flicker")
    print("      (e.g., AC-powered LED or fluorescent lamp)")
    
    app = SyncMeasurementApp()
    
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
