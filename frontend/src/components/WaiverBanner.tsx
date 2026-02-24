import { useState, useEffect } from "react";



interface WaiverBannerProps {
    pdfUrl: string | null;
}

export default function WaiverBanner({ pdfUrl }: WaiverBannerProps) {
    const[isVisible, setIsVisible] = useState(!!pdfUrl);


    useEffect(() => {
        if (pdfUrl) {
            const timer = setTimeout(() => setIsVisible(false), 10000);
            return () => clearTimeout(timer);
        }
    }, [pdfUrl]);

    if (!isVisible || !pdfUrl) return null;

    return (
        <div className="fixed top-0 left-0 right-0 duration-700 z-100 animate-banner">
            <div className="flex items-center justify-between px-4 py-3 text-black border-b-2 shadow-2xl bg-amber-700 md:px-6 border-black/10">
                <div className="flex items-center gap-3">
                    <span className="hidden text-xl md:inline">🏁</span>
                    <div>
                        <p className="italic font-black leading-none tracking-tight uppercase">Ready to go!</p>
                        <p className="text-[9px] uppercase font-bold opacity-75">Disclaimer deposited</p>
                    </div>
                </div>

                <div className="flex items-center gap-2">
                    <a
                        href={pdfUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="bg-black text-white px-3 py-1.5 text-[10px] font-black uppercase hover:bg-neutral-800 transition"
                    >
                        Open PDF
                    </a>
                    <button
                        onClick={() => setIsVisible(false)}
                        className="p-1 rounded hover:bg-black10"
                    >
                        ✕
                    </button>
                </div>
            </div>
        </div>
    );
}