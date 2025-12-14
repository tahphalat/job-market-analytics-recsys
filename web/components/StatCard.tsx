import clsx from 'clsx';

type Props = {
  label: string;
  value: string | number;
  hint?: string;
  className?: string;
};

export function StatCard({ label, value, hint, className }: Props) {
  return (
    <div className={clsx('rounded-2xl border border-border/70 bg-surface/80 px-4 py-3 shadow-soft backdrop-blur', className)}>
      <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-secondary">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-primary">{value}</p>
      {hint ? <p className="mt-1 text-sm text-muted">{hint}</p> : null}
    </div>
  );
}
