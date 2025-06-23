# Sprint Proposal: SRT API Frontend Enhancement Features

## Executive Summary

This proposal outlines a comprehensive plan to implement three remaining frontend features for the Stock Ratings Tracker (SRT) API:
1. **All Action Type Filter** - View all rating types simultaneously
2. **Sort Controls UI** - Interactive sorting interface
3. **Sorting Support** - Frontend implementation (backend already complete)

## Related Documentation

### Existing Sprint Documents
- **Previous Sprint Proposal**: [`../sprint_proposals/2025_06_22-api_frontend_enhancement.md`](2025_06_22-api_frontend_enhancement.md)
- **Original Implementation Plan**: [`2025_06_12/20_16/proposed_implementation_and_milestones.md`](2025_06_12/20_16/proposed_implementation_and_milestones.md)
- **Milestones Overview**: [`2025_06_12/20_16/milestones.md`](2025_06_12/20_16/milestones.md)

### Feature Specifications
- **All Action Type Filter**: [`all-action-type-filter.md`](all-action-type-filter.md)
- **Sort Controls UI**: [`sort-controls-ui.md`](sort-controls-ui.md)
- **Sorting Support**: [`sorting-support.md`](sorting-support.md)

### Completed Features Reference
- **Backend API Enhancements**: [`completed/backend-api-enhancements.md`](completed/backend-api-enhancements.md)
- **Svelte Frontend Setup**: [`completed/svelte-frontend-setup.md`](completed/svelte-frontend-setup.md)
- **Date Range Support**: [`completed/date-range-support.md`](completed/date-range-support.md)
- **Date Range Picker UI**: [`completed/date-range-picker-ui.md`](completed/date-range-picker-ui.md)
- **Display Local Ratings**: [`completed/display-local-ratings.md`](completed/display-local-ratings.md)

## Current State Analysis

### Completed Features
- ✅ Backend API Enhancements (date ranges, sorting, local-only mode)
- ✅ Svelte Frontend Setup
- ✅ Date Range Support (backend)
- ✅ Date Range Picker UI
- ✅ Display Local Ratings functionality

### Incomplete Features
1. **All Action Type Filter** (Frontend only)
2. **Sort Controls UI** (Frontend only)
3. **Sorting Support UI** (Frontend implementation pending)

## Sprint Structure

### Sprint 1: Foundation & All Action Type Filter (1 week)

**Objectives:**
- Implement "All" action type filter
- Establish component patterns for remaining features
- Set up comprehensive testing framework

**User Stories:**
1. As a user, I want to view all rating types at once for comprehensive analysis
2. As a user, I want the filter to remember my selection between sessions

**Tasks:**
1. Add "All" option to action type dropdown
2. Implement filter logic (omit action_type parameter when "All" selected)
3. Update API integration layer
4. Add unit tests for filter component
5. Add E2E tests for "All" filter functionality

**Git Branch:** `feature/all-action-type-filter`

**Reference Implementation**: See [`all-action-type-filter.md`](all-action-type-filter.md) for detailed specifications

### Sprint 2: Sort Controls UI Implementation (1.5 weeks)

**Objectives:**
- Design and implement sorting UI controls
- Integrate with existing table display
- Ensure mobile responsiveness

**User Stories:**
1. As a user, I want to sort ratings by any column to find patterns
2. As a user, I want visual indicators showing current sort state
3. As a mobile user, I want sorting controls that work on small screens

**Tasks:**
1. Design decision: Dropdown controls vs. clickable headers
2. Implement chosen UI pattern
3. Add sort state management in Svelte stores
4. Create visual indicators (arrows/icons) for sort direction
5. Implement mobile-responsive design
6. Add accessibility features (ARIA labels, keyboard navigation)
7. Unit tests for sort controls
8. Integration tests with API

**Git Branch:** `feature/sort-controls-ui`

**Reference Implementation**: See [`sort-controls-ui.md`](sort-controls-ui.md) for UI specifications

### Sprint 3: Complete Sorting Integration & Polish (1 week)

**Objectives:**
- Complete frontend-backend sorting integration
- Performance optimization
- UI/UX refinements

**User Stories:**
1. As a user, I want sorting to work seamlessly with other filters
2. As a user, I want fast sorting even with large datasets
3. As a user, I want my sort preferences persisted

**Tasks:**
1. Optimize API calls (debouncing, caching)
2. Implement sort preference persistence (localStorage)
3. Add loading states during sort operations
4. Performance testing with large datasets
5. Cross-browser compatibility testing
6. Final UI polish and animations

**Git Branch:** `feature/sorting-integration`

**Reference Implementation**: See [`sorting-support.md`](sorting-support.md) for backend integration details

### Sprint 4: Integration Testing & Documentation (0.5 weeks)

**Objectives:**
- Comprehensive testing of all features together
- Documentation updates
- Deployment preparation

**Tasks:**
1. Full regression testing
2. Update user documentation
3. Update developer documentation (including [`../../CLAUDE.md`](../../CLAUDE.md))
4. Performance benchmarking
5. Security review
6. Deployment checklist completion

**Git Branch:** `feature/final-integration`

## Technical Considerations

### Architecture Decisions

1. **State Management Strategy**
   - Use Svelte stores for filter and sort state
   - Consider implementing a central state store if complexity grows
   - Persist user preferences in localStorage

2. **API Integration Pattern**
   - Maintain existing REST client pattern
   - Implement request debouncing for sort changes
   - Add request cancellation for superseded requests

3. **Component Architecture**
   ```
   FilterControls.svelte
   ├── ActionTypeFilter.svelte
   └── SortControls.svelte
       ├── SortFieldSelector.svelte
       └── SortOrderToggle.svelte
   ```

### Development Flow

1. **Feature Branches**: Each sprint gets its own feature branch
2. **PR Strategy**: Open PRs early for visibility, merge when complete
3. **Testing**: Write tests alongside implementation
4. **Code Review**: Mandatory review before merging to `develop`
5. **Integration**: Merge to `develop` branch, then to `main` after full testing

### Risk Mitigation

| Risk | Impact | Mitigation Strategy |
|------|--------|-------------------|
| Sort performance with large datasets | High | Implement pagination, virtual scrolling |
| Filter state conflicts | Medium | Comprehensive state management testing |
| Mobile responsiveness issues | Medium | Mobile-first design approach |
| Breaking existing functionality | High | Extensive regression testing |
| API compatibility | Low | Backend already supports all needed features |

## Dependencies & Blockers

### Dependencies
- ✅ Backend sorting support (completed - see [`completed/backend-api-enhancements.md`](completed/backend-api-enhancements.md))
- ✅ Svelte frontend setup (completed - see [`completed/svelte-frontend-setup.md`](completed/svelte-frontend-setup.md))
- ✅ API parameter handling (completed)

### Potential Blockers
1. **UI/UX Design Decisions**: Need early decisions on dropdown vs. clickable headers
2. **Performance Requirements**: Define acceptable response times for large datasets
3. **Browser Support**: Clarify minimum browser versions to support

## Testing Strategy

### Unit Testing
- Component-level tests for each new UI element
- Store mutation tests
- API integration layer tests

### Integration Testing
- Filter + Sort combination tests
- Multi-filter interaction tests
- API response handling

### E2E Testing
- Full user workflows with Puppeteer (see existing tests in `viscera/test/client/e2e-mocha/`)
- Cross-browser testing
- Mobile device testing

### Performance Testing
- Load testing with 10k+ records
- Sort operation benchmarks
- Memory usage profiling

## Decisions Required

1. **Sort UI Pattern**
   - Option A: Dropdown + toggle button (more explicit, better for mobile)
   - Option B: Clickable table headers (more intuitive, standard pattern)
   - **Recommendation**: Implement both - clickable headers on desktop, dropdown on mobile

2. **State Persistence**
   - What to persist: sort preferences, filter selections
   - Storage method: localStorage vs. user profile (if auth exists)
   - **Recommendation**: Start with localStorage, migrate to user profile later

3. **Performance Thresholds**
   - Maximum acceptable sort time: 500ms for 1000 records
   - Loading indicator threshold: Show after 200ms
   - **Recommendation**: Implement virtual scrolling if >500 records

## Success Criteria

1. All three features fully functional
2. 90%+ test coverage for new code
3. Performance benchmarks met
4. No regression in existing features
5. Positive user feedback in UAT
6. Documentation complete and accurate

## Timeline Summary

- **Total Duration**: 4 weeks
- **Sprint 1**: Week 1 (All Action Type Filter)
- **Sprint 2**: Weeks 2-3 (Sort Controls UI)
- **Sprint 3**: Week 3-4 (Sorting Integration)
- **Sprint 4**: Week 4 (Testing & Documentation)

## Implementation References

### Code Locations
- **Frontend Components**: `viscera/client/svelte-app/src/components/`
- **API Hooks**: `viscera/server/hooks/`
- **Test Suite**: `viscera/test/`
- **E2E Tests**: `viscera/test/client/e2e-mocha/`

### Key Files to Modify
- **Action Type Filter**: Update `FilterControls.svelte`
- **Sort Controls**: Create new `SortControls.svelte`
- **API Client**: Update API calls in `lib/api.js`
- **Svelte Stores**: Add/update stores in `lib/stores.js`

## Next Steps

1. Review and approve this proposal
2. Clarify any requirements or constraints
3. Make decisions on UI patterns
4. Set up sprint tracking in project management tool
5. Schedule sprint planning session
6. Begin Sprint 1 implementation

## Appendices

### A. Feature Interaction Matrix
| Feature | All Filter | Sort Controls | Date Range | Local Only |
|---------|-----------|--------------|------------|------------|
| All Filter | - | ✓ Works together | ✓ Works together | ✓ Works together |
| Sort Controls | ✓ | - | ✓ Works together | ✓ Works together |
| Date Range | ✓ | ✓ | - | ✓ Works together |
| Local Only | ✓ | ✓ | ✓ | - |

### B. API Endpoint Usage
```javascript
// Example: All features combined
GET /ratings?
  start_date=2025-01-01&
  end_date=2025-01-31&
  sort_by=dtISO&
  sort_order=desc&
  local_only=false
  // Note: action_type omitted when "All" selected
```

### C. Component Hierarchy
```
App.svelte
├── FilterControls.svelte
│   ├── DateRangePicker.svelte ✓
│   ├── ActionTypeFilter.svelte (Sprint 1)
│   └── LocalOnlyToggle.svelte ✓
├── SortControls.svelte (Sprint 2)
│   ├── SortFieldSelector.svelte
│   └── SortOrderToggle.svelte
└── RatingsTable.svelte ✓
    └── RatingsRow.svelte ✓
```

### D. Related Milestone Tracking
See [`2025_06_12/20_16/milestones.md`](2025_06_12/20_16/milestones.md) for the complete milestone breakdown and current progress.