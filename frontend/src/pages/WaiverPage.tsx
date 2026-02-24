import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

interface WaiverPageProps {
    onSign: (pdfUrl?: string) => void;
}


export default function WaiverPage({ onSign }: WaiverPageProps) {
    const [template, setTemplate] = useState<any>(null);
    const [name, setName] = useState("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetch("/api/registrations/waivers/")
            .then(res => res.json())
            .then(data => {
                const activeTemplate = Array.isArray(data) ? data[0] : data;
                setTemplate(activeTemplate);
            })
            .catch((err) => console.error("Error loading:", err))
    }, []);

    const navigate = useNavigate();

    const handleSign = async () => {
        setLoading(true);
        try{
            const response = await fetch("/api/registrations/waivers/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    name: name,
                    email: "test@example.com",  //auth-context
                    registration: 1, //beispiel-ID
                    template: template?.id,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                //const data = await response.json();
                onSign(data.pdf_url);
                navigate("/");
            }else if (response.status === 400 && data.registration) {
              console.log("Already signed, redirecting to the homepage...");
              onSign(undefined);
            }else {
                console.error("Error saving:", data);
                alert("Error saving. Please try again.")
            }

        } catch (error) {
            console.error("Network error:", error);
        } finally {
            setLoading(false);
        }
    };
    
    if (!template) {
        return ( 
          <div className="flex-col items-center p-10 font-mono text-white">
          <p>Loading document...</p>
          <button onClick={() => window.location.reload()} className="mt-4 underline text-amber-700">
            Try again
          </button>
        </div>
    );
    }

    return (
        <div className="flex flex-col items-center min-h-screen p-6 text-white bg-black">
            <div className="w-full max-w-2xl p-8 mt-12 space-y-8 border bg-neutral-900/50 border-white/10">
              <h1 className="text-4xl italic font-black uppercase text-amber-700">
                {template.title}
              </h1>

              <div className="h-64 p-6 overflow-y-auto font-mono text-sm leading-relaxed border bg-black/50 border-white/5">
                {template.body}
              </div>

              <div className="space-4">
                <p className="text-[10px] uppercase tracking-widest opacity-50">Your digital signature</p>

                <input
                  type="text"
                  placeholder="FULL NAME"
                  className="w-full p-4 uppercase bg-black border outline-none border-white/20 focus:border-amber-700 fond-bold"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />

                <button
                  disabled={loading || name.length < 5}
                  onClick={handleSign}
                  className="w-full py-4 font-black text-black uppercase transition-all shadow-lg bg-amber-700 hover:bg-amber-600 disabled:opacity-20"
                >
                  {loading ? (
                    <>
                      <svg className="w-5 h-5 text-black animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Generate legally compliant PDF...
                    </>
                  ) : (
                    "Accept & Participate"
                  )}
                </button>              
              </div>
            </div>
        </div>
    );
}

