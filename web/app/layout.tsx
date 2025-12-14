import type { Metadata } from 'next';
import { Inter, Space_Grotesk } from 'next/font/google';
import './globals.css';
import NavBar from './components/NavBar';
import Footer from './components/Footer';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap'
});

const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-space-grotesk',
  display: 'swap'
});

export const metadata: Metadata = {
  title: 'JobScope | Job Market Signals & Portfolio',
  description: 'Kaggle + Remotive job market signals, skill graph, and portfolio-ready story — demo currently paused.',
  openGraph: {
    title: 'JobScope | Job Market Signals & Portfolio',
    description: 'A Next.js + Tailwind dashboard with KPIs, trends, skill graph, and recommender from Kaggle + Remotive artifacts.',
    url: 'https://jobscope.local',
    type: 'website'
  }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${spaceGrotesk.variable} bg-background text-primary antialiased selection:bg-accent selection:text-black`}>
        <div className="relative min-h-screen">
          <div className="pointer-events-none fixed inset-0 opacity-60">
            <div className="grid-overlay absolute inset-0" />
          </div>
          <div className="relative z-10 flex min-h-screen flex-col">
            <NavBar />
            <main className="flex-1">{children}</main>
            <Footer />
          </div>
        </div>
      </body>
    </html>
  );
}
