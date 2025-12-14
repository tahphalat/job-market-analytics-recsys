'use client';

import { Container } from '../../../components/Container';
import { SectionTitle } from '../../../components/SectionTitle';
import { Card } from '../../../components/Card';
import { Badge } from '../../../components/Badge';
import { Button } from '../../../components/Button';
import { ArtifactsGate } from '../../../src/components/ArtifactsGate';

export default function JobScopePage() {
  return (
    <ArtifactsGate>
      <Container className="pb-16 pt-10 lg:pt-14">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-4">
            <Badge>Case Study</Badge>
            <h1 className="font-display text-4xl leading-tight sm:text-5xl">JobScope: job market signals in 30 seconds</h1>
            <p className="max-w-3xl text-mist/80">
              Dashboard-first portfolio project using Next.js App Router and Tailwind. Designed to answer three questions quickly: what roles are hot, which skills appear
              together, and how a candidate should respond.
            </p>
            <div className="flex flex-wrap items-center gap-3">
              <Button href="/demo">View demo</Button>
              <Button variant="ghost" href="/about">
                About this build
              </Button>
            </div>
          </div>
          <Badge className="bg-accent/20 text-accent">Dashboard</Badge>
        </div>

        <div className="mt-10 grid gap-6">
          <Card>
            <SectionTitle eyebrow="Overview" title="KPI + sources (Kaggle vs Remotive)" subtitle="Totals, unique companies, and source mix will sit here." />
            <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {['Total jobs', 'Unique companies', 'Kaggle share', 'Remotive share'].map((label) => (
                <div key={label} className="rounded-2xl border border-white/5 bg-white/5 p-4">
                  <p className="text-sm text-mist/70">{label}</p>
                  <p className="mt-2 text-2xl font-semibold text-cloud">Placeholder</p>
                </div>
              ))}
            </div>
          </Card>

          <Card>
            <SectionTitle eyebrow="Trends" title="Top titles + Top skills" subtitle="Charts will render here after wiring client fetch to artifacts." />
            <div className="mt-4 grid gap-4 lg:grid-cols-2">
              <div className="rounded-2xl border border-white/5 bg-ink/60 p-4">
                <p className="text-sm text-mist/70">Top titles</p>
                <div className="mt-3 h-36 rounded-xl border border-white/5 bg-ink/80" />
              </div>
              <div className="rounded-2xl border border-white/5 bg-ink/60 p-4">
                <p className="text-sm text-mist/70">Top skills</p>
                <div className="mt-3 h-36 rounded-xl border border-white/5 bg-ink/80" />
              </div>
            </div>
          </Card>

          <Card>
            <SectionTitle eyebrow="Skill Graph" title="Co-occurrence network" subtitle="Skill nodes and edges visualized from exported artifact." />
            <div className="mt-4 h-48 rounded-2xl border border-white/5 bg-ink/60" />
          </Card>

          <Card>
            <SectionTitle eyebrow="Insights" title="Fast bullets" subtitle="3–6 highlights extracted from the data once hooked up." />
            <ul className="mt-3 list-disc space-y-2 pl-5 text-mist/80">
              <li>Placeholder insight one</li>
              <li>Placeholder insight two</li>
              <li>Placeholder insight three</li>
            </ul>
          </Card>

          <Card>
            <SectionTitle eyebrow="Recommendation demo" title="DE / DA / DS paths" subtitle="Recommendations + reasons from artifacts will render here." />
            <div className="mt-3 rounded-2xl border border-white/5 bg-ink/60 p-4 text-mist/80">Loading…</div>
            <div className="mt-4 flex flex-wrap gap-2 text-xs text-mist/60">
              <Badge>Transparent reasons</Badge>
              <Badge>Client fetch only</Badge>
              <Badge>Static artifacts</Badge>
            </div>
          </Card>

          <div className="rounded-2xl border border-white/5 bg-white/5 p-5 text-sm text-mist/70">
            Data sources: Kaggle job postings and Remotive public API. Artifacts copied via <code className="text-accent">make export_web</code> into
            <code className="text-accent"> /public/artifacts</code>. Remotive attribution placeholder.
          </div>
        </div>
      </Container>
    </ArtifactsGate>
  );
}
