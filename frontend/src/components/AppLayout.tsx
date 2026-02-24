import type { ReactNode } from "react";
import { NavLink } from "react-router-dom";


type AppLayoutProps = {
    children: ReactNode;
};

export function AppLayout({ children }: AppLayoutProps) {
    return (
        <div className="min-h-screen text-white bg-neutral-900">
            <header className="border-b border-white/">
            <div className="flex items-center justify-between max-w-5xl px-6 py-4 mx-auto">
                <div className="text-2xl font-bold tracking-tight md:text-3xl">
                    Haselrodeo
                </div>

                <nav className="flex gap-4 text-sm md:text-base opacity-80">
                    <NavLink
                    to="/events"
                    className={({ isActive }) =>
                      `text-amber-700 hover:text-amber-400 ${
                        isActive ? "font-semibold underline underline-offset-4" : ""
                    }`
                }
                >
                    Events
                </NavLink>

                <NavLink
                    to="/quarries"
                    className={({ isActive }) => 
                    `text-amber-700 hover:text-amber-400 ${
                       isActive ? "font-semibold underline underline-offset-4" : ""
                    }`
                }
                >
                    Steinbrüche
                </NavLink>
              </nav>
            </div>  
        </header>
        
        <main className="max-w-5xl px-6 py-8 mx-auto">
            {children}
        </main>
        </div>
    );
}
