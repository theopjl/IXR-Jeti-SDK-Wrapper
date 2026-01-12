# Dual Device Comparison Workflow

## Overview

This workflow allows you to compare measurements from two JETI spectroradiometers by collecting data separately from each device and then performing analysis on the two datasets.

## Workflow Steps

### Step 1: Collect Data from Device 1

Run `dual_device_measurement.py` for the first device:

```bash
python examples/dual_device_measurement.py
```

**Interactive prompts:**
1. Select which device to measure (by index)
2. Choose measurement type (Radiance or Irradiance)
3. Enter number of samples
4. Enter base filename (e.g., `device1_test`)

**Output:** `reports/device1_test_DD-MM-YYYY_HHMMSS.csv`

### Step 2: Collect Data from Device 2

Run `dual_device_measurement.py` again for the second device:

```bash
python examples/dual_device_measurement.py
```

**Important:**
- Use the **same measurement type** (Radiance or Irradiance)
- Use the **same number of samples**
- Keep lighting conditions stable between measurements

**Interactive prompts:**
1. Select the second device
2. Choose **same** measurement type as Device 1
3. Enter **same** number of samples
4. Enter base filename (e.g., `device2_test`)

**Output:** `reports/device2_test_DD-MM-YYYY_HHMMSS.csv`

### Step 3: Analyze and Compare

Run `analyze_comparison.py`:

```bash
python examples/analyze_comparison.py
```

**Interactive prompts:**
1. Select first measurement file (Device 1 data)
2. Select second measurement file (Device 2 data)

**Validation:**
The script will verify that:
- Both files use the same measurement type
- Wavelength ranges match
- Number of samples match

**Output:** `reports/device1_vs_device2_analysis_DD-MM-YYYY_HHMMSS.csv`

## Benefits of Separate Collection

### 1. **Temporal Accuracy**
- Measuring both devices simultaneously was problematic because light conditions could change between Device 1 and Device 2 measurements
- Now you measure one device completely, ensuring all samples from that device see the same conditions

### 2. **Flexibility**
- Can re-analyze data without re-measuring
- Can collect data at different times and compare later
- Single script is reusable for any device comparison

### 3. **Maintainability**
- Simpler code: measurement script handles one device
- Analysis logic is completely separate from data collection
- Easier to debug and modify

## File Formats

### Measurement File (Single Device)
```
JETI Spectroradiometer Measurements
Measurement Type, Irradiance
Collection Date, 2025-12-17 14:30:00
Number of Samples, 30
Device Serial, ABC12345
Wavelength Start (nm), 380
Wavelength End (nm), 780

MEASUREMENT DATA
Sample, Timestamp, Irradiance_W/m2, Illuminance_lx, x, y, CCT_K, CRI_Ra, R1, R2, ...
1, 14:30:01.234, 1.23E-03, 4.56E+02, 0.3127, 0.3290, 6500.0, 85.2, ...

SPECTRAL DATA
Wavelength_nm, S1_W/m2/nm, S2_W/m2/nm, S3_W/m2/nm, ...
380, 1.23E-05, 1.24E-05, 1.22E-05, ...
```

### Analysis File (Comparison)
```
JETI Dual Device Comparison Analysis Report
Measurement Type, Irradiance
Device 1 Serial, ABC12345
Device 2 Serial, DEF67890
...

SUMMARY STATISTICS
Metric, Mean, Std Dev, Min, Max
Irradiance Diff (%), 2.345, 0.123, 2.100, 2.600
...

DETAILED PER-SAMPLE COMPARISON
Sample, Timestamp_Dev1, Timestamp_Dev2, Dev1_Irr, Dev2_Irr, Irr_Diff_Abs, Irr_Diff_%, ...
```

## Best Practices

1. **Stable Conditions**: Keep light source and environment as stable as possible during both measurement sessions
2. **Timing**: Minimize time between Device 1 and Device 2 measurements if comparing the same light source
3. **Documentation**: Use descriptive filenames that identify the test conditions
4. **Sample Size**: Use 30-50 samples for robust statistical analysis
5. **Measurement Type**: Ensure both devices measure the same type (Radiance or Irradiance)

## Troubleshooting

### "Measurement type mismatch"
- Ensure both measurement files use the same mode (Radiance or Irradiance)
- Check the measurement type in the CSV file metadata

### "Wavelength range mismatch"  
- Both devices should use the same wavelength range (default: 380-780 nm)
- This is automatically set in the measurement script

### "Sample count mismatch"
- Both files must have the same number of samples
- Re-run one of the measurements with matching sample count

## Analysis Metrics

The comparison includes:

- **Spectral**: Wavelength-by-wavelength differences, correlation coefficient
- **Radiometric**: Broadband irradiance (absolute and relative differences)
- **Photometric**: Illuminance (absolute and relative differences)
- **Colorimetric**: CIE xy, Delta E, CCT differences, Duv differences
- **Color Rendering**: CRI Ra and R1-R14 differences
- **Statistics**: Mean, standard deviation, min, max for all metrics
