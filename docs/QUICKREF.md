# JETI SDK Python Wrapper - Quick Reference Card

## Installation
```bash
pip install numpy
```

## Import
```python
from jeti_wrapper import JetiRadioEx, JetiException
```

## Basic Pattern
```python
device = JetiRadioEx()
device.open_device(0)
device.measure()
device.wait_for_measurement()
results = device.get_radiometric_value()
device.close_device()
```

## With Context Manager
```python
with JetiRadioEx() as device:
    device.open_device(0)
    device.measure()
    device.wait_for_measurement()
    results = device.get_radiometric_value()
```

## Classes

| Class          | Purpose                          |
|----------------|----------------------------------|
| JetiCore       | Core device functions            |
| JetiRadio      | Basic radiometric measurements   |
| JetiRadioEx    | Extended radiometric + spectra   |
| JetiSpectro    | Basic spectroscopic              |
| JetiSpectroEx  | Extended spectroscopic           |

## Common Methods

### Device Management
```python
num = device.get_num_devices()           # Find devices
device.open_device(0)                    # Open device 0
device.open_com_device(3, 115200)        # Open COM3
device.close_device()                    # Close device
```

### Measurement (JetiRadio)
```python
device.measure()                         # Auto settings
device.get_measure_status()              # Check if running
device.wait_for_measurement()            # Wait for completion
device.break_measurement()               # Cancel
```

### Measurement (JetiRadioEx)
```python
device.measure(tint, avg, step)          # With parameters
# tint: integration time (ms), 0=auto
# avg: averages (1-n)
# step: wavelength step (1, 5, 10 nm)
```

### Results (Radiometric)
```python
radio = device.get_radiometric_value()   # W/m²
photo = device.get_photometric_value()   # lx
x, y = device.get_chromaticity_xy()      # CIE x,y
cct = device.get_cct()                   # Kelvin
cri = device.get_cri()                   # numpy array[15]
```

### Results (Spectral)
```python
spectrum = device.get_spectral_radiance(380, 780)  # numpy array
```

### Spectroscopic
```python
device.start_light_measurement(tint, avg)
device.wait_for_measurement()
spectrum = device.get_light_spectrum_wavelength(380, 780, 5.0)
pixels = device.get_light_spectrum_pixel()
```

## Error Handling
```python
from jeti_wrapper import JetiException, JetiError

try:
    device.measure()
except JetiException as e:
    if e.error_code == JetiError.OVEREXPOSURE:
        print("Overexposed!")
    elif e.error_code == JetiError.TIMEOUT:
        print("Timeout!")
    else:
        print(f"Error: {e}")
```

## Common Error Codes
```python
JetiError.SUCCESS           # 0x00000000
JetiError.TIMEOUT           # 0x00000008
JetiError.OVEREXPOSURE      # 0x00000020
JetiError.MEASURE_FAIL      # 0x00000022
JetiError.NOT_CONNECTED     # 0x00000014
```

## Data Export
```python
import numpy as np

# Get spectrum
spectrum = device.get_spectral_radiance(380, 780)
wavelengths = np.arange(380, 781)

# Save as CSV
data = np.column_stack((wavelengths, spectrum))
np.savetxt('data.csv', data, delimiter=',')

# Save as text
np.savetxt('data.txt', data, fmt='%.6e')
```

## Measurement Parameters

| Parameter    | Type  | Range/Values        | Description              |
|--------------|-------|---------------------|--------------------------|
| tint         | float | 0.0 or 1.0-10000.0  | Integration time (ms)    |
| average      | int   | 1-1000              | Number of averages       |
| step         | int   | 1, 5, or 10         | Wavelength step (nm)     |
| wl_start     | int   | 300-900             | Start wavelength (nm)    |
| wl_end       | int   | 300-900             | End wavelength (nm)      |

## Typical Workflows

### Quick Measurement
```python
from jeti_wrapper import JetiRadioEx

device = JetiRadioEx()
device.open_device(0)
device.measure()                          # Auto everything
device.wait_for_measurement()
print(f"{device.get_radiometric_value():.3E} W/m²")
device.close_device()
```

### Controlled Measurement
```python
device = JetiRadioEx()
device.open_device(0)
device.measure(
    integration_time=100.0,               # 100ms
    average=5,                            # 5 averages
    step=1                                # 1nm resolution
)
device.wait_for_measurement()
spectrum = device.get_spectral_radiance(380, 780)
device.close_device()
```

### Multiple Measurements
```python
import numpy as np

device = JetiRadioEx()
device.open_device(0)

results = []
for i in range(10):
    device.measure()
    device.wait_for_measurement()
    results.append(device.get_radiometric_value())

mean = np.mean(results)
std = np.std(results)
device.close_device()
```

### With Analysis
```python
device = JetiRadioEx()
device.open_device(0)
device.measure()
device.wait_for_measurement()

# Get all results
spectrum = device.get_spectral_radiance(380, 780)
radio = device.get_radiometric_value()
photo = device.get_photometric_value()
x, y = device.get_chromaticity_xy()
cct = device.get_cct()
cri = device.get_cri()

# Analyze
peak_idx = np.argmax(spectrum)
peak_wl = 380 + peak_idx
print(f"Peak at {peak_wl}nm")
print(f"CCT: {cct:.1f}K")
print(f"CRI Ra: {cri[0]:.1f}")

device.close_device()
```

## Device Information
```python
# Count devices
num = device.get_num_devices()

# Serial numbers
board, spec, dev = device.get_serial_device(0)

# DLL version
major, minor, build = device.get_dll_version()

# Pixel count
pixels = device.get_pixel_count()
```

## Tips

1. **Start with auto**: Use `integration_time=0.0` first
2. **Use context managers**: Ensures cleanup
3. **Handle exceptions**: Always catch JetiException
4. **Check device count**: Before opening
5. **Close devices**: Always close when done

## Example Scripts

| Script                | Description                      |
|-----------------------|----------------------------------|
| quick_start.py        | Simplest example                 |
| radio_sample.py       | Interactive basic radiometric    |
| radio_sample_ex.py    | Interactive extended radiometric |
| spectro_ex_sample.py  | Spectroscopic measurements       |
| sync_sample.py        | Synchronized measurements        |
| advanced_example.py   | Analysis and export              |

## Run Examples
```bash
python quick_start.py
python radio_sample.py
python radio_sample_ex.py
python spectro_ex_sample.py
python sync_sample.py
python advanced_example.py
```

## Test Installation
```bash
python test_wrapper.py
```

## Documentation Files

- **README.md** - Main documentation
- **USAGE_GUIDE.md** - Detailed examples
- **PROJECT_SUMMARY.md** - Project overview
- **This file** - Quick reference

## Support

- Check README.md for detailed documentation
- See USAGE_GUIDE.md for examples
- Refer to original JETI SDK PDFs
- Contact JETI for hardware issues

## Minimum Working Example
```python
from jeti_wrapper import JetiRadioEx

with JetiRadioEx() as device:
    device.open_device(0)
    device.measure()
    device.wait_for_measurement()
    print(device.get_radiometric_value())
```

## Common Units

| Value          | Unit        |
|----------------|-------------|
| Radiometric    | W/m²        |
| Photometric    | lx          |
| Wavelength     | nm          |
| CCT            | K (Kelvin)  |
| Integration    | ms          |
| Spectral rad.  | W/m²/nm     |

---

**Version**: 1.0.0 | **Python**: ≥3.11 | **OS**: Windows | **SDK**: 4.8.10
