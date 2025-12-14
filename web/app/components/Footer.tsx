export default function Footer() {
  return (
    <footer className="border-t border-white/5 bg-ink/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl flex-col gap-2 px-4 py-6 text-sm text-mist/80 lg:px-8 lg:flex-row lg:items-center lg:justify-between">
        <p>© 2025 JobScope. All rights reserved.</p>
        <div className="flex flex-wrap items-center gap-3">
          <span className="rounded-full bg-white/5 px-3 py-1 text-xs uppercase tracking-wide text-mist">Next.js + Tailwind</span>
          <span className="text-xs text-mist/60">Source attribution placeholder for Remotive and Kaggle.</span>
        </div>
      </div>
    </footer>
  );
}
