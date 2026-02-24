import type { ReactNode } from "react";

export function PageTitle({ children }: { children: ReactNode }) {
    return (
        <h1 className="mb-4 text-2xl font-bold text-left sm:text-4xl">
            {children}
        </h1>
    );
}