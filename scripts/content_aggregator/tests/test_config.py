import unittest
from unittest.mock import patch
from pathlib import Path
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import get_config

class TestGetConfig(unittest.TestCase):

    @patch('os.getenv')
    def test_config_loaded_successfully(self, mock_getenv):
        """Tests that the config is loaded correctly when env vars are set."""
        # Configure the mock to return specific values
        mock_getenv.side_effect = lambda key: {
            "SOURCE_DIRECTORY": "/tmp/source",
            "QUARTZ_CONTENT_DIRECTORY": "/tmp/quartz"
        }.get(key)

        source_dir, quartz_dir = get_config()
        self.assertEqual(source_dir, Path("/tmp/source"))
        self.assertEqual(quartz_dir, Path("/tmp/quartz"))

    @patch('os.getenv')
    def test_missing_source_directory(self, mock_getenv):
        """Tests that the script exits if SOURCE_DIRECTORY is not set."""
        mock_getenv.side_effect = lambda key: {
            "QUARTZ_CONTENT_DIRECTORY": "/tmp/quartz"
        }.get(key)

        with self.assertRaises(SystemExit) as cm:
            get_config()
        self.assertEqual(cm.exception.code, 1)

    @patch('os.getenv')
    def test_missing_quartz_content_directory(self, mock_getenv):
        """Tests that the script exits if QUARTZ_CONTENT_DIRECTORY is not set."""
        mock_getenv.side_effect = lambda key: {
            "SOURCE_DIRECTORY": "/tmp/source"
        }.get(key)

        with self.assertRaises(SystemExit) as cm:
            get_config()
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
