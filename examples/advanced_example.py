"""
Advanced example: Spectral measurement with data export
Demonstrates spectrum acquisition, numpy operations, and data export
"""

import sys
from pathlib import Path

# Add src directory to path for development mode
_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root / "src"))

from jeti import JetiRadioEx, JetiException
import numpy as np
from datetime import datetime
import os


class SpectralAnalyzer:
    """Advanced spectral measurement with analysis and export"""
    
    def __init__(self):
        self.device = None
        self.spectrum_data = None
        self.wavelengths = None
        
    def connect(self, device_num: int = 0):
        """Connect to JETI device"""
        self.device = JetiRadioEx()
        
        num_devices = self.device.get_num_devices()
        if num_devices == 0:
            raise RuntimeError("No JETI devices found")
        
        print(f"Found {num_devices} device(s)")
        self.device.open_device(device_num)
        print(f"Connected to device {device_num}")
        
        # Get device info
        major, minor, build = self.device.get_dll_version()
        print(f"DLL Version: {major}.{minor}.{build}")
    
    def measure_spectrum(self, wl_start: int = 380, wl_end: int = 780,
                        integration_time: float = 0.0, average: int = 1):
        """
        Measure spectral radiance
        
        Args:
            wl_start: Start wavelength (nm)
            wl_end: End wavelength (nm)
            integration_time: Integration time in ms (0 for auto)
            average: Number of averages
        """
        print(f"\nMeasuring spectrum {wl_start}-{wl_end}nm...")
        print(f"Integration time: {'auto' if integration_time == 0 else f'{integration_time}ms'}")
        print(f"Averages: {average}")
        
        # Start measurement
        self.device.measure(integration_time, average, step=1)
        
        # Wait with progress indication
        print("Measuring", end="", flush=True)
        while self.device.get_measure_status():
            print(".", end="", flush=True)
            import time
            time.sleep(0.1)
        print(" Done!")
        
        # Get spectrum
        self.spectrum_data = self.device.get_spectral_radiance(wl_start, wl_end)
        self.wavelengths = np.arange(wl_start, wl_end + 1)
        
        print(f"Acquired {len(self.spectrum_data)} spectral points")
        
        return self.spectrum_data
    
    def analyze_spectrum(self):
        """Perform spectral analysis"""
        if self.spectrum_data is None:
            print("No spectrum data available")
            return None
        
        print("\n" + "=" * 60)
        print("SPECTRAL ANALYSIS")
        print("=" * 60)
        
        # Basic statistics
        print("\nStatistics:")
        print(f"  Min value:     {np.min(self.spectrum_data):.3E}")
        print(f"  Max value:     {np.max(self.spectrum_data):.3E}")
        print(f"  Mean value:    {np.mean(self.spectrum_data):.3E}")
        print(f"  Std deviation: {np.std(self.spectrum_data):.3E}")
        print(f"  Total power:   {np.sum(self.spectrum_data):.3E}")
        
        # Find peak
        peak_idx = np.argmax(self.spectrum_data)
        peak_wavelength = self.wavelengths[peak_idx]
        peak_value = self.spectrum_data[peak_idx]
        print(f"\nPeak wavelength: {peak_wavelength} nm")
        print(f"Peak value:      {peak_value:.3E}")
        
        # Calculate centroid wavelength
        centroid = np.sum(self.wavelengths * self.spectrum_data) / np.sum(self.spectrum_data)
        print(f"Centroid wavelength: {centroid:.2f} nm")
        
        # Spectral width (FWHM approximation)
        half_max = peak_value / 2
        above_half = self.spectrum_data >= half_max
        if np.any(above_half):
            indices = np.where(above_half)[0]
            fwhm = self.wavelengths[indices[-1]] - self.wavelengths[indices[0]]
            print(f"Spectral width (FWHM): {fwhm:.1f} nm")
        
        # Color measurements
        print("\n" + "-" * 60)
        print("COLOR MEASUREMENTS")
        print("-" * 60)
        
        radiometric = self.device.get_radiometric_value(
            int(self.wavelengths[0]), int(self.wavelengths[-1])
        )
        photometric = self.device.get_photometric_value()
        x, y = self.device.get_chromaticity_xy()
        cct = self.device.get_cct()
        
        print(f"Radiometric:   {radiometric:.3E} W/m²")
        print(f"Photometric:   {photometric:.3E} lx")
        print(f"Chromaticity:  x={x:.4f}, y={y:.4f}")
        print(f"CCT:           {cct:.1f} K")
        
        print("=" * 60)
        
        return {
            'peak_wavelength': peak_wavelength,
            'peak_value': peak_value,
            'centroid': centroid,
            'radiometric': radiometric,
            'photometric': photometric,
            'cct': cct,
            'chromaticity_x': x,
            'chromaticity_y': y
        }
    
    def export_data(self, filename: str = None, metadata: dict = None):
        """
        Export spectrum data to file
        
        Args:
            filename: Output filename (default: auto-generated with timestamp)
            metadata: Additional metadata to include in header
        """
        if self.spectrum_data is None:
            print("No spectrum data to export")
            return
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"jeti_spectrum_{timestamp}.txt"
        
        # Prepare header
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
        
        # Combine wavelengths and spectrum
        data = np.column_stack((self.wavelengths, self.spectrum_data))
        
        # Save to file
        np.savetxt(filename, data, fmt='%.6e', header=header)
        print(f"\nData exported to: {filename}")
        print(f"File size: {os.path.getsize(filename)} bytes")
    
    def export_csv(self, filename: str = None, include_analysis: bool = True):
        """
        Export spectrum and analysis to CSV format
        
        Args:
            filename: Output filename
            include_analysis: Include analysis results in separate section
        """
        if self.spectrum_data is None:
            print("No spectrum data to export")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"jeti_spectrum_{timestamp}.csv"
        
        with open(filename, 'w') as f:
            # Header
            f.write("# JETI Spectral Measurement Data\n")
            f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n")
            
            # Spectrum data
            f.write("Wavelength_nm,SpectralRadiance_W_m2_nm\n")
            for wl, val in zip(self.wavelengths, self.spectrum_data):
                f.write(f"{wl},{val:.6e}\n")
            
            # Analysis results
            if include_analysis:
                f.write("\n# Analysis Results\n")
                analysis = self.analyze_spectrum()
                if analysis:
                    for key, value in analysis.items():
                        f.write(f"# {key}: {value}\n")
        
        print(f"\nCSV data exported to: {filename}")
    
    def compare_spectra(self, other_spectrum: np.ndarray, label1: str = "Current",
                       label2: str = "Reference"):
        """
        Compare current spectrum with another spectrum
        
        Args:
            other_spectrum: Another spectrum array (same length)
            label1: Label for current spectrum
            label2: Label for reference spectrum
        """
        if self.spectrum_data is None:
            print("No spectrum data available")
            return
        
        if len(other_spectrum) != len(self.spectrum_data):
            print("Spectra must have the same length")
            return
        
        print("\n" + "=" * 60)
        print("SPECTRUM COMPARISON")
        print("=" * 60)
        
        # Calculate correlation
        correlation = np.corrcoef(self.spectrum_data, other_spectrum)[0, 1]
        print(f"\nCorrelation coefficient: {correlation:.4f}")
        
        # Calculate RMS difference
        rms_diff = np.sqrt(np.mean((self.spectrum_data - other_spectrum)**2))
        print(f"RMS difference: {rms_diff:.3E}")
        
        # Calculate relative difference
        rel_diff = np.abs(self.spectrum_data - other_spectrum) / (other_spectrum + 1e-10)
        mean_rel_diff = np.mean(rel_diff) * 100
        print(f"Mean relative difference: {mean_rel_diff:.2f}%")
        
        # Peak comparison
        peak1_idx = np.argmax(self.spectrum_data)
        peak2_idx = np.argmax(other_spectrum)
        peak1_wl = self.wavelengths[peak1_idx]
        peak2_wl = self.wavelengths[peak2_idx]
        
        print(f"\n{label1} peak: {peak1_wl} nm")
        print(f"{label2} peak: {peak2_wl} nm")
        print(f"Peak shift: {peak1_wl - peak2_wl} nm")
        
        print("=" * 60)
    
    def disconnect(self):
        """Disconnect from device"""
        if self.device:
            self.device.close_device()
            print("Device disconnected")


def main():
    """Example usage of SpectralAnalyzer"""
    analyzer = SpectralAnalyzer()
    
    try:
        # Connect to device
        analyzer.connect(device_num=0)
        
        # Measure spectrum
        spectrum = analyzer.measure_spectrum(
            wl_start=380,
            wl_end=780,
            integration_time=0.0,  # Auto
            average=1
        )
        
        # Analyze
        analysis = analyzer.analyze_spectrum()
        
        # Export data
        analyzer.export_data(
            metadata={
                'Integration time': 'auto',
                'Averages': 1,
                'Step': '1 nm'
            }
        )
        
        # Export CSV
        analyzer.export_csv(include_analysis=True)
        
        print("\n✓ Measurement and export completed successfully!")
        
    except JetiException as e:
        print(f"\nJETI Error: {e}")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        analyzer.disconnect()


if __name__ == "__main__":
    main()
