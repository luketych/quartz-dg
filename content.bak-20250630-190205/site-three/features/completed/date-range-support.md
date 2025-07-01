# Date Range Support

## Overview
Currently we can only select single dates. This feature will give us options to both select a single date, or retrieve all ratings within a range of dates.

## Status
✅ **Completed** (Backend implementation)

## Implementation Details

### Backend API Enhancements
- **Endpoint Modified:** `/ratings`
- **New Query Parameters:**
  - `start_date`: Beginning of date range
  - `end_date`: End of date range
- **Database Query Logic:** Updated to filter ratings within the specified date range

### Milestones

**Milestone 1: Backend API Enhancements**
- [✓] **Date Range Support**
  - Modified the relevant API endpoint to accept `start_date` and `end_date` query parameters
  - Updated the database query logic to filter ratings within the specified date range

**Milestone 2: Frontend UI Enhancements for Date Range Selection**
- [✓] **Date Input UI**
  - Added input fields for selecting start and end dates
- [✓] **API Integration**
  - Modified the API call logic to pass the selected date(s) or range to the backend

## Technical Specifications

### API Request Format
```
GET /ratings?start_date=2025-01-01&end_date=2025-01-31
```

### Database Query
The backend now supports Sequelize date range queries using the `dtISO` field to filter results within the specified range.

## Testing Requirements
- Unit tests for date range parsing
- Integration tests for API endpoint with various date range scenarios
- Edge cases: same date for start/end, invalid date formats, future dates