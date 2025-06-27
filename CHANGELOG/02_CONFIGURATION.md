# Configuration and Setup Guide

This document covers the necessary configuration changes and the one-time setup required to use the new multi-site deployment system.

## 1. GitHub Personal Access Token (PAT)

The entire automated system relies on a GitHub Personal Access Token (PAT) with the correct permissions.

-   **Purpose**: The token is used by the GitHub Actions workflow to:
    1.  Create new repositories in your target organization (`luke-quartz`).
    2.  Push the built websites to those repositories.
-   **Required Scopes**: The PAT must have the `repo` scope (for pushing code) and the `admin:org` scope (for creating repositories).
-   **Creation**: The token must be created by a user who is an **owner** of the target GitHub organization.

### Storing the Token as a Secret

Once created, the PAT must be stored as a repository secret in the source repository (`luketych/quartz-dg`).

-   **Secret Name**: `LUKE_QUARTZ_ORG_ADMIN_TOKEN`
-   **Location**: In your `luketych/quartz-dg` repository, go to `Settings` > `Secrets and variables` > `Actions` and create a new repository secret with this name and the token as its value.

**Security Note**: This token is extremely powerful. Treat it like a password and do not expose it publicly.

## 2. Dynamic `baseUrl` in `quartz.config.ts`

To ensure that links, images, and other assets work correctly on each independently deployed site, the `baseUrl` in Quartz's configuration must be set dynamically.

-   **File Modified**: `viscera/quartz.config.ts`
-   **Change**: The `baseUrl` property was changed from a hardcoded value to one that is read from an environment variable.

```typescript
// inside viscera/quartz.config.ts

const config: QuartzConfig = {
  configuration: {
    // ... other properties
    baseUrl: process.env.BASE_URL,
    // ... other properties
  },
  // ... plugins
}
```

### How it's Used in the Workflow

The `deploy.yml` workflow sets this `BASE_URL` environment variable for each site's build step.

-   The `Build Site` step in the workflow includes:
    ```yaml
    env:
      BASE_URL: ${{ matrix.site }}
    run: npx quartz build --directory "content/${{ matrix.site }}"
    ```
-   This means when Quartz builds `site-one`, the `baseUrl` is automatically set to `site-one`, resulting in correct paths like `/site-one/path/to/page`.

## 3. How to Add a New Site

With this new system, adding a new website is incredibly simple:

1.  **Create a new folder** inside the `viscera/content` directory (e.g., `viscera/content/new-cool-site`).
2.  Add your Markdown files and other content inside this new folder.
3.  Commit and push the changes to the `feature-unique_urls` branch.

That's it. The workflow will automatically detect the new folder, create the `luke-quartz/new-cool-site` repository for you, and deploy the new site.
