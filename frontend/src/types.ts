export type ID = number;
export type SlotKind = "DRIVING" | "BREAK";


export type ScheduleItem = {
    id: ID;
    start: string;
    end: string | null;
    title: string;
    description: string;
    order: number;
};

export type FoodServiceWindow = {
    id: ID;
    kind:
    "Foodtruck" | "LUNCH" | "DINNER" | "BREAKFAST" | "SNACK";
    vendor: string;
    start: string;
    end: string | null;
    location: string;
};

export type ScheduleSlot = {
    id: ID;
    group: string;
    quarry: number | null;
    quarry_name?: string | null;
    quarry_gpx_url?: string | null;
    kind: SlotKind;
    start: string;
    end?: string | null
};

export type Event = {
    id: ID;
    title: string;
    location: string;
    start: string;
    end: string | null;
    capacity: number;
    going_attendees: number;
    going_guides: number;
    going_count?: number;
    
    description?: string;
    schedule_items?: ScheduleItem[];
    food_windows?: FoodServiceWindow[];
    schedule_slots?: ScheduleSlot[];
};

export type Quarry = {
    id: ID;
    name: string;
    latitude: number | null;
    longitude: number | null;
    gpx_url: string;
    description: string;
};