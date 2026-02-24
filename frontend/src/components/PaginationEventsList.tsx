import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";
import type { Event } from "../types";
//import { fmt } from "../lib/dates";

type DRFPage<T> = { count: number; next: string | null; previous: string | null; results: T[] };


function toRel(u: string | null) {
  if (!u) return null;
  try { const url = new URL(u); return url.pathname + url.search; } catch { return u; }
}

function fmtDateOnly(dt?: string | null) {
  if (!dt) return "-";
  return new Date(dt).toLocaleDateString();
}
function fmtTimeOnly(dt?: string | null) {
  if (!dt) return "-";
  return new Date(dt).toLocaleTimeString([], {hour: "2-digit", minute: "2-digit"});
}


const ORDERING = [
  { value: "start", label: "Start (aufsteigend)" },
  { value: "-start", label: "Start (absteigend)" },
  { value: "title", label: "Titel A-Z" },
  { value: "-title", label: "Titel Z-A" },
];

export default function PaginationEventsList() {
  const [items, setItems] = useState<Event[]>([]);
  const [count, setCount] = useState(0);
  const [next, setNext] = useState<string | null>(null);
  const [prev, setPrev] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  //URL-Steuerung 
  const [pageUrl, setPageUrl] = useState<string>("/events/?ordering=start");

  useEffect(() => {
    const ctrl = new AbortController();
    setLoading(true);
    setErr(null);

    api.get<DRFPage<Event>>(pageUrl, { signal: ctrl.signal })
      .then(r => {
        setItems(r.data.results ?? []);
        setCount(r.data.count ?? 0);
        setNext(toRel(r.data.next));
        setPrev(toRel(r.data.previous));
      })
      .catch(e => { if (e?.name !== "CanceledError") setErr(String(e?.message ?? e)); })
      .finally(() => setLoading(false));

    return () => ctrl.abort();
  }, [pageUrl]);

  const setOrdering = (ord: string) => setPageUrl(`/events/?ordering=${encodeURIComponent(ord)}`);
  const goPrev = () => prev && setPageUrl(prev);
  const goNext = () => next && setPageUrl(next);

  //aktuellen ordering-Wert aus pageUrl lesen
  const currentOrdering =
    new URLSearchParams(pageUrl.split("?")[1] || "").get("ordering") || "start";

  if (loading) return <div className="p-6">Lade Events…</div>;
  if (err) return <div className="p-6 text-red-400">Fehler: {err}</div>;

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <h1 className="text-3xl font-bold">Haselrodeo</h1>

        <label className="text-sm">
          <span className="mr-2 opacity-80">Sortieren nach:</span>
          <select
            className="px-2 py-1 bg-transparent border border-blue-900 rounded-lg"
            value={currentOrdering}
            onChange={e => setOrdering(e.target.value)}
          >
            {ORDERING.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
        </label>
      </div>

      <div className="mt-3 text-sm opacity-70">{count} Einträge</div>

      {!items.length ? (
        <p className="mt-6 opacity-70">Keine Events vorhanden.</p>
      ) : (
        <div className="mt-6 space-y-3">
          {items.map(ev => (
            <div key={ev.id} className="p-4 border shadow-sm rounded-2xl">
              <h3 className="text-lg font-semibold">
                <Link to={`/events/${ev.id}`} className="underline underline-offset-2 hover:opacity-80">
                  {ev.title}
                </Link>
              </h3>
              <p className="text-sm opacity-80">
                {ev.location ?? "—"} • {fmtDateOnly(ev.start)}, {fmtTimeOnly(ev.start)}
                {ev.end ? ` – ${fmtTimeOnly(ev.end)}` : ""}
              </p>

              {"going_count" in (ev as any) ? (
                <p className="mt-1 text-sm">Zugesagt: {(ev as any).going_count}</p>
              ) : (
                <p className="mt-1 text-sm">
                  Zugesagt: {(ev as any).going_attendees ?? 0} TN · {(ev as any).going_guides ?? 0} Guides
                </p>
              )}

              {ev.description && <p className="mt-2">{ev.description}</p>}

              <div className="mt-3">
                <Link
                  to={`/events/${ev.id}`}
                  className="inline-block px-3 py-1 border rounded-lg bg-white/10 border-white/10 hover:bg-white/20"
                >
                  Details ansehen
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="flex items-center gap-2 mt-8">
        <button
          className="px-3 py-1 border rounded-lg bg-white/10 border-white/10 disabled:opacity-40"
          onClick={goPrev}
          disabled={!prev}
        >
           zurück
        </button>
        <button
          className="px-3 py-1 border rounded-lg bg-white/10 border-white/10 disabled:opacity-40"
          onClick={goNext}
          disabled={!next}
        >
          weiter 
        </button>
      </div>
    </div>
  );
}
