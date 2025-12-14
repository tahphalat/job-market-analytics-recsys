import Link from 'next/link';
import { Container } from '../../components/Container';
import { SectionTitle } from '../../components/SectionTitle';
import { Card } from '../../components/Card';
import { Badge } from '../../components/Badge';

export default function AboutPage() {
  return (
    <Container className="pb-12 pt-10 lg:pt-14">
      <div className="space-y-4">
        <Badge>About</Badge>
        <h1 className="font-display text-4xl">Built like a product sprint</h1>
        <p className="text-mist/80">
          JobScope was built in a day as a recruiter-friendly narrative: a simple dashboard that loads DSDE artifacts on the client, visualizes trends, and demos a
          recommendation slice for DE/DA/DS roles.
        </p>
      </div>
      <div className="mt-8 grid gap-4 rounded-3xl border border-white/5 bg-white/5 p-6">
        <SectionTitle title="Approach" subtitle="Minimal stack: Next.js App Router, Tailwind, client fetch against exported artifacts." />
        <div className="grid gap-3 sm:grid-cols-2">
          <Card className="bg-ink/60">
            <p className="text-sm text-mist/70">Data</p>
            <p className="text-mist/90">
              Kaggle job postings + Remotive API. Artifacts are copied into <code className="text-accent">/public/artifacts</code> via <code className="text-accent">make
              export_web</code>.
            </p>
          </Card>
          <Card className="bg-ink/60">
            <p className="text-sm text-mist/70">Frontend</p>
            <p className="text-mist/90">Next.js, Tailwind, client fetch hooks, small composable cards. Optimized for a quick skim.</p>
          </Card>
        </div>
        <Card className="bg-ink/60 text-sm text-mist/70">
          <p>
            Remotive attribution: jobs sourced from <Link href="https://remotive.com" className="text-accent underline">remotive.com</Link>. Kaggle dataset:
            arshkon/linkedin-job-postings.
          </p>
        </Card>
      </div>
    </Container>
  );
}
