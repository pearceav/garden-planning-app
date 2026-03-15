<script lang="ts">
	import type { PlantGroup, Category } from '$lib/types';
	import { getPlantPixels, GRID_SIZE } from '$lib/pixelArt';

	interface Props {
		groups: PlantGroup[];
	}

	let { groups }: Props = $props();

	const CATEGORY_COLORS: Record<Category, string> = {
		fruits: '#e63946',
		veggies: '#2a9d8f',
		herbs: '#fb8500',
		flowers: '#e91e63'
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

	function bedStyle(type: string): { stroke: string; strokeWidth: number; dash: string; fill: string } {
		const t = type.toLowerCase();
		if (t.includes('yard') || t.includes('grass')) return { stroke: '#66bb6a', strokeWidth: 2, dash: '8 4', fill: '#a5d6a7' };
		if (t.includes('wood')) return { stroke: '#8B6914', strokeWidth: 3, dash: 'none', fill: '#d4a574' };
		if (t.includes('metal')) return { stroke: '#78909c', strokeWidth: 2, dash: '6 3', fill: '#b0bec5' };
		if (t.includes('stone') || t.includes('brick')) return { stroke: '#8d6e63', strokeWidth: 3, dash: 'none', fill: '#bcaaa4' };
		if (t.includes('fabric')) return { stroke: '#66bb6a', strokeWidth: 2, dash: '4 4', fill: '#a5d6a7' };
		if (t.includes('grow bag')) return { stroke: '#4a4a4a', strokeWidth: 2, dash: '3 3', fill: '#9e9e9e' };
		if (t.includes('self-water')) return { stroke: '#1e88e5', strokeWidth: 2, dash: 'none', fill: '#90caf9' };
		if (t.includes('terra cotta')) return { stroke: '#bf360c', strokeWidth: 2, dash: 'none', fill: '#e6a07c' };
		if (t.includes('plastic')) return { stroke: '#7cb342', strokeWidth: 2, dash: 'none', fill: '#c5e1a5' };
		if (t.includes('barrel')) return { stroke: '#5d4037', strokeWidth: 3, dash: 'none', fill: '#a1887f' };
		return { stroke: '#78909c', strokeWidth: 2, dash: '6 3', fill: '#d4a574' };
	}

	function parseSizeFt(size: string): { widthFt: number; heightFt: number } {
		const dimMatch = size.match(/(\d+(?:\.\d+)?)\s*(?:ft)?\s*x\s*(\d+(?:\.\d+)?)\s*(?:ft)?/i);
		if (dimMatch) {
			return { widthFt: parseFloat(dimMatch[1]), heightFt: parseFloat(dimMatch[2]) };
		}
		const diaMatch = size.match(/(\d+(?:\.\d+)?)\s*ft\s*diameter/i);
		if (diaMatch) {
			const d = parseFloat(diaMatch[1]);
			return { widthFt: d, heightFt: d };
		}
		return { widthFt: 3, heightFt: 3 };
	}

	function isIndividualContainers(group: PlantGroup): boolean {
		const t = group.container.type.toLowerCase();
		return t.includes('barrel') || t.includes('terra cotta') || t.includes('plastic pot');
	}

	function isCircularBed(group: PlantGroup): boolean {
		if (isIndividualContainers(group)) return true;
		const t = group.container.type.toLowerCase();
		const { widthFt, heightFt } = parseSizeFt(group.container.size);
		return t.includes('metal') && widthFt === heightFt && widthFt <= 2;
	}

	const MIN_CELL = 58;

	function bedLayout(group: PlantGroup) {
		const { widthFt, heightFt } = parseSizeFt(group.container.size);
		const plantCount = group.plants.length;

		if (isIndividualContainers(group)) {
			const containerR = 40;
			const gap = 20;
			const width = plantCount * containerR * 2 + (plantCount - 1) * gap + BED_PAD * 2;
			const height = containerR * 2 + BED_PAD * 2;
			return { cols: plantCount, rows: 1, width, height, cellW: containerR * 2 + gap, cellH: height };
		}

		const baseW = widthFt * PX_PER_FT;
		const baseH = heightFt * PX_PER_FT;
		const cols = Math.ceil(Math.sqrt(plantCount * (baseW / baseH)));
		const rows = Math.ceil(plantCount / cols);

		const width = Math.max(baseW, cols * MIN_CELL + BED_PAD * 2);
		const height = Math.max(baseH, rows * MIN_CELL + BED_PAD * 2);
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

		const bedsW =
			colWidths.reduce((a, b) => a + b, 0) + BED_GAP * (colWidths.length - 1) + YARD_PAD * 2;
		const totalW = Math.max(bedsW, 500);
		const totalH =
			rowHeights.reduce((a, b) => a + b, 0) +
			(LABEL_HEIGHT + BED_GAP) * (rowHeights.length - 1) +
			LABEL_HEIGHT +
			YARD_PAD * 2;

		return { beds: positioned, width: totalW, height: totalH + 90 };
	}

	let layout = $derived(computeBeds(groups));

	function truncate(name: string, max: number): string {
		return name.length > max ? name.slice(0, max - 1) + '\u2026' : name;
	}

	function waterTooltip(group: PlantGroup): string {
		const lines = group.plants
			.filter((p) => p.water_needs)
			.map((p) => `${p.name}: ${p.water_needs}`);
		return lines.length ? `Water Needs — ${group.name}\n${lines.join('\n')}` : group.name;
	}

	const legendCategories: Category[] = ['fruits', 'veggies', 'herbs', 'flowers'];

	let uniqueBedTypes = $derived(
		[...new Set(groups.map((g) => g.container.type))]
	);
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
		{@const style = bedStyle(bed.group.container.type)}
		{@const circular = isCircularBed(bed.group)}
		{@const individual = isIndividualContainers(bed.group)}
		<g class="bed-group">
		<title>{waterTooltip(bed.group)}</title>

		{#if individual}
			<!-- Individual containers (barrels, pots) - each plant gets its own circle -->
			{@const containerR = 40}
			{@const gap = 20}
			{@const totalW = bed.group.plants.length * containerR * 2 + (bed.group.plants.length - 1) * gap}
			{@const startX = bed.x + (bed.layout.width - totalW) / 2 + containerR}
			{#each bed.group.plants as plant, pi}
				{@const cx = startX + pi * (containerR * 2 + gap)}
				{@const cy = bed.y + bed.layout.height / 2}
				{@const pixels = getPlantPixels(plant.name)}
				{@const pxSize = 4}
				{@const iconSize = GRID_SIZE * pxSize}
				<!-- Container circle -->
				<circle
					{cx}
					{cy}
					r={containerR}
					fill={style.fill}
					fill-opacity="0.35"
					stroke={style.stroke}
					stroke-width={style.strokeWidth}
					stroke-dasharray={style.dash}
				/>
				<!-- Pixel art plant -->
				<g>
					<title>{plant.name} ({plant.category})</title>
					{#each pixels as px}
						<rect
							x={cx - iconSize / 2 + px.x * pxSize}
							y={cy - iconSize / 2 - 4 + px.y * pxSize}
							width={pxSize}
							height={pxSize}
							fill={px.color}
						/>
					{/each}
					<text
						x={cx}
						y={cy + iconSize / 2 + 8}
						text-anchor="middle"
						fill={CATEGORY_COLORS[plant.category]}
						font-size="8"
						font-weight="600"
					>
						{truncate(plant.name, 12)}
					</text>
				</g>
			{/each}
		{:else}
			<!-- Shared bed shape -->
			{#if circular}
				<circle
					cx={bed.x + bed.layout.width / 2}
					cy={bed.y + bed.layout.height / 2}
					r={bed.layout.width / 2}
					fill={style.fill}
					fill-opacity="0.35"
					stroke={style.stroke}
					stroke-width={style.strokeWidth}
					stroke-dasharray={style.dash}
				/>
			{:else}
				<rect
					x={bed.x}
					y={bed.y}
					width={bed.layout.width}
					height={bed.layout.height}
					rx="6"
					fill={style.fill}
					fill-opacity="0.35"
					stroke={style.stroke}
					stroke-width={style.strokeWidth}
					stroke-dasharray={style.dash}
				/>
			{/if}

			<!-- Plants inside shared bed -->
			{@const pxSize = Math.min(4, (bed.layout.cellW - 12) / GRID_SIZE, (bed.layout.cellH - 18) / GRID_SIZE)}
			{#each bed.group.plants as plant, pi}
				{@const col = pi % bed.layout.cols}
				{@const row = Math.floor(pi / bed.layout.cols)}
				{@const cx = bed.x + BED_PAD + col * bed.layout.cellW + bed.layout.cellW / 2}
				{@const cy = bed.y + BED_PAD + row * bed.layout.cellH + bed.layout.cellH / 2 - 4}
				{@const pixels = getPlantPixels(plant.name)}
				{@const iconSize = GRID_SIZE * pxSize}

				<g>
					<title>{plant.name} ({plant.category})</title>
					{#each pixels as px}
						<rect
							x={cx - iconSize / 2 + px.x * pxSize}
							y={cy - iconSize / 2 + px.y * pxSize}
							width={pxSize}
							height={pxSize}
							fill={px.color}
						/>
					{/each}
					<text
						x={cx}
						y={cy + iconSize / 2 + 10}
						text-anchor="middle"
						fill={CATEGORY_COLORS[plant.category]}
						font-size="8"
						font-weight="600"
					>
						{truncate(plant.name, 12)}
					</text>
				</g>
			{/each}
		{/if}

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
		</g>
	{/each}

	<!-- Plant category legend -->
	<text x={YARD_PAD} y={layout.height - 68} font-size="10" font-weight="600" fill="#555">Plants:</text>
	{#each legendCategories as cat, i}
		<circle
			cx={YARD_PAD + 50 + i * 70}
			cy={layout.height - 70}
			r="6"
			fill={CATEGORY_COLORS[cat]}
		/>
		<text
			x={YARD_PAD + 60 + i * 70}
			y={layout.height - 66}
			font-size="9"
			fill="#555"
		>
			{CATEGORY_LABELS[cat]}
		</text>
	{/each}

	<!-- Bed type legend -->
	<text x={YARD_PAD} y={layout.height - 38} font-size="10" font-weight="600" fill="#555">Beds:</text>
	{#each uniqueBedTypes as bedType, i}
		{@const style = bedStyle(bedType)}
		<rect
			x={YARD_PAD + 50 + i * 120}
			y={layout.height - 46}
			width="20"
			height="12"
			rx="2"
			fill={style.fill}
			fill-opacity="0.35"
			stroke={style.stroke}
			stroke-width={style.strokeWidth}
			stroke-dasharray={style.dash}
		/>
		<text
			x={YARD_PAD + 74 + i * 120}
			y={layout.height - 36}
			font-size="9"
			fill="#555"
		>
			{bedType}
		</text>
	{/each}
</svg>

<style>
	.garden-layout {
		width: 100%;
		height: auto;
		border-radius: 12px;
	}
	.bed-group {
		cursor: pointer;
	}
</style>
