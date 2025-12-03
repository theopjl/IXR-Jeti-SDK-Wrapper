"""
Python wrapper for JETI SDK
Compatible with Python >= 3.11
Uses numpy for data structures

Author: Generated for JETI SDK v4.8.10
Date: 2025
"""

import ctypes
from ctypes import (
    c_uint32, c_int32, c_float, c_double, c_char_p, c_void_p, c_bool,
    c_uint16, c_uint8, POINTER, c_ulonglong, c_wchar_p
)
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Dict
from enum import IntEnum


def _get_dll_path(dll_name: str) -> Path:
    """
    Get the path to a DLL file relative to the package location.
    
    Args:
        dll_name: Name of the DLL file (e.g., 'jeti_core64.dll')
        
    Returns:
        Path to the DLL file
    """
    # DLLs are in the 'dlls' folder adjacent to the package root
    package_dir = Path(__file__).resolve().parent
    # Go up from src/jeti to project root, then into dlls/
    dll_path = package_dir.parent.parent / "dlls" / dll_name
    
    if not dll_path.exists():
        # Fallback: check if DLLs are in same directory as wrapper (for development)
        dll_path = package_dir / dll_name
        
    if not dll_path.exists():
        # Last fallback: check package root
        dll_path = package_dir.parent.parent / dll_name
        
    return dll_path


# Error codes
class JetiError(IntEnum):
    SUCCESS = 0x00000000
    ERROR_OPEN = 0x00000001
    ERROR_OPEN_PORT = 0x00000002
    ERROR_PORT_SETTING = 0x00000003
    ERROR_BUFFER_SIZE = 0x00000004
    ERROR_PURGE = 0x00000005
    ERROR_TIMEOUT_SETTING = 0x00000006
    ERROR_SEND = 0x00000007
    TIMEOUT = 0x00000008
    BREAK = 0x00000009
    ERROR_RECEIVE = 0x0000000A
    ERROR_NAK = 0x0000000B
    ERROR_CONVERT = 0x0000000C
    ERROR_PARAMETER = 0x0000000D
    BUSY = 0x0000000E
    CHECKSUM_ERROR = 0x00000011
    INVALID_STEPWIDTH = 0x00000012
    INVALID_NUMBER = 0x00000013
    NOT_CONNECTED = 0x00000014
    INVALID_HANDLE = 0x00000015
    INVALID_CALIB = 0x00000016
    CALIB_NOT_READ = 0x00000017
    OVEREXPOSURE = 0x00000020
    MEASURE_FAIL = 0x00000022
    ADAPTION_FAIL = 0x00000023
    FILE_NOT_FOUND = 0x00000050
    NO_SLM_DIR = 0x00000051
    NO_STRAYLIGHT = 0x00000052
    NO_MEM = 0x00000053
    NO_SN = 0x00000054
    DLL_ERROR = 0x00000080
    CALC_ERROR = 0x00000081
    ERROR_READ = 0x00000100
    FATAL_ERROR = 0x000000FF


class JetiException(Exception):
    """Exception raised for JETI SDK errors"""
    def __init__(self, error_code: int, message: str = ""):
        self.error_code = error_code
        error_name = JetiError(error_code).name if error_code in JetiError._value2member_map_ else "UNKNOWN"
        self.message = f"JETI Error 0x{error_code:08X} ({error_name}): {message}"
        super().__init__(self.message)


def _check_error(error_code: int, function_name: str = ""):
    """Check error code and raise exception if not successful"""
    if error_code != JetiError.SUCCESS:
        raise JetiException(error_code, f"in {function_name}" if function_name else "")


class JetiCore:
    """
    Core functionality for JETI devices
    Provides low-level device communication and control
    """
    
    def __init__(self, dll_path: Optional[str] = None):
        """
        Initialize JETI Core wrapper
        
        Args:
            dll_path: Path to jeti_core64.dll. If None, looks in package dlls/ folder
        """
        if dll_path is None:
            dll_path = str(_get_dll_path("jeti_core64.dll"))
        
        self._dll = ctypes.WinDLL(dll_path)
        self._device_handle = None
        self._setup_functions()
    
    def _setup_functions(self):
        """Setup function signatures for the DLL"""
        # Device handling
        self._dll.JETI_GetNumDevices.argtypes = [POINTER(c_uint32)]
        self._dll.JETI_GetNumDevices.restype = c_uint32
        
        self._dll.JETI_GetSerialDevice.argtypes = [c_uint32, c_char_p, c_char_p, c_char_p]
        self._dll.JETI_GetSerialDevice.restype = c_uint32
        
        self._dll.JETI_OpenDevice.argtypes = [c_uint32, POINTER(c_void_p)]
        self._dll.JETI_OpenDevice.restype = c_uint32
        
        self._dll.JETI_OpenCOMDevice.argtypes = [c_uint32, c_uint32, POINTER(c_void_p)]
        self._dll.JETI_OpenCOMDevice.restype = c_uint32
        
        self._dll.JETI_CloseDevice.argtypes = [c_void_p]
        self._dll.JETI_CloseDevice.restype = c_uint32
        
        self._dll.JETI_GetIdentifier.argtypes = [c_void_p, c_char_p]
        self._dll.JETI_GetIdentifier.restype = c_uint32
        
        self._dll.JETI_Reset.argtypes = [c_void_p]
        self._dll.JETI_Reset.restype = c_uint32
        
        self._dll.JETI_GetPixel.argtypes = [c_void_p, POINTER(c_uint32)]
        self._dll.JETI_GetPixel.restype = c_uint32
        
        self._dll.JETI_GetTint.argtypes = [c_void_p, POINTER(c_float)]
        self._dll.JETI_GetTint.restype = c_uint32
        
        self._dll.JETI_GetCoreDLLVersion.argtypes = [POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16)]
        self._dll.JETI_GetCoreDLLVersion.restype = c_uint32
        
        self._dll.JETI_GetFirmwareVersion.argtypes = [c_void_p, c_char_p]
        self._dll.JETI_GetFirmwareVersion.restype = c_uint32
    
    def get_num_devices(self) -> int:
        """Get number of connected JETI devices"""
        num_devices = c_uint32()
        error = self._dll.JETI_GetNumDevices(ctypes.byref(num_devices))
        _check_error(error, "JETI_GetNumDevices")
        return num_devices.value
    
    def get_serial_device(self, device_num: int) -> Tuple[str, str, str]:
        """
        Get serial numbers for a device
        
        Args:
            device_num: Device number (0-based)
            
        Returns:
            Tuple of (board_serial, spec_serial, device_serial)
        """
        board_serial = ctypes.create_string_buffer(16)
        spec_serial = ctypes.create_string_buffer(16)
        device_serial = ctypes.create_string_buffer(16)
        
        error = self._dll.JETI_GetSerialDevice(
            device_num, board_serial, spec_serial, device_serial
        )
        _check_error(error, "JETI_GetSerialDevice")
        
        return (
            board_serial.value.decode('ascii'),
            spec_serial.value.decode('ascii'),
            device_serial.value.decode('ascii')
        )
    
    def open_device(self, device_num: int = 0):
        """
        Open a JETI device
        
        Args:
            device_num: Device number (0-based)
        """
        device_handle = c_void_p()
        error = self._dll.JETI_OpenDevice(device_num, ctypes.byref(device_handle))
        _check_error(error, "JETI_OpenDevice")
        self._device_handle = device_handle
    
    def open_com_device(self, com_port: int, baudrate: int = 115200):
        """
        Open a JETI device on specific COM port
        
        Args:
            com_port: COM port number (1-255)
            baudrate: Baudrate (e.g., 115200, 921600)
        """
        device_handle = c_void_p()
        error = self._dll.JETI_OpenCOMDevice(com_port, baudrate, ctypes.byref(device_handle))
        _check_error(error, "JETI_OpenCOMDevice")
        self._device_handle = device_handle
    
    def close_device(self):
        """Close the device connection"""
        if self._device_handle is not None:
            error = self._dll.JETI_CloseDevice(self._device_handle)
            _check_error(error, "JETI_CloseDevice")
            self._device_handle = None
    
    def get_identifier(self) -> str:
        """Get device identifier string"""
        identifier = ctypes.create_string_buffer(256)
        error = self._dll.JETI_GetIdentifier(self._device_handle, identifier)
        _check_error(error, "JETI_GetIdentifier")
        return identifier.value.decode('ascii')
    
    def reset(self):
        """Reset the device"""
        error = self._dll.JETI_Reset(self._device_handle)
        _check_error(error, "JETI_Reset")
    
    def get_pixel_count(self) -> int:
        """Get number of pixels in the sensor"""
        pixel_count = c_uint32()
        error = self._dll.JETI_GetPixel(self._device_handle, ctypes.byref(pixel_count))
        _check_error(error, "JETI_GetPixel")
        return pixel_count.value
    
    def get_integration_time(self) -> float:
        """Get current integration time in ms"""
        tint = c_float()
        error = self._dll.JETI_GetTint(self._device_handle, ctypes.byref(tint))
        _check_error(error, "JETI_GetTint")
        return tint.value
    
    def get_dll_version(self) -> Tuple[int, int, int]:
        """Get DLL version (major, minor, build)"""
        major = c_uint16()
        minor = c_uint16()
        build = c_uint16()
        error = self._dll.JETI_GetCoreDLLVersion(
            ctypes.byref(major), ctypes.byref(minor), ctypes.byref(build)
        )
        _check_error(error, "JETI_GetCoreDLLVersion")
        return (major.value, minor.value, build.value)
    
    def get_firmware_version(self) -> str:
        """Get device firmware version"""
        version = ctypes.create_string_buffer(256)
        error = self._dll.JETI_GetFirmwareVersion(self._device_handle, version)
        _check_error(error, "JETI_GetFirmwareVersion")
        return version.value.decode('ascii')
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_device()
        return False


class JetiRadio(JetiCore):
    """
    Radiometric measurement functionality for JETI devices
    Extends JetiCore with radiometric measurement capabilities
    """
    
    def __init__(self, dll_path: Optional[str] = None):
        """
        Initialize JETI Radio wrapper
        
        Args:
            dll_path: Path to jeti_radio64.dll. If None, looks in package dlls/ folder
        """
        if dll_path is None:
            dll_path = str(_get_dll_path("jeti_radio64.dll"))
        
        self._dll = ctypes.WinDLL(dll_path)
        self._device_handle = None
        self._setup_radio_functions()
    
    def _setup_radio_functions(self):
        """Setup function signatures for radio DLL"""
        # Device management
        self._dll.JETI_GetNumRadio.argtypes = [POINTER(c_uint32)]
        self._dll.JETI_GetNumRadio.restype = c_uint32
        
        self._dll.JETI_GetSerialRadio.argtypes = [c_uint32, c_char_p, c_char_p, c_char_p]
        self._dll.JETI_GetSerialRadio.restype = c_uint32
        
        self._dll.JETI_OpenRadio.argtypes = [c_uint32, POINTER(c_void_p)]
        self._dll.JETI_OpenRadio.restype = c_uint32
        
        self._dll.JETI_CloseRadio.argtypes = [c_void_p]
        self._dll.JETI_CloseRadio.restype = c_uint32
        
        # Measurement functions
        self._dll.JETI_Measure.argtypes = [c_void_p]
        self._dll.JETI_Measure.restype = c_uint32
        
        self._dll.JETI_MeasureStatus.argtypes = [c_void_p, POINTER(c_bool)]
        self._dll.JETI_MeasureStatus.restype = c_uint32
        
        self._dll.JETI_MeasureBreak.argtypes = [c_void_p]
        self._dll.JETI_MeasureBreak.restype = c_uint32
        
        # Results
        self._dll.JETI_Radio.argtypes = [c_void_p, POINTER(c_float)]
        self._dll.JETI_Radio.restype = c_uint32
        
        self._dll.JETI_Photo.argtypes = [c_void_p, POINTER(c_float)]
        self._dll.JETI_Photo.restype = c_uint32
        
        self._dll.JETI_Chromxy.argtypes = [c_void_p, POINTER(c_float), POINTER(c_float)]
        self._dll.JETI_Chromxy.restype = c_uint32
        
        self._dll.JETI_CCT.argtypes = [c_void_p, POINTER(c_float)]
        self._dll.JETI_CCT.restype = c_uint32
        
        self._dll.JETI_CRI.argtypes = [c_void_p, POINTER(c_float)]
        self._dll.JETI_CRI.restype = c_uint32
        
        self._dll.JETI_GetRadioDLLVersion.argtypes = [POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16)]
        self._dll.JETI_GetRadioDLLVersion.restype = c_uint32
    
    def get_num_devices(self) -> int:
        """Get number of connected radio measurement devices"""
        num_devices = c_uint32()
        error = self._dll.JETI_GetNumRadio(ctypes.byref(num_devices))
        _check_error(error, "JETI_GetNumRadio")
        return num_devices.value
    
    def get_serial_device(self, device_num: int) -> Tuple[str, str, str]:
        """Get serial numbers for a device"""
        board_serial = ctypes.create_string_buffer(16)
        spec_serial = ctypes.create_string_buffer(16)
        device_serial = ctypes.create_string_buffer(16)
        
        error = self._dll.JETI_GetSerialRadio(
            device_num, board_serial, spec_serial, device_serial
        )
        _check_error(error, "JETI_GetSerialRadio")
        
        return (
            board_serial.value.decode('ascii'),
            spec_serial.value.decode('ascii'),
            device_serial.value.decode('ascii')
        )
    
    def open_device(self, device_num: int = 0):
        """Open a radio measurement device"""
        device_handle = c_void_p()
        error = self._dll.JETI_OpenRadio(device_num, ctypes.byref(device_handle))
        _check_error(error, "JETI_OpenRadio")
        self._device_handle = device_handle
    
    def close_device(self):
        """Close the device connection"""
        if self._device_handle is not None:
            error = self._dll.JETI_CloseRadio(self._device_handle)
            _check_error(error, "JETI_CloseRadio")
            self._device_handle = None
    
    def measure(self):
        """Start a radiometric measurement with automatic integration time"""
        error = self._dll.JETI_Measure(self._device_handle)
        _check_error(error, "JETI_Measure")
    
    def get_measure_status(self) -> bool:
        """
        Get measurement status
        
        Returns:
            True if measurement is still running, False if finished
        """
        status = c_bool()
        error = self._dll.JETI_MeasureStatus(self._device_handle, ctypes.byref(status))
        _check_error(error, "JETI_MeasureStatus")
        return status.value
    
    def break_measurement(self):
        """Cancel an ongoing measurement"""
        error = self._dll.JETI_MeasureBreak(self._device_handle)
        _check_error(error, "JETI_MeasureBreak")
    
    def wait_for_measurement(self, poll_interval: float = 0.1):
        """
        Wait for measurement to complete
        
        Args:
            poll_interval: Time between status checks in seconds
        """
        import time
        while self.get_measure_status():
            time.sleep(poll_interval)
    
    def get_radiometric_value(self) -> float:
        """Get radiometric value from last measurement in W/m²"""
        radio = c_float()
        error = self._dll.JETI_Radio(self._device_handle, ctypes.byref(radio))
        _check_error(error, "JETI_Radio")
        return radio.value
    
    def get_photometric_value(self) -> float:
        """Get photometric value from last measurement in lx"""
        photo = c_float()
        error = self._dll.JETI_Photo(self._device_handle, ctypes.byref(photo))
        _check_error(error, "JETI_Photo")
        return photo.value
    
    def get_chromaticity_xy(self) -> Tuple[float, float]:
        """Get CIE 1931 chromaticity coordinates x, y"""
        x = c_float()
        y = c_float()
        error = self._dll.JETI_Chromxy(self._device_handle, ctypes.byref(x), ctypes.byref(y))
        _check_error(error, "JETI_Chromxy")
        return (x.value, y.value)
    
    def get_cct(self) -> float:
        """Get correlated color temperature in Kelvin"""
        cct = c_float()
        error = self._dll.JETI_CCT(self._device_handle, ctypes.byref(cct))
        _check_error(error, "JETI_CCT")
        return cct.value
    
    def get_cri(self) -> np.ndarray:
        """
        Get color rendering indices (CRI)
        
        Returns:
            numpy array with 15 CRI values (Ra, R1-R14)
        """
        cri_array = (c_float * 15)()
        error = self._dll.JETI_CRI(self._device_handle, cri_array)
        _check_error(error, "JETI_CRI")
        return np.array([cri_array[i] for i in range(15)])
    
    def get_all_values(self) -> Dict[str, any]:
        """
        Get all measurement results
        
        Returns:
            Dictionary with all measurement values
        """
        return {
            'radiometric': self.get_radiometric_value(),
            'photometric': self.get_photometric_value(),
            'chromaticity_xy': self.get_chromaticity_xy(),
            'cct': self.get_cct(),
            'cri': self.get_cri()
        }
    
    def get_dll_version(self) -> Tuple[int, int, int]:
        """Get DLL version (major, minor, build)"""
        major = c_uint16()
        minor = c_uint16()
        build = c_uint16()
        error = self._dll.JETI_GetRadioDLLVersion(
            ctypes.byref(major), ctypes.byref(minor), ctypes.byref(build)
        )
        _check_error(error, "JETI_GetRadioDLLVersion")
        return (major.value, minor.value, build.value)


class JetiRadioEx(JetiRadio):
    """
    Extended radiometric measurement functionality
    Provides more control over measurement parameters
    """
    
    def __init__(self, dll_path: Optional[str] = None):
        """
        Initialize JETI Radio Ex wrapper
        
        Args:
            dll_path: Path to jeti_radio_ex64.dll. If None, looks in package dlls/ folder
        """
        if dll_path is None:
            dll_path = str(_get_dll_path("jeti_radio_ex64.dll"))
        
        self._dll = ctypes.WinDLL(dll_path)
        self._device_handle = None
        self._setup_radio_ex_functions()
    
    def _setup_radio_ex_functions(self):
        """Setup function signatures for radio ex DLL"""
        # Device management
        self._dll.JETI_GetNumRadioEx.argtypes = [POINTER(c_uint32)]
        self._dll.JETI_GetNumRadioEx.restype = c_uint32
        
        self._dll.JETI_GetSerialRadioEx.argtypes = [c_uint32, c_char_p, c_char_p, c_char_p]
        self._dll.JETI_GetSerialRadioEx.restype = c_uint32
        
        self._dll.JETI_OpenRadioEx.argtypes = [c_uint32, POINTER(c_void_p)]
        self._dll.JETI_OpenRadioEx.restype = c_uint32
        
        self._dll.JETI_CloseRadioEx.argtypes = [c_void_p]
        self._dll.JETI_CloseRadioEx.restype = c_uint32
        
        # Measurement functions
        self._dll.JETI_MeasureEx.argtypes = [c_void_p, c_float, c_uint16, c_uint32]
        self._dll.JETI_MeasureEx.restype = c_uint32
        
        self._dll.JETI_MeasureStatusEx.argtypes = [c_void_p, POINTER(c_bool)]
        self._dll.JETI_MeasureStatusEx.restype = c_uint32
        
        self._dll.JETI_MeasureBreakEx.argtypes = [c_void_p]
        self._dll.JETI_MeasureBreakEx.restype = c_uint32
        
        # Results with wavelength range
        self._dll.JETI_SpecRadEx.argtypes = [c_void_p, c_uint32, c_uint32, POINTER(c_float)]
        self._dll.JETI_SpecRadEx.restype = c_uint32
        
        self._dll.JETI_RadioEx.argtypes = [c_void_p, c_uint32, c_uint32, POINTER(c_float)]
        self._dll.JETI_RadioEx.restype = c_uint32
        
        self._dll.JETI_PhotoEx.argtypes = [c_void_p, POINTER(c_float)]
        self._dll.JETI_PhotoEx.restype = c_uint32
        
        self._dll.JETI_ChromxyEx.argtypes = [c_void_p, POINTER(c_float), POINTER(c_float)]
        self._dll.JETI_ChromxyEx.restype = c_uint32
        
        self._dll.JETI_CCTEx.argtypes = [c_void_p, POINTER(c_float)]
        self._dll.JETI_CCTEx.restype = c_uint32
        
        self._dll.JETI_CRIEx.argtypes = [c_void_p, c_float, POINTER(c_float)]
        self._dll.JETI_CRIEx.restype = c_uint32
        
        self._dll.JETI_GetRadioExDLLVersion.argtypes = [POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16)]
        self._dll.JETI_GetRadioExDLLVersion.restype = c_uint32
    
    def get_num_devices(self) -> int:
        """Get number of connected radio measurement devices"""
        num_devices = c_uint32()
        error = self._dll.JETI_GetNumRadioEx(ctypes.byref(num_devices))
        _check_error(error, "JETI_GetNumRadioEx")
        return num_devices.value
    
    def get_serial_device(self, device_num: int) -> Tuple[str, str, str]:
        """Get serial numbers for a device"""
        board_serial = ctypes.create_string_buffer(16)
        spec_serial = ctypes.create_string_buffer(16)
        device_serial = ctypes.create_string_buffer(16)
        
        error = self._dll.JETI_GetSerialRadioEx(
            device_num, board_serial, spec_serial, device_serial
        )
        _check_error(error, "JETI_GetSerialRadioEx")
        
        return (
            board_serial.value.decode('ascii'),
            spec_serial.value.decode('ascii'),
            device_serial.value.decode('ascii')
        )
    
    def open_device(self, device_num: int = 0):
        """Open a radio measurement device"""
        device_handle = c_void_p()
        error = self._dll.JETI_OpenRadioEx(device_num, ctypes.byref(device_handle))
        _check_error(error, "JETI_OpenRadioEx")
        self._device_handle = device_handle
    
    def close_device(self):
        """Close the device connection"""
        if self._device_handle is not None:
            error = self._dll.JETI_CloseRadioEx(self._device_handle)
            _check_error(error, "JETI_CloseRadioEx")
            self._device_handle = None
    
    def measure(self, integration_time: float = 0.0, average: int = 1, step: int = 1):
        """
        Start a radiometric measurement with specified parameters
        
        Args:
            integration_time: Integration time in ms (0 for automatic)
            average: Number of averages
            step: Step width in nm (1, 5, or 10)
        """
        error = self._dll.JETI_MeasureEx(self._device_handle, integration_time, average, step)
        _check_error(error, "JETI_MeasureEx")
    
    def get_measure_status(self) -> bool:
        """
        Get measurement status
        
        Returns:
            True if measurement is still running, False if finished
        """
        status = c_bool()
        error = self._dll.JETI_MeasureStatusEx(self._device_handle, ctypes.byref(status))
        _check_error(error, "JETI_MeasureStatusEx")
        return status.value
    
    def break_measurement(self):
        """Cancel an ongoing measurement"""
        error = self._dll.JETI_MeasureBreakEx(self._device_handle)
        _check_error(error, "JETI_MeasureBreakEx")
    
    def get_spectral_radiance(self, wavelength_start: int = 380, 
                              wavelength_end: int = 780) -> np.ndarray:
        """
        Get spectral radiance data
        
        Args:
            wavelength_start: Start wavelength in nm
            wavelength_end: End wavelength in nm
            
        Returns:
            numpy array with spectral radiance values
        """
        num_values = wavelength_end - wavelength_start + 1
        sprad_array = (c_float * num_values)()
        error = self._dll.JETI_SpecRadEx(
            self._device_handle, wavelength_start, wavelength_end, sprad_array
        )
        _check_error(error, "JETI_SpecRadEx")
        return np.array([sprad_array[i] for i in range(num_values)])
    
    def get_radiometric_value(self, wavelength_start: int = 380, 
                             wavelength_end: int = 780) -> float:
        """
        Get radiometric value in specified wavelength range
        
        Args:
            wavelength_start: Start wavelength in nm
            wavelength_end: End wavelength in nm
            
        Returns:
            Radiometric value in W/m²
        """
        radio = c_float()
        error = self._dll.JETI_RadioEx(
            self._device_handle, wavelength_start, wavelength_end, ctypes.byref(radio)
        )
        _check_error(error, "JETI_RadioEx")
        return radio.value
    
    def get_photometric_value(self) -> float:
        """Get photometric value in lx"""
        photo = c_float()
        error = self._dll.JETI_PhotoEx(self._device_handle, ctypes.byref(photo))
        _check_error(error, "JETI_PhotoEx")
        return photo.value
    
    def get_chromaticity_xy(self) -> Tuple[float, float]:
        """Get CIE 1931 chromaticity coordinates x, y"""
        x = c_float()
        y = c_float()
        error = self._dll.JETI_ChromxyEx(self._device_handle, ctypes.byref(x), ctypes.byref(y))
        _check_error(error, "JETI_ChromxyEx")
        return (x.value, y.value)
    
    def get_cct(self) -> float:
        """Get correlated color temperature in Kelvin"""
        cct = c_float()
        error = self._dll.JETI_CCTEx(self._device_handle, ctypes.byref(cct))
        _check_error(error, "JETI_CCTEx")
        return cct.value
    
    def get_cri(self, cct: Optional[float] = None) -> np.ndarray:
        """
        Get color rendering indices
        
        Args:
            cct: CCT value (if None, will be calculated)
            
        Returns:
            numpy array with 15 CRI values
        """
        if cct is None:
            cct = self.get_cct()
        
        cri_array = (c_float * 15)()
        error = self._dll.JETI_CRIEx(self._device_handle, cct, cri_array)
        _check_error(error, "JETI_CRIEx")
        return np.array([cri_array[i] for i in range(15)])
    
    def get_dll_version(self) -> Tuple[int, int, int]:
        """Get DLL version (major, minor, build)"""
        major = c_uint16()
        minor = c_uint16()
        build = c_uint16()
        error = self._dll.JETI_GetRadioExDLLVersion(
            ctypes.byref(major), ctypes.byref(minor), ctypes.byref(build)
        )
        _check_error(error, "JETI_GetRadioExDLLVersion")
        return (major.value, minor.value, build.value)


class JetiSpectro:
    """
    Spectrometer functionality for JETI devices
    Provides spectral measurement capabilities
    """
    
    def __init__(self, dll_path: Optional[str] = None):
        """
        Initialize JETI Spectro wrapper
        
        Args:
            dll_path: Path to jeti_spectro64.dll. If None, looks in package dlls/ folder
        """
        if dll_path is None:
            dll_path = str(_get_dll_path("jeti_spectro64.dll"))
        
        self._dll = ctypes.WinDLL(dll_path)
        self._device_handle = None
        self._setup_spectro_functions()
    
    def _setup_spectro_functions(self):
        """Setup function signatures for spectro DLL"""
        # Device management
        self._dll.JETI_GetNumSpectro.argtypes = [POINTER(c_uint32)]
        self._dll.JETI_GetNumSpectro.restype = c_uint32
        
        self._dll.JETI_GetSerialSpectro.argtypes = [c_uint32, c_char_p, c_char_p, c_char_p]
        self._dll.JETI_GetSerialSpectro.restype = c_uint32
        
        self._dll.JETI_OpenSpectro.argtypes = [c_uint32, POINTER(c_void_p)]
        self._dll.JETI_OpenSpectro.restype = c_uint32
        
        self._dll.JETI_CloseSpectro.argtypes = [c_void_p]
        self._dll.JETI_CloseSpectro.restype = c_uint32
        
        # Measurement functions - note: these need pixel count
        self._dll.JETI_GetSpectroDLLVersion.argtypes = [POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16)]
        self._dll.JETI_GetSpectroDLLVersion.restype = c_uint32
    
    def get_num_devices(self) -> int:
        """Get number of connected spectro devices"""
        num_devices = c_uint32()
        error = self._dll.JETI_GetNumSpectro(ctypes.byref(num_devices))
        _check_error(error, "JETI_GetNumSpectro")
        return num_devices.value
    
    def get_serial_device(self, device_num: int) -> Tuple[str, str, str]:
        """Get serial numbers for a device"""
        board_serial = ctypes.create_string_buffer(16)
        spec_serial = ctypes.create_string_buffer(16)
        device_serial = ctypes.create_string_buffer(16)
        
        error = self._dll.JETI_GetSerialSpectro(
            device_num, board_serial, spec_serial, device_serial
        )
        _check_error(error, "JETI_GetSerialSpectro")
        
        return (
            board_serial.value.decode('ascii'),
            spec_serial.value.decode('ascii'),
            device_serial.value.decode('ascii')
        )
    
    def open_device(self, device_num: int = 0):
        """Open a spectro device"""
        device_handle = c_void_p()
        error = self._dll.JETI_OpenSpectro(device_num, ctypes.byref(device_handle))
        _check_error(error, "JETI_OpenSpectro")
        self._device_handle = device_handle
    
    def close_device(self):
        """Close the device connection"""
        if self._device_handle is not None:
            error = self._dll.JETI_CloseSpectro(self._device_handle)
            _check_error(error, "JETI_CloseSpectro")
            self._device_handle = None
    
    def get_dll_version(self) -> Tuple[int, int, int]:
        """Get DLL version (major, minor, build)"""
        major = c_uint16()
        minor = c_uint16()
        build = c_uint16()
        error = self._dll.JETI_GetSpectroDLLVersion(
            ctypes.byref(major), ctypes.byref(minor), ctypes.byref(build)
        )
        _check_error(error, "JETI_GetSpectroDLLVersion")
        return (major.value, minor.value, build.value)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_device()
        return False


class JetiSpectroEx:
    """
    Extended spectrometer functionality for JETI devices
    Provides advanced spectral measurement capabilities
    """
    
    def __init__(self, dll_path: Optional[str] = None):
        """
        Initialize JETI Spectro Ex wrapper
        
        Args:
            dll_path: Path to jeti_spectro_ex64.dll. If None, looks in package dlls/ folder
        """
        if dll_path is None:
            dll_path = str(_get_dll_path("jeti_spectro_ex64.dll"))
        
        self._dll = ctypes.WinDLL(dll_path)
        self._device_handle = None
        self._setup_spectro_ex_functions()
    
    def _setup_spectro_ex_functions(self):
        """Setup function signatures for spectro ex DLL"""
        # Device management
        self._dll.JETI_GetNumSpectroEx.argtypes = [POINTER(c_uint32)]
        self._dll.JETI_GetNumSpectroEx.restype = c_uint32
        
        self._dll.JETI_GetSerialSpectroEx.argtypes = [c_uint32, c_char_p, c_char_p, c_char_p]
        self._dll.JETI_GetSerialSpectroEx.restype = c_uint32
        
        self._dll.JETI_OpenSpectroEx.argtypes = [c_uint32, POINTER(c_void_p)]
        self._dll.JETI_OpenSpectroEx.restype = c_uint32
        
        self._dll.JETI_CloseSpectroEx.argtypes = [c_void_p]
        self._dll.JETI_CloseSpectroEx.restype = c_uint32
        
        # Measurement functions
        self._dll.JETI_StartLightEx.argtypes = [c_void_p, c_float, c_uint16]
        self._dll.JETI_StartLightEx.restype = c_uint32
        
        self._dll.JETI_SpectroStatusEx.argtypes = [c_void_p, POINTER(c_bool)]
        self._dll.JETI_SpectroStatusEx.restype = c_uint32
        
        self._dll.JETI_SpectroBreakEx.argtypes = [c_void_p]
        self._dll.JETI_SpectroBreakEx.restype = c_uint32
        
        self._dll.JETI_LightWaveEx.argtypes = [c_void_p, c_uint32, c_uint32, c_float, POINTER(c_float)]
        self._dll.JETI_LightWaveEx.restype = c_uint32
        
        self._dll.JETI_PixelCountEx.argtypes = [c_void_p, POINTER(c_uint32)]
        self._dll.JETI_PixelCountEx.restype = c_uint32
        
        self._dll.JETI_LightPixEx.argtypes = [c_void_p, POINTER(c_int32)]
        self._dll.JETI_LightPixEx.restype = c_uint32
        
        self._dll.JETI_GetSpectroExDLLVersion.argtypes = [POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16)]
        self._dll.JETI_GetSpectroExDLLVersion.restype = c_uint32
    
    def get_num_devices(self) -> int:
        """Get number of connected spectro devices"""
        num_devices = c_uint32()
        error = self._dll.JETI_GetNumSpectroEx(ctypes.byref(num_devices))
        _check_error(error, "JETI_GetNumSpectroEx")
        return num_devices.value
    
    def get_serial_device(self, device_num: int) -> Tuple[str, str, str]:
        """Get serial numbers for a device"""
        board_serial = ctypes.create_string_buffer(16)
        spec_serial = ctypes.create_string_buffer(16)
        device_serial = ctypes.create_string_buffer(16)
        
        error = self._dll.JETI_GetSerialSpectroEx(
            device_num, board_serial, spec_serial, device_serial
        )
        _check_error(error, "JETI_GetSerialSpectroEx")
        
        return (
            board_serial.value.decode('ascii'),
            spec_serial.value.decode('ascii'),
            device_serial.value.decode('ascii')
        )
    
    def open_device(self, device_num: int = 0):
        """Open a spectro device"""
        device_handle = c_void_p()
        error = self._dll.JETI_OpenSpectroEx(device_num, ctypes.byref(device_handle))
        _check_error(error, "JETI_OpenSpectroEx")
        self._device_handle = device_handle
    
    def close_device(self):
        """Close the device connection"""
        if self._device_handle is not None:
            error = self._dll.JETI_CloseSpectroEx(self._device_handle)
            _check_error(error, "JETI_CloseSpectroEx")
            self._device_handle = None
    
    def start_light_measurement(self, integration_time: float = 100.0, average: int = 1):
        """
        Start a light measurement
        
        Args:
            integration_time: Integration time in ms (0 for automatic)
            average: Number of averages
        """
        error = self._dll.JETI_StartLightEx(self._device_handle, integration_time, average)
        _check_error(error, "JETI_StartLightEx")
    
    def get_status(self) -> bool:
        """
        Get measurement status
        
        Returns:
            True if measurement is still running, False if finished
        """
        status = c_bool()
        error = self._dll.JETI_SpectroStatusEx(self._device_handle, ctypes.byref(status))
        _check_error(error, "JETI_SpectroStatusEx")
        return status.value
    
    def break_measurement(self):
        """Cancel an ongoing measurement"""
        error = self._dll.JETI_SpectroBreakEx(self._device_handle)
        _check_error(error, "JETI_SpectroBreakEx")
    
    def wait_for_measurement(self, poll_interval: float = 0.1):
        """
        Wait for measurement to complete
        
        Args:
            poll_interval: Time between status checks in seconds
        """
        import time
        while self.get_status():
            time.sleep(poll_interval)
    
    def get_light_spectrum_wavelength(self, wavelength_start: int = 380, 
                                      wavelength_end: int = 780,
                                      step: float = 5.0) -> np.ndarray:
        """
        Get light spectrum in wavelength domain
        
        Args:
            wavelength_start: Start wavelength in nm
            wavelength_end: End wavelength in nm
            step: Step width in nm
            
        Returns:
            numpy array with light spectrum
        """
        num_values = int((wavelength_end - wavelength_start) / step) + 1
        light_array = (c_float * num_values)()
        error = self._dll.JETI_LightWaveEx(
            self._device_handle, wavelength_start, wavelength_end, step, light_array
        )
        _check_error(error, "JETI_LightWaveEx")
        return np.array([light_array[i] for i in range(num_values)])
    
    def get_pixel_count(self) -> int:
        """Get number of pixels in the sensor"""
        pixel_count = c_uint32()
        error = self._dll.JETI_PixelCountEx(self._device_handle, ctypes.byref(pixel_count))
        _check_error(error, "JETI_PixelCountEx")
        return pixel_count.value
    
    def get_light_spectrum_pixel(self) -> np.ndarray:
        """
        Get light spectrum in pixel domain
        
        Returns:
            numpy array with raw pixel values
        """
        pixel_count = self.get_pixel_count()
        light_array = (c_int32 * pixel_count)()
        error = self._dll.JETI_LightPixEx(self._device_handle, light_array)
        _check_error(error, "JETI_LightPixEx")
        return np.array([light_array[i] for i in range(pixel_count)], dtype=np.int32)
    
    def get_dll_version(self) -> Tuple[int, int, int]:
        """Get DLL version (major, minor, build)"""
        major = c_uint16()
        minor = c_uint16()
        build = c_uint16()
        error = self._dll.JETI_GetSpectroExDLLVersion(
            ctypes.byref(major), ctypes.byref(minor), ctypes.byref(build)
        )
        _check_error(error, "JETI_GetSpectroExDLLVersion")
        return (major.value, minor.value, build.value)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_device()
        return False
