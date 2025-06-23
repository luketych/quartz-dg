# Sorting Support

## Overview
Ability to sort results by various fields including dtISO, analyst, analystName, tickerSymbol, actionPT, type, and exchange.

## Status
✅ **Completed** (Backend implementation)
⏳ **Pending** (Frontend UI controls)

## Implementation Details

### Backend API Enhancements
- **Endpoint Modified:** `/ratings`
- **New Query Parameters:**
  - `sort_by`: Field to sort by (e.g., `dtISO`, `analyst`, `analystName`, `tickerSymbol`, `actionPT`, `type`, `exchange`)
  - `sort_order`: Sort direction (`asc` or `desc`)
- **Database Query Logic:** Updated to order results based on these parameters

### Milestones

**Milestone 1: Backend API Enhancements**
- [✓] **Sorting Support**
  - Modified the API endpoint to accept `sort_by` and `sort_order` query parameters
  - Updated database query logic to order results based on these parameters

**Milestone 5: Frontend - Sorting Results**
- [ ] **UI Controls**
  - Add UI elements for sorting (e.g., dropdowns for sort field and order, or clickable table headers)
- [ ] **API Integration/Client-Side Logic**
  - Server-Side Sorting (Recommended): Re-fetch data from API with new sort parameters
  - Alternative: Client-side sorting for small datasets
- [ ] **State Management**
  - Update frontend state to reflect current sort order and re-render data

## Technical Specifications

### API Request Format
```
GET /ratings?sort_by=dtISO&sort_order=desc
GET /ratings?sort_by=analyst&sort_order=asc
```

### Sortable Fields
- `dtISO` - Date/time of rating
- `analyst` - Analyst identifier
- `analystName` - Full analyst name
- `tickerSymbol` - Stock ticker symbol
- `actionPT` - Action price target
- `type` - Rating type
- `exchange` - Stock exchange

## Implementation Approach
- **Server-Side Sorting (Recommended):** More robust and performant for larger datasets or paginated results
- **Client-Side Sorting (Alternative):** Only for small datasets that are fully loaded

## Testing Requirements
- Test sorting by all available fields
- Test both ascending and descending order
- Verify interactions between sorting and other filters (date range, action type)
- Performance testing for large datasets