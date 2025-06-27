# Debugging and Troubleshooting Journey

This document chronicles the series of errors encountered and fixes implemented while developing the multi-site deployment workflow. Understanding this journey is crucial for future debugging and appreciating the nuances of the final solution.

### 1. Initial Problem: Workflows Not Appearing in GitHub Actions

-   **Symptom**: After creating the `provision-repos.yml` workflow, it would not show up in the GitHub Actions UI.
-   **Initial Hypothesis**: A simple syntax error like a missing `shell: bash`.
-   **Investigation**: This was incorrect. We then suspected incorrect file paths (`viscera/content` vs. `content`), which was a real issue but not the root cause.
-   **Root Cause**: GitHub's workflow parser has a security model that requires jobs performing sensitive actions to explicitly declare their required permissions. Our custom `run` script that called `gh repo create` was deemed sensitive.
-   **The Loop of Incorrect Fixes**:
    1.  We tried adding `permissions: contents: read` at the job level. Failed.
    2.  We moved it to the top level. Failed.
    3.  We tried `contents: write`. Failed.
    4.  We incorrectly tried `organizations: write`, which is not a valid permission for this context and caused a new linting error.
-   **Final Solution**: We **eliminated the separate `provision-repos.yml` file entirely**. We merged the logic into the `deploy.yml` workflow, which was already trusted by the parser. This simplified the design and bypassed the complex permission issue with the separate file.

### 2. Workflow Error: `fromJson` Could Not Parse Matrix

-   **Symptom**: The `deploy` job failed immediately with an error: `Error from function 'fromJson': Unexpected symbol: '}'`.
-   **Root Cause**: The shell script in the `set-matrix` step was not robust. The command `echo $sites | jq ...` was not correctly handling the list of site names, leading to malformed JSON being passed to the next job.
-   **Solution**: The script was rewritten to be more robust, using a safer `jq` pipeline to guarantee the creation of a valid JSON array: `json_array=$(echo "$sites" | jq -R . | jq -s -c .)`.

### 3. Workflow Error: `Unable to resolve action ... v4 done`

-   **Symptom**: The `deploy` job failed with an error message indicating it could not find version `v4 done` of the `peaceiris/actions-gh-pages` action.
-   **Root Cause**: A simple but critical typo. A stray word `done` had been accidentally left in the YAML file on the line after the action's version number.
-   **Solution**: Removed the stray word. This also revealed that the entire configuration block for the action was missing.

### 4. Git Error: `index.lock file exists`

-   **Symptom**: When trying to commit changes from the terminal, Git returned a fatal error about a `.git/index.lock` file existing.
-   **Root Cause**: A previous Git process had been interrupted or crashed, leaving the lock file behind. This is a safety mechanism to prevent repository corruption.
-   **Solution**: Manually remove the lock file with `rm .git/index.lock`, which allows subsequent Git commands to proceed.

This debugging journey highlights the importance of understanding GitHub Actions' permission model, ensuring robust shell scripting for data handoffs between jobs, and paying close attention to YAML syntax.
