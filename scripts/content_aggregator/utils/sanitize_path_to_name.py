import os
from pathlib import Path

def sanitize_path_to_name(path: Path) -> str:
    """Converts a Path object into a URL-friendly string.

    This is used to create a flat file structure in the Quartz content
    directory from a nested source directory structure. It strips a
    prefix from the path to make the names shorter and more readable.

    Args:
        path: The Path object to sanitize.

    Returns:
        A string with path separators replaced by double dashes.
    """
    path_str = str(path)
    
    # As requested, shorten the path by removing the common dev directory prefix.
    prefix = '/Users/luketych/Dev/'
    if path_str.startswith(prefix):
        path_str = path_str[len(prefix):]
        
    return path_str.replace(os.sep, '--')
