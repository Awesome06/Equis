import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "The David Protocol",
  description: "Credit scoring for the credit invisible",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body className="antialiased font-sans">
        <main className="min-h-screen bg-slate-50/50">
          {children}
        </main>
      </body>
    </html>
  );
}
