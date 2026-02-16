#Haselrodeo – Event Management Plattform

Eine Fullstack-Applikation zur Digitalisierung von Enduro-Events. Das System automatisiert die Teilnehmerregistrierung, 
Zeitplan-Verwaltung und das Dokumenten-Management für Enduro-Rennen.

#Highlights & Features
-Dynamisches Slot-Management: Automatisierte Berechnung und Zuweisung von Startzeiten für Fahrer (Backend-Logik in Django).
-Interaktives Dashboard: Typsicheres Frontend mit React und TypeScript für Organisatoren und Teilnehmer.
-Geodaten-Integration: Verwaltung von Steinbruch-Locations und GPS-Koordinaten mittels PostGIS/PostgreSQL.
-Automatisierte PDF-Waiver: Generierung von Haftungsausschlüssen basierend auf Teilnehmerdaten.
-RESTful API: Saubere Kommunikation zwischen Django Backend und React Frontend.

#Tech-Stack
Frontend:
- React (Vite)
- TypeScript
- Tailwind CSS (Styling)
- Lucide React (Icons)

Backend:
- Django & Django REST Framework (DRF)
- PostgreSQL / PostGIS
- ReportLab (PDF-Generierung)

Infrastruktur & Tools:
- Git / GitHub
- VS Code Integration

#Architektur-Ansatz
Das Projekt verfolgt einen API-First-Ansatz. Das Django-Backend fungiert als "Single Source of Truth", 
während das React-Frontend durch strikte Typisierung (TypeScript) eine hohe Wartbarkeit und Fehlerresistenz gewährleistet. 
Besonderer Wert wurde auf die Skalierbarkeit der Datenbankstruktur (ER-Modell) gelegt, um auch komplexe Renn-Szenarien abzubilden.


#Hinweis zum Showcase
Dieses Repository dient als Code-Arbeitsprobe. 
Sensible Daten wie Umgebungsvariablen (`.env`) und die Datenbank selbst (`db.sqlite3`) sind aus Sicherheitsgründen nicht enthalten. 
Der Fokus liegt auf der Demonstration von Clean Code, Typisierung und Datenbank-Design.


#Erstellt mit Leidenschaft für den Enduro-Sport :)
