export interface SeedsByCategory {
	fruits: string[];
	veggies: string[];
	herbs: string[];
	flowers: string[];
}

export interface Container {
	type: string;
	size: string;
	depth: string;
}

export interface PlantInGroup {
	name: string;
	category: Category;
	water_needs?: string;
}

export interface PlantGroup {
	name: string;
	plants: PlantInGroup[];
	container: Container;
	reason: string;
	placement: string;
}

export interface BloomSchedule {
	spring: string[];
	summer: string[];
	fall: string[];
}

export interface GardenPlan {
	plant_groups: PlantGroup[];
	aesthetic_tips: string[];
	bloom_schedule: BloomSchedule;
}

export interface GardenPreferences {
	yard_width: number;
	yard_depth: number;
	sun_exposure: string;
	bed_types: string[];
}

export interface SavedGarden {
	id: string;
	name: string;
	createdAt: string;
	seeds: string[];
	plan: GardenPlan;
}

export type Category = 'fruits' | 'veggies' | 'herbs' | 'flowers';
