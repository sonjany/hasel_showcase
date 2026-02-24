import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";
import type { Quarry } from "../types";
import { PageTitle } from "../components/PageTitle";

export default function QuarriesList() {
    const [items, setItems] = useState<Quarry[]>([]);
    const [err, setErr] = useState<string | null>(null);

    useEffect(() => {
        api.get<Quarry[]>("/quarries/")
        .then(r => setItems(r.data))
        .catch(e => setErr(String(e?.message ?? e)));
    }, []);

    if (err) return <div className="p-6 text-red-400">Fehler: {err}</div>;


    return (
        <div className="max-w-5xl p-6 mx-auto">
          {/*<h1 className="mb-4 text-3xl font-bold">Steinbrüche</h1>*/}
          <PageTitle>Steinbrüche</PageTitle>
          {!items.length ? <p className="text-shadow-amber-300">no rides</p> : (
            <ul className="grid gap-4 md:grid-cols-2">
              {items.map(q => (
                <li key={q.id} className="p-4 border rounded-xl bg-white/5 border-white/10">
                  <div className="text-xl font-semibold">{q.name}</div>
                  <div className="text-sm opacity-80">
                    {q.latitude ?? "—"}, {q.longitude ?? "—"}
                  </div>
                  {q.gpx_url && (
                    <a href={q.gpx_url} className="text-sm underline underline-offset-2" target="_blank" rel="noreferrer">
                     GPX-Link
                    </a>
                  )}
                  <div className="mt-2 text-sm opacity-90 line-clamp-3">{q.description}</div>
                  <Link to={`/quarries/${q.id}`} className="inline-block px-3 py-1 mt-3 rounded-lg bg-white/10 hover:bg-white/20">
                    Details
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
    );
}