Move the following functions from index.js to separate files under the hooks directory:
    generateHash()
    checkHashDoesntExist()
    absorbConsoleErrors()
    _getFlags()
    _setHardFlags()

For example, generateHash() will become hooks/generateHash.js

---

Change the names of the following functions:

in hooks/index.js:
    _getFlags() to getFlags()
    _setHardFlags() to setHardFlags()

in hooks/fetchRatings.js:
    getDateRange() to _getDateRange()

---

Inside of the server/hooks folder create a new folder called utilFunctions and move all the functions from index.js into it. Also move fetchRatings.js into this folder.

Why:
    It makes more sense to me to have all the utility functions in a single folder, rather than shown as hooks, which is confusing. As a compromise, and in order to keep things inline with feathersjs conventions, we will create a new folder called utilFunctions and move all the functions from index.js into it. 

---

Create a new folder (server/errors) and move all of the error functions into that folder.
For example, after this refactor we will have server/errors/index.js and server/errors/uniqueConstraintError.js. index.js will simply act as the entry point for all error functions, exporting them to the rest of the application. 

---

Remove tradeSignals:
  - model
  - service
  - etc

Why:
    In the past I was refactoring the code to replace ratings with tradeSignals. But it makes more sense to move back to ratings.

---

Move server/util.js outside to a separate, new folder called viscera/util.

Why:
    This makes the separation more clear, and it makes sense if we want to shed useful utility functions in the future and generalize them, so that they can be added to a shared library.

---

Move server/app.hooks.js to hooks/ folder.

Why:
    I don't like everything spread out in the main folder, and all of the redundancies everywhere. I like things that have a clearly defined purpose for existing to be grouped together and consistent, so that it's super simple to understand the structure and layout of the codebase.

---

Move services/ratings/hooks.js to server/hooks/ratings.js

---

Move findExistingRatings() to hook new hookFunctions folder

--- 

Move conditionallyFetchAndCreateRatings() to the new hookFunctions folder: hooks/hookFunctions/conditionallyFetchAndCreateRatings.js
    Also move its private functions into the new file conditionallyFetchAndCreateRatings.js:
        _fetchAndPrepareBenzingaRatings()
        _identifyAndCreateNewRatings()
        _finalizeResponse()
    
---

Can we delete isQueryEmpty()? Or is it still needed?

---

Write docstrings for all hookFunctions, including the private functions.

---