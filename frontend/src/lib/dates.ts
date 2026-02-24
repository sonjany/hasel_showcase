export function fmt(dt?: string | null) {
    if (!dt) return "-";
    const d = new Date(dt);
    return isNaN(d.getTime())
      ? "-"
      : new Intl.DateTimeFormat(undefined, { dateStyle: "medium", timeStyle: "short" }).format(d);
}