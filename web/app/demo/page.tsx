'use client';

import Link from 'next/link';
import { Container } from '../../components/Container';
import { SectionTitle } from '../../components/SectionTitle';
import { Card } from '../../components/Card';
import { Badge } from '../../components/Badge';

export default function DemoPage() {
  return (
    <Container className="pb-14 pt-10 lg:pt-14">
      <div className="mb-8 space-y-3">
        <Badge>Demo in 2 minutes</Badge>
        <h1 className="font-display text-4xl">Data Engineer / Analyst / Scientist</h1>
        <p className="text-mist/80">
          Client-side picks pulled from <code className="text-accent">demo_profiles.json</code> and <code className="text-accent">demo_recs.json</code>. Each suggestion shows a
          relevance score and the skills that triggered it.
        </p>
        <Link href="/projects/jobscope" className="text-sm font-semibold text-accent underline-offset-4 hover:underline">
          Back to dashboard
        </Link>
      </div>

      <div className="grid gap-6">
        <Card>
          <SectionTitle eyebrow="Profiles" title="Who we recommend for" subtitle="Profiles will load here with the skills they emphasize." />
        </Card>
        <Card>
          <SectionTitle eyebrow="Recommendations" title="Jobs + reasons" subtitle="Recommendations will render below with reasons once wired." />
          <div className="mt-3 h-48 rounded-xl border border-white/5 bg-ink/60" />
        </Card>
      </div>
    </Container>
  );
}
