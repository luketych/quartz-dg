# Implementing the Root `index.md` Deployment

This document details the steps, errors, and solutions involved in implementing the deployment for the main `content/index.md` file to the organization's root URL (`https://luke-quartz.github.io/`).

### 1. The Goal

The objective was to have a central landing page for the entire site collection, served from the root of the organization's GitHub Pages URL, in addition to the individual sites in their subdirectories.

### 2. Initial Implementation: A New Workflow Job

To handle this special case, a new, independent job named `deploy-root` was added to the `.github/workflows/deploy.yml` file.

-   **Logic**: This job was designed to run in parallel with the existing site deployments. It would isolate the `content/index.md` file, build it separately, and deploy the result to the special `luke-quartz/luke-quartz.github.io` repository.
-   **Key Difference**: Unlike the other sites which deploy to a `gh-pages` branch, organization root pages must be deployed to the `main` branch.

### 3. Error 1: `SyntaxError: Cannot use import statement outside a module`

-   **Symptom**: The new `deploy-root` job failed during the build step with a Node.js module error.
-   **Cause**: We had neglected to install the project's dependencies in the workflow. The `npx quartz build` command was failing because it couldn't find the required packages.
-   **Solution**: An `npm install` step was added to both the `deploy-root` and `deploy` jobs to ensure a complete and stable build environment.

### 4. Error 2: `404 Not Found` on the Live Site

-   **Symptom**: After the workflow succeeded, the URL `https://luke-quartz.github.io/` returned a 404 error. The deployment repository was empty.
-   **Cause**: The `content/index.md` file on our local disk was empty. When Quartz was asked to build an empty file, it correctly produced no output. The deployment action therefore had nothing to push.
-   **Solution**: We added a title and placeholder content to the `content/index.md` file. This involved first deleting the empty file and then recreating it with content, as our editing tools had issues with empty files.

### 5. Error 3: `fatal: A branch named 'main' already exists`

-   **Symptom**: The `deploy-root` job failed again during the deployment step.
-   **Cause**: The deployment action (`peaceiris/actions-gh-pages`) was trying to create the `main` branch, but it already existed from the previous (empty) deployment attempt. This created a history conflict.
-   **Solution**: We added `force_orphan: true` to the deployment step's configuration. This is a standard practice for deployment branches, as it creates a fresh, clean commit history every time, ignoring previous builds.

### 6. Error 4: `Failed to emit from plugin '404Page': Invalid URL`

-   **Symptom**: The build step started failing again, this time with an error from a Quartz plugin.
-   **Cause**: The plugin that generates the 404 page requires a full, valid URL for the `baseUrl` configuration. We were providing an empty string for the root page and just the site name for the others (e.g., `site-one`), neither of which is a valid URL.
-   **Solution**: We updated the `BASE_URL` environment variable in all build steps to be the full, absolute URL (e.g., `https://luke-quartz.github.io` and `https://luke-quartz.github.io/site-one`). This satisfied the plugin and ensured all links would be generated correctly.

After fixing this final issue, the workflow completed successfully, and the root index page was deployed as intended.
