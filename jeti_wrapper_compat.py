"""
Compatibility module for backward compatibility.

This module allows using the old import path:
    from jeti_wrapper import JetiRadio, JetiException, ...

For new code, prefer using:
    from jeti import JetiRadio, JetiException, ...
    
Or if installed as a package:
    from jeti import JetiRadio, JetiException, ...
"""

import sys
from pathlib import Path

# Add src directory to path for development
_src_path = Path(__file__).resolve().parent / "src"
if str(_src_path) not in sys.path:
    sys.path.insert(0, str(_src_path))

# Re-export everything from the new package location
from jeti import (
    JetiCore,
    JetiRadio,
    JetiRadioEx,
    JetiSpectro,
    JetiSpectroEx,
    JetiException,
    JetiError,
    _get_dll_path,
)

__all__ = [
    'JetiCore',
    'JetiRadio',
    'JetiRadioEx',
    'JetiSpectro',
    'JetiSpectroEx',
    'JetiException',
    'JetiError',
    '_get_dll_path',
]
