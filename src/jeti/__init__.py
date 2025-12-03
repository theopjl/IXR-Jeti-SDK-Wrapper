"""
JETI SDK Python Wrapper
Version 1.0.0

A Python wrapper for JETI SDK v4.8.10
Compatible with Python >= 3.11

Classes:
    JetiCore - Core device functionality
    JetiRadio - Radiometric measurements
    JetiRadioEx - Extended radiometric measurements
    JetiSpectro - Spectroscopic measurements
    JetiSpectroEx - Extended spectroscopic measurements

Exceptions:
    JetiException - Main exception class
    JetiError - Error code enumeration
"""

from .wrapper import (
    JetiCore,
    JetiRadio,
    JetiRadioEx,
    JetiSpectro,
    JetiSpectroEx,
    JetiException,
    JetiError,
    _get_dll_path,
)

__version__ = "1.0.0"
__author__ = "JETI SDK Wrapper"
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
