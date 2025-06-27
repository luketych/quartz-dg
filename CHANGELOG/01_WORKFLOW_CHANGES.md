# Detailed Workflow Changes: `deploy.yml`

This document details the implementation of the `viscera/.github/workflows/deploy.yml` file, which is the engine of the new multi-site deployment system.

## Trigger and Permissions

-   **Triggers**: The workflow runs on any `push` to the `feature-unique_urls` branch and can also be manually triggered (`workflow_dispatch`).
-   **Permissions**: The workflow uses job-level permissions for security and correctness:
    -   The `list-sites` job has `contents: read` to check out the repository code.
    -   The `deploy` job has `contents: write` to allow the `peaceiris/actions-gh-pages` action to push the built site to the external repositories.

## Job 1: `list-sites`

This job acts as a setup step to determine which sites need to be deployed.

1.  **Checkout**: Checks out the repository's code.
2.  **Set Matrix (`set-matrix` step)**:
    -   It runs a shell script that lists all subdirectories within the `content` folder.
    -   It then uses `jq` to format this list into a JSON array.
    -   This JSON array (e.g., `{"site":["site-one","site-two"]}`) is passed as an `output` to the next job.

## Job 2: `deploy`

This is the main job, and it uses a **matrix strategy** based on the output from the `list-sites` job. This means all the steps within this job will run in parallel for each site identified.

-   `needs: list-sites`: Ensures this job only starts after `list-sites` has successfully completed.
-   `strategy: matrix: ${{ fromJson(needs.list-sites.outputs.matrix) }}`: This line reads the JSON output from the previous job and configures the matrix. For each element in the `site` array, a parallel job instance is created, with the site name available as `${{ matrix.site }}`.

### Key Steps within the `deploy` Job

1.  **Checkout & Setup Node**: Standard steps to check out the code and set up the correct Node.js environment (v22).

2.  **Provision Repository**: This is a critical step for automation.
    -   **Environment**: It uses the `LUKE_QUARTZ_ORG_ADMIN_TOKEN` secret and the `luke-quartz` organization name.
    -   **Logic**: It runs a shell script that uses the GitHub CLI (`gh`) to check if a repository named `${{ matrix.site }}` exists in the target organization.
    -   If the repository does **not** exist, it runs `gh repo create` to create it on the fly. This makes adding a new site as simple as adding a new folder to the `content` directory.

3.  **Build Site**: 
    -   It runs `npx quartz build --directory "content/${{ matrix.site }}"`.
    -   This command tells Quartz to perform a build, but to only consider the files within the specific site's subfolder (e.g., `content/site-one`). The output is placed in the `public` directory.

4.  **Deploy to External Repository**:
    -   This step uses the `peaceiris/actions-gh-pages@v4` action, which is specifically designed for this purpose.
    -   **`personal_token`**: It is authenticated using your `LUKE_QUARTZ_ORG_ADMIN_TOKEN` secret.
    -   **`external_repository`**: This crucial parameter tells the action to push to a repository outside of the one the workflow is running in. It is set to `luke-quartz/${{ matrix.site }}`.
    -   **`publish_dir`**: Specifies that the contents of the `./public` directory (where the site was just built) should be deployed.
    -   **`publish_branch`**: Deploys to the `gh-pages` branch of the target repository, which is the standard for GitHub Pages sites.
