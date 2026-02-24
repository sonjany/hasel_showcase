
import { NavLink } from "react-router-dom";

export default function Tile({
    to,
    title,
    desc,
}: {
    to: string;
    title: string;
    desc: string;
}) {
    return (
        <NavLink
        to={to}
        className="flex flex-col justify-between p-4 transition border aspect-square border-white/15 bg-black/40 hover:border-amber-400/50 hover:bg-black/60 group"
    >
            <div className="text-sm font-bold tracking-wide uppercase transition-colors group-hover:text-amber-400">
                {title}
            </div>

            <div className="mt-1 text-[10px] uppercase opacity-60 leading-tight">
                {desc}
            </div>

            <div className="text-[10px]font-bold text-amber-400 tracking-widest uppercase">
            →
        </div>
    </NavLink>
    );
}