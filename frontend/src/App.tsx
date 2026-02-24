import { useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import PaginatedEventsList from "./components/PaginationEventsList";
import EventDetail from "./pages/EventDetail";
import QuarryDetail from "./pages/QuarryDetail";
import QuarriesListPage from "./pages/QuarriesListPage";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import WaiverPage from "./pages/WaiverPage";

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [hasSignedWaiver, setHasSignedWaiver] = useState(false);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null); //speicher pdf-link

  const handleLoginSuccess = async (email: string) => {
    setIsLoggedIn(true);

    try {
      const response = await fetch(`/api/registrations/waivers/?email=${email}`);

      if (!response.ok) {
        console.log("Signature not found (server response was not OK)");
        setHasSignedWaiver(false);
        return;

      }

      const data = await response.json();

      if (Array.isArray(data) && data.length > 0) {
        console.log("Signature found! Redirect to the homepage.");
        setHasSignedWaiver(true);
        setPdfUrl(data[0].pdf_url);
      }
      
    } catch (err) {
      console.log("Network error during waiver check:", err);
      setHasSignedWaiver(false);
    }
  };

  if (!isLoggedIn) {
    return <LoginPage onLogin={() => handleLoginSuccess("test@example.com")} />;
  }
  if (!hasSignedWaiver) {
    return (
      <WaiverPage
        onSign={(url?: string) => {
          setPdfUrl(url ?? null);
          setHasSignedWaiver(true);
        }}
      />
    );
  }

  return (
    <Routes>
      <Route path="/" element={<HomePage pdfUrl={pdfUrl} />} /> //Startseite
      <Route path="/events" element={<PaginatedEventsList />} /> //Event-Bereich
      <Route path="/events/:id" element={<EventDetail />} />
      <Route path="/quarries" element={<QuarriesListPage />} /> //Locations
      <Route path="/quarries/:id" element={<QuarryDetail />} />
      <Route path="*" element={<Navigate to="/" replace />} /> //Catch-URL
      existiert nicht
    </Routes>
  );
}

