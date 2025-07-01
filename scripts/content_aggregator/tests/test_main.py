import unittest
from unittest.mock import patch
from pathlib import Path
import sys
import os
import io

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import main

class TestMainIntegration(unittest.TestCase):

    @patch('main.get_config')
    @patch('main.find_codebases')
    def test_script_generation(self, mock_find_codebases, mock_get_config):
        """Tests that the main script generates the correct shell commands."""
        # 1. Setup
        # Mock the configuration to point to temporary directories
        source_dir = Path('/tmp/fake_source')
        quartz_dir = Path('/tmp/fake_quartz')
        mock_get_config.return_value = (source_dir, quartz_dir)

        # Mock the discovered codebases
        mock_find_codebases.return_value = [
            Path('project1'),
            Path('nested/project2')
        ]

        # 2. Execution
        # Redirect stdout to capture the script's output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        main()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # 3. Verification
        output = captured_output.getvalue()

        # Check for cleaning commands
        self.assertIn(f"find '{quartz_dir / 'codebases'}' -mindepth 1 -delete", output)
        self.assertIn(f"find '{quartz_dir / 'descriptions'}' -mindepth 1 -delete", output)
        self.assertIn(f"find '{quartz_dir / 'visceras'}' -mindepth 1 -delete", output)

        # Check for project1 commands
        self.assertIn("echo 'Processing project1'", output)
        self.assertIn(f"cp -R '{source_dir / 'project1' / 'descriptions'}' '{quartz_dir / 'descriptions' / 'project1'}'", output)
        self.assertIn(f"cp -R '{source_dir / 'project1' / 'viscera'}' '{quartz_dir / 'visceras' / 'project1'}'", output)
        self.assertIn(f"cp -R '{source_dir / 'project1'}' '{quartz_dir / 'codebases' / 'project1'}'", output)

        # Check for project2 commands (with sanitized name and nested paths)
        self.assertIn("echo 'Processing nested/project2'", output)
        self.assertIn(f"cp -R '{source_dir / 'nested/project2' / 'descriptions'}' '{quartz_dir / 'descriptions' / 'nested/project2'}'", output)
        self.assertIn(f"cp -R '{source_dir / 'nested/project2' / 'viscera'}' '{quartz_dir / 'visceras' / 'nested/project2'}'", output)
        self.assertIn(f"cp -R '{source_dir / 'nested/project2'}' '{quartz_dir / 'codebases' / 'nested--project2'}'", output)

if __name__ == '__main__':
    unittest.main()
