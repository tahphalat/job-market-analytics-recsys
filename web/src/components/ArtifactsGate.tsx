'use client';

import { ReactNode, useEffect, useState } from 'react';
import { ArtifactMissingError, loadArtifactsIndex } from '../lib/artifacts/fetchers';
import { Card } from '../../components/Card';
import { Badge } from '../../components/Badge';
import { Container } from '../../components/Container';

type GateState = 'loading' | 'ready' | 'missing' | 'error';

type Props = {
  children: ReactNode;
};

export function ArtifactsGate({ children }: Props) {
  const [state, setState] = useState<GateState>('loading');
  const [message, setMessage] = useState<string>('');

  useEffect(() => {
    let mounted = true;
    loadArtifactsIndex()
      .then(() => {
        if (!mounted) return;
        setState('ready');
      })
      .catch((err) => {
        if (!mounted) return;
        if (err instanceof ArtifactMissingError) {
          setState('missing');
          setMessage(err.message);
        } else {
          setState('error');
          setMessage(err instanceof Error ? err.message : 'Unknown error');
        }
      });
    return () => {
      mounted = false;
    };
  }, []);

  if (state === 'ready') {
    return <>{children}</>;
  }

  const heading = state === 'missing' ? 'DSDE artifacts not found' : 'Unable to load artifacts';
  const hint = state === 'missing' ? 'Run: make run_all && make export_web' : 'Check console/logs for details';

  return (
    <Container className="pb-16 pt-10 lg:pt-14">
      <Card className="space-y-4">
        <div className="flex items-center gap-3">
          <Badge>Artifacts</Badge>
          <p className="text-sm text-mist/70">Client-side fetch from /public/artifacts</p>
        </div>
        <h1 className="font-display text-3xl">{heading}</h1>
        <p className="text-mist/80">{message || 'Artifacts are required for the dashboard experience.'}</p>
        <div className="rounded-xl border border-white/10 bg-ink/60 px-4 py-3 text-sm text-mist/80">
          <p className="font-semibold text-cloud">{hint}</p>
          <p>Artifacts live in <code className="text-accent">web/public/artifacts</code> after export.</p>
        </div>
      </Card>
    </Container>
  );
}
