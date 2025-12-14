'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const links = [
  { href: '/', label: 'Home' },
  { href: '/projects/jobscope', label: 'JobScope' },
  { href: '/about', label: 'About' },
  { href: '/contact', label: 'Contact' }
];

function isActive(pathname: string, href: string) {
  if (href === '/') {
    return pathname === '/';
  }
  return pathname.startsWith(href);
}

export default function NavBar() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 border-b border-white/5 bg-ink/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 lg:px-8">
        <Link href="/" className="group flex items-center gap-2 text-lg font-semibold text-cloud">
          <div className="h-9 w-9 rounded-xl bg-gradient-to-br from-accent to-highlight p-[2px] shadow-glow">
            <div className="grid h-full w-full place-items-center rounded-[10px] bg-ink text-sm font-bold text-cloud group-hover:bg-card transition-colors">
              JS
            </div>
          </div>
          <div className="leading-tight">
            <div className="font-display text-xl">JobScope</div>
            {/* <p className="text-xs text-mist/80">30-second job story</p> */}
          </div>
        </Link>
        <nav className="flex items-center gap-2">
          {links.map((link) => {
            const active = isActive(pathname, link.href);
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`rounded-full px-4 py-2 text-sm font-medium transition hover:text-accent ${
                  active ? 'bg-white/10 text-cloud border border-white/10' : 'text-mist/80'
                }`}
              >
                {link.label}
              </Link>
            );
          })}
          <Link
            href="/projects/jobscope"
            className="ml-3 hidden items-center gap-2 rounded-full bg-gradient-to-r from-accent to-highlight px-4 py-2 text-sm font-semibold text-ink shadow-glow transition hover:scale-[1.01] md:inline-flex"
          >
            View JobScope
          </Link>
        </nav>
      </div>
    </header>
  );
}
