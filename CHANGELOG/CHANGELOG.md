# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2025-06-26

### Added

- **Dynamic Multi-Site Deployment Workflow**:
  - Created a new GitHub Actions workflow at `viscera/.github/workflows/deploy.yml`.
  - The workflow automatically discovers all subdirectories within the `viscera/content/` folder.
  - It dynamically builds each subdirectory as a separate Quartz site.
  - Deploys all built sites to corresponding subpaths on GitHub Pages (e.g., `/site-one`, `/site-two`).

- **Project Documentation (`descriptions/`)**:
  - `strategies.md`: Outlines the core strategy for managing multiple sites.
  - `pitfalls.md`: Details potential issues and their solutions.
  - `milestones.md`: Provides a clear checklist for implementation.
  - `quartz_flow.md`: Explains the Quartz build process.
  - `plugin_ecosystem.md`: Describes how to use plugins for customization.

- **Content Directories**:
  - Created initial content directories `content/site-one` and `content/site-two` as examples.

### Changed

- **`viscera/quartz.config.ts`**:
  - Modified the configuration to be dynamic.
  - The `baseUrl` is now set using a `BASE_URL` environment variable, allowing for correct link generation when deploying to subpaths.

- **`descriptions/strategies.md`**:
  - Updated the strategy document to include references to the initial research in `multiple_sites_in_content_folder.md`.

### Fixed

- **Project Structure**:
  - Moved the main `content` directory into the `viscera` directory to align with the standard Quartz project layout.
  - Moved the `deploy.yml` workflow to `viscera/.github/workflows/` to match the repository root.
  - Corrected all paths within the `deploy.yml` script to work from its new location.

- **`viscera/quartz.config.ts`**:
  - Modified the configuration to be dynamic.
  - The `baseUrl` is now set using a `BASE_URL` environment variable, allowing for correct link generation when deploying to subpaths.

- **`descriptions/strategies.md`**:
  - Updated the strategy document to include references to the initial research in `multiple_sites_in_content_folder.md`.
