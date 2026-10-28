"""
Test runner using Python standard library unittest.
"""
import sys
import os
import unittest

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.test_engines import (
    test_inr_formatting,
    test_financial_calculations,
    test_render_url_generation,
    test_weather_protocols,
    test_sample_image_generators,
    test_demo_schemas,
    test_chat_fallbacks
)

class EngineTests(unittest.TestCase):
    def test_all_modules(self):
        test_inr_formatting()
        test_financial_calculations()
        test_render_url_generation()
        test_weather_protocols()
        test_demo_schemas()
        test_chat_fallbacks()

    def test_image_generators(self):
        try:
            test_sample_image_generators()
        except ImportError:
            print("Pillow not installed in active environment, skipping image generator test")

if __name__ == "__main__":
    unittest.main()
