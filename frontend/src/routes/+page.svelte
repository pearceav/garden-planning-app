<script lang="ts">
	import SeedSelector from '$lib/components/SeedSelector.svelte';
	import GardenPlan from '$lib/components/GardenPlan.svelte';
	import { generatePlan } from '$lib/api/client';
	import { selectedList, clearSelection } from '$lib/stores/selectedSeeds';
	import { gardenPlan, planLoading, planError, clearPlan, activeSavedGardenId } from '$lib/stores/gardenPlan';
	import { savedGardens } from '$lib/stores/savedGardens';
	import { gardenPreferences } from '$lib/stores/gardenPreferences';

	async function handleGenerate() {
		planLoading.set(true);
		planError.set(null);
		activeSavedGardenId.set(null);

		try {
			const plan = await generatePlan($selectedList, $gardenPreferences);
			gardenPlan.set(plan);
		} catch (e) {
			planError.set(e instanceof Error ? e.message : 'Failed to generate plan');
		} finally {
			planLoading.set(false);
		}
	}

	function handleSave() {
		if (!$gardenPlan) return;

		const name = prompt('Enter a name for this garden plan:');
		if (name) {
			savedGardens.save(name, $selectedList, $gardenPlan);
			alert('Garden plan saved!');
		}
	}

	function handleStartOver() {
		clearPlan();
		clearSelection();
	}

	function handleDelete() {
		if (!$activeSavedGardenId) return;
		if (confirm('Delete this saved garden plan?')) {
			savedGardens.delete($activeSavedGardenId);
			clearPlan();
			clearSelection();
		}
	}
</script>

<div class="page">
	{#if $planLoading}
		<div class="loading-overlay">
			<div class="loading-content">
				<div class="spinner"></div>
				<p>Generating your garden plan...</p>
				<p class="loading-hint">This may take a moment</p>
			</div>
		</div>
	{:else if $planError}
		<div class="error-container">
			<h2>Something went wrong</h2>
			<p>{$planError}</p>
			<button onclick={handleStartOver}>Try Again</button>
		</div>
	{:else if $gardenPlan}
		<GardenPlan
			plan={$gardenPlan}
			onSave={handleSave}
			onStartOver={handleStartOver}
			onDelete={$activeSavedGardenId ? handleDelete : undefined}
		/>
	{:else}
		<SeedSelector onGenerate={handleGenerate} />
	{/if}
</div>

<style>
	.page {
		min-height: 400px;
	}

	.loading-overlay {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: 400px;
	}

	.loading-content {
		text-align: center;
	}

	.spinner {
		width: 48px;
		height: 48px;
		border: 4px solid var(--color-border);
		border-top-color: var(--color-primary);
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin: 0 auto 1rem;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	.loading-hint {
		color: var(--color-text-muted);
		font-size: 0.9rem;
	}

	.error-container {
		text-align: center;
		padding: 3rem;
		background: var(--color-bg-alt);
		border-radius: 12px;
	}

	.error-container h2 {
		color: var(--color-error);
		margin-bottom: 1rem;
	}

	.error-container button {
		margin-top: 1rem;
		padding: 0.75rem 1.5rem;
		background: var(--color-primary);
		color: white;
		border: none;
		border-radius: 8px;
		cursor: pointer;
	}
</style>
