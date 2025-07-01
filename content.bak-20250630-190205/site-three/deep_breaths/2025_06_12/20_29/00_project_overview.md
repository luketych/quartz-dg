# Project Overview: FeathersJS Ratings API

**Date:** 2025-06-12

## Goal

The primary goal of this project is to develop a FeathersJS API service (`ratings_api`) that manages financial ratings data. This service is responsible for:
1.  Fetching ratings data from an external source (Benzinga API).
2.  Storing and managing these ratings in a local database (likely Sequelize-based).
3.  Providing CRUD-like operations for ratings, with specific logic for conditional fetching and creation to avoid duplicates.

## Technology Stack

*   **Backend Framework:** FeathersJS (v5, using ESM modules)
*   **Database:** SQL-based (interactions suggest Sequelize or a similar ORM)
*   **Testing:** Mocha, Chai (implied by `assert`), Sinon (for mocks/stubs)
*   **HTTP Client:** Axios (for making requests to Benzinga)
*   **Environment Management:** `dotenv` for environment variables.
*   **Utilities:** `object-hash` for generating hashes, `uuid` for unique IDs.

## Core Functionality Under Development/Debug

The current focus is on the `ratings` service, specifically its `find` method and associated hooks. The hooks are designed to:
*   Conditionally fetch new ratings from Benzinga if a specific query parameter (`perform_fetch: 'true'`) is provided.
*   Prevent duplicate entries by checking existing hashes.
*   Handle various scenarios like API errors from Benzinga, missing API tokens, and empty responses.
*   Allow querying of existing ratings from the local database.
