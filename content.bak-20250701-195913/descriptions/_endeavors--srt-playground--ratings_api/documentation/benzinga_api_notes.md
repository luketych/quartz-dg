# 📘 Benzinga API Notes

## Overview

These notes describe key behavioral details, quirks, and design decisions surrounding the use of the Benzinga Ratings Calendar API.

---

## 📌 API Usage

### Endpoint Used

```
https://api.benzinga.com/api/v2.1/calendar/ratings
```

### Required Parameters

* `token`: Your Benzinga API token
* `date_from`: ISO-formatted date string (e.g., `2024-01-01`)
* `date_to`: Same format as `date_from`
* `action`: Filter by rating type (e.g., `upgrades`, `downgrades`, etc.)
* `page`: Integer for pagination
* `pagesize`: Recommended to use `1000`
* `fields`: A long, comma-separated field list to limit response size

### Supported Actions (e.g., for `type` param)

```ts
['Downgrades', 'Maintains', 'Reinstates', 'Reiterates', 'Upgrades',
 'Assumes', 'Initiates Coverage On', 'Terminates Coverage On',
 'Removes', 'Suspends', 'Firm Dissolved']
```

---

## ⚠️ Known Idiosyncrasies & Edge Cases

### 1. **Out-of-Range Ratings Returned**

* Despite setting `date_from` and `date_to`, the API sometimes returns results outside this range.
* **Fix**: All records are post-filtered manually using `moment(...).isBetween()` to ensure correct date range inclusion.

### 2. **Duplicate Data Across Pages**

* Some paginated results are identical to the previous page.
* **Fix**: A hash of `ratings.map(r => r.id)` is tracked across pages. If a page is identical to the last one, pagination halts.

### 3. **Missing Ratings Array**

* Occasionally, `response.data.ratings` is not present or isn't an array.
* **Fix**: This is checked explicitly, and if not valid, the fetch loop exits with a warning.

### 4. **Time Parsing Edge Case**

* Ratings include separate `date` and `time` fields. We manually merge them using:

```js
moment.tz(`${date}T${time}`, 'America/New_York')
```

* This produces both UTC and local time representations (`dtISO`, `dtNY`).

### 5. **Future Date Requests Return Latest Data**

* When `date_from` and `date_to` are set to a future date, the API does not return an empty set or an error.
* Instead, it returns the most recent available ratings data.
* **Behavior**: Tests and data handling logic should account for this by expecting current data, not an empty response, for future-dated queries.

### 6. **Out-of-Bounds Pagination Returns 400 Error**

* When requesting a page number that is out of bounds (e.g., `page=100` when only 5 pages of data exist for the query), the API returns an HTTP 400 Bad Request error.
* The error response typically includes a message like: `{"errors":{"page":["The selected page is invalid."]}}`.
* **Behavior**: Client logic or fetching utilities should be prepared to handle this 400 error gracefully, rather than expecting an empty data array or a different error code for out-of-bounds pagination.

---


## ⚖️ Field Mapping Logic

| Original Field  | Mapped To       |
| --------------- | --------------- |
| action\_company | `type`          |
| action\_pt      | `actionPT`      |
| analyst\_name   | `analystName`   |
| analyst\_firm   | `analyst`       |
| company\_name   | `companyName`   |
| pt\_current     | `ptCurrent`     |
| pt\_prior       | `ptPrior`       |
| rating\_current | `ratingCurrent` |
| rating\_prior   | `ratingPrior`   |
| ticker          | `tickerSymbol`  |
| time            | `timeNY`        |

Extra fields include: `dtISO`, `dtNY`, `fetchedByEventTicker`, and `source: 'benzinga'`.

---

## ✅ Data Validation & Cleanup

* All fetched records are filtered by date range and deduplicated using `${ticker}_${dtISO}` key.
* Output is returned in `ctx.data`, ready for use in FeathersJS hooks or service layers.

---

## ⚙️ Design Goals

* Ensure only accurate, in-range data is returned.
* Avoid repeated or infinite loops due to repeated pages.
* Support clean integration with FeathersJS context pipeline.
* Provide detailed logging and error context for retry/resilience.

---

## 🔗 TODO / Future Improvements

* Add retry/backoff logic on rate-limiting errors (e.g., HTTP 429)
* Support multiple tokens for rotation if rate limits are hit
* Cache common action types for high-volume days (e.g., earnings season)
