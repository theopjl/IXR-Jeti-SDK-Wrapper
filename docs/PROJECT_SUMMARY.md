# JETI SDK Python Wrapper - Project Summary

## Overview

This is a complete Python wrapper for the JETI SDK version 4.8.10, providing an object-oriented interface to JETI radiometric and spectroscopic measurement devices.

## Project Structure

```
Jeti/
├── jeti_wrapper.py          # Main wrapper module with all classes
├── __init__.py              # Package initialization
├── requirements.txt         # Python dependencies
├── README.md               # Main documentation
├── USAGE_GUIDE.md          # Comprehensive usage guide
│
├── Examples (Python versions of C samples):
│   ├── quick_start.py              # Simplest example
│   ├── radio_sample.py             # Basic radiometric (from RadioSample.c)
│   ├── radio_sample_ex.py          # Extended radiometric (from RadioSampleEx.c)
│   ├── spectro_ex_sample.py        # Spectroscopic (from SpectroExSample.c)
│   ├── sync_sample.py              # Synchronized (from SyncSample.c)
│   └── advanced_example.py         # Advanced analysis & export
│
├── test_wrapper.py          # Test suite
│
├── Original C files:
│   ├── RadioSample.c
│   ├── RadioSampleEx.c
│   ├── SpectroExSample.c
│   └── SyncSample.c
│
├── Header files:
│   ├── jeti_core.h
│   ├── jeti_radio.h
│   ├── jeti_radio_ex.h
│   ├── jeti_spectro.h
│   └── jeti_spectro_ex.h
│
└── DLL files (required, not included):
    ├── jeti_core64.dll
    ├── jeti_radio64.dll
    ├── jeti_radio_ex64.dll
    ├── jeti_spectro64.dll
    └── jeti_spectro_ex64.dll
```

## Key Features

### 1. Object-Oriented Design

Five main classes, each handling specific functionality:

- **JetiCore**: Low-level device communication
- **JetiRadio**: Basic radiometric measurements
- **JetiRadioEx**: Extended radiometric with full control
- **JetiSpectro**: Basic spectroscopic measurements
- **JetiSpectroEx**: Extended spectroscopic measurements

### 2. Numpy Integration

All spectral data uses numpy arrays for efficient processing:
- Spectral radiance arrays
- CRI value arrays
- Pixel data arrays

### 3. Error Handling

- Custom `JetiException` class
- `JetiError` enumeration with all SDK error codes
- Automatic error checking after each DLL call
- Descriptive error messages

### 4. Pythonic Interface

- Context manager support (`with` statement)
- Property-style methods where appropriate
- Clear, descriptive method names
- Type hints throughout

### 5. Complete Examples

All original C examples converted to Python:
- Object-oriented structure
- Interactive menus
- Progress indicators
- Data export functionality

## Main Classes

### JetiCore
```python
core = JetiCore()
core.open_device(0)
pixel_count = core.get_pixel_count()
version = core.get_dll_version()
core.close_device()
```

### JetiRadio
```python
radio = JetiRadio()
radio.open_device(0)
radio.measure()
radio.wait_for_measurement()

radiometric = radio.get_radiometric_value()
photometric = radio.get_photometric_value()
x, y = radio.get_chromaticity_xy()
cct = radio.get_cct()
cri = radio.get_cri()  # Returns numpy array

radio.close_device()
```

### JetiRadioEx
```python
radio_ex = JetiRadioEx()
radio_ex.open_device(0)

# More control over parameters
radio_ex.measure(
    integration_time=100.0,  # ms
    average=5,
    step=1  # nm
)
radio_ex.wait_for_measurement()

# Get spectral data
spectrum = radio_ex.get_spectral_radiance(380, 780)
# Returns numpy array

radio_ex.close_device()
```

### JetiSpectroEx
```python
spectro = JetiSpectroEx()
spectro.open_device(0)

spectro.start_light_measurement(integration_time=100.0, average=1)
spectro.wait_for_measurement()

# Get spectrum (wavelength-based)
spectrum = spectro.get_light_spectrum_wavelength(380, 780, step=5.0)

# Get raw pixels
pixels = spectro.get_light_spectrum_pixel()

spectro.close_device()
```

## Usage Examples

### Quick Start
```python
from jeti_wrapper import JetiRadioEx

with JetiRadioEx() as device:
    device.open_device(0)
    device.measure()
    device.wait_for_measurement()
    print(f"Radiometric: {device.get_radiometric_value():.3E} W/m²")
```

### With Error Handling
```python
from jeti_wrapper import JetiRadioEx, JetiException, JetiError

device = JetiRadioEx()
try:
    device.open_device(0)
    device.measure()
    device.wait_for_measurement()
    radio = device.get_radiometric_value()
    print(f"Result: {radio:.3E} W/m²")
except JetiException as e:
    if e.error_code == JetiError.OVEREXPOSURE:
        print("Sensor overexposed!")
    else:
        print(f"Error: {e}")
finally:
    device.close_device()
```

### Export Data
```python
import numpy as np
from jeti_wrapper import JetiRadioEx

device = JetiRadioEx()
device.open_device(0)
device.measure()
device.wait_for_measurement()

spectrum = device.get_spectral_radiance(380, 780)
wavelengths = np.arange(380, 781)
data = np.column_stack((wavelengths, spectrum))
np.savetxt('spectrum.csv', data, delimiter=',')

device.close_device()
```

## Installation

1. **Install Python** (>= 3.11)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Copy DLL files** to the project directory:
   - jeti_core64.dll
   - jeti_radio64.dll
   - jeti_radio_ex64.dll
   - jeti_spectro64.dll
   - jeti_spectro_ex64.dll

4. **Test installation**:
   ```bash
   python test_wrapper.py
   ```

## Testing

Run the test suite:
```bash
python test_wrapper.py
```

Tests include:
- Import verification
- Error code validation
- Exception handling
- Device instantiation
- Context manager support
- Numpy integration
- DLL version check (requires DLLs)
- Device search (requires hardware)

## Example Scripts

### Basic Examples

1. **quick_start.py**: Simplest possible measurement
2. **radio_sample.py**: Interactive basic radiometric measurements
3. **radio_sample_ex.py**: Interactive extended radiometric measurements

### Advanced Examples

4. **spectro_ex_sample.py**: Spectroscopic measurements with data export
5. **sync_sample.py**: Synchronized measurements with flicker detection
6. **advanced_example.py**: Spectral analysis and comparison

## Measurement Types

### Radiometric Measurements
- Radiometric value (W/m²)
- Photometric value (lx)
- CIE 1931 chromaticity coordinates (x, y)
- CIE 1931 10° chromaticity coordinates
- CIE 1976 chromaticity coordinates (u', v')
- Correlated Color Temperature (CCT) in Kelvin
- Duv (distance from Planckian locus)
- Color Rendering Index (CRI) - 15 values

### Spectroscopic Data
- Spectral radiance (wavelength-based)
- Raw pixel data
- Configurable wavelength range
- Configurable step width (1, 5, or 10 nm)

### Measurement Parameters
- Integration time (auto or manual, in ms)
- Number of averages
- Wavelength range (typically 380-780 nm)
- Step width (1, 5, or 10 nm)

## Key Advantages Over C API

1. **Object-oriented**: Clean class hierarchy
2. **Memory management**: Automatic buffer handling
3. **Error handling**: Exceptions instead of error codes
4. **Data structures**: Numpy arrays instead of C arrays
5. **Type safety**: Type hints throughout
6. **Context managers**: Automatic cleanup
7. **Pythonic**: Following Python conventions

## Technical Details

### DLL Interface
- Uses `ctypes.WinDLL` for 64-bit DLLs
- Automatic type conversion
- Proper pointer handling
- String encoding/decoding

### Data Types
```python
DWORD → c_uint32
FLOAT → c_float
BOOL → c_bool
WORD → c_uint16
BYTE → c_uint8
INT32 → c_int32
DWORD_PTR → c_void_p
char* → c_char_p
```

### Thread Safety
Not thread-safe by default. Use separate device objects for concurrent measurements.

## Compatibility

- **Python**: >= 3.11
- **OS**: Windows (required for DLLs)
- **Dependencies**: numpy
- **Architecture**: 64-bit
- **JETI SDK**: Version 4.8.10

## Documentation Files

1. **README.md**: Main documentation with API reference
2. **USAGE_GUIDE.md**: Comprehensive usage examples
3. **This file**: Project overview and summary

## Conversion from C

All C examples have been faithfully converted:

| C File              | Python File            | Features                          |
|---------------------|------------------------|-----------------------------------|
| RadioSample.c       | radio_sample.py        | Basic radiometric                |
| RadioSampleEx.c     | radio_sample_ex.py     | Extended radiometric with spectra|
| SpectroExSample.c   | spectro_ex_sample.py   | Spectroscopic measurements       |
| SyncSample.c        | sync_sample.py         | Synchronized measurements        |
| -                   | advanced_example.py    | Advanced analysis (new)          |

## Error Handling Comparison

**C Code**:
```c
DWORD dwError;
dwError = JETI_Measure(dwDevice);
if (dwError != JETI_SUCCESS) {
    printf("Error: 0x%08X\n", dwError);
}
```

**Python Code**:
```python
try:
    device.measure()
except JetiException as e:
    print(f"Error: {e}")
```

## Data Handling Comparison

**C Code**:
```c
FLOAT *fSprad = (FLOAT*)malloc(401 * sizeof(FLOAT));
JETI_SpecRadEx(dwDevice, 380, 780, fSprad);
// Use data
free(fSprad);
```

**Python Code**:
```python
spectrum = device.get_spectral_radiance(380, 780)
# Use data - automatically managed numpy array
```

## Future Enhancements

Possible improvements:
1. Async/await support for measurements
2. Callback functions for progress
3. Plotting utilities (matplotlib integration)
4. Configuration file support
5. Multi-device management
6. Measurement scheduling
7. Data logging utilities

## Known Limitations

1. Windows-only (DLL dependency)
2. Not thread-safe without synchronization
3. Single device per object
4. No hot-plug detection
5. Limited callback support

## Support and Resources

- **Wrapper source**: `jeti_wrapper.py`
- **Examples**: All `.py` files
- **Documentation**: README.md, USAGE_GUIDE.md
- **Original SDK docs**: `JETI_SDK_Programmers_Guide_*.pdf`
- **JETI support**: Contact JETI Technische Instrumente GmbH

## License

This wrapper interfaces with proprietary JETI SDK.
Copyright (C) 2025 - JETI Technische Instrumente GmbH

## Version History

**Version 1.0.0** (2025)
- Initial release
- Complete wrapper for SDK 4.8.10
- All five module classes
- All C examples converted
- Comprehensive documentation
- Test suite
- Example scripts

## Conclusion

This Python wrapper provides a complete, modern, and Pythonic interface to the JETI SDK. It maintains full compatibility with the original C API while offering the advantages of Python's ease of use, numpy integration, and object-oriented design.

All original functionality is preserved and enhanced with:
- Better error handling
- Cleaner API
- Automatic memory management
- Type safety
- Comprehensive examples and documentation

The wrapper is production-ready and suitable for scientific measurements, automated testing, and integration into larger Python applications.
