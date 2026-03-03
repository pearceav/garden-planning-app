# Saved Gardens Sidebar

## Context
Users can save garden plans but have no way to view or load them. We need a sidebar showing saved plans that persists across the app.

## Changes

### 1. Create `frontend/src/lib/components/Sidebar.svelte`
- Subscribes to `savedGardens` store, renders list of saved plans
- Each item shows name, seed count, and date
- Click loads the plan by calling `gardenPlan.set(garden.plan)` and `selectedSeeds.set(new Set(garden.seeds))`
- Delete button with `confirm()` dialog (matches existing `prompt()` pattern for save)
- Empty state message when no plans saved
- Styled with existing CSS variables (green theme, `--color-primary`, `--color-bg-alt`, etc.)
- 260px fixed width, scrollable

### 2. Modify `frontend/src/routes/+layout.svelte`
- Import `Sidebar` component
- Wrap `<Sidebar />` + `<main>` in a `.content-area` flex row div
- Adjust `main` styles: remove `width: 100%` and `margin: 0 auto`, keep `flex: 1`
- Add responsive breakpoint at 768px: sidebar stacks above content on small screens

## No changes needed
- `+page.svelte` already reacts to `$gardenPlan` being set — loading a saved plan will render `GardenPlan` automatically
- No new stores or types needed
- No backend changes

## Verification
1. Frontend dev server should hot-reload
2. Save a garden plan → it appears in sidebar
3. Click saved plan → it loads in main area
4. Delete a saved plan → removed from sidebar
5. Refresh page → saved plans persist from localStorage
