# Luke's Multi-Site Deployment Guide

This repository has been heavily customized to support a multi-site architecture where multiple, independent websites are built and deployed from this single source repository. This guide explains the unique workflow.

### The Goal: Unique URLs for Each Site

The primary motivation for this setup is to deploy each site to its own unique, clean URL (e.g., `https://luke-quartz.github.io/site-one/`) rather than having them all live under the source repository's URL (`https://luketych.github.io/quartz-dg/...`). To achieve this, each site is deployed to a dedicated repository within the `luke-quartz` GitHub organization.

This works because GitHub Pages serves content from a repository at the URL `https://<organization-name>.github.io/<repository-name>`. By deploying the content for `site-one` to a repository named `luke-quartz/site-one`, its final, public URL automatically becomes `https://luke-quartz.github.io/site-one/`. The workflow handles this entire process, ensuring each site gets its own clean, predictable URL.

### Local Workflow: Adding and Syncing Content

1.  **Add/Edit Content**: All website content lives in subdirectories within the `content/` folder (e.g., `content/site-one`, `content/site-two`). Make your changes here as you normally would.

2.  **Sync Your Changes**: When you are ready to commit your changes, run the following command from this directory (`viscera`):
    ```bash
    npx quartz sync --no-pull
    ```
    This command is a convenient wrapper that will automatically stage your changes, ask you for a commit message, and push the commit to GitHub. The `--no-pull` flag is important as it prevents pulling from the upstream `jackyzha0/quartz` repository, keeping our fork's focus on content.

### The Automated Deployment Process

Pushing your commit to the `feature-unique_urls` branch automatically triggers the powerful `/.github/workflows/deploy.yml` workflow. Here’s what happens:

1.  **Site Detection**: The workflow automatically detects every site folder inside `content/`.
2.  **Matrix Deployment**: It creates a parallel deployment job for each site.
3.  **Repository Provisioning**: For each site, the workflow checks if a corresponding repository exists in the `luke-quartz` organization. If not, it creates it on the fly.
4.  **Build & Deploy**: The workflow builds each site individually and pushes the final static files to the `gh-pages` branch of its dedicated repository.

### Critical Setup: The Personal Access Token (PAT)

This entire automated process is powered by a **Personal Access Token (PAT)** that must be configured correctly.

-   **Secret Name**: `LUKE_QUARTZ_ORG_ADMIN_TOKEN`
-   **Location**: This must be stored as a repository secret in `Settings` > `Secrets and variables` > `Actions`.
-   **Required Scopes**: The token **must** have the following scopes to function:
    -   `repo`: To push the built websites to the deployment repositories.
    -   `admin:org`: To create new repositories automatically when a new site folder is added.

---

# Quartz v4

> “[One] who works with the door open gets all kinds of interruptions, but [they] also occasionally gets clues as to what the world is and what might be important.” — Richard Hamming

Quartz is a set of tools that helps you publish your [digital garden](https://jzhao.xyz/posts/networked-thought) and notes as a website for free.
Quartz v4 features a from-the-ground rewrite focusing on end-user extensibility and ease-of-use.

🔗 Read the documentation and get started: https://quartz.jzhao.xyz/

[Join the Discord Community](https://discord.gg/cRFFHYye7t)

## Sponsors

<p align="center">
  <a href="https://github.com/sponsors/jackyzha0">
    <img src="https://cdn.jsdelivr.net/gh/jackyzha0/jackyzha0/sponsorkit/sponsors.svg" />
  </a>
</p>
