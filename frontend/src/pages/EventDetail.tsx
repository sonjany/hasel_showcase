import { useEffect, useState, useMemo } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../lib/api";
import type { Event, ScheduleSlot } from "../types";
import { PageTitle } from "../components/PageTitle";
import type { ReactNode } from "react";


function fmtDateOnly(dt?: string | null) {
  if (!dt) return "-";
  return new Date(dt).toLocaleDateString();
}
function fmtTimeOnly(dt?: string | null) {
  if (!dt) return "-";
  return new Date(dt).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

/*UI Hilfen*/
function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="mt-8">
      <h2 className="mb-3 text-xl font-semibold">{title}</h2>
      <div className="p-4 border rounded-2xl bg-white/5 border-white/10">
        {children}
      </div>
    </section>
  );
}

/*Gruppen-Table*/
function GroupedSlots({ slots }: { slots: ScheduleSlot[] }) {
  if (!slots?.length) return <p className="opacity-70">Keine Fahr-Slots</p>;

  const groups = useMemo(() => {
    const driving = slots.filter((s) => s.kind === "DRIVING")
    const m = new Map<string, ScheduleSlot[]>();
    for (const s of driving) {
      const key = s.group || "Gruppe";
      if (!m.has(key)) m.set(key, []);
      m.get(key)!.push(s);
    }
    for (const [, arr] of m) {
      arr.sort(
        (a, b) =>
          +new Date(a.start) - +new Date(b.start) ||
          String(a.quarry_name ?? "").localeCompare(String(b.quarry_name ?? ""))
      );
    }
    const keys = [...m.keys()].sort((a, b) =>
      a.localeCompare(b, undefined, { numeric: true })
    );
    return keys.map((k) => ({ name: k, items: m.get(k)! }));
  }, [slots]);

  /*const minutes = (a?: string | null, b?: string | null) => {
    if (!a || !b) return 0;
    return Math.max(0, Math.round((+new Date(b) - +new Date(a)) / 60000));
  }*/

  return (
    <div className="space-y-6">
      {groups.map(({ name, items }) => (
      <div key={name} className="p-4 border rounded-2xl border-white/10">
      <h3 className="text-lg font-semibold">{name}</h3>
       
            <div className="overflow-x-auto">
              <table className="min-w-[560px] w-full text-sm">
                <thead>
                  <tr className="text-left border-b border-white/10">
                    <th className="py-2 pr-4">Zeit</th>
                    {/*<th className="py-2 pr-4">Typ</th>*/}
                    <th className="py-2 pr-4">Steinbruch</th>
                    <th className="py-2 pr-4">Links</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((s) => (
                      <tr key={s.id} className="border-b border-white/5">
                        <td className="py-2 pr-4 whitespace-nowrap">
                          {fmtDateOnly(s.start)}, {fmtTimeOnly(s.start)}
                          {s.end ? ` – ${fmtTimeOnly(s.end)}` : ""}
                        </td>
                        <td className="py-2 pr-4">{s.quarry_name || "-"}
                        </td>
                          
                        <td className="py-2 pr-4">
                          {s.quarry_gpx_url ? (
                            <a
                              className="underline underline-offset-2 hover:opacity-80"
                              href={s.quarry_gpx_url}
                              target="_blank"
                            >
                              GPX
                            </a>
                          ) : s.quarry ? (
                            <Link
                              to={`/quarries/${s.quarry}`}
                              className="underline underline-offset-2 hover:opacity-80"
                            >
                              Steinbruch
                            </Link>
                          ) : (
                            "—"
                          )}
                        </td>
                      </tr>
                    ))}
                  
                </tbody>
              </table>
            </div>
          </div>
        ))}
      
    </div>
  );
}

/*Seite*/
type GuideItem = { id: number; first_name: string; last_name: string };

export default function EventDetail() {
  const { id } = useParams();
  const [data, setData] = useState<Event | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [guides, setGuides] = useState<GuideItem[]>([]);

  useEffect(() => {
    setLoading(true);
    api
      .get<Event>(`/events/${id}/`)
      .then((r) => setData(r.data))
      .catch((e) => setErr(String(e?.message ?? e)))
      .finally(() => setLoading(false));

    //Guides aus Registrations-API ohne Email
    api
      .get<{ results?: any[] }>(
        `/registrations/registrations/?event=${id}&role=GUIDE&status=GOING`
      )
      .then((r) => {
        const arr = (r.data as any).results ?? (r.data as any);
        const list = (Array.isArray(arr) ? arr : []).map((x: any) => ({
          id: x.id,
          first_name: x.first_name,
          last_name: x.last_name,
        }));
        setGuides(list);
      })
      .catch(() => setGuides([]));
  }, [id]);

  const globalBreaks = useMemo(() => {
    const breaks = (data?.schedule_slots ?? []).filter((s) => s.kind === "BREAK");
    breaks.sort((a, b) => +new Date(a.start) - +new Date(b.start));
    const seen = new Set<string>();
    const uniq: typeof breaks = [];
    for (const s of breaks) {
      const key = `${s.start}|${s.end ?? ""}`;
      if (!seen.has(key)) {
        seen.add(key);
        uniq.push(s);
      }
    }
    return uniq;
  }, [data]);

  if (loading) return <div className="p-6 text-xl">Lade Event…</div>;
  if (err) return <div className="p-6 text-red-400">Fehler {err}</div>;
  if (!data) return null;

  return (
    <div className="max-w-4xl p-6 mx-auto">
      <Link to="/events" className="inline-block mb-2 text-sm opacity-80 hover:opacity-100">
        ...zurück zur Liste
      </Link>

      <PageTitle>{data.title}</PageTitle>

<div className="opacity-80">
  {fmtDateOnly(data.start)}, {fmtTimeOnly(data.start)}
  {data.end ? ` – ${fmtTimeOnly(data.end)}` : ""} • {data.location || "-"}
</div>

{/*Guides-wenn vorhanden*/}
{guides?.length > 0 && (
  <div className="mt-2 text-sm">
    <span className="opacity-80">Guides:</span>{" "}
    {guides.map(g => `${g.first_name} ${g.last_name}`).join(", ")}
  </div>
)}

{/*Pausen*/}
{globalBreaks.length > 0 && (
  <div className="mt-2 text-sm opacity-80">
    {globalBreaks.length === 1 ? "Pause:" : "Pausen:"}{""}
    {globalBreaks
      .map((b) => `${fmtTimeOnly(b.start)}${b.end ? `- ${fmtTimeOnly(b.end)}` : ""}`)
      .join(" • ")}
  </div>
)}

      <Section title="Gruppen & Fahrzeiten">
        <GroupedSlots slots={data.schedule_slots || []} />
      </Section>
    </div>
  );
}
