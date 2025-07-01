import subprocess
from pathlib import Path

from config import get_config

def find_codebases() -> list[Path]:
    """Discovers codebases by searching for directories containing both 'descriptions' and 'viscera' folders.

    This function uses the external 'find' command for robust and efficient
    directory traversal.

    Returns:
        A list of Path objects, each representing a codebase to be processed.
    """
    source_directory, quartz_content_dir = get_config()
    quartz_project_dir = quartz_content_dir.parent.parent

    print(f"\n🔍 Starting codebase discovery in: {source_directory}")
    print(f"   (Excluding the script's own project directory: {quartz_project_dir})")
    print("   Strategy: To find projects with both 'descriptions' and 'viscera', I will do two fast searches and find the overlap.")

    def run_find_and_collect(search_for: str) -> set[str]:
        """Runs the find command and streams results for real-time feedback."""
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
            '-not', '-path', f'{quartz_project_dir}/*'
        ]
        
        found_dirs = set()
        # Using Popen to stream output for real-time feedback
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
                    print(f"       Found candidate: {parent_dir}")
        
        print(f"     -> Found {len(found_dirs)} total potential projects with '{search_for}'.")
        return found_dirs

    description_dirs = run_find_and_collect('descriptions')
    viscera_dirs = run_find_and_collect('viscera')

    # The intersection of these two sets gives us the valid codebase directories
    print("\n   - Calculating final list...")
    valid_codebase_dirs = sorted(list(description_dirs.intersection(viscera_dirs)))
    print(f"✅ Found {len(valid_codebase_dirs)} valid codebases to process.\n")

    return [Path(d) for d in valid_codebase_dirs]
