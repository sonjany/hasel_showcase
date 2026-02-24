import { NavLink } from "react-router-dom";
import Tile from "../components/Tile.tsx";
import WaiverBanner from "../components/WaiverBanner.tsx";

interface HomePageProps {
  pdfUrl: string | null;
}

export default function HomePage({ pdfUrl }: HomePageProps) {
  return (
    <div className="relative flex flex-col w-full min-h-screen overflow-hidden">
      {/*Banner*/}
      <WaiverBanner pdfUrl={pdfUrl} />

      {/*Hintergrundbild*/}
      <div
        className="absolute inset-0 bg-center bg-cover -z-20"
        style={{ backgroundImage: "url('/hero.jpg')" }}
      />

      {/*Overlay*/}
      <div className="absolute inset-0 -z-10 bg-linear-to-b from-black/70 via-black/40 to-black/80" />

      {/*Content*/}
      <div className="flex flex-col justify-between flex-1 w-full p-6 mx-auto md:p-12 max-w-7xl">
        {/*Header*/}
        <div className="pt-4">
          <h1 className="text-5xl italic font-black tracking-tighter uppercase md:text-8xl text-whitw ">
            Hasel<span className="text-amber-600">rodeo</span>
          </h1>
          {pdfUrl && (
            <a href={pdfUrl} target="_blank" rel="noreferrer">
                Your signed waiver
            </a>
          )}
          <p className="mt-2 text-sm md:text-xl font-medium tracking-[0.2em] uppercase opacity-80">
            welcome to the dirt 2026
          </p>
        </div>

        {/*Nächstes Event/Kacheln*/}
        <div className="mb-8 space-y-4">
          {/*Nächtes Event*/}
          <NavLink
            to="/events/1" //dynamisch
            className="block p-5 transition border-l-4 border-amber-600 bg-black/40 hover:bg-black/20"
          >
            <div className="flex items-center justify-between gap-4">
              <div>
                <div className="text-[10px] tracking-[0.3em] uppercase text-amber-600 font-bold">
                  Nächstes Event
                </div>
                <div className="text-2xl font-bold tracking-tight uppercase">
                  Steinbruch I
                </div>
                <div className="font-mono text-xs opacity-70">
                  08. AUG 2026 | 09.00 - 18.00
                </div>
              </div>
              <div className="flex items-center justify-center w-10 h-10 border rounded-full border-amber-600 text-amber-600">
                →
              </div>
            </div>
          </NavLink>

          {/*Kacheln*/}
          <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
            <Tile to="/events" title="Events" desc="Alle Termine" />

            <Tile to="/quarries" title="Steinbrüche" desc="Infos & Locations" />

            <Tile to="/gallery" title="Galerie" desc="Bilder" />

            <Tile to="/chat" title="Chat" desc="Orga" />
          </div>
        </div>
      </div>
    </div>
  );
}
