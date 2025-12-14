import Link, { LinkProps } from 'next/link';
import { AnchorHTMLAttributes, ReactNode } from 'react';
import clsx from 'clsx';

type Props = LinkProps & Omit<AnchorHTMLAttributes<HTMLAnchorElement>, 'href'> & {
  href: string;
  children: ReactNode;
  className?: string;
};

export function TextLink({ href, children, className, ...rest }: Props) {
  return (
    <Link href={href} className={clsx('text-link', className)} {...rest}>
      {children}
    </Link>
  );
}
