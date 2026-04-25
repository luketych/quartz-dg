import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def get_config(env: str = 'prod') -> tuple[Path, Path, list[str]]:
    """Loads and validates configuration from the appropriate .env file based on the environment.

    Args:
        env (str): The environment to load configuration for (default: 'prod').

    Returns:
        A tuple containing the source directory, Quartz content directory,
        and a list of content types to aggregate.

    Raises:
        SystemExit: If the required environment variables are not set.
    """
    # Determine the path to the .env file, which should be in the same directory
    # as this script's parent folder.
    script_dir = Path(__file__).parent
    dotenv_path = script_dir / f'.env.{env}' if env != 'prod' else script_dir / '.env'

    if not dotenv_path.exists():
        print(f"Error: Configuration file not found at {dotenv_path}")
        print("Please ensure the .env file is correctly set up.")
        exit(1)

    # Load environment variables
    load_dotenv(dotenv_path=dotenv_path)

    source_dir = os.getenv("SOURCE_CODEBASES_DIR")
    quartz_content_dir = os.getenv("QUARTZ_CONTENT_DIRECTORY")
    content_types_str = os.getenv("CONTENT_TYPES_TO_AGGREGATE", "descriptions")

    if not source_dir or not quartz_content_dir:
        print("Error: SOURCE_CODEBASES_DIR and QUARTZ_CONTENT_DIRECTORY must be set in the .env file.", file=sys.stderr)
        sys.exit(1)

    content_types = [item.strip() for item in content_types_str.split(',')]

    return Path(source_dir), Path(quartz_content_dir), content_types
