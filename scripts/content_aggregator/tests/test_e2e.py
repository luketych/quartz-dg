import unittest
import tempfile
import shutil
from pathlib import Path
import subprocess
import sys
import os
import io
from unittest.mock import patch

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import main

class TestEndToEnd(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory structure for testing."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.source_dir = self.test_dir / 'source'
        self.quartz_dir = self.test_dir / 'quartz_content'

        # Create mock project structures
        for proj in ['proj1', 'nested/project2']:
            proj_path = self.source_dir / proj
            proj_path.mkdir(parents=True, exist_ok=True)
            (proj_path / 'descriptions').mkdir()
            (proj_path / 'viscera').mkdir()
            (proj_path / 'file.txt').touch()

    def tearDown(self):
        """Clean up the temporary directories."""
        shutil.rmtree(self.test_dir)

    @patch('main.get_config')
    @patch('main.find_codebases')
    def test_e2e_flow(self, mock_find_codebases, mock_get_config):
        """Tests the full end-to-end flow of the script."""
        # 1. Setup
        # Mock the configuration to point to our temporary directories
        mock_get_config.return_value = (self.source_dir, self.quartz_dir)

        # Mock discovery to avoid running 'find' in the test
        mock_find_codebases.return_value = [
            Path('proj1'),
            Path('nested/project2')
        ]

        # 2. Execution
        # Run main to generate the script
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        script_content = captured_output.getvalue()
        script_path = self.test_dir / 'aggregate.sh'
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make the script executable and run it
        subprocess.run(['chmod', '+x', str(script_path)], check=True)
        subprocess.run([str(script_path)], check=True)

        # 3. Verification
        # Check that directories were created
        self.assertTrue((self.quartz_dir / 'codebases').is_dir())
        self.assertTrue((self.quartz_dir / 'descriptions').is_dir())
        self.assertTrue((self.quartz_dir / 'visceras').is_dir())

        # Check proj1 files
        self.assertTrue((self.quartz_dir / 'codebases' / 'proj1').is_dir())
        self.assertTrue((self.quartz_dir / 'descriptions' / 'proj1').is_dir())
        self.assertTrue((self.quartz_dir / 'visceras' / 'proj1').is_dir())

        # Check proj2 files (nested and sanitized)
        self.assertTrue((self.quartz_dir / 'codebases' / 'nested--project2').is_dir())
        self.assertTrue((self.quartz_dir / 'descriptions' / 'nested' / 'project2').is_dir())
        self.assertTrue((self.quartz_dir / 'visceras' / 'nested' / 'project2').is_dir())

if __name__ == '__main__':
    unittest.main()
