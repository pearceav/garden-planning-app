<script lang="ts">
	import type { PlantGroup, Category } from '$lib/types';

	interface Props {
		groups: PlantGroup[];
	}

	let { groups }: Props = $props();

	const CATEGORY_COLORS: Record<Category, string> = {
		fruits: '#e63946',
		veggies: '#2a9d8f',
		herbs: '#8338ec',
		flowers: '#fb8500'
	};

	const CATEGORY_LABELS: Record<Category, string> = {
		fruits: 'Fruits',
		veggies: 'Veggies',
		herbs: 'Herbs',
		flowers: 'Flowers'
	};

	const PX_PER_FT = 60;
	const BED_PAD = 25;
	const BED_GAP = 40;
	const YARD_PAD = 30;
	const LABEL_HEIGHT = 40;

	function isWoodBed(type: string): boolean {
		return type.toLowerCase().includes('wood');
	}

	function parseSizeFt(size: string): { widthFt: number; heightFt: number } {
		const match = size.match(/(\d+(?:\.\d+)?)\s*(?:ft)?\s*x\s*(\d+(?:\.\d+)?)\s*(?:ft)?/i);
		if (match) {
			return { widthFt: parseFloat(match[1]), heightFt: parseFloat(match[2]) };
		}
		return { widthFt: 3, heightFt: 3 };
	}

	function bedLayout(group: PlantGroup) {
		const { widthFt, heightFt } = parseSizeFt(group.container.size);
		const width = widthFt * PX_PER_FT;
		const height = heightFt * PX_PER_FT;
		const plantCount = group.plants.length;
		const cols = Math.ceil(Math.sqrt(plantCount * (width / height)));
		const rows = Math.ceil(plantCount / cols);
		const cellW = (width - BED_PAD * 2) / cols;
		const cellH = (height - BED_PAD * 2) / rows;
		return { cols, rows, width, height, cellW, cellH };
	}

	function computeBeds(groups: PlantGroup[]) {
		const perRow = groups.length <= 2 ? groups.length : 2;
		const beds = groups.map((g, i) => {
			const layout = bedLayout(g);
			const col = i % perRow;
			const row = Math.floor(i / perRow);
			return { group: g, layout, col, row };
		});

		const colWidths: number[] = [];
		const rowHeights: number[] = [];
		for (const bed of beds) {
			colWidths[bed.col] = Math.max(colWidths[bed.col] || 0, bed.layout.width);
			rowHeights[bed.row] = Math.max(rowHeights[bed.row] || 0, bed.layout.height);
		}

		const positioned = beds.map((bed) => {
			let x = YARD_PAD;
			for (let c = 0; c < bed.col; c++) x += colWidths[c] + BED_GAP;
			x += (colWidths[bed.col] - bed.layout.width) / 2;

			let y = YARD_PAD;
			for (let r = 0; r < bed.row; r++) y += rowHeights[r] + LABEL_HEIGHT + BED_GAP;

			return { ...bed, x, y };
		});

		const totalW =
			colWidths.reduce((a, b) => a + b, 0) + BED_GAP * (colWidths.length - 1) + YARD_PAD * 2;
		const totalH =
			rowHeights.reduce((a, b) => a + b, 0) +
			(LABEL_HEIGHT + BED_GAP) * (rowHeights.length - 1) +
			LABEL_HEIGHT +
			YARD_PAD * 2;

		return { beds: positioned, width: totalW, height: totalH + 50 };
	}

	let layout = $derived(computeBeds(groups));

	function truncate(name: string, max: number): string {
		return name.length > max ? name.slice(0, max - 1) + '\u2026' : name;
	}

	const legendCategories: Category[] = ['fruits', 'veggies', 'herbs', 'flowers'];
</script>

<svg
	viewBox="0 0 {layout.width} {layout.height}"
	class="garden-layout"
	role="img"
	aria-label="Garden layout showing plant beds"
>
	<!-- Yard background -->
	<rect
		x="0"
		y="0"
		width={layout.width}
		height={layout.height}
		rx="12"
		fill="#e8f5e9"
		stroke="#a5d6a7"
		stroke-width="2"
	/>

	{#each layout.beds as bed}
		{@const isWood = isWoodBed(bed.group.container.type)}

		<!-- Bed shape -->
		<rect
			x={bed.x}
			y={bed.y}
			width={bed.layout.width}
			height={bed.layout.height}
			rx="6"
			fill="#d4a574"
			fill-opacity="0.35"
			stroke={isWood ? '#8B6914' : '#78909c'}
			stroke-width={isWood ? 3 : 2}
			stroke-dasharray={isWood ? 'none' : '6 3'}
		/>

		<!-- Plants inside bed -->
		{#each bed.group.plants as plant, pi}
			{@const col = pi % bed.layout.cols}
			{@const row = Math.floor(pi / bed.layout.cols)}
			{@const cx = bed.x + BED_PAD + col * bed.layout.cellW + bed.layout.cellW / 2}
			{@const cy = bed.y + BED_PAD + row * bed.layout.cellH + bed.layout.cellH / 2}

			<g>
				<title>{plant.name} ({plant.category})</title>
				<circle
					{cx}
					{cy}
					r="20"
					fill={CATEGORY_COLORS[plant.category]}
					fill-opacity="0.9"
					stroke="white"
					stroke-width="2"
				/>
				<text
					x={cx}
					y={cy + 4}
					text-anchor="middle"
					fill="white"
					font-size="8"
					font-weight="600"
				>
					{truncate(plant.name, 9)}
				</text>
				<text
					x={cx}
					y={cy + 36}
					text-anchor="middle"
					fill="#333"
					font-size="9"
				>
					{plant.name}
				</text>
			</g>
		{/each}

		<!-- Bed label -->
		<text
			x={bed.x + bed.layout.width / 2}
			y={bed.y + bed.layout.height + 16}
			text-anchor="middle"
			font-size="12"
			font-weight="600"
			fill="#333"
		>
			{bed.group.name}
		</text>
		<text
			x={bed.x + bed.layout.width / 2}
			y={bed.y + bed.layout.height + 30}
			text-anchor="middle"
			font-size="10"
			fill="#666"
		>
			{bed.group.container.type} &mdash; {bed.group.container.size}
		</text>
	{/each}

	<!-- Legend -->
	{#each legendCategories as cat, i}
		<circle
			cx={layout.width - 140 + i * 34}
			cy={layout.height - 40}
			r="6"
			fill={CATEGORY_COLORS[cat]}
		/>
		<text
			x={layout.width - 140 + i * 34}
			y={layout.height - 40 + 14}
			text-anchor="middle"
			font-size="7"
			fill="#555"
		>
			{CATEGORY_LABELS[cat]}
		</text>
	{/each}
</svg>

<style>
	.garden-layout {
		width: 100%;
		height: auto;
		max-height: 550px;
		border-radius: 12px;
	}
</style>
