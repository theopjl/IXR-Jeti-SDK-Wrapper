"""
JETI Dual Device Comparison Analysis
Compares two single-device measurement files

Reads two CSV files from measure.py and performs
data dispersion analysis.

Calculates:
- Mean and standard deviation of absolute differences
- Mean and standard deviation of relative differences
- Mean and standard deviation of device intensities
"""

import sys
import csv
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime


def read_measurement_file(filepath: str) -> Dict:
    """
    Read single-device measurement data from CSV file (new format from measure.py)
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        Dictionary with metadata and spectral intensity data
    """
    print(f"Reading {Path(filepath).name}...")
    
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Parse header (first row)
    header = rows[0]
    
    # Extract metadata from header
    # Format: ['Serial {serial}', 'Wavelength (nm)', 'Sample(s) 1 to {num}', '{measurement_type}']
    device_serial = header[0].replace('Serial ', '').strip() if header[0].startswith('Serial') else "Unknown"
    num_samples_info = header[2] if len(header) > 2 else ""
    measurement_type = header[3] if len(header) > 3 else "Unknown"
    
    # Extract number of samples from data
    num_samples = len(rows[1]) - 1  # -1 for wavelength column
    
    # Parse data rows
    wavelengths = []
    intensity_data = []  # List of lists: [wavelength][sample]
    
    for row in rows[1:]:
        if not row or not row[0]:
            continue
        
        try:
            wl = float(row[0])
            wavelengths.append(wl)
            
            sample_intensities = []
            for i in range(1, len(row)):
                sample_intensities.append(float(row[i]))
            intensity_data.append(sample_intensities)
        except (ValueError, IndexError):
            continue
    
    wavelength_start = int(wavelengths[0]) if wavelengths else 0
    wavelength_end = int(wavelengths[-1]) if wavelengths else 0
    
    return {
        'metadata': {
            'device_serial': device_serial,
            'measurement_type': measurement_type,
            'num_samples': num_samples,
            'wavelength_start': wavelength_start,
            'wavelength_end': wavelength_end
        },
        'wavelengths': wavelengths,
        'intensity_data': intensity_data  # [wavelength_idx][sample_idx]
    }


def validate_compatibility(data1: Dict, data2: Dict) -> None:
    """
    Validate that two measurement files are compatible for comparison
    
    Args:
        data1, data2: Data dictionaries from read_measurement_file
        
    Raises:
        ValueError: If files are incompatible
    """
    meta1 = data1['metadata']
    meta2 = data2['metadata']
    
    # Check measurement type
    if meta1['measurement_type'] != meta2['measurement_type']:
        raise ValueError(
            f"Measurement type mismatch: "
            f"File 1 = {meta1['measurement_type']}, "
            f"File 2 = {meta2['measurement_type']}"
        )
    
    # Check wavelength range
    if meta1['wavelength_start'] != meta2['wavelength_start'] or \
       meta1['wavelength_end'] != meta2['wavelength_end']:
        raise ValueError(
            f"Wavelength range mismatch: "
            f"File 1 = {meta1['wavelength_start']}-{meta1['wavelength_end']} nm, "
            f"File 2 = {meta2['wavelength_start']}-{meta2['wavelength_end']} nm"
        )
    
    # Check number of samples
    if meta1['num_samples'] != meta2['num_samples']:
        raise ValueError(
            f"Sample count mismatch: "
            f"File 1 has {meta1['num_samples']} samples, "
            f"File 2 has {meta2['num_samples']} samples"
        )
    
    # Check wavelength arrays match
    if len(data1['wavelengths']) != len(data2['wavelengths']):
        raise ValueError(
            f"Wavelength array length mismatch: "
            f"File 1 has {len(data1['wavelengths'])} wavelengths, "
            f"File 2 has {len(data2['wavelengths'])} wavelengths"
        )
    
    print("✓ Files are compatible for comparison")


def analyze_data(data1: Dict, data2: Dict) -> Dict:
    """
    Perform data dispersion analysis between two measurement files
    
    Args:
        data1, data2: Data dictionaries from read_measurement_file
        
    Returns:
        Dictionary with dispersion statistics (mean and std dev)
    """
    print("\nAnalyzing data dispersion...")
    
    intensity1 = np.array(data1['intensity_data'])  # [wavelength][sample]
    intensity2 = np.array(data2['intensity_data'])
    
    # Calculate absolute and relative differences across all data points
    abs_diff = intensity2 - intensity1
    rel_diff = np.where(intensity1 != 0, (abs_diff / intensity1) * 100, 0)
    
    # Calculate dispersion statistics
    results = {
        'dispersion': {
            'absolute_difference': {
                'mean': float(np.mean(abs_diff)),
                'std': float(np.std(abs_diff))
            },
            'relative_difference_percent': {
                'mean': float(np.mean(rel_diff)),
                'std': float(np.std(rel_diff))
            },
            'device1_intensity': {
                'mean': float(np.mean(intensity1)),
                'std': float(np.std(intensity1))
            },
            'device2_intensity': {
                'mean': float(np.mean(intensity2)),
                'std': float(np.std(intensity2))
            }
        }
    }
    
    print("✓ Analysis complete!")
    
    return results


def save_analysis_report(data1: Dict, data2: Dict, analysis: Dict, output_path: str):
    """
    Save simplified dispersion analysis report to CSV
    
    Args:
        data1, data2: Original data dictionaries
        analysis: Analysis results
        output_path: Path for output file
    """
    print(f"\nSaving analysis report to {Path(output_path).name}...")
    
    meta1 = data1['metadata']
    meta2 = data2['metadata']
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow(['JETI Dual Device Data Dispersion Analysis'])
        writer.writerow(['Measurement Type', meta1['measurement_type']])
        writer.writerow(['Device 1 Serial', meta1['device_serial']])
        writer.writerow(['Device 2 Serial', meta2['device_serial']])
        writer.writerow(['Number of Samples', meta1['num_samples']])
        writer.writerow(['Wavelength Range', f"{meta1['wavelength_start']}-{meta1['wavelength_end']} nm"])
        writer.writerow([])
        
        # Dispersion statistics
        writer.writerow(['DATA DISPERSION STATISTICS'])
        writer.writerow([])
        writer.writerow(['Metric', 'Mean', 'Std Dev'])
        
        disp = analysis['dispersion']
        
        writer.writerow(['Absolute Difference (Device2 - Device1)',
                        f"{disp['absolute_difference']['mean']:.6E}",
                        f"{disp['absolute_difference']['std']:.6E}"])
        
        writer.writerow(['Relative Difference (%)',
                        f"{disp['relative_difference_percent']['mean']:.3f}",
                        f"{disp['relative_difference_percent']['std']:.3f}"])
        
        writer.writerow([])
        writer.writerow(['Device 1 Intensity',
                        f"{disp['device1_intensity']['mean']:.6E}",
                        f"{disp['device1_intensity']['std']:.6E}"])
        
        writer.writerow(['Device 2 Intensity',
                        f"{disp['device2_intensity']['mean']:.6E}",
                        f"{disp['device2_intensity']['std']:.6E}"])
    
    print("✓ Report saved successfully!")


def main():
    """Main analysis workflow"""
    print("=" * 70)
    print("JETI DUAL DEVICE COMPARISON ANALYSIS")
    print("=" * 70)
    print()
    
    reports_dir = Path(__file__).parent.parent / "reports"
    
    # Get available CSV files
    csv_files = sorted(reports_dir.glob("*.csv"))
    csv_files = [f for f in csv_files if '_analysis' not in f.stem]  # Exclude analysis files
    
    if not csv_files:
        print("No measurement CSV files found in reports/ directory")
        return
    
    print("Available measurement files:")
    for idx, file in enumerate(csv_files, 1):
        print(f"  {idx}. {file.name}")
    print()
    
    # Get first file
    print("SELECT FIRST MEASUREMENT FILE (Device 1)")
    print("-" * 70)
    while True:
        try:
            choice = input("Select file number (or enter full path): ").strip()
            if choice.isdigit():
                file_idx = int(choice) - 1
                if 0 <= file_idx < len(csv_files):
                    file1 = csv_files[file_idx]
                    break
            else:
                file1 = Path(choice)
                if file1.exists():
                    break
            print("Invalid selection. Please try again.")
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")
    
    print(f"✓ Selected: {file1.name}")
    print()
    
    # Get second file
    print("SELECT SECOND MEASUREMENT FILE (Device 2)")
    print("-" * 70)
    while True:
        try:
            choice = input("Select file number (or enter full path): ").strip()
            if choice.isdigit():
                file_idx = int(choice) - 1
                if 0 <= file_idx < len(csv_files):
                    file2 = csv_files[file_idx]
                    break
            else:
                file2 = Path(choice)
                if file2.exists():
                    break
            print("Invalid selection. Please try again.")
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")
    
    print(f"✓ Selected: {file2.name}")
    print()
    
    # Read both files
    print("=" * 70)
    print("LOADING DATA")
    print("=" * 70)
    data1 = read_measurement_file(str(file1))
    data2 = read_measurement_file(str(file2))
    
    # Validate compatibility
    print()
    print("=" * 70)
    print("VALIDATING COMPATIBILITY")
    print("=" * 70)
    try:
        validate_compatibility(data1, data2)
    except ValueError as e:
        print(f"\n❌ ERROR: {e}")
        print("\nThe selected files are not compatible for comparison.")
        return
    
    # Analyze
    print()
    print("=" * 70)
    print("PERFORMING ANALYSIS")
    print("=" * 70)
    analysis = analyze_data(data1, data2)
    
    # Generate output filename
    now = datetime.now()
    date_str = now.strftime('%d-%m-%Y')
    time_str = now.strftime('%H%M%S')
    output_name = f"{file1.stem}_vs_{file2.stem}_analysis_{date_str}_{time_str}.csv"
    output_file = reports_dir / output_name
    
    # Save report
    print()
    print("=" * 70)
    print("SAVING REPORT")
    print("=" * 70)
    save_analysis_report(data1, data2, analysis, str(output_file))
    
    print()
    print("=" * 70)
    print("ANALYSIS COMPLETE!")
    print("=" * 70)
    print(f"Report saved to: {output_file}")
    print()
    
    # Print summary
    print("QUICK SUMMARY:")
    print("-" * 70)
    disp = analysis['dispersion']
    print(f"Absolute difference:       {disp['absolute_difference']['mean']:.6E} ± {disp['absolute_difference']['std']:.6E}")
    print(f"Relative difference:       {disp['relative_difference_percent']['mean']:+.3f}% ± {disp['relative_difference_percent']['std']:.3f}%")
    print(f"Device 1 intensity:        {disp['device1_intensity']['mean']:.6E} ± {disp['device1_intensity']['std']:.6E}")
    print(f"Device 2 intensity:        {disp['device2_intensity']['mean']:.6E} ± {disp['device2_intensity']['std']:.6E}")
    print()


if __name__ == "__main__":
    from datetime import datetime
    main()
