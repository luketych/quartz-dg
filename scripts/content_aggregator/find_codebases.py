import subprocess
from pathlib import Path

from config import get_config

def find_codebases(env: str = 'prod') -> list[Path]:
    """Discovers codebases by searching for directories containing all specified content types.

    The content types to search for are defined in the .env file.

    This function uses the external 'find' command for robust and efficient
    directory traversal.

    Returns:
        A list of Path objects, each representing a codebase to be processed.
    """
    source_directory, quartz_content_dir, content_types = get_config(env=env)
    quartz_project_dir = quartz_content_dir.parent.parent

    print(f"\n🔍 Starting codebase discovery in: {source_directory}")
    print(f"   (Excluding the script's own project directory: {quartz_project_dir})")
    print(f"   Strategy: Finding projects with all of the following subdirectories: {', '.join(content_types)}")

    def run_find_and_collect(search_for: str) -> set[str]:
        """Runs the find command and collects parent directories."""
        print(f"\n   - Pass: Searching for all '{search_for}' directories...")
        find_cmd = [
            'find', str(source_directory),
            '-type', 'd',
            '-name', search_for,
            '-not', '-path', '*/.git/*',
            '-not', '-path', '*/node_modules/*',
            '-not', '-path', '*/__pycache__/*',
            '-not', '-path', '*/build/*',
            '-not', '-path', '*/dist/*',
            '-not', '-path', '*/.venv/*',
            '-not', '-path', '*/venv/*',
            '-not', '-path', '*/env/*',
        ]
        # In prod, exclude the script's own project directory to avoid recursion.
        if env == 'prod':
            find_cmd.extend(['-not', '-path', f'{quartz_project_dir}/*'])
        
        found_dirs = set()
        process = subprocess.Popen(find_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        stdout_output, stderr_output = process.communicate()

        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, find_cmd, stderr=stderr_output)

        if stdout_output:
            for line in stdout_output.strip().split('\n'):
                path_str = line.strip()
                if path_str:
                    parent_dir = str(Path(path_str).parent)
                    found_dirs.add(parent_dir)
        
        print(f"     -> Found {len(found_dirs)} total potential projects with '{search_for}'.")
        return found_dirs

    if not content_types:
        print("⚠️ No content types specified in configuration. Nothing to do.")
        return []

    # Run find for each content type and collect the results
    all_found_dirs = [run_find_and_collect(content_type) for content_type in content_types]
    
    # Calculate the intersection of all sets to find codebases that have all required directories
    print("\n   - Calculating final list by finding the intersection of all passes...")
    valid_codebase_dirs_set = set.intersection(*all_found_dirs)
    valid_codebase_dirs = sorted(list(valid_codebase_dirs_set))

    print(f"✅ Found {len(valid_codebase_dirs)} valid codebases to process.\n")

    return [Path(d) for d in valid_codebase_dirs]
