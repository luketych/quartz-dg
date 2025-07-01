import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from find_codebases import find_codebases

class TestFindCodebases(unittest.TestCase):

    @patch('find_codebases.get_config')
    @patch('subprocess.run')
    def test_finds_multiple_codebases(self, mock_subprocess_run, mock_get_config):
        """Tests that multiple valid codebases are discovered correctly."""
        mock_get_config.return_value = (Path('/tmp/source'), Path('/tmp/quartz'))

        # Mock the output of the two 'find' commands
        mock_descriptions_output = "/tmp/source/proj1/descriptions\n/tmp/source/proj2/descriptions"
        mock_viscera_output = "/tmp/source/proj1/viscera\n/tmp/source/proj2/viscera"
        
        mock_subprocess_run.side_effect = [
            MagicMock(stdout=mock_descriptions_output, check=True),
            MagicMock(stdout=mock_viscera_output, check=True)
        ]

        result = find_codebases()
        self.assertEqual(result, [Path('proj1'), Path('proj2')])

    @patch('find_codebases.get_config')
    @patch('subprocess.run')
    def test_finds_no_codebases(self, mock_subprocess_run, mock_get_config):
        """Tests that an empty list is returned when no codebases are found."""
        mock_get_config.return_value = (Path('/tmp/source'), Path('/tmp/quartz'))

        mock_subprocess_run.side_effect = [
            MagicMock(stdout='', check=True),
            MagicMock(stdout='', check=True)
        ]

        result = find_codebases()
        self.assertEqual(result, [])

    @patch('find_codebases.get_config')
    @patch('subprocess.run')
    def test_handles_mismatched_dirs(self, mock_subprocess_run, mock_get_config):
        """Tests that only directories with *both* subfolders are included."""
        mock_get_config.return_value = (Path('/tmp/source'), Path('/tmp/quartz'))

        mock_descriptions_output = "/tmp/source/proj1/descriptions\n/tmp/source/proj3/descriptions"
        mock_viscera_output = "/tmp/source/proj2/viscera\n/tmp/source/proj3/viscera"
        
        mock_subprocess_run.side_effect = [
            MagicMock(stdout=mock_descriptions_output, check=True),
            MagicMock(stdout=mock_viscera_output, check=True)
        ]

        result = find_codebases()
        # Only proj3 has both, so it's the only one that should be returned
        self.assertEqual(result, [Path('proj3')])

if __name__ == '__main__':
    unittest.main()
