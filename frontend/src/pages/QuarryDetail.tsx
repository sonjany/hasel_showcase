import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../lib/api";
import type { Quarry } from "../types";
 

export default function QuarryDetail() {
    const { id } = useParams();
    const [ q, setQ ] = useState<Quarry | null>(null);
    const [ err, setErr] = useState<string | null>(null);

    useEffect(() => {
        api.get<Quarry>(`/quarries/${id}/`)
          .then(r => setQ(r.data))
          .catch(e => setErr(String(e?.message ?? e)));
    }, [id]);

    if (err) return <div className="p-6 text-red-400">Fehler: {err}</div>;
    if (!q) return <div className="p-6">Lade...</div>;

    return (
        <div className="max-w-3xl p-6 mx-auto">
            <Link to="/quarries" className="text-sm opacity-80 hover:opacity-100">zurück</Link>
            <h1 className="mt-2 text-3xl font-bold">{q.name}</h1>
            <div className="opacity-80">{q.latitude ?? "-"}, {q.longitude ?? "-"}</div>
            {q.gpx_url && (
                <p className="mt-2">
                    <a href={q.gpx_url} className="underline underline-offset-2" target="_blank" rel="noreferrer">
                        GPX-Link öffnen
                    </a>
                </p>
            )}
            {q.description && <p className="mt-4 leading-relaxed">{q.description}</p>}
        </div>
    );
}
