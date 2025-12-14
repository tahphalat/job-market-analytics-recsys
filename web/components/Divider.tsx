import clsx from 'clsx';

type Props = {
  className?: string;
};

export function Divider({ className }: Props) {
  return <div className={clsx('divider', className)} />;
}
