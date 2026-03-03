<script lang="ts">
	import { savedGardens } from '$lib/stores/savedGardens';
	import { gardenPlan, activeSavedGardenId } from '$lib/stores/gardenPlan';
	import { selectedSeeds } from '$lib/stores/selectedSeeds';
	import type { SavedGarden } from '$lib/types';

	function loadGarden(garden: SavedGarden) {
		selectedSeeds.set(new Set(garden.seeds));
		gardenPlan.set(garden.plan);
		activeSavedGardenId.set(garden.id);
	}

	function formatDate(isoString: string): string {
		return new Date(isoString).toLocaleDateString(undefined, {
			month: 'short',
			day: 'numeric',
			year: 'numeric'
		});
	}
</script>

<aside class="sidebar">
	<h2>Saved Gardens</h2>

	{#if $savedGardens.length === 0}
		<p class="empty-message">No saved plans yet. Generate a plan and save it to see it here.</p>
	{:else}
		<ul class="garden-list">
			{#each $savedGardens as garden (garden.id)}
				<li>
					<button
						class="garden-item"
						class:active={$activeSavedGardenId === garden.id}
						onclick={() => loadGarden(garden)}
					>
						<span class="garden-name">{garden.name}</span>
						<span class="garden-meta">
							{garden.seeds.length} seeds &middot; {formatDate(garden.createdAt)}
						</span>
					</button>
				</li>
			{/each}
		</ul>
	{/if}
</aside>

<style>
	.sidebar {
		width: 260px;
		min-width: 260px;
		background: white;
		border-right: 1px solid var(--color-border);
		padding: 1.25rem;
		overflow-y: auto;
	}

	h2 {
		font-size: 1rem;
		color: var(--color-primary-dark);
		margin: 0 0 1rem;
		padding-bottom: 0.5rem;
		border-bottom: 2px solid var(--color-primary-light);
	}

	.empty-message {
		color: var(--color-text-muted);
		font-size: 0.85rem;
		line-height: 1.4;
	}

	.garden-list {
		list-style: none;
		padding: 0;
		margin: 0;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.garden-item {
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 0.15rem;
		padding: 0.6rem 0.75rem;
		background: var(--color-bg-alt);
		border: 1px solid transparent;
		border-radius: 8px;
		cursor: pointer;
		text-align: left;
		transition: all 0.15s;
	}

	.garden-item:hover {
		border-color: var(--color-primary);
		background: var(--color-primary-light);
	}

	.garden-item.active {
		border-color: var(--color-primary);
		background: var(--color-primary-light);
	}

	.garden-name {
		font-weight: 600;
		font-size: 0.9rem;
		color: var(--color-text);
	}

	.garden-meta {
		font-size: 0.75rem;
		color: var(--color-text-muted);
	}

	@media (max-width: 768px) {
		.sidebar {
			width: 100%;
			min-width: unset;
			border-right: none;
			border-bottom: 1px solid var(--color-border);
		}
	}
</style>
