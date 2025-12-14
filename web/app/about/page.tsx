import Link from 'next/link';
import profile from '../../src/content/profile.json';
import { Container } from '../../components/Container';
import { SectionTitle } from '../../components/SectionTitle';
import { Card } from '../../components/Card';
import { Badge } from '../../components/Badge';

export default function AboutPage() {
  const skills = ['SQL', 'Python', 'ETL', 'Cloud (AWS/GCP/Azure)', 'Airflow', 'Spark/PySpark', 'Dashboard', 'ML basics'];

  return (
    <Container className="pb-12 pt-10 lg:pt-14">
      <div className="space-y-4">
        <Badge>About</Badge>
        <h1 className="font-display text-4xl">Built like a product sprint</h1>
        <p className="text-mist/80">{profile.tagline}</p>
      </div>
      <div className="mt-8 grid gap-4 rounded-3xl border border-white/5 bg-white/5 p-6">
        <SectionTitle title={profile.name} subtitle="Minimal stack: Next.js App Router, Tailwind, client fetch against exported artifacts." />
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
        <Card className="bg-ink/60">
          <p className="text-sm text-mist/70">Skills & tools (top picks)</p>
          <div className="mt-2 flex flex-wrap gap-2">
            {skills.map((s) => (
              <span key={s} className="rounded-full bg-white/10 px-3 py-1 text-xs font-semibold text-mist">
                {s}
              </span>
            ))}
          </div>
        </Card>
        <div className="grid gap-3 sm:grid-cols-3">
          <Card className="bg-ink/60">
            <p className="text-sm text-mist/70">GitHub</p>
            <Link href="https://github.com" className="text-accent underline">
              github.com/your-handle
            </Link>
          </Card>
          <Card className="bg-ink/60">
            <p className="text-sm text-mist/70">LinkedIn</p>
            <Link href="https://www.linkedin.com" className="text-accent underline">
              linkedin.com/in/your-handle
            </Link>
          </Card>
          <Card className="bg-ink/60">
            <p className="text-sm text-mist/70">Email</p>
            <Link href={`mailto:${profile.contact}`} className="text-accent underline">
              {profile.contact}
            </Link>
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
