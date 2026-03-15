import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import type { SavedGarden, GardenPlan, PlantInGroup } from '$lib/types';

const STORAGE_KEY = 'savedGardens';

function migratePlants(gardens: SavedGarden[]): SavedGarden[] {
	for (const garden of gardens) {
		for (const group of garden.plan.plant_groups) {
			group.plants = group.plants.map((p: PlantInGroup | string) =>
				typeof p === 'string' ? { name: p, category: 'veggies' as const, water_needs: '' } : { ...p, water_needs: p.water_needs ?? '' }
			);
		}
	}
	return gardens;
}

function loadFromStorage(): SavedGarden[] {
	if (!browser) return [];
	const stored = localStorage.getItem(STORAGE_KEY);
	return stored ? migratePlants(JSON.parse(stored)) : [];
}

function saveToStorage(gardens: SavedGarden[]) {
	if (browser) {
		localStorage.setItem(STORAGE_KEY, JSON.stringify(gardens));
	}
}

function createSavedGardensStore() {
	const { subscribe, set, update } = writable<SavedGarden[]>(loadFromStorage());

	return {
		subscribe,
		save: (name: string, seeds: string[], plan: GardenPlan) => {
			update((gardens) => {
				const newGarden: SavedGarden = {
					id: crypto.randomUUID(),
					name,
					createdAt: new Date().toISOString(),
					seeds,
					plan
				};
				const updated = [...gardens, newGarden];
				saveToStorage(updated);
				return updated;
			});
		},
		delete: (id: string) => {
			update((gardens) => {
				const updated = gardens.filter((g) => g.id !== id);
				saveToStorage(updated);
				return updated;
			});
		},
		clear: () => {
			if (browser) {
				localStorage.removeItem(STORAGE_KEY);
			}
			set([]);
		}
	};
}

export const savedGardens = createSavedGardensStore();
