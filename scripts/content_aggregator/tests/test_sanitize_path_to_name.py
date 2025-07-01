import unittest
from pathlib import Path
import sys
import os

# Add the parent directory to the Python path to allow for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.sanitize_path_to_name import sanitize_path_to_name

class TestSanitizePathToName(unittest.TestCase):

    def test_simple_path(self):
        """Tests a simple, one-level path."""
        path = Path("project_a")
        self.assertEqual(sanitize_path_to_name(path), "project_a")

    def test_nested_path(self):
        """Tests a nested, multi-level path."""
        path = Path("category/project_b")
        self.assertEqual(sanitize_path_to_name(path), "category--project_b")

    def test_path_with_special_chars(self):
        """Tests a path with special characters like spaces and underscores."""
        path = Path("my_category/project with spaces")
        self.assertEqual(sanitize_path_to_name(path), "my_category--project with spaces")

    def test_empty_path(self):
        """Tests an empty path. It should return an empty string."""
        path = Path()
        self.assertEqual(sanitize_path_to_name(path), ".")

if __name__ == '__main__':
    unittest.main()
