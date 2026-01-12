# JETI Spectroradiometer Examples - Documentation Guide

This document provides a comprehensive analysis of the JETI spectroradiometer example files. It is intended to serve as a reference for creating equivalent examples for other spectroradiometer devices.

---

## Table of Contents

1. [Overview](#overview)
2. [Common Patterns](#common-patterns)
3. [Example Files Breakdown](#example-files-breakdown)
4. [API Categories](#api-categories)
5. [Code Structure Patterns](#code-structure-patterns)
6. [Measurement Workflows](#measurement-workflows)
7. [Data Export Patterns](#data-export-patterns)
8. [User Interaction Patterns](#user-interaction-patterns)

---

## Overview

The JETI examples demonstrate different aspects of spectroradiometer usage, from simple quick-start measurements to advanced spectral analysis. The examples are organized by complexity and use case:

- **Quick Start**: Minimal code for first-time users
- **Basic Radiometric**: Standard radiometric measurements (Radio/RadioEx classes)
- **Spectroscopic**: Light spectrum measurements (SpectroEx class)
- **Advanced**: Spectral analysis with data export
- **Synchronized**: Specialized synchronized measurements with flicker detection

### Device Classes

The JETI SDK provides multiple device classes:

1. **JetiRadio**: Basic radiometric measurements with automatic settings
2. **JetiRadioEx**: Extended radiometric with manual control (integration time, averaging, step)
3. **JetiSpectroEx**: Spectroscopic light measurements with pixel-level access

---

## Common Patterns

### 1. Import Setup

All examples use consistent import patterns:

```python
import sys
from pathlib import Path

# Development mode path setup
_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root / "src"))

from jeti import JetiRadioEx, JetiException  # Import specific classes
import numpy as np  # For data processing
```

**Pattern Purpose**: Allows running examples without installing the package

### 2. Exception Handling

All JETI operations use try-except blocks with the custom `JetiException`:

```python
try:
    device.some_operation()
except JetiException as e:
    print(f"Error: {e}")
    return
```

**Pattern Purpose**: Graceful error handling with informative messages

### 3. Device Lifecycle

Standard workflow for device operations:

```python
# 1. Create instance
device = JetiRadioEx()

# 2. Find devices
num_devices = device.get_num_devices()

# 3. Open device
device.open_device(device_index)

# 4. Perform operations
device.measure(...)

# 5. Close device (in finally block)
device.close_device()
```

### 4. Measurement Flow

Consistent pattern for performing measurements:

```python
# Start measurement
device.measure(integration_time, average, step)

# Wait for completion
while device.get_measure_status():
    time.sleep(0.1)

# Retrieve results
result = device.get_radiometric_value(start_wl, end_wl)
```

---

## Example Files Breakdown

### 1. quick_start.py

**Purpose**: Minimal example for beginners - demonstrates the simplest measurement workflow

**Key Features**:
- Single device, automatic settings
- Basic measurement with default parameters
- Essential result retrieval (radiometric, photometric, chromaticity, CCT, CRI)
- Clean linear flow (no menus or loops)

**Device Class**: `JetiRadioEx`

**Workflow**:
1. Create device instance
2. Find and open first device
3. Perform measurement with auto settings (`integration_time=0.0`)
4. Wait for measurement completion
5. Retrieve and display core results:
   - Radiometric value (W/m² over 380-780nm)
   - Photometric value (lux)
   - Chromaticity coordinates (x, y)
   - Correlated Color Temperature (CCT in Kelvin)
   - Color Rendering Index (CRI Ra value)
6. Close device

**Code Characteristics**:
- ~80 lines total
- No user input
- No data export
- Scientific notation formatting (`.3E`)
- Results table formatting with separators

**Key Methods Used**:
```python
get_num_devices()
open_device(index)
measure(integration_time, average, step)
wait_for_measurement()  # Convenience wrapper
get_radiometric_value(wl_start, wl_end)
get_photometric_value()
get_chromaticity_xy()
get_cct()
get_cri()
close_device()
```

---

### 2. radio_sample.py

**Purpose**: Port of C SDK RadioSample - basic radiometric measurements with interactive menu

**Key Features**:
- Multiple device selection support
- Serial number display
- Interactive menu system
- Individual API method testing
- Full CRI array display (Ra + R1-R14)

**Device Class**: `JetiRadio` (basic class, auto settings only)

**Application Structure**:
```python
class RadioMeasurementApp:
    def __init__(self)
    def initialize_device(self)    # Device discovery and opening
    def perform_measurement(self)  # Complete measurement workflow
    def display_results(self)      # Format and display all results
    def run_menu(self)             # Interactive menu loop
    def cleanup(self)              # Resource cleanup
```

**Multi-Device Selection Flow**:
```python
num_devices = device.get_num_devices()
if num_devices > 1:
    for i in range(num_devices):
        board_sn, spec_sn, device_sn = device.get_serial_device(i)
        print(f"Device {i}: Board S/N: {board_sn}...")
    device_num = int(input("Enter device number to open: "))
```

**Menu Options**:
- Full measurement workflow
- Individual operations:
  - Start measurement
  - Break measurement
  - Check status
  - Get radiometric value
  - Get photometric value
  - Get chromaticity xy
  - Get CCT
  - Get CRI

**Progress Indication Pattern**:
```python
print("Measuring", end="", flush=True)
while device.get_measure_status():
    print(".", end="", flush=True)
    time.sleep(0.1)
print(" Done!")
```

**CRI Display Pattern**:
```python
cri = device.get_cri()
print(f"  Ra (General):  {cri[0]:.2f}")
for i in range(1, 15):
    print(f"  R{i:2d}:           {cri[i]:.2f}")
```

---

### 3. radio_sample_ex.py

**Purpose**: Extended radiometric measurements with manual parameter control

**Key Features**:
- Manual control over integration time, averaging, and step width
- DLL version display
- Spectral radiance retrieval
- Wavelength range specification
- Interactive parameter input
- Data export to file

**Device Class**: `JetiRadioEx` (extended control)

**Additional Capabilities vs radio_sample.py**:
- Custom integration time (not just automatic)
- Averaging control (multiple measurements)
- Step width control (1, 5, or 10 nm)
- Spectral radiance access
- File export functionality

**Application Structure**:
```python
class RadioExMeasurementApp:
    def initialize_device(self)           # + DLL version display
    def perform_measurement(tint, avg, step)  # Parameterized
    def display_results(wl_start, wl_end)     # Wavelength range
    def get_spectrum(wl_start, wl_end)        # NEW
    def run_interactive_measurement(self)     # NEW - user input
    def run_menu(self)
    def cleanup(self)
```

**Measurement Parameters**:
```python
def perform_measurement(self, 
                       integration_time: float = 0.0,  # ms, 0=auto
                       average: int = 1,                # num averages
                       step: int = 1):                  # nm steps
```

**DLL Version Display**:
```python
major, minor, build = self.device.get_dll_version()
print(f"DLL Version: {major}.{minor}.{build}")
```

**Spectral Radiance Retrieval**:
```python
spectrum = self.device.get_spectral_radiance(wavelength_start, wavelength_end)
print(f"Spectrum shape: {spectrum.shape}")
print(f"Number of points: {len(spectrum)}")
for i in range(min(10, len(spectrum))):
    wavelength = wavelength_start + i
    print(f"  {wavelength}nm: {spectrum[i]:.3E}")
```

**File Export Pattern**:
```python
wavelengths = np.arange(wl_start, wl_end + 1)
data = np.column_stack((wavelengths, spectrum))
np.savetxt(filename, data, fmt='%.6e', 
           header='Wavelength(nm)\tSpectralRadiance')
```

**Interactive Parameter Input**:
```python
tint = float(input("Integration time in ms (0 for automatic): "))
avg = int(input("Number of averages: "))
step = int(input("Step width in nm (1, 5, or 10): "))
```

**Menu Options**:
1. Default measurement (auto, 1 avg, 1nm step)
2. Interactive measurement (user-specified parameters)
3. Get spectral radiance (with optional file save)

---

### 4. spectro_ex_sample.py

**Purpose**: Spectroscopic light measurements with pixel-level access

**Key Features**:
- Light spectrum measurements (not radiometric)
- Pixel count access
- Raw pixel spectrum retrieval
- Wavelength-based spectrum with custom step
- Different measurement type (light vs. radiometric)

**Device Class**: `JetiSpectroEx` (spectroscopic class)

**Key Differences from Radio Classes**:

| Aspect | Radio/RadioEx | SpectroEx |
|--------|---------------|-----------|
| Measurement Type | Radiometric | Light Spectrum |
| Start Method | `measure()` | `start_light_measurement()` |
| Status Method | `get_measure_status()` | `get_status()` |
| Result Retrieval | `get_radiometric_value()` | `get_light_spectrum_wavelength()` |
| Additional Access | N/A | Pixel-level data |

**Application Structure**:
```python
class SpectroExMeasurementApp:
    def initialize_device(self)          # + pixel count display
    def perform_light_measurement(...)   # Light measurement workflow
    def display_spectrum_info(...)       # Spectrum statistics
    def get_pixel_spectrum(self)         # NEW - raw pixel data
    def run_interactive_measurement(self)
    def run_menu(self)
    def cleanup(self)
```

**Device Initialization Additions**:
```python
# Display pixel count
pixel_count = self.device.get_pixel_count()
print(f"Pixel count: {pixel_count}")
```

**Light Measurement Flow**:
```python
def perform_light_measurement(self, 
                             integration_time: float = 100.0,  # Default 100ms
                             average: int = 1,
                             wavelength_start: int = 380,
                             wavelength_end: int = 780,
                             step: float = 5.0):  # Can be float
    
    # Start light measurement
    self.device.start_light_measurement(integration_time, average)
    
    # Wait for completion
    while self.device.get_status():
        time.sleep(0.1)
    
    # Get light spectrum
    spectrum = self.device.get_light_spectrum_wavelength(
        wavelength_start, wavelength_end, step
    )
```

**Pixel Spectrum Access**:
```python
pixel_count = self.device.get_pixel_count()
pixel_spectrum = self.device.get_light_spectrum_pixel()

print(f"Data type: {pixel_spectrum.dtype}")
print(f"Min value:  {np.min(pixel_spectrum)}")
print(f"Max value:  {np.max(pixel_spectrum)}")

for i in range(min(10, len(pixel_spectrum))):
    print(f"  Pixel {i}: {pixel_spectrum[i]}")
```

**Spectrum Statistics Display**:
```python
print(f"Number of points: {len(spectrum)}")
print(f"  Min value:  {np.min(spectrum):.3E}")
print(f"  Max value:  {np.max(spectrum):.3E}")
print(f"  Mean value: {np.mean(spectrum):.3E}")
print(f"  Std dev:    {np.std(spectrum):.3E}")
```

**Menu Options**:
1. Default light measurement (100ms, 1 avg, 380-780nm, 5nm step)
2. Interactive measurement (custom parameters)
3. Individual operations:
   - Start light measurement
   - Break measurement
   - Get status
   - Get light spectrum (wavelength-based)
   - Get light spectrum (pixel-based)

---

### 5. advanced_example.py

**Purpose**: Professional spectral analysis with numpy operations and multiple export formats

**Key Features**:
- Object-oriented analyzer class
- Comprehensive spectral analysis (peak, FWHM, centroid)
- Multiple data export formats (text, CSV)
- Spectrum comparison functionality
- Metadata inclusion in exports
- Progress indication
- Color measurements integration

**Device Class**: `JetiRadioEx`

**Class-Based Architecture**:
```python
class SpectralAnalyzer:
    def __init__(self)
    def connect(device_num)           # Device connection
    def measure_spectrum(...)          # Spectrum acquisition
    def analyze_spectrum(self)         # Statistical analysis
    def export_data(filename, metadata)  # Text export
    def export_csv(filename)           # CSV export
    def compare_spectra(other)         # Spectrum comparison
    def disconnect(self)               # Cleanup
```

**State Management**:
```python
def __init__(self):
    self.device = None
    self.spectrum_data = None  # Current spectrum
    self.wavelengths = None     # Wavelength array
```

**Connection with Info Display**:
```python
def connect(self, device_num: int = 0):
    self.device = JetiRadioEx()
    num_devices = self.device.get_num_devices()
    if num_devices == 0:
        raise RuntimeError("No JETI devices found")
    
    self.device.open_device(device_num)
    
    # Display device info
    major, minor, build = self.device.get_dll_version()
    print(f"DLL Version: {major}.{minor}.{build}")
```

**Comprehensive Spectral Analysis**:
```python
def analyze_spectrum(self):
    # Basic statistics
    print(f"  Min value:     {np.min(self.spectrum_data):.3E}")
    print(f"  Max value:     {np.max(self.spectrum_data):.3E}")
    print(f"  Mean value:    {np.mean(self.spectrum_data):.3E}")
    print(f"  Std deviation: {np.std(self.spectrum_data):.3E}")
    print(f"  Total power:   {np.sum(self.spectrum_data):.3E}")
    
    # Peak detection
    peak_idx = np.argmax(self.spectrum_data)
    peak_wavelength = self.wavelengths[peak_idx]
    peak_value = self.spectrum_data[peak_idx]
    
    # Centroid wavelength
    centroid = np.sum(self.wavelengths * self.spectrum_data) / np.sum(self.spectrum_data)
    
    # FWHM calculation
    half_max = peak_value / 2
    above_half = self.spectrum_data >= half_max
    if np.any(above_half):
        indices = np.where(above_half)[0]
        fwhm = self.wavelengths[indices[-1]] - self.wavelengths[indices[0]]
    
    # Color measurements
    radiometric = self.device.get_radiometric_value(
        int(self.wavelengths[0]), int(self.wavelengths[-1])
    )
    photometric = self.device.get_photometric_value()
    x, y = self.device.get_chromaticity_xy()
    cct = self.device.get_cct()
```

**Text Export with Metadata**:
```python
def export_data(self, filename: str = None, metadata: dict = None):
    # Auto-generate filename with timestamp
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"jeti_spectrum_{timestamp}.txt"
    
    # Build header
    header_lines = [
        "JETI Spectral Measurement Data",
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Wavelength range: {self.wavelengths[0]}-{self.wavelengths[-1]} nm",
        f"Number of points: {len(self.spectrum_data)}"
    ]
    
    if metadata:
        header_lines.append("\nMeasurement parameters:")
        for key, value in metadata.items():
            header_lines.append(f"  {key}: {value}")
    
    header_lines.append("\nData format: Wavelength(nm)  SpectralRadiance(W/m²/nm)")
    header = '\n'.join(header_lines)
    
    # Combine and save
    data = np.column_stack((self.wavelengths, self.spectrum_data))
    np.savetxt(filename, data, fmt='%.6e', header=header)
    print(f"File size: {os.path.getsize(filename)} bytes")
```

**CSV Export with Analysis**:
```python
def export_csv(self, filename: str = None, include_analysis: bool = True):
    with open(filename, 'w') as f:
        # Header
        f.write("# JETI Spectral Measurement Data\n")
        f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Spectrum data
        f.write("Wavelength_nm,SpectralRadiance_W_m2_nm\n")
        for wl, val in zip(self.wavelengths, self.spectrum_data):
            f.write(f"{wl},{val:.6e}\n")
        
        # Analysis section
        if include_analysis:
            f.write("\n# Analysis Results\n")
            analysis = self.analyze_spectrum()
            for key, value in analysis.items():
                f.write(f"# {key}: {value}\n")
```

**Spectrum Comparison**:
```python
def compare_spectra(self, other_spectrum: np.ndarray, 
                   label1: str = "Current",
                   label2: str = "Reference"):
    # Correlation coefficient
    correlation = np.corrcoef(self.spectrum_data, other_spectrum)[0, 1]
    
    # RMS difference
    rms_diff = np.sqrt(np.mean((self.spectrum_data - other_spectrum)**2))
    
    # Relative difference
    rel_diff = np.abs(self.spectrum_data - other_spectrum) / (other_spectrum + 1e-10)
    mean_rel_diff = np.mean(rel_diff) * 100
    
    # Peak comparison
    peak1_idx = np.argmax(self.spectrum_data)
    peak2_idx = np.argmax(other_spectrum)
    peak_shift = self.wavelengths[peak1_idx] - self.wavelengths[peak2_idx]
```

**Usage Pattern**:
```python
analyzer = SpectralAnalyzer()
analyzer.connect(device_num=0)

spectrum = analyzer.measure_spectrum(
    wl_start=380, wl_end=780,
    integration_time=0.0, average=1
)

analysis = analyzer.analyze_spectrum()

analyzer.export_data(metadata={
    'Integration time': 'auto',
    'Averages': 1,
    'Step': '1 nm'
})

analyzer.export_csv(include_analysis=True)
analyzer.disconnect()
```

---

### 6. sync_sample.py

**Purpose**: Synchronized measurements with optical trigger and flicker detection

**Key Features**:
- Flicker frequency detection
- Sync mode enable/disable
- Custom sync frequency setting
- Direct DLL access for advanced features
- Specialized for periodic light sources (AC-powered LEDs, fluorescent)

**Device Class**: `JetiRadio` + direct core DLL access

**Advanced Architecture**:
```python
class SyncMeasurementApp:
    def __init__(self)
    def _setup_core_functions(self)      # Load and configure DLL functions
    def initialize_device(self)
    def get_flicker_frequency(self)      # Auto-detect flicker
    def set_sync_mode(enable)            # Enable/disable sync
    def set_sync_frequency(frequency)    # Set sync freq
    def get_sync_frequency(self)         # Query sync freq
    def perform_sync_measurement(self)   # Full sync workflow
    def display_sync_info(self)
    def run_menu(self)
    def cleanup(self)                    # + sync mode disable
```

**Direct DLL Access Setup**:
```python
def _setup_core_functions(self):
    from jeti import _get_dll_path
    dll_path = str(_get_dll_path("jeti_core64.dll"))
    self._core_dll = ctypes.WinDLL(dll_path)
    
    # Configure function signatures
    self._core_dll.JETI_GetFlickerFreq.argtypes = [
        ctypes.c_void_p, POINTER(c_float), POINTER(c_uint32)
    ]
    self._core_dll.JETI_GetFlickerFreq.restype = c_uint32
    
    self._core_dll.JETI_SetSyncMode.argtypes = [ctypes.c_void_p, c_uint8]
    self._core_dll.JETI_SetSyncMode.restype = c_uint32
    # ... more functions
```

**Flicker Detection**:
```python
def get_flicker_frequency(self) -> float:
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
```

**Sync Mode Control**:
```python
def set_sync_mode(self, enable: bool):
    error = self._core_dll.JETI_SetSyncMode(
        self.device._device_handle,
        1 if enable else 0
    )
    if error != 0:
        raise JetiException(error, "JETI_SetSyncMode")

def set_sync_frequency(self, frequency: float):
    error = self._core_dll.JETI_SetSyncFreq(
        self.device._device_handle,
        frequency
    )
    if error != 0:
        raise JetiException(error, "JETI_SetSyncFreq")
```

**Synchronized Measurement Workflow**:
```python
def perform_sync_measurement(self):
    # Try auto-detection
    flicker_freq = self.get_flicker_frequency()
    
    if flicker_freq == 0.0:
        sync_freq = float(input("Enter sync frequency in Hz: "))
    else:
        print(f"Detected flicker frequency: {flicker_freq:.2f} Hz")
        use_detected = input("Use detected frequency? (y/n): ")
        if use_detected == 'y':
            sync_freq = flicker_freq
    
    # Enable sync mode
    self.set_sync_mode(True)
    
    # Set frequency
    self.set_sync_frequency(sync_freq)
    
    # Verify
    actual_freq = self.get_sync_frequency()
    print(f"Actual sync frequency: {actual_freq:.2f} Hz")
    
    # Perform measurement
    self.device.measure()
    while self.device.get_measure_status():
        time.sleep(0.1)
    
    radio = self.device.get_radiometric_value()
    
    # Disable sync mode
    self.set_sync_mode(False)
```

**Cleanup with Sync Disable**:
```python
def cleanup(self):
    if self.device is not None:
        try:
            # Ensure sync mode is disabled
            try:
                self.set_sync_mode(False)
            except:
                pass
            
            self.device.close_device()
        except JetiException as e:
            print(f"Error closing device: {e}")
```

---

## API Categories

### Device Management
- `get_num_devices()` → int
- `get_serial_device(index)` → (board_sn, spec_sn, device_sn)
- `open_device(index)` → None
- `close_device()` → None
- `get_dll_version()` → (major, minor, build)
- `get_pixel_count()` → int (SpectroEx only)

### Measurement Control
- `measure(integration_time, average, step)` → None (RadioEx)
- `measure()` → None (Radio, auto settings)
- `start_light_measurement(integration_time, average)` → None (SpectroEx)
- `break_measurement()` → None
- `get_measure_status()` → bool (Radio/RadioEx)
- `get_status()` → bool (SpectroEx)
- `wait_for_measurement()` → None (convenience wrapper)

### Radiometric Results
- `get_radiometric_value(wl_start, wl_end)` → float (W/m²) (RadioEx)
- `get_radiometric_value()` → float (Radio, full range)
- `get_photometric_value()` → float (lux)

### Color/Spectral Results
- `get_chromaticity_xy()` → (x, y)
- `get_cct()` → float (Kelvin)
- `get_cri(cct)` → array[15] (RadioEx, optional CCT parameter)
- `get_cri()` → array[15] (Radio)

### Spectral Data
- `get_spectral_radiance(wl_start, wl_end)` → ndarray (RadioEx)
- `get_light_spectrum_wavelength(wl_start, wl_end, step)` → ndarray (SpectroEx)
- `get_light_spectrum_pixel()` → ndarray (SpectroEx)

### Synchronization (Advanced, direct DLL)
- `JETI_GetFlickerFreq(handle, freq_ptr, warning_ptr)` → error
- `JETI_SetSyncMode(handle, enable)` → error
- `JETI_SetSyncFreq(handle, frequency)` → error
- `JETI_GetSyncFreq(handle, freq_ptr)` → error

---

## Code Structure Patterns

### 1. Single-Shot Scripts (quick_start.py)
```python
def main_function():
    """Single purpose function"""
    try:
        # Linear workflow
        device = create_and_open()
        perform_measurement()
        display_results()
    except JetiException as e:
        handle_error(e)
    finally:
        cleanup()

if __name__ == "__main__":
    main_function()
```

### 2. Class-Based Applications (radio_sample.py, radio_sample_ex.py, spectro_ex_sample.py)
```python
class MeasurementApp:
    def __init__(self):
        self.device = None
    
    def initialize_device(self) -> bool:
        """Returns success/failure"""
        ...
    
    def perform_measurement(...) -> dict:
        """Returns measurement results"""
        ...
    
    def run_menu(self):
        """Interactive menu loop"""
        while True:
            choice = display_menu()
            if choice == '0':
                break
            handle_choice(choice)
    
    def cleanup(self):
        """Resource cleanup"""
        if self.device:
            self.device.close_device()

def main():
    app = MeasurementApp()
    try:
        if app.initialize_device():
            app.run_menu()
    except KeyboardInterrupt:
        print("\nInterrupted!")
    finally:
        app.cleanup()

if __name__ == "__main__":
    main()
```

### 3. Analyzer Classes (advanced_example.py)
```python
class SpecializedAnalyzer:
    def __init__(self):
        self.device = None
        self.data = None
        self.metadata = None
    
    def connect(...) -> None:
        """Establish connection"""
        ...
    
    def acquire_data(...) -> data:
        """Data acquisition"""
        ...
    
    def analyze(...) -> results:
        """Analysis operations"""
        ...
    
    def export(...) -> None:
        """Data export"""
        ...
    
    def disconnect(self):
        """Cleanup"""
        ...

def main():
    analyzer = SpecializedAnalyzer()
    try:
        analyzer.connect()
        data = analyzer.acquire_data()
        results = analyzer.analyze()
        analyzer.export()
    finally:
        analyzer.disconnect()
```

---

## Measurement Workflows

### Workflow 1: Auto Measurement (JetiRadio)
```python
device = JetiRadio()
device.open_device(0)

# Start with automatic settings
device.measure()

# Wait for completion
while device.get_measure_status():
    time.sleep(0.1)

# Get results
radiometric = device.get_radiometric_value()
photometric = device.get_photometric_value()

device.close_device()
```

### Workflow 2: Manual Control (JetiRadioEx)
```python
device = JetiRadioEx()
device.open_device(0)

# Custom parameters
integration_time = 100.0  # ms
average = 5              # averages
step = 1                 # nm

device.measure(integration_time, average, step)

while device.get_measure_status():
    time.sleep(0.1)

# Wavelength-specific radiometric
radiometric = device.get_radiometric_value(380, 780)

# Get spectrum
spectrum = device.get_spectral_radiance(380, 780)

device.close_device()
```

### Workflow 3: Light Measurement (JetiSpectroEx)
```python
device = JetiSpectroEx()
device.open_device(0)

# Start light measurement
device.start_light_measurement(
    integration_time=100.0,
    average=1
)

while device.get_status():
    time.sleep(0.1)

# Get wavelength-based spectrum
spectrum = device.get_light_spectrum_wavelength(
    wavelength_start=380,
    wavelength_end=780,
    step=5.0
)

# Or get raw pixel data
pixel_spectrum = device.get_light_spectrum_pixel()

device.close_device()
```

### Workflow 4: Synchronized Measurement
```python
device = JetiRadio()
device.open_device(0)

# Get device handle for DLL access
handle = device._device_handle

# Detect flicker frequency
flicker_freq = detect_flicker(handle)

# Enable sync mode
set_sync_mode(handle, True)
set_sync_frequency(handle, flicker_freq)

# Measure
device.measure()
while device.get_measure_status():
    time.sleep(0.1)

radiometric = device.get_radiometric_value()

# Disable sync mode
set_sync_mode(handle, False)

device.close_device()
```

---

## Data Export Patterns

### Pattern 1: Simple numpy savetxt
```python
wavelengths = np.arange(start, end + 1)
data = np.column_stack((wavelengths, spectrum))
np.savetxt(filename, data, fmt='%.6e', 
           header='Wavelength(nm)\tSpectralRadiance')
```

### Pattern 2: Formatted Text with Metadata
```python
# Build header
header_lines = [
    "Measurement Data",
    f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    f"Range: {start}-{end} nm",
    "\nParameters:"
]
for key, value in metadata.items():
    header_lines.append(f"  {key}: {value}")

header = '\n'.join(header_lines)

# Save with header
data = np.column_stack((wavelengths, spectrum))
np.savetxt(filename, data, fmt='%.6e', header=header)
```

### Pattern 3: CSV Format
```python
with open(filename, 'w') as f:
    # Header comments
    f.write("# Measurement Data\n")
    f.write(f"# Date: {datetime.now()}\n\n")
    
    # Column headers
    f.write("Wavelength_nm,Intensity\n")
    
    # Data rows
    for wl, val in zip(wavelengths, spectrum):
        f.write(f"{wl},{val:.6e}\n")
```

### Pattern 4: Auto-Generated Filenames
```python
if filename is None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"measurement_{timestamp}.txt"
```

---

## User Interaction Patterns

### Pattern 1: Multi-Device Selection
```python
num_devices = device.get_num_devices()

if num_devices == 0:
    print("No devices found!")
    return False

if num_devices > 1:
    print(f"Found {num_devices} devices:")
    for i in range(num_devices):
        board_sn, spec_sn, device_sn = device.get_serial_device(i)
        print(f"Device {i}: S/N {board_sn}, {spec_sn}, {device_sn}")
    
    device_num = int(input("Enter device number: "))
    if device_num >= num_devices:
        print("Invalid device number!")
        return False
else:
    device_num = 0

device.open_device(device_num)
```

### Pattern 2: Interactive Menu
```python
while True:
    print("\n" + "=" * 60)
    print("MAIN MENU")
    print("=" * 60)
    print("1) Option 1")
    print("2) Option 2")
    print("0) Exit")
    print("=" * 60)
    
    choice = input("\nYour choice: ").strip().lower()
    
    if choice == '1':
        perform_option_1()
        input("\nPress Enter to continue...")
    elif choice == '0':
        break
    else:
        print("Invalid choice!")
```

### Pattern 3: Progress Indication
```python
# Dots progress
print("Measuring", end="", flush=True)
while device.get_measure_status():
    print(".", end="", flush=True)
    time.sleep(0.1)
print(" Done!")
```

### Pattern 4: Yes/No Prompts
```python
response = input("Save to file? (y/n): ").strip().lower()
if response == 'y':
    filename = input("Filename: ").strip()
    save_data(filename)
```

### Pattern 5: Parameter Input with Defaults
```python
integration_time = float(input("Integration time in ms (0 for automatic): "))
average = int(input("Number of averages: "))
```

---

## Key Takeaways for Porting

When creating equivalent examples for another spectroradiometer:

1. **Maintain example hierarchy**: quick_start → basic → extended → advanced
2. **Preserve workflow patterns**: initialize → measure → wait → retrieve → cleanup
3. **Keep error handling consistent**: try-except with device-specific exception
4. **Use similar naming conventions**: `get_*`, `set_*`, `measure()`, etc.
5. **Include progress feedback**: dots, status messages
6. **Provide multiple complexity levels**: auto settings vs. manual control
7. **Support multi-device scenarios**: device enumeration and selection
8. **Include data export**: simple text, CSV, with metadata
9. **Add analysis capabilities**: statistics, peak finding, comparison
10. **Create interactive menus**: for testing individual functions

### Example Naming Convention
- `quick_start.py` - minimal example
- `{device_type}_sample.py` - basic functionality
- `{device_type}_sample_ex.py` - extended control
- `spectro_*_sample.py` - spectroscopic functions
- `advanced_example.py` - analysis and export
- `sync_sample.py` - special features

### Required Adaptations
- Replace `Jeti*` classes with new device classes
- Replace `JetiException` with new exception type
- Adapt measurement parameters (integration time, averaging, etc.)
- Map equivalent methods (radiometric, photometric, spectral)
- Adjust wavelength ranges if different
- Modify DLL/library loading if applicable
- Update import paths and module names

---

## End of Documentation

This document provides a complete reference for replicating the JETI example structure for other spectroradiometer devices. Each pattern and workflow is designed to be device-agnostic and can be adapted to different APIs while maintaining the same user experience and educational progression.
