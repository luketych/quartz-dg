# Migration Guide: From Quartz `v4` to Luke's Multi-Site Version

This document is a comprehensive guide for anyone familiar with the original `jackyzha0/quartz/v4` branch. It explains the architectural differences, new workflows, and setup requirements for this customized, multi-site version.

## 1. High-Level Goal: What's Different?

The standard Quartz `v4` setup is designed to publish a single website from a single repository. This fork has been fundamentally re-architected to **build and deploy multiple, independent websites from this single source repository**.

-   **v4 URL**: `https://<your-name>.github.io/<source-repo-name>`
-   **Our URL**: `https://<org-name>.github.io/<site-name>`

This is achieved by deploying each site to its own dedicated repository within a separate GitHub organization.

## 2. Architectural and Structural Changes

-   **Git Repository Root**: The Git repository no longer lives at the top level. The new root is the `viscera/` directory. All `git` commands should be run from here.
-   **Content Folder**: The `content/` directory now contains subdirectories, where each subdirectory is a complete, independent Quartz site (e.g., `content/site-one`, `content/site-two`).
-   **Root Index Page**: A special `content/index.md` file exists to create a main landing page for the entire organization at `https://<org-name>.github.io/`.

## 3. The Automated Deployment Workflow

All automation is handled by a single, powerful GitHub Actions workflow located at `viscera/.github/workflows/deploy.yml`. Pushing to the `feature-unique_urls` branch triggers this workflow.

It consists of three main jobs:

1.  **`list-sites`**: This job runs first. It scans the `content/` directory and generates a list (a "matrix") of all the site subdirectories it finds.

2.  **`deploy-root`**: This job runs in parallel with the site deployments. It handles the special case of the main `index.md` file, building it and deploying it to the `main` branch of the `luke-quartz/luke-quartz.github.io` repository.

3.  **`deploy` (Matrix Job)**: This job uses the matrix from `list-sites` to run a separate, parallel deployment for **each site**.
    -   **Just-in-Time Provisioning**: It checks if a repository for the site exists in the `luke-quartz` organization. If not, it creates it automatically using the GitHub CLI.
    -   **Dynamic Build**: It runs `npx quartz build` pointing specifically to that site's content directory (e.g., `content/site-one`).
    -   **External Deployment**: It uses the `peaceiris/actions-gh-pages` action to push the built site to the `gh-pages` branch of the correct external repository (e.g., `luke-quartz/site-one`).

## 4. Key Configuration Change

To ensure links and assets work correctly on each deployed site, the `baseUrl` in `viscera/quartz.config.ts` was made dynamic:

```typescript
// ...
baseUrl: process.env.BASE_URL,
// ...
```

The workflow is responsible for setting the `BASE_URL` environment variable to the full, correct URL for each build job.

## 5. How to Use This Fork

### Adding Content

1.  **Add a new site**: Simply create a new folder in `content/`.
2.  **Add/edit content**: Make your changes inside the appropriate site folder.
3.  **Commit and push**: From the `viscera/` directory, run the command:
    ```bash
    npx quartz sync --no-pull
    ```
    The `--no-pull` flag is important to prevent accidental merges from the original upstream repository. This command will stage, commit, and push your changes, triggering the deployment workflow.

### Required First-Time Setup

To use this fork yourself, you would need to:

1.  Create a new, empty GitHub organization to hold the deployed sites.
2.  Create a **Personal Access Token (PAT)** with the `repo` and `admin:org` scopes.
3.  In your fork of this repository, go to `Settings` > `Secrets and variables` > `Actions` and create a new repository secret named `LUKE_QUARTZ_ORG_ADMIN_TOKEN` with the value of your PAT.
4.  Update the organization name (`luke-quartz`) in the `deploy.yml` workflow to your new organization's name.

## 6. Merging Updates from `v4`

This fork is designed to make merging future updates from the original `v4` branch as painless as possible. For detailed instructions, please see the dedicated guide at `CHANGELOG/04_MERGING_STRATEGY.md`.
