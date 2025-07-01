# Testing Strategy for Content Aggregator

This document outlines the testing strategy for the content aggregation script. The goal is to ensure the script is reliable, maintainable, and behaves as expected under various conditions. We will use a combination of unit, integration, and end-to-end (E2E) tests.

## 1. Unit Tests

Unit tests will focus on testing individual functions in isolation to verify their correctness.

### `utils.sanitize_path_to_name`
-   **Test Case**: Simple, one-level path.
-   **Test Case**: Nested, multi-level path.
-   **Test Case**: Path with special characters (e.g., spaces, underscores).
-   **Test Case**: An empty path object (should handle gracefully).

### `config.get_config`
-   **Test Case**: Mock environment variables to ensure they are loaded and returned correctly as `Path` objects.
-   **Test Case**: Mock a missing `SOURCE_DIRECTORY` to verify that the script raises a `SystemExit`.
-   **Test Case**: Mock a missing `QUARTZ_CONTENT_DIRECTORY` to verify that the script raises a `SystemExit`.

### `find_codebases.find_codebases`
-   **Test Case**: Mock `subprocess.run` to simulate the `find` command returning multiple valid codebase paths.
-   **Test Case**: Mock `subprocess.run` to simulate the `find` command returning a single valid codebase path.
-   **Test Case**: Mock `subprocess.run` to simulate the `find` command returning no results.
-   **Test Case**: Mock `subprocess.run` to simulate finding directories that have `descriptions` but not `viscera`, and vice-versa, ensuring they are correctly excluded.

## 2. Integration Tests

Integration tests will verify that different modules work together correctly.

-   **Test Case**: Test the integration between `find_codebases` and `main`. This will involve creating a temporary directory structure with mock projects and running the `main` function. The test will capture the `stdout` and assert that the generated shell script contains the correct commands for the mock projects.
-   **Test Case**: Test the integration of `get_config` with the main logic by setting up a temporary `.env` file and asserting that the paths in the generated script are resolved correctly.

## 3. End-to-End (E2E) Tests

E2E tests will simulate the full workflow of the script to ensure it works from start to finish in a controlled environment.

**E2E Test Workflow:**
1.  **Setup**:
    -   Create a temporary source directory (e.g., `/tmp/source`).
    -   Inside, create a few mock project directories, each containing `descriptions` and `viscera` subfolders and some dummy files.
    -   Create a temporary Quartz content directory (e.g., `/tmp/quartz_content`).
    -   Create a temporary `.env` file pointing to these temporary directories.
2.  **Execution**:
    -   Run the `main.py` script, redirecting its output to a temporary shell script (e.g., `/tmp/aggregate.sh`).
    -   Make the generated script executable (`chmod +x`).
    -   Execute the generated shell script.
3.  **Verification**:
    -   Assert that the temporary Quartz content directory has been correctly populated.
    -   Check for the existence of the `codebases`, `descriptions`, and `visceras` directories.
    -   Verify that the project files have been copied to the correct locations with the correct sanitized names.
4.  **Teardown**:
    -   Remove all temporary directories, files, and the generated shell script to ensure a clean state.
