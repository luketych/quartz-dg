# Sort Controls UI

## Overview
Frontend UI controls for sorting displayed ratings by various fields. Users can sort results by dtISO, analyst, analystName, tickerSymbol, actionPT, type, and exchange in ascending or descending order.

## Status
⏳ **Pending**

## Implementation Details

### UI Elements
- **Sort Field Dropdown:** Select which field to sort by
- **Sort Order Toggle:** Switch between ascending/descending
- **Alternative:** Clickable table headers for direct sorting

### Frontend Components
- Sort control component (dropdown + order toggle)
- OR: Enhanced table component with sortable headers
- Integration with existing results display

### Milestones

**Milestone 5: Frontend - Sorting Results**
- [ ] **UI Controls**
  - Add dropdowns for sort field and order
  - OR: Implement clickable table headers
  - Visual indicators for current sort state
- [ ] **API Integration/Client-Side Logic**
  - Server-Side Sorting: Re-fetch data with new `sort_by` and `sort_order` parameters
  - Update API calls when sort options change
- [ ] **State Management**
  - Maintain current sort state in Svelte store
  - Persist sort preferences (optional)
  - Re-render data when sort changes

## Technical Specifications

### Sortable Fields
- `dtISO` - Date/time of rating
- `analyst` - Analyst identifier  
- `analystName` - Full analyst name
- `tickerSymbol` - Stock ticker symbol
- `actionPT` - Action price target
- `type` - Rating type
- `exchange` - Stock exchange

### UI Options

**Option 1: Dropdown Controls**
```svelte
<select bind:value={sortBy}>
  <option value="dtISO">Date</option>
  <option value="analyst">Analyst</option>
  <option value="tickerSymbol">Symbol</option>
  <!-- etc -->
</select>

<button on:click={toggleSortOrder}>
  {sortOrder === 'asc' ? '↑' : '↓'}
</button>
```

**Option 2: Clickable Headers**
```svelte
<th on:click={() => handleSort('dtISO')}>
  Date {getSortIcon('dtISO')}
</th>
```

### API Integration
```javascript
function fetchSortedData() {
  const params = {
    sort_by: sortBy,
    sort_order: sortOrder,
    // ... other filters
  };
  return api.get('/ratings', { params });
}
```

## Benefits
- Easy data exploration and analysis
- Find highest/lowest price targets
- Group by analyst or symbol
- Chronological or reverse chronological viewing
- Improved data table usability

## Testing Requirements
- Test sorting by all available fields
- Test ascending and descending order toggles
- Verify sort persistence across filter changes
- Test performance with large datasets
- Ensure sort indicators update correctly
- Mobile responsiveness of sort controls