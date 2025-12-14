import { Container } from './Container';
import { Button } from './Button';
import Link from 'next/link';

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
        <div className="flex flex-wrap gap-3 pt-4 animate-fade-in-up" style={{ animationDelay: '2s' }}>
          <Button href="/projects/jobscope">View Dashboard</Button>
          <Button href="https://jobscope.streamlit.app" variant="ghost" target="_blank" rel="noreferrer">
            Open Streamlit App
          </Button>
        </div>
      </div>
    </Container>
  );
};
