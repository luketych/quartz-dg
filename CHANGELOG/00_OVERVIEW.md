# Overview of Multi-Site Deployment Changes

This document provides a high-level overview of the significant architectural changes implemented to transition the Quartz repository from a single-site setup (as in the `v4` branch) to a scalable, multi-site deployment system.

## Core Objective

The primary goal was to host multiple, independent Quartz sites from a single source repository, with each site having its own unique, clean URL (e.g., `https://<org-name>.github.io/site-one/`) instead of being tied to the source repository's name.

## Key Architectural Changes

1.  **Multi-Site Content Structure**:
    *   The original `content` directory has been moved to `viscera/content`.
    *   Each independent website now resides in its own subdirectory within `viscera/content` (e.g., `viscera/content/site-one`, `viscera/content/site-two`).

2.  **Deployment to an External Organization**:
    *   To achieve unique URLs, each site is deployed to its own dedicated, empty repository within a separate GitHub organization (`luke-quartz` in our case).
    *   This decouples the deployment URL from the source code's repository name (`luketych/quartz-dg`).

3.  **Unified and Automated Workflow (`deploy.yml`)**:
    *   A single, powerful GitHub Actions workflow located at `viscera/.github/workflows/deploy.yml` now manages the entire process.
    *   The workflow uses a **matrix strategy** to automatically detect every site folder within `viscera/content`.
    *   For each site found, it runs a parallel job that performs all necessary steps.

4.  **Just-in-Time Repository Provisioning**:
    *   The workflow automatically checks if a target repository exists in the `luke-quartz` organization for each site.
    *   If the repository does not exist, the workflow creates it on the fly using the GitHub CLI (`gh`). This completely automates the setup for new sites.

5.  **Dynamic Configuration**:
    *   The `viscera/quartz.config.ts` file was modified to dynamically set the `baseUrl` for each site at build time using an environment variable. This ensures that links and assets within each deployed site resolve correctly to their unique URLs.

## How it Works: A Quick Summary

When changes are pushed to the `feature-unique_urls` branch:

1.  The `deploy.yml` workflow triggers.
2.  It lists all folders inside `viscera/content` (e.g., `site-one`, `site-two`).
3.  It starts a separate, parallel deployment job for each site.
4.  Each job first ensures the target repository (`luke-quartz/site-one`) exists, creating it if necessary.
5.  It then builds the Quartz site from the corresponding content folder (`viscera/content/site-one`).
6.  Finally, it pushes the built website to the `gh-pages` branch of the target repository.

This new architecture provides a highly scalable and maintainable system for managing an arbitrary number of websites from a single, unified codebase.
