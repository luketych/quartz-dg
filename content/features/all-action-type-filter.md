# All Action Type Filter

## Overview
New Action Type: "All" - allows viewing all rating action types at once instead of filtering by a specific type.

![CleanShot 2025-06-12 at 20.17.35@2x](/Users/luketych/Dev/_endeavors/srt-playground/ratings_api/descriptions/attachments/CleanShot 2025-06-12 at 20.17.35@2x.png)

## Status
⏳ **Pending**

## Implementation Details

### Frontend Changes
- **UI Update:** Add "All" option to action type dropdown/filter
- **Filter Logic:** When "All" is selected, include all action types in results
- **API Integration:** Either omit action_type parameter or send special "All" value

### Milestones

**Milestone 4: Frontend - "All" Action Type**
- [ ] **UI Update**
  - Add "All" to action type dropdown
  - Ensure it appears as default or selectable option
- [ ] **Filtering Logic**
  - If "All" is selected, omit `action_type` filter from API call
  - OR: API needs to understand "All" as a special value
  - Ensure correct interaction with other filters (date range, etc.)

## Technical Specifications

### API Request Formats
```
// Option 1: Omit action_type when "All" is selected
GET /ratings?start_date=2025-01-01&end_date=2025-01-31

// Option 2: Send "All" as special value
GET /ratings?action_type=all&start_date=2025-01-01&end_date=2025-01-31
```

### Implementation Approaches
1. **Frontend-only:** Don't send action_type parameter when "All" is selected
2. **Backend support:** Recognize "all" as special value that returns all types
3. **Hybrid:** Frontend omits parameter, backend treats missing action_type as "all"

## Benefits
- Users can view all rating types at once for comprehensive overview
- Reduces need for multiple queries when analyzing overall rating activity
- Improves data exploration capabilities

## Testing Requirements
- Verify "All" option appears in dropdown
- Test that selecting "All" returns ratings of all action types
- Ensure other filters still work when "All" is selected
- Verify switching between "All" and specific action types works correctly