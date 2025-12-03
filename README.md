# JETI SDK Python Wrapper

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python wrapper for JETI SDK version 4.8.10, compatible with Python >= 3.11

## Overview

This wrapper provides a Python interface to the JETI SDK for radiometric and spectroscopic measurements. It uses `ctypes` to interface with the JETI DLLs and `numpy` for data management.

## Features

- **Object-oriented design** with separate classes for different functionality:
  - `JetiCore`: Core device functionality
  - `JetiRadio`: Radiometric measurements
  - `JetiRadioEx`: Extended radiometric measurements with more control
  - `JetiSpectro`: Spectroscopic measurements
  - `JetiSpectroEx`: Extended spectroscopic measurements

- **Error handling** with custom exceptions
- **Numpy integration** for efficient data handling
- **Context manager support** for automatic resource cleanup

## Project Structure

```
jeti/
├── dlls/                    # JETI SDK DLL files (64-bit)
├── include/                 # SDK header files
├── src/jeti/               # Python package
├── examples/
│   ├── c/                  # Original C examples
│   └── python/             # Python examples
├── tests/                  # Unit tests
├── docs/                   # Documentation
├── .github/workflows/      # CI/CD
├── pyproject.toml          # Package configuration
└── README.md
```

## Requirements

- Python >= 3.11
- numpy >= 1.24.0
- Windows OS (required for DLL support)
- JETI device drivers installed

## Installation

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/theopjl/IXR-Jeti-SDK-Wrapper
cd IXR-Jeti-SDK-Wrapper

# Install in development mode
pip install -e ".[dev]"
```

### Quick Install

```bash
pip install numpy
```

The DLL files should be placed in the `dlls/` directory:
- `jeti_core64.dll`
- `jeti_radio64.dll`
- `jeti_radio_ex64.dll`
- `jeti_spectro64.dll`
- `jeti_spectro_ex64.dll`

## Usage

### Basic Radiometric Measurement

```python
from jeti import JetiRadio, JetiException

try:
    # Create device object
    device = JetiRadio()
    
    # Find and open device
    num_devices = device.get_num_devices()
    if num_devices > 0:
        device.open_device(0)  # Open first device
        
        # Perform measurement
        device.measure()
        device.wait_for_measurement()
        
        # Get results
        radiometric = device.get_radiometric_value()
        photometric = device.get_photometric_value()
        x, y = device.get_chromaticity_xy()
        cct = device.get_cct()
        cri = device.get_cri()
        
        print(f"Radiometric: {radiometric:.3E} W/m²")
        print(f"Photometric: {photometric:.3E} lx")
        print(f"CCT: {cct:.1f} K")
        
        # Close device
        device.close_device()
        
except JetiException as e:
    print(f"Error: {e}")
```

### Using Context Manager

```python
from jeti import JetiRadioEx

with JetiRadioEx() as device:
    device.open_device(0)
    device.measure(integration_time=100.0, average=1, step=1)
    device.wait_for_measurement()
    
    # Get spectral radiance
    spectrum = device.get_spectral_radiance(380, 780)
    print(f"Spectrum shape: {spectrum.shape}")
```

### Spectroscopic Measurement

```python
from jeti import JetiSpectroEx
import numpy as np

device = JetiSpectroEx()
device.open_device(0)

# Start light measurement
device.start_light_measurement(integration_time=100.0, average=1)
device.wait_for_measurement()

# Get spectrum (wavelength-based)
spectrum = device.get_light_spectrum_wavelength(380, 780, step=5.0)

# Get raw pixel data
pixel_data = device.get_light_spectrum_pixel()

# Save to file
wavelengths = np.arange(380, 781, 5)
np.savetxt('spectrum.txt', np.column_stack((wavelengths, spectrum)))

device.close_device()
```

## Example Scripts

The package includes several example scripts in `examples/python/`:

### quick_start.py
Simplest measurement example.
```bash
python examples/python/quick_start.py
```

### radio_sample.py
Basic radiometric measurement application with interactive menu.
```bash
python examples/python/radio_sample.py
```

### radio_sample_ex.py
Extended radiometric measurements with custom parameters and spectral data.
```bash
python examples/python/radio_sample_ex.py
```

### spectro_ex_sample.py
Spectroscopic light measurements with wavelength and pixel-based data.
```bash
python examples/python/spectro_ex_sample.py
```

### sync_sample.py
Synchronized measurements using optical trigger and cycle mode.
```bash
python examples/python/sync_sample.py
```

## Class Overview

### JetiCore
Core device functionality for low-level communication and control.

**Key methods:**
- `get_num_devices()` - Get number of connected devices
- `open_device(device_num)` - Open a specific device
- `close_device()` - Close the device
- `get_identifier()` - Get device identifier
- `get_pixel_count()` - Get sensor pixel count

### JetiRadio
Radiometric measurements with automatic settings.

**Key methods:**
- `measure()` - Start measurement (automatic integration time)
- `get_measure_status()` - Check if measurement is running
- `get_radiometric_value()` - Get radiometric value (W/m²)
- `get_photometric_value()` - Get photometric value (lx)
- `get_chromaticity_xy()` - Get CIE 1931 x,y coordinates
- `get_cct()` - Get correlated color temperature (K)
- `get_cri()` - Get color rendering indices (numpy array)

### JetiRadioEx
Extended radiometric measurements with manual control.

**Key methods:**
- `measure(integration_time, average, step)` - Start measurement with parameters
- `get_spectral_radiance(wl_start, wl_end)` - Get spectral radiance data
- All methods from JetiRadio

**Parameters:**
- `integration_time`: Integration time in ms (0 for automatic)
- `average`: Number of averages
- `step`: Wavelength step (1, 5, or 10 nm)

### JetiSpectroEx
Extended spectroscopic measurements.

**Key methods:**
- `start_light_measurement(integration_time, average)` - Start light measurement
- `get_light_spectrum_wavelength(start, end, step)` - Get wavelength-based spectrum
- `get_light_spectrum_pixel()` - Get raw pixel data
- `get_pixel_count()` - Get number of pixels

## Error Handling

The wrapper includes comprehensive error handling with custom exceptions:

```python
from jeti import JetiException, JetiError

try:
    device.measure()
except JetiException as e:
    print(f"Error code: 0x{e.error_code:08X}")
    print(f"Message: {e.message}")
    
    if e.error_code == JetiError.TIMEOUT:
        print("Measurement timed out")
    elif e.error_code == JetiError.OVEREXPOSURE:
        print("Sensor overexposed")
```

## Error Codes

Common error codes (see `JetiError` enum in wrapper):
- `SUCCESS` (0x00000000) - No error
- `TIMEOUT` (0x00000008) - Timeout error
- `OVEREXPOSURE` (0x00000020) - Sensor overexposure
- `MEASURE_FAIL` (0x00000022) - Measurement failed
- `NOT_CONNECTED` (0x00000014) - Device not connected

## Data Types

All spectral data is returned as numpy arrays:
- Spectral radiance: `np.ndarray` of float32
- CRI values: `np.ndarray` of 15 floats (Ra, R1-R14)
- Pixel data: `np.ndarray` of int32

## Notes

- All DLL files must be 64-bit versions for 64-bit Python
- Integration time is in milliseconds
- Wavelengths are in nanometers
- Use integration_time=0.0 for automatic adaptation
- The wrapper automatically handles C string buffers and data type conversions

## Troubleshooting

**"No matching device found"**
- Check device is connected and powered on
- Verify device drivers are installed
- Try specifying COM port manually using `open_com_device(port, baudrate)`

**"Could not open device"**
- Device may already be open in another application
- Try different device number if multiple devices are connected

**"DLL not found"**
- Ensure all DLL files are in the same directory as the wrapper
- Use absolute path when initializing: `JetiRadio(dll_path=r"C:\path\to\jeti_radio64.dll")`

**Import errors**
- Make sure numpy is installed: `pip install numpy`
- Verify Python version is 3.11 or higher

## License

This wrapper is provided for use with JETI instruments.
Copyright (C) 2025 - JETI Technische Instrumente GmbH

## Version

Wrapper version: 1.0.0
JETI SDK version: 4.8.10

## Author

Generated from JETI SDK C headers and documentation
