"""
JETI Dual Device Comparison Analysis
Compares two single-device measurement files

Reads two CSV files from measure.py and performs
comprehensive intensity comparison analysis.

Calculates:
- Spectral intensity differences
- Per-sample and per-wavelength statistics
- Correlation analysis
- Statistical summaries
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
    Perform comprehensive intensity comparison analysis between two measurement files
    
    Args:
        data1, data2: Data dictionaries from read_measurement_file
        
    Returns:
        Dictionary with all analysis results
    """
    print("\nAnalyzing intensity data...")
    
    intensity1 = np.array(data1['intensity_data'])  # [wavelength][sample]
    intensity2 = np.array(data2['intensity_data'])
    wavelengths = data1['wavelengths']
    num_samples = data1['metadata']['num_samples']
    num_wavelengths = len(wavelengths)
    
    results = {
        'per_sample': [],
        'per_wavelength': [],
        'statistics': {}
    }
    
    # Per-sample analysis (comparing full spectra for each sample pair)
    print("  - Computing per-sample statistics...")
    for sample_idx in range(num_samples):
        spectrum1 = intensity1[:, sample_idx]
        spectrum2 = intensity2[:, sample_idx]
        
        # Absolute and relative differences
        abs_diff = spectrum2 - spectrum1
        rel_diff = np.where(spectrum1 != 0, (abs_diff / spectrum1) * 100, 0)
        
        # Correlation
        correlation = np.corrcoef(spectrum1, spectrum2)[0, 1]
        
        # RMSE
        rmse = np.sqrt(np.mean(abs_diff**2))
        
        # Mean absolute error
        mae = np.mean(np.abs(abs_diff))
        
        # Peak intensity comparison
        peak1 = np.max(spectrum1)
        peak2 = np.max(spectrum2)
        peak1_wl = wavelengths[np.argmax(spectrum1)]
        peak2_wl = wavelengths[np.argmax(spectrum2)]
        
        sample_result = {
            'sample': sample_idx + 1,
            'correlation': correlation,
            'rmse': rmse,
            'mae': mae,
            'mean_abs_diff': np.mean(abs_diff),
            'mean_rel_diff': np.mean(rel_diff),
            'std_abs_diff': np.std(abs_diff),
            'std_rel_diff': np.std(rel_diff),
            'max_abs_diff': np.max(np.abs(abs_diff)),
            'max_rel_diff': np.max(np.abs(rel_diff)),
            'peak1': peak1,
            'peak2': peak2,
            'peak_diff': peak2 - peak1,
            'peak_diff_rel': ((peak2 - peak1) / peak1 * 100) if peak1 != 0 else 0,
            'peak1_wavelength': peak1_wl,
            'peak2_wavelength': peak2_wl
        }
        
        results['per_sample'].append(sample_result)
    
    # Per-wavelength analysis (comparing across samples for each wavelength)
    print("  - Computing per-wavelength statistics...")
    for wl_idx, wl in enumerate(wavelengths):
        wl_intensities1 = intensity1[wl_idx, :]
        wl_intensities2 = intensity2[wl_idx, :]
        
        abs_diff = wl_intensities2 - wl_intensities1
        rel_diff = np.where(wl_intensities1 != 0, (abs_diff / wl_intensities1) * 100, 0)
        
        wl_result = {
            'wavelength': wl,
            'dev1_mean': np.mean(wl_intensities1),
            'dev2_mean': np.mean(wl_intensities2),
            'dev1_std': np.std(wl_intensities1),
            'dev2_std': np.std(wl_intensities2),
            'mean_abs_diff': np.mean(abs_diff),
            'mean_rel_diff': np.mean(rel_diff),
            'std_abs_diff': np.std(abs_diff),
            'std_rel_diff': np.std(rel_diff)
        }
        
        results['per_wavelength'].append(wl_result)
    
    # Overall statistics
    print("  - Computing overall statistics...")
    stats = results['statistics']
    
    # Sample-level statistics
    stats['correlation'] = {
        'mean': np.mean([r['correlation'] for r in results['per_sample']]),
        'std': np.std([r['correlation'] for r in results['per_sample']]),
        'min': np.min([r['correlation'] for r in results['per_sample']]),
        'max': np.max([r['correlation'] for r in results['per_sample']])
    }
    
    stats['rmse'] = {
        'mean': np.mean([r['rmse'] for r in results['per_sample']]),
        'std': np.std([r['rmse'] for r in results['per_sample']]),
        'min': np.min([r['rmse'] for r in results['per_sample']]),
        'max': np.max([r['rmse'] for r in results['per_sample']])
    }
    
    stats['mae'] = {
        'mean': np.mean([r['mae'] for r in results['per_sample']]),
        'std': np.std([r['mae'] for r in results['per_sample']]),
        'min': np.min([r['mae'] for r in results['per_sample']]),
        'max': np.max([r['mae'] for r in results['per_sample']])
    }
    
    stats['mean_rel_diff'] = {
        'mean': np.mean([r['mean_rel_diff'] for r in results['per_sample']]),
        'std': np.std([r['mean_rel_diff'] for r in results['per_sample']]),
        'min': np.min([r['mean_rel_diff'] for r in results['per_sample']]),
        'max': np.max([r['mean_rel_diff'] for r in results['per_sample']])
    }
    
    stats['peak_diff_rel'] = {
        'mean': np.mean([r['peak_diff_rel'] for r in results['per_sample']]),
        'std': np.std([r['peak_diff_rel'] for r in results['per_sample']]),
        'min': np.min([r['peak_diff_rel'] for r in results['per_sample']]),
        'max': np.max([r['peak_diff_rel'] for r in results['per_sample']])
    }
    
    print("✓ Analysis complete!")
    
    return results


def save_analysis_report(data1: Dict, data2: Dict, analysis: Dict, output_path: str):
    """
    Save analysis report to CSV
    
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
        writer.writerow(['JETI Dual Device Intensity Comparison Analysis Report'])
        writer.writerow(['Measurement Type', meta1['measurement_type']])
        writer.writerow(['Device 1 Serial', meta1['device_serial']])
        writer.writerow(['Device 2 Serial', meta2['device_serial']])
        writer.writerow(['Number of Samples', meta1['num_samples']])
        writer.writerow(['Wavelength Range', f"{meta1['wavelength_start']}-{meta1['wavelength_end']} nm"])
        writer.writerow([])
        
        # Summary statistics
        writer.writerow(['SUMMARY STATISTICS (Across All Samples)'])
        writer.writerow([])
        writer.writerow(['Metric', 'Mean', 'Std Dev', 'Min', 'Max'])
        
        stats = analysis['statistics']
        writer.writerow(['Spectral Correlation', 
                        f"{stats['correlation']['mean']:.6f}",
                        f"{stats['correlation']['std']:.6f}",
                        f"{stats['correlation']['min']:.6f}",
                        f"{stats['correlation']['max']:.6f}"])
        
        writer.writerow(['RMSE (Root Mean Square Error)', 
                        f"{stats['rmse']['mean']:.6E}",
                        f"{stats['rmse']['std']:.6E}",
                        f"{stats['rmse']['min']:.6E}",
                        f"{stats['rmse']['max']:.6E}"])
        
        writer.writerow(['MAE (Mean Absolute Error)', 
                        f"{stats['mae']['mean']:.6E}",
                        f"{stats['mae']['std']:.6E}",
                        f"{stats['mae']['min']:.6E}",
                        f"{stats['mae']['max']:.6E}"])
        
        writer.writerow(['Mean Relative Difference (%)', 
                        f"{stats['mean_rel_diff']['mean']:.3f}",
                        f"{stats['mean_rel_diff']['std']:.3f}",
                        f"{stats['mean_rel_diff']['min']:.3f}",
                        f"{stats['mean_rel_diff']['max']:.3f}"])
        
        writer.writerow(['Peak Intensity Relative Diff (%)', 
                        f"{stats['peak_diff_rel']['mean']:.3f}",
                        f"{stats['peak_diff_rel']['std']:.3f}",
                        f"{stats['peak_diff_rel']['min']:.3f}",
                        f"{stats['peak_diff_rel']['max']:.3f}"])
        
        writer.writerow([])
        
        # Per-sample comparison
        writer.writerow(['PER-SAMPLE COMPARISON'])
        writer.writerow([])
        
        header = ['Sample', 'Correlation', 'RMSE', 'MAE', 
                 'Mean_Abs_Diff', 'Mean_Rel_Diff_%', 'Std_Abs_Diff', 'Std_Rel_Diff_%',
                 'Max_Abs_Diff', 'Max_Rel_Diff_%',
                 'Dev1_Peak', 'Dev2_Peak', 'Peak_Diff', 'Peak_Diff_%',
                 'Dev1_Peak_WL_nm', 'Dev2_Peak_WL_nm']
        writer.writerow(header)
        
        for result in analysis['per_sample']:
            row = [
                result['sample'],
                f"{result['correlation']:.6f}",
                f"{result['rmse']:.6E}",
                f"{result['mae']:.6E}",
                f"{result['mean_abs_diff']:.6E}",
                f"{result['mean_rel_diff']:.3f}",
                f"{result['std_abs_diff']:.6E}",
                f"{result['std_rel_diff']:.3f}",
                f"{result['max_abs_diff']:.6E}",
                f"{result['max_rel_diff']:.3f}",
                f"{result['peak1']:.6E}",
                f"{result['peak2']:.6E}",
                f"{result['peak_diff']:.6E}",
                f"{result['peak_diff_rel']:.3f}",
                f"{result['peak1_wavelength']:.1f}",
                f"{result['peak2_wavelength']:.1f}"
            ]
            writer.writerow(row)
        
        writer.writerow([])
        
        # Per-wavelength statistics
        writer.writerow(['PER-WAVELENGTH STATISTICS (Averaged Across Samples)'])
        writer.writerow([])
        
        wl_header = ['Wavelength_nm', 
                     'Dev1_Mean', 'Dev1_Std', 'Dev2_Mean', 'Dev2_Std',
                     'Mean_Abs_Diff', 'Mean_Rel_Diff_%', 'Std_Abs_Diff', 'Std_Rel_Diff_%']
        writer.writerow(wl_header)
        
        for wl_result in analysis['per_wavelength']:
            row = [
                f"{wl_result['wavelength']:.1f}",
                f"{wl_result['dev1_mean']:.6E}",
                f"{wl_result['dev1_std']:.6E}",
                f"{wl_result['dev2_mean']:.6E}",
                f"{wl_result['dev2_std']:.6E}",
                f"{wl_result['mean_abs_diff']:.6E}",
                f"{wl_result['mean_rel_diff']:.3f}",
                f"{wl_result['std_abs_diff']:.6E}",
                f"{wl_result['std_rel_diff']:.3f}"
            ]
            writer.writerow(row)
        
        writer.writerow([])
        
        # Detailed intensity differences per sample per wavelength
        writer.writerow(['DETAILED INTENSITY DIFFERENCES (Device2 - Device1)'])
        writer.writerow([])
        
        intensity1 = np.array(data1['intensity_data'])
        intensity2 = np.array(data2['intensity_data'])
        diff = intensity2 - intensity1
        
        diff_header = ['Wavelength_nm'] + [f'Sample_{i+1}_Diff' for i in range(meta1['num_samples'])]
        writer.writerow(diff_header)
        
        for wl_idx, wl in enumerate(data1['wavelengths']):
            row = [f"{wl:.1f}"] + [f"{diff[wl_idx, sample_idx]:.6E}" 
                                   for sample_idx in range(meta1['num_samples'])]
            writer.writerow(row)
    
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
    stats = analysis['statistics']
    print(f"Spectral correlation:      {stats['correlation']['mean']:.6f} ± {stats['correlation']['std']:.6f}")
    print(f"RMSE:                      {stats['rmse']['mean']:.6E} ± {stats['rmse']['std']:.6E}")
    print(f"Mean relative diff:        {stats['mean_rel_diff']['mean']:+.3f}% ± {stats['mean_rel_diff']['std']:.3f}%")
    print(f"Peak intensity diff:       {stats['peak_diff_rel']['mean']:+.3f}% ± {stats['peak_diff_rel']['std']:.3f}%")
    print()


if __name__ == "__main__":
    from datetime import datetime
    main()
