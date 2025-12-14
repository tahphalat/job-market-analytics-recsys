import Link from 'next/link';
import { Container } from './Container';

export const Hero = () => {
  return (
    <Container className="pt-24 pb-16">
      <div className="space-y-6 max-w-2xl">
        <h1 className="text-display-1 font-display font-medium leading-none text-primary overflow-hidden whitespace-nowrap animate-typewriter w-0">
          JobScope
        </h1>
        <p className="text-display-3 font-display text-secondary animate-fade-in-up" style={{ animationDelay: '1.5s' }}>
          Market signals for <span className="text-accent">Data Engineers</span>.
        </p>
        <p className="text-body text-muted animate-fade-in-up max-w-lg" style={{ animationDelay: '1.8s' }}>
          Real-time analysis of job postings to help you find the right skills, right now.
        </p>
        <div className="flex gap-4 pt-4 animate-fade-in-up" style={{ animationDelay: '2s' }}>
          <Link href="/projects/jobscope" className="text-sm font-semibold text-primary hover:text-accent transition-colors">
            View Dashboard &rarr;
          </Link>
          <Link href="/demo" className="text-sm font-semibold text-muted hover:text-primary transition-colors">
            Explainable AI &rarr;
          </Link>
        </div>
      </div>
    </Container>
  );
};
