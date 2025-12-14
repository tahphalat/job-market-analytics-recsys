import { AnchorHTMLAttributes, ButtonHTMLAttributes, ReactNode } from 'react';
import clsx from 'clsx';
import Link from 'next/link';

type Variant = 'primary' | 'ghost';

type CommonProps = {
  variant?: Variant;
  children: ReactNode;
  className?: string;
};

type ButtonProps = CommonProps & ButtonHTMLAttributes<HTMLButtonElement> & { href?: undefined };
type LinkProps = CommonProps & AnchorHTMLAttributes<HTMLAnchorElement> & { href: string };

function baseClasses(variant: Variant) {
  if (variant === 'ghost') {
    return 'border border-white/10 text-cloud hover:border-accent hover:text-accent';
  }
  return 'bg-gradient-to-r from-accent to-highlight text-ink shadow-glow hover:scale-[1.01]';
}

export function Button(props: ButtonProps | LinkProps) {
  const { variant = 'primary', children, className, ...rest } = props;
  const classes = clsx(
    'inline-flex items-center justify-center rounded-full px-5 py-3 text-sm font-semibold transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent',
    baseClasses(variant),
    className
  );

  if ('href' in rest && rest.href) {
    const { href, ...linkProps } = rest;
    return (
      <Link href={href} className={classes} {...linkProps}>
        {children}
      </Link>
    );
  }

  return (
    <button className={classes} {...(rest as ButtonProps)}>
      {children}
    </button>
  );
}
