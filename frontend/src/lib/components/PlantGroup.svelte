<script lang="ts">
	import type { PlantGroup, Category } from '$lib/types';

	interface Props {
		group: PlantGroup;
	}

	let { group }: Props = $props();

	function limitSentences(text: string, max: number): string {
		const sentences = text.match(/[^.!?]+[.!?]+/g);
		if (!sentences || sentences.length <= max) return text;
		return sentences.slice(0, max).join('').trim();
	}

	const categoryColors: Record<Category, string> = {
		fruits: 'var(--color-fruits)',
		veggies: 'var(--color-veggies)',
		herbs: 'var(--color-herbs)',
		flowers: 'var(--color-flowers)'
	};
</script>

<div class="plant-group">
	<h3>{group.name}</h3>

	<div class="plants">
		{#each group.plants as plant}
			<span class="plant-tag" style="background: {categoryColors[plant.category]}">{plant.name}</span>
		{/each}
	</div>

	<div class="details">
		<div class="container-info">
			<strong>Container:</strong>
			<span>{group.container.type}</span>
			<span class="size">{group.container.size} &bull; {group.container.depth} deep</span>
		</div>

		<div class="reason">
			<strong>Why they work together:</strong>
			<p>{limitSentences(group.reason, 3)}</p>
		</div>

		<div class="placement">
			<strong>Placement:</strong>
			<span>{limitSentences(group.placement, 3)}</span>
		</div>
	</div>
</div>

<style>
	.plant-group {
		background: white;
		border-radius: 12px;
		padding: 1.5rem;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
	}

	h3 {
		margin: 0 0 1rem;
		color: var(--color-primary);
		font-size: 1.1rem;
	}

	.plants {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		margin-bottom: 1rem;
	}

	.plant-tag {
		color: white;
		padding: 0.25rem 0.75rem;
		border-radius: 20px;
		font-size: 0.85rem;
		text-transform: capitalize;
	}

	.details {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		font-size: 0.9rem;
	}

	.container-info {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		align-items: baseline;
	}

	.size {
		color: var(--color-text-muted);
		font-size: 0.85rem;
	}

	.reason p {
		margin: 0.25rem 0 0;
		color: var(--color-text-muted);
		line-height: 1.5;
	}

	.placement {
		display: flex;
		gap: 0.5rem;
	}
</style>
