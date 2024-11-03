import type { Metadata } from "next";
import "./globals.css";
import ErrorBoundary from "../components/ErrorBoundary";
import { AuthProvider } from "../context/AuthContext";
import Navbar from "../components/Navbar";
import { JetBrains_Mono } from 'next/font/google';

const jetBrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-jetbrains',
});

export const metadata: Metadata = {
  title: "Quark Investimentos",
  description: "HACKATHON Quark Investimentos",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={jetBrainsMono.variable}>
      <body className="font-jetbrains">
        <AuthProvider>
          <Navbar />
          <main className="max-w-2xl m-auto">{children}</main>
        </AuthProvider>
      </body>
    </html>
  );
}
