import { writable } from 'svelte/store';
import type { GardenPlan } from '$lib/types';

export const gardenPlan = writable<GardenPlan | null>(null);
export const planLoading = writable(false);
export const planError = writable<string | null>(null);
export const activeSavedGardenId = writable<string | null>(null);

export function clearPlan() {
	gardenPlan.set(null);
	planError.set(null);
	activeSavedGardenId.set(null);
}
