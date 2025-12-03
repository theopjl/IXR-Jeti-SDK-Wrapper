"""
Test script for JETI Python Wrapper
Tests basic functionality without requiring actual hardware
"""

import sys
from pathlib import Path

# Add src directory to path for development mode
_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root / "src"))

import pytest
import numpy as np

from jeti import (
    JetiCore, JetiRadio, JetiRadioEx,
    JetiSpectro, JetiSpectroEx,
    JetiException, JetiError
)


class TestImports:
    """Test that all classes can be imported"""
    
    def test_import_core(self):
        """Test JetiCore import"""
        from jeti import JetiCore
        assert JetiCore is not None
    
    def test_import_radio(self):
        """Test JetiRadio import"""
        from jeti import JetiRadio
        assert JetiRadio is not None
    
    def test_import_radio_ex(self):
        """Test JetiRadioEx import"""
        from jeti import JetiRadioEx
        assert JetiRadioEx is not None
    
    def test_import_spectro(self):
        """Test JetiSpectro import"""
        from jeti import JetiSpectro
        assert JetiSpectro is not None
    
    def test_import_spectro_ex(self):
        """Test JetiSpectroEx import"""
        from jeti import JetiSpectroEx
        assert JetiSpectroEx is not None
    
    def test_import_exception(self):
        """Test JetiException import"""
        from jeti import JetiException
        assert JetiException is not None
    
    def test_import_error(self):
        """Test JetiError import"""
        from jeti import JetiError
        assert JetiError is not None


class TestErrorCodes:
    """Test error code enumeration"""
    
    def test_success_code(self):
        """Test SUCCESS error code"""
        assert JetiError.SUCCESS == 0x00000000
    
    def test_timeout_code(self):
        """Test TIMEOUT error code"""
        assert JetiError.TIMEOUT == 0x00000008
    
    def test_overexposure_code(self):
        """Test OVEREXPOSURE error code"""
        assert JetiError.OVEREXPOSURE == 0x00000020
    
    def test_measure_fail_code(self):
        """Test MEASURE_FAIL error code"""
        assert JetiError.MEASURE_FAIL == 0x00000022
    
    def test_not_connected_code(self):
        """Test NOT_CONNECTED error code"""
        assert JetiError.NOT_CONNECTED == 0x00000014


class TestExceptionHandling:
    """Test custom exception handling"""
    
    def test_exception_creation(self):
        """Test exception can be created"""
        exc = JetiException(JetiError.TIMEOUT, "Test timeout")
        assert exc.error_code == JetiError.TIMEOUT
    
    def test_exception_message(self):
        """Test exception message formatting"""
        exc = JetiException(JetiError.TIMEOUT, "Test timeout")
        assert "TIMEOUT" in exc.message
        assert "0x00000008" in exc.message
    
    def test_exception_raise_catch(self):
        """Test exception can be raised and caught"""
        with pytest.raises(JetiException) as exc_info:
            raise JetiException(JetiError.TIMEOUT, "Test timeout")
        
        assert exc_info.value.error_code == JetiError.TIMEOUT


class TestNumpyIntegration:
    """Test numpy array handling"""
    
    def test_cri_array_shape(self):
        """Test CRI array shape simulation"""
        cri_data = [90.0] + [85.0 + i for i in range(14)]
        cri_array = np.array(cri_data)
        assert cri_array.shape == (15,)
    
    def test_cri_array_values(self):
        """Test CRI array values"""
        cri_data = [90.0] + [85.0 + i for i in range(14)]
        cri_array = np.array(cri_data)
        assert cri_array[0] == 90.0
        assert cri_array[1] == 85.0
    
    def test_spectrum_array(self):
        """Test spectrum array simulation"""
        spectrum = np.zeros(401, dtype=np.float32)  # 380-780nm
        assert spectrum.shape == (401,)
        assert spectrum.dtype == np.float32
    
    def test_pixel_array(self):
        """Test pixel array simulation"""
        pixels = np.zeros(1024, dtype=np.int32)
        assert pixels.shape == (1024,)
        assert pixels.dtype == np.int32


class TestContextManager:
    """Test context manager support (without actual device)"""
    
    def test_context_manager_protocol(self):
        """Test that classes have context manager methods"""
        # Check that __enter__ and __exit__ methods exist
        assert hasattr(JetiSpectroEx, '__enter__')
        assert hasattr(JetiSpectroEx, '__exit__')
        assert hasattr(JetiSpectro, '__enter__')
        assert hasattr(JetiSpectro, '__exit__')
        assert hasattr(JetiCore, '__enter__')
        assert hasattr(JetiCore, '__exit__')


class TestDLLPathResolution:
    """Test DLL path resolution logic"""
    
    def test_dll_path_function_exists(self):
        """Test that _get_dll_path function exists"""
        from jeti import _get_dll_path
        assert callable(_get_dll_path)
    
    def test_dll_path_returns_path(self):
        """Test that _get_dll_path returns a Path object"""
        from jeti import _get_dll_path
        result = _get_dll_path("jeti_core64.dll")
        assert isinstance(result, Path)
    
    def test_dll_path_contains_dll_name(self):
        """Test that returned path contains the DLL name"""
        from jeti import _get_dll_path
        result = _get_dll_path("jeti_core64.dll")
        assert result.name == "jeti_core64.dll"


# Optional tests that require DLLs (will be skipped if DLLs not present)
class TestWithDLLs:
    """Tests that require actual DLL files"""
    
    @pytest.fixture
    def has_dlls(self):
        """Check if DLLs are available"""
        from jeti import _get_dll_path
        dll_path = _get_dll_path("jeti_radio_ex64.dll")
        return dll_path.exists()
    
    @pytest.mark.skipif(
        not Path(__file__).parent.parent.joinpath("dlls", "jeti_radio_ex64.dll").exists(),
        reason="DLLs not present"
    )
    def test_dll_version(self):
        """Test DLL version retrieval"""
        device = JetiRadioEx()
        major, minor, build = device.get_dll_version()
        assert isinstance(major, int)
        assert isinstance(minor, int)
        assert isinstance(build, int)


def run_all_tests():
    """Run all tests using pytest"""
    exit_code = pytest.main([__file__, "-v", "--tb=short"])
    return exit_code == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
