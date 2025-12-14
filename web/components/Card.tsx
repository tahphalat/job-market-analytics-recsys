import { ReactNode } from 'react';
import clsx from 'clsx';

type Props = {
  children: ReactNode;
  className?: string;
};

export function Card({ children, className }: Props) {
  return <div className={clsx('card rounded-2xl border border-white/10 bg-white/5 p-6', className)}>{children}</div>;
}
