import type { Metadata } from 'next';
import { Inter, Orbitron } from 'next/font/google';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const orbitron = Orbitron({
  subsets: ['latin'],
  variable: '--font-orbitron',
  display: 'swap',
});

export const metadata: Metadata = {
  title: '👑 ANTIGRAVITY — Cognitive Civilization Control Center',
  description: 'A premium, real-time command center and cognitive operating interface for a persistent autonomous AI civilization.',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${orbitron.variable} h-full scroll-smooth antialiased`}
    >
      <body className="h-full bg-[#030307] text-slate-100 flex flex-col font-sans select-none">
        {children}
      </body>
    </html>
  );
}
