# Guide for Merging `v4` Updates

This document provides a forward-looking strategy for merging future updates from the original `jackyzha0/quartz/v4` branch into our customized, multi-site `feature-unique_urls` branch.

## Core Principles

1.  **Our Customizations are Isolated**: The vast majority of our changes are confined to the `viscera/.github/workflows` directory and the `viscera/quartz.config.ts` file. The core Quartz application code has not been touched.
2.  **Content is King**: Our `viscera/content` directory is unique to our fork and should always be preserved.
3.  **Upstream is the Source of Truth for Quartz**: The `v4` branch should be considered the canonical source for the Quartz application itself.

## Recommended Merge Process

When a new version or significant update is released on the `v4` branch, the following process is recommended to incorporate the changes:

1.  **Fetch Upstream Changes**:
    -   Ensure you have a remote configured that points to the original `jackyzha0/quartz` repository. If not, add it:
        ```bash
        git remote add upstream https://github.com/jackyzha0/quartz.git
        ```
    -   Fetch the latest changes from the upstream repository:
        ```bash
        git fetch upstream
        ```

2.  **Start from a Clean Branch**:
    -   It's best practice to not merge directly into `feature-unique_urls`. Create a new branch to handle the merge:
        ```bash
        git checkout -b merge-v4-updates feature-unique_urls
        ```

3.  **Perform the Merge**:
    -   Merge the `v4` branch from the upstream remote into your new branch:
        ```bash
        git merge upstream/v4
        ```

4.  **Resolve Conflicts**:
    -   Conflicts are most likely to occur in files that both we and the upstream have modified. Based on our current changes, the most likely candidate is `quartz.config.ts`.
    -   **Conflict Resolution Strategy for `quartz.config.ts`**:
        -   **Accept Upstream Changes First**: Prioritize accepting the changes from the `v4` branch, as they may introduce new configuration options or plugin structures.
        -   **Re-apply Our Customization**: After accepting the upstream changes, manually re-introduce our dynamic `baseUrl` configuration:
            ```typescript
            baseUrl: process.env.BASE_URL,
            ```
    -   **Other Conflicts**: If other files have conflicts (e.g., `package.json` due to new dependencies), carefully review the changes. In most cases, you will want to accept the incoming changes from `v4` to keep the Quartz application up-to-date.

5.  **Test the Merged Branch**:
    -   After resolving conflicts, it is critical to test that the application still works as expected.
    -   Run a local build for one of the sites to ensure Quartz can still process the content:
        ```bash
        npx quartz build --directory viscera/content/site-one
        ```
    -   Commit the resolved merge and push the `merge-v4-updates` branch to your `luketych/quartz-dg` repository. This will trigger the deployment workflow. Verify that it runs successfully.

6.  **Complete the Merge**:
    -   Once you have confirmed that the merged branch builds and deploys correctly, you can merge it back into your main working branch:
        ```bash
        git checkout feature-unique_urls
        git merge merge-v4-updates
        ```

By following this structured approach, you can safely incorporate updates from the core Quartz project while preserving the custom multi-site deployment functionality we have built.
