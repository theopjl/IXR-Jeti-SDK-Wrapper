# JETI SDK Python Wrapper - Usage Guide

## Quick Start

### 1. Installation

```bash
# Install required packages
pip install -r requirements.txt

# Or manually
pip install numpy
```

### 2. Verify Installation

```python
python test_wrapper.py
```

This will run basic tests to verify the wrapper is working correctly.

### 3. First Measurement

```python
python quick_start.py
```

## Step-by-Step Examples

### Example 1: Simple Measurement

```python
from jeti_wrapper import JetiRadio

# Create device
device = JetiRadio()

# Open device
device.open_device(0)

# Measure
device.measure()
device.wait_for_measurement()

# Get results
print(f"Radiometric: {device.get_radiometric_value():.3E} W/m²")
print(f"Photometric: {device.get_photometric_value():.3E} lx")

# Close
device.close_device()
```

### Example 2: Controlled Measurement

```python
from jeti_wrapper import JetiRadioEx

device = JetiRadioEx()
device.open_device(0)

# Measure with specific parameters
device.measure(
    integration_time=100.0,  # 100ms
    average=5,               # 5 averages
    step=1                   # 1nm step
)
device.wait_for_measurement()

# Get spectrum
spectrum = device.get_spectral_radiance(380, 780)
print(f"Spectrum shape: {spectrum.shape}")

device.close_device()
```

### Example 3: Using Context Manager

```python
from jeti_wrapper import JetiRadioEx

with JetiRadioEx() as device:
    device.open_device(0)
    device.measure()
    device.wait_for_measurement()
    
    results = {
        'radiometric': device.get_radiometric_value(),
        'photometric': device.get_photometric_value(),
        'cct': device.get_cct()
    }
    
print(f"CCT: {results['cct']:.1f} K")
```

### Example 4: Spectroscopic Measurement

```python
from jeti_wrapper import JetiSpectroEx
import numpy as np

device = JetiSpectroEx()
device.open_device(0)

# Measure light spectrum
device.start_light_measurement(integration_time=100.0, average=1)
device.wait_for_measurement()

# Get wavelength-based spectrum
spectrum = device.get_light_spectrum_wavelength(
    wavelength_start=380,
    wavelength_end=780,
    step=5.0
)

# Save to file
wavelengths = np.arange(380, 781, 5)
data = np.column_stack((wavelengths, spectrum))
np.savetxt('spectrum.csv', data, delimiter=',', 
           header='Wavelength(nm),Intensity')

device.close_device()
```

### Example 5: Error Handling

```python
from jeti_wrapper import JetiRadioEx, JetiException, JetiError

device = JetiRadioEx()

try:
    num_devices = device.get_num_devices()
    
    if num_devices == 0:
        print("No devices found")
    else:
        device.open_device(0)
        device.measure()
        device.wait_for_measurement()
        
        radio = device.get_radiometric_value()
        print(f"Measurement: {radio:.3E} W/m²")
        
except JetiException as e:
    if e.error_code == JetiError.TIMEOUT:
        print("Measurement timed out")
    elif e.error_code == JetiError.OVEREXPOSURE:
        print("Sensor overexposed - reduce light level")
    else:
        print(f"Error: {e}")
finally:
    device.close_device()
```

### Example 6: Batch Measurements

```python
from jeti_wrapper import JetiRadioEx
import numpy as np
import time

device = JetiRadioEx()
device.open_device(0)

# Collect multiple measurements
measurements = []
num_measurements = 10

print(f"Collecting {num_measurements} measurements...")
for i in range(num_measurements):
    device.measure(integration_time=100.0, average=1, step=1)
    device.wait_for_measurement()
    
    radio = device.get_radiometric_value()
    measurements.append(radio)
    print(f"  {i+1}: {radio:.3E} W/m²")
    
    time.sleep(0.5)  # Wait between measurements

# Convert to numpy array for analysis
measurements = np.array(measurements)

print(f"\nStatistics:")
print(f"  Mean:   {np.mean(measurements):.3E} W/m²")
print(f"  Std:    {np.std(measurements):.3E} W/m²")
print(f"  CV:     {(np.std(measurements)/np.mean(measurements)*100):.2f}%")

device.close_device()
```

### Example 7: COM Port Connection

```python
from jeti_wrapper import JetiRadio

device = JetiRadio()

# Open specific COM port
device.open_com_device(
    com_port=3,           # COM3
    baudrate=115200       # 115200 baud
)

device.measure()
device.wait_for_measurement()

print(f"Radiometric: {device.get_radiometric_value():.3E} W/m²")

device.close_device()
```

## Interactive Examples

Run the provided interactive examples:

### Radio Measurement (Basic)
```bash
python radio_sample.py
```
Features:
- Device selection
- Automatic measurement
- Manual operation of individual functions
- Display all color metrics

### Radio Measurement (Extended)
```bash
python radio_sample_ex.py
```
Features:
- Custom integration time
- Spectral data export
- Wavelength range selection

### Spectroscopic Measurement
```bash
python spectro_ex_sample.py
```
Features:
- Light spectrum measurement
- Wavelength and pixel-based data
- Data export capabilities

### Synchronized Measurement
```bash
python sync_sample.py
```
Features:
- Flicker frequency detection
- Synchronized measurements
- Cycle mode operation

### Advanced Analysis
```bash
python advanced_example.py
```
Features:
- Spectral analysis
- Data export (TXT and CSV)
- Statistical analysis
- Spectrum comparison

## Common Tasks

### Get Device Information

```python
from jeti_wrapper import JetiRadioEx

device = JetiRadioEx()

# Get number of devices
num = device.get_num_devices()
print(f"Found {num} devices")

# Get serial numbers
for i in range(num):
    board, spec, dev = device.get_serial_device(i)
    print(f"Device {i}:")
    print(f"  Board S/N: {board}")
    print(f"  Spec S/N:  {spec}")
    print(f"  Device S/N: {dev}")

# Get DLL version
major, minor, build = device.get_dll_version()
print(f"DLL Version: {major}.{minor}.{build}")
```

### Save Spectrum Data

```python
from jeti_wrapper import JetiRadioEx
import numpy as np

device = JetiRadioEx()
device.open_device(0)
device.measure()
device.wait_for_measurement()

# Get spectrum
spectrum = device.get_spectral_radiance(380, 780)
wavelengths = np.arange(380, 781)

# Save as CSV
data = np.column_stack((wavelengths, spectrum))
np.savetxt('spectrum.csv', data, delimiter=',',
           header='Wavelength(nm),SpectralRadiance(W/m²/nm)',
           comments='')

# Save as text with metadata
header = f"""JETI Spectral Data
Date: {datetime.now()}
Wavelength Range: 380-780 nm
"""
np.savetxt('spectrum.txt', data, header=header)

device.close_device()
```

### Automatic Integration Time

```python
from jeti_wrapper import JetiRadioEx

device = JetiRadioEx()
device.open_device(0)

# Use 0.0 for automatic integration time
device.measure(integration_time=0.0, average=1, step=1)
device.wait_for_measurement()

results = device.get_all_values()

device.close_device()
```

### Manual Integration Time Optimization

```python
from jeti_wrapper import JetiRadioEx, JetiException, JetiError

device = JetiRadioEx()
device.open_device(0)

# Try different integration times
tints = [10, 50, 100, 200, 500]

for tint in tints:
    try:
        device.measure(integration_time=tint, average=1, step=1)
        device.wait_for_measurement()
        
        radio = device.get_radiometric_value()
        print(f"Tint={tint}ms: {radio:.3E} W/m²")
        
    except JetiException as e:
        if e.error_code == JetiError.OVEREXPOSURE:
            print(f"Tint={tint}ms: Overexposed")
        elif e.error_code == JetiError.MEASURE_FAIL:
            print(f"Tint={tint}ms: Too dark")

device.close_device()
```

## Troubleshooting

### Problem: "No devices found"

**Solutions:**
1. Check device is powered on and connected
2. Verify USB cable is working
3. Check device drivers are installed
4. Try specifying COM port manually:
```python
device.open_com_device(com_port=3, baudrate=115200)
```

### Problem: "Could not open device"

**Solutions:**
1. Close other applications using the device
2. Try different device number if multiple devices connected
3. Restart the device
4. Check COM port is not in use

### Problem: "DLL not found"

**Solutions:**
1. Ensure all DLL files are in the same directory:
   - jeti_core64.dll
   - jeti_radio64.dll
   - jeti_radio_ex64.dll
   - jeti_spectro64.dll
   - jeti_spectro_ex64.dll

2. Use absolute path:
```python
device = JetiRadioEx(dll_path=r"C:\path\to\jeti_radio_ex64.dll")
```

### Problem: "Measurement timeout"

**Solutions:**
1. Increase timeout (not directly supported - use longer poll interval)
2. Check light source is on
3. Try automatic integration time
4. Reduce averaging

### Problem: "Overexposure error"

**Solutions:**
1. Reduce light level
2. Reduce integration time
3. Use neutral density filter
4. Increase measurement distance

### Problem: Import errors

**Solutions:**
```bash
# Check Python version
python --version  # Should be >= 3.11

# Install numpy
pip install numpy

# Verify installation
python -c "import numpy; print(numpy.__version__)"
```

## Best Practices

### 1. Always Use Context Managers or try/finally

```python
# Good
with JetiRadioEx() as device:
    device.open_device(0)
    # ... do measurements ...

# Also good
device = JetiRadioEx()
try:
    device.open_device(0)
    # ... do measurements ...
finally:
    device.close_device()
```

### 2. Handle Exceptions

```python
from jeti_wrapper import JetiException

try:
    # ... measurement code ...
except JetiException as e:
    print(f"JETI Error: {e}")
except Exception as e:
    print(f"General Error: {e}")
```

### 3. Check Device Count Before Opening

```python
num_devices = device.get_num_devices()
if num_devices == 0:
    print("No devices found")
    sys.exit(1)
```

### 4. Use Automatic Integration Time Initially

```python
# Start with auto
device.measure(integration_time=0.0, average=1, step=1)

# Then optimize if needed
```

### 5. Average Multiple Measurements for Stability

```python
# Use hardware averaging
device.measure(integration_time=100, average=5, step=1)

# Or software averaging
measurements = []
for i in range(5):
    device.measure()
    device.wait_for_measurement()
    measurements.append(device.get_radiometric_value())
    
mean_value = np.mean(measurements)
```

## Performance Tips

1. **Use appropriate step width**: 1nm for high resolution, 5nm or 10nm for faster measurements
2. **Minimize averages**: Start with 1, increase only if needed
3. **Reuse device objects**: Don't create new objects for each measurement
4. **Use compiled numpy operations**: Leverage numpy's vectorization
5. **Batch operations**: Collect data first, then analyze

## API Reference

See `README.md` for complete API documentation.

## Additional Resources

- Original C examples in: RadioSample.c, RadioSampleEx.c, SpectroExSample.c, SyncSample.c
- JETI SDK documentation: JETI_SDK_Programmers_Guide_*.pdf
- Wrapper source: jeti_wrapper.py

## Support

For issues with:
- **JETI devices/SDK**: Contact JETI Technische Instrumente GmbH
- **Python wrapper**: Check this guide and README.md
- **Hardware connection**: Refer to device manual
