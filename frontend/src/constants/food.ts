export const FOOD_KINDS = [
    "FOODTRUCK",
    "LUNCH",
    "DINNER",
    "BREAKFAST",
    "SNACK",
] as const;
export type Foodkind = typeof FOOD_KINDS[number];

export const FOOD_KIND_LABELS: Record<Foodkind, string> = {
    FOODTRUCK: "Foodtruck",
    LUNCH: "Mittagessen",
    DINNER: "Abendessen",
    BREAKFAST: "Frühstück",
    SNACK: "Snack",
};

export const FOOD_KIND_OPTIONS = FOOD_KINDS.map(k => ({
    value: k,
    label: FOOD_KIND_LABELS[k],
}));