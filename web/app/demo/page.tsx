'use client';

import { Container } from '../../components/Container';
import { Card } from '../../components/Card';
import { Badge } from '../../components/Badge';

export default function DemoPage() {
  return (
    <Container className="pb-14 pt-10 lg:pt-14">
      <div className="space-y-3">
        <Badge>Demo paused</Badge>
        <h1 className="font-display text-4xl">Explainable AI demo is temporarily disabled</h1>
        <p className="text-mist/80">The interactive demo is commented out for now while we focus on the main dashboard.</p>
      </div>

      <Card className="mt-8 text-mist/80">
        {/* Demo content has been commented out temporarily.
        <SectionTitle eyebrow="Profiles" title="Who we recommend for" subtitle="Profiles will load here with the skills they emphasize." />
        <SectionTitle eyebrow="Recommendations" title="Jobs + reasons" subtitle="Recommendations will render below with reasons once wired." />
        <SectionTitle eyebrow="Demo in 2 minutes" title="Checklist" subtitle="Follow these steps for a smooth run." />
        */}
        <p>Please visit the main dashboard instead.</p>
      </Card>
    </Container>
  );
}
