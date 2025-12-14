import { ReactNode } from 'react';
import clsx from 'clsx';

type Props = {
  children: ReactNode;
  className?: string;
};

export function Container({ children, className }: Props) {
  return <div className={clsx('mx-auto w-full max-w-6xl px-4 lg:px-8', className)}>{children}</div>;
}
