import { ReactNode } from 'react';
import clsx from 'clsx';

type Props = {
  eyebrow?: string;
  title: string;
  subtitle?: ReactNode;
  className?: string;
};

export function SectionTitle({ eyebrow, title, subtitle, className }: Props) {
  return (
    <div className={clsx('space-y-2', className)}>
      {eyebrow ? <p className="pill">{eyebrow}</p> : null}
      <h2 className="font-display text-3xl">{title}</h2>
      {subtitle ? <div className="text-mist/80">{subtitle}</div> : null}
    </div>
  );
}
