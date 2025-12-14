import { ReactNode } from 'react';

interface BentoItemProps {
  title: string;
  value?: string | number;
  subtitle?: string;
  className?: string;
  children?: ReactNode;
}

export const BentoItem = ({ title, value, subtitle, className = "", children }: BentoItemProps) => {
  return (
    <div className={`rounded-xl border border-border bg-surface/40 p-6 flex flex-col justify-between hover:bg-surface/60 transition-colors ${className}`}>
      <div>
        <h3 className="text-sm font-medium text-muted uppercase tracking-wider mb-2">{title}</h3>
        {value && <p className="text-4xl font-display text-primary">{value}</p>}
        {children}
      </div>
      {subtitle && <p className="text-sm text-secondary mt-4">{subtitle}</p>}
    </div>
  );
};

export const BentoGrid = ({ children }: { children: ReactNode }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {children}
    </div>
  );
};
