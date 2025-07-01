import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def get_config() -> tuple[Path, Path]:
    """Loads and validates the source and target directories from the .env file.

    Returns:
        A tuple containing the source and Quartz content directories as Path objects.

    Raises:
        SystemExit: If the required environment variables are not set.
    """
    # Determine the path to the .env file, which should be in the same directory
    # as this script's parent folder.
    dotenv_path = Path(__file__).resolve().parent / '.env'
    load_dotenv(dotenv_path=dotenv_path)

    source_dir = os.getenv("SOURCE_DIRECTORY")
    quartz_content_dir = os.getenv("QUARTZ_CONTENT_DIRECTORY")

    if not source_dir or not quartz_content_dir:
        print("Error: SOURCE_DIRECTORY and QUARTZ_CONTENT_DIRECTORY must be set in the .env file.", file=sys.stderr)
        sys.exit(1)

    return Path(source_dir), Path(quartz_content_dir)
