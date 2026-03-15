import type { SeedsByCategory, GardenPlan, GardenPreferences } from '$lib/types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export async function fetchSeeds(): Promise<SeedsByCategory> {
	const res = await fetch(`${API_BASE}/seeds`);
	if (!res.ok) {
		throw new Error('Failed to fetch seeds');
	}
	return res.json();
}

export async function generatePlan(
	selectedSeeds: string[],
	preferences: GardenPreferences
): Promise<GardenPlan> {
	const res = await fetch(`${API_BASE}/garden/plan`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ selected_seeds: selectedSeeds, preferences })
	});
	if (!res.ok) {
		const error = await res.json().catch(() => ({ detail: 'Failed to generate plan' }));
		throw new Error(error.detail || 'Failed to generate plan');
	}
	return res.json();
}
