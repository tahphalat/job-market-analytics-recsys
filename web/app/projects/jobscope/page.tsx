'use client';

import { useEffect, useMemo, useState } from 'react';
import { ResponsiveContainer, BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';
import { Container } from '../../../components/Container';
import { SectionTitle } from '../../../components/SectionTitle';
import { Card } from '../../../components/Card';
import { Badge } from '../../../components/Badge';
import { Button } from '../../../components/Button';
import { ArtifactsGate } from '../../../src/components/ArtifactsGate';
import { ArtifactMissingError, loadDemoProfiles, loadDemoRecs, loadKpiSummary, loadSkillGraph, loadTopSkills, loadTopTitles } from '../../../src/lib/artifacts/fetchers';
import { DemoProfile, DemoRec, KpiSummary, SkillGraph } from '../../../src/lib/artifacts/types';

type TrendDatum = { name: string; count: number };

function numberWithCommas(num?: number) {
  if (num === undefined || Number.isNaN(num)) return '—';
  return num.toLocaleString('en-US');
}

function percent(part: number, whole: number) {
  if (!whole) return '0%';
  const pct = (part / whole) * 100;
  if (pct === 0) return '0%';
  if (pct < 0.1) return '<0.1%';
  if (pct < 1) return `${pct.toFixed(1)}%`;
  return `${Math.round(pct)}%`;
}

function SoWhat({ kpi }: { kpi: KpiSummary | null }) {
  if (!kpi) return null;
  const kaggle = kpi.sources?.kaggle ?? 0;
  const remotive = kpi.sources?.remotive ?? 0;
  const total = kaggle + remotive || kpi.total_jobs;
  return (
    <p className="text-sm text-mist/80">
      So what: We scanned {numberWithCommas(total)} postings across {numberWithCommas(kpi.unique_companies)} companies. Kaggle dominates ({percent(kaggle, total)}), Remotive adds remote
      flavor ({percent(remotive, total)}). Use this mix to benchmark reach and bias.
    </p>
  );
}

function TrendChart({ title, data }: { title: string; data: TrendDatum[] }) {
  if (!data || data.length === 0) {
    return (
      <div className="rounded-2xl border border-white/5 bg-ink/60 p-4">
        <p className="text-sm text-mist/70">{title}</p>
        <p className="mt-3 text-sm text-mist/70">No data available.</p>
      </div>
    );
  }
  const sliced = data.slice(0, 10);
  return (
    <div className="rounded-2xl border border-white/5 bg-ink/60 p-4">
      <p className="text-sm text-mist/70">{title}</p>
      <div className="mt-3 h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={sliced} margin={{ left: -20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
            <XAxis dataKey="name" tick={{ fill: '#cbd5e1', fontSize: 11 }} interval={0} angle={-20} textAnchor="end" height={60} />
            <YAxis tick={{ fill: '#cbd5e1', fontSize: 11 }} />
            <Tooltip contentStyle={{ background: '#0b1222', border: '1px solid #1f2937', color: '#e2e8f0' }} />
            <Bar dataKey="count" fill="url(#accentGradient)" radius={[6, 6, 0, 0]} />
            <defs>
              <linearGradient id="accentGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#38bdf8" />
                <stop offset="100%" stopColor="#0ea5e9" />
              </linearGradient>
            </defs>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function SkillGraphTable({ graph }: { graph: SkillGraph | null }) {
  if (!graph) {
    return <p className="text-sm text-mist/70">Skill graph not available.</p>;
  }
  const edges = (graph.edges || []).filter((e) => e.source && e.target && e.weight !== undefined);
  const nodes = (graph.nodes || []).filter((n) => n.label);
  const hasEdges = edges.length > 0;
  const rows = hasEdges
    ? edges.sort((a, b) => (b.weight || 0) - (a.weight || 0)).slice(0, 20)
    : nodes.sort((a, b) => (b.count || 0) - (a.count || 0)).slice(0, 20);

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-sm">
        <thead className="text-mist/70">
          <tr>
            <th className="py-2 pr-4 text-left">{hasEdges ? 'Skill A' : 'Skill'}</th>
            <th className="py-2 pr-4 text-left">{hasEdges ? 'Skill B' : 'Mentions'}</th>
            <th className="py-2 text-left">{hasEdges ? 'Co-occur count' : 'Count'}</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-white/5 text-mist/90">
          {rows.map((row, idx) =>
            hasEdges ? (
              <tr key={`${row.source}-${row.target}-${idx}`}>
                <td className="py-2 pr-4">{row.source}</td>
                <td className="py-2 pr-4">{row.target}</td>
                <td className="py-2">{row.weight ?? '—'}</td>
              </tr>
            ) : (
              <tr key={`${(row as any).label}-${idx}`}>
                <td className="py-2 pr-4">{(row as any).label}</td>
                <td className="py-2 pr-4">{(row as any).count ?? '—'}</td>
                <td className="py-2">—</td>
              </tr>
            )
          )}
        </tbody>
      </table>
      {!hasEdges ? <p className="mt-3 text-sm text-mist/70">No edge pairs found; showing top nodes instead.</p> : null}
    </div>
  );
}

function Reasons({ reasons }: { reasons: string[] }) {
  if (!reasons || reasons.length === 0) return null;
  return (
    <div className="mt-2 flex flex-wrap gap-2">
      {reasons.map((reason) => (
        <span key={reason} className="rounded-full bg-white/5 px-2 py-1 text-xs text-mist/80">
          {reason}
        </span>
      ))}
    </div>
  );
}

export default function JobScopePage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [kpi, setKpi] = useState<KpiSummary | null>(null);
  const [topTitles, setTopTitles] = useState<TrendDatum[]>([]);
  const [topSkills, setTopSkills] = useState<TrendDatum[]>([]);
  const [graph, setGraph] = useState<SkillGraph | null>(null);
  const [recs, setRecs] = useState<Record<string, DemoRec[]>>({});
  const [profiles, setProfiles] = useState<DemoProfile[]>([]);
  const [selectedProfile, setSelectedProfile] = useState<string>('');

  useEffect(() => {
    let mounted = true;
    async function loadAll() {
      try {
        const [kpiData, titlesData, skillsData, graphData, recsData, profilesData] = await Promise.all([
          loadKpiSummary(),
          loadTopTitles(),
          loadTopSkills(),
          loadSkillGraph(),
          loadDemoRecs(),
          loadDemoProfiles()
        ]);
        if (!mounted) return;
        setKpi(kpiData);
        setTopTitles(titlesData.map((t) => ({ name: t.value, count: t.count })));
        setTopSkills(skillsData.map((s) => ({ name: s.value, count: s.count })));
        setGraph(graphData);
        setRecs(recsData);
        setProfiles(profilesData);
        const profileName = profilesData?.[0]?.name || Object.keys(recsData)[0] || '';
        setSelectedProfile(profileName);
        setError(null);
      } catch (err) {
        const message = err instanceof ArtifactMissingError ? 'Artifacts missing. Run: make run_all && make export_web' : 'Failed to load artifacts.';
        if (mounted) {
          setError(message);
        }
      } finally {
        if (mounted) setLoading(false);
      }
    }
    loadAll();
    return () => {
      mounted = false;
    };
  }, []);

  const selectedRecs = useMemo(() => {
    if (!selectedProfile) return [];
    return recs[selectedProfile] ? recs[selectedProfile].slice(0, 10) : [];
  }, [recs, selectedProfile]);

  const profileBlurb = profiles.find((p) => p.name === selectedProfile)?.profile || selectedProfile;

  return (
    <ArtifactsGate>
      <Container className="pb-16 pt-10 lg:pt-14">
        <div className="grid gap-6">
          <Card>
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="space-y-3">
                <Badge>Case Study</Badge>
                <h1 className="font-display text-4xl leading-tight sm:text-5xl">JobScope: job market signals in 30 seconds</h1>
                <p className="max-w-3xl text-mist/80">
                  Problem: ซูเปอร์มาร์เก็ตงานของเยอะ — ไม่รู้เลือกงานไหน, ไม่รู้ช่วงนี้อะไรมาแรง, ไม่รู้ควรอัปสกิลอะไรเพิ่ม. Project goal: สรุปตลาด + แนะนำงาน + เหตุผลที่ match.
                </p>
                <div className="flex flex-wrap items-center gap-3">
                  <Button href="/demo">View demo</Button>
                  <Button variant="ghost" href="/about">
                    About this build
                  </Button>
                </div>
                <div className="text-sm text-mist/70">
                  Data sources: Kaggle job postings + Remotive API (
                  <a href="https://remotive.com" target="_blank" rel="noreferrer" className="text-accent underline">
                    remotive.com
                  </a>
                  ).
                </div>
              </div>
              <pre className="w-full max-w-sm rounded-2xl border border-white/10 bg-ink/80 p-4 text-xs text-mist/80">
{`[Kaggle jobs]  [Remotive API]
      \\          /
   canonical schema + dedupe
           |
     analytics tables
           |
  KPIs | trends | skill graph
           |
   TF-IDF recommender
           |
      web artifacts`}
              </pre>
            </div>
          </Card>

          <Card>
            <SectionTitle eyebrow="Section A" title="Overview (KPI + sources)" subtitle="Totals, companies, and source mix live from kpi_summary.json." />
            <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <div className="rounded-2xl border border-white/5 bg-white/5 p-4">
                <p className="text-sm text-mist/70">Total jobs</p>
                <p className="mt-2 text-2xl font-semibold text-cloud">{loading ? 'Loading…' : numberWithCommas(kpi?.total_jobs)}</p>
              </div>
              <div className="rounded-2xl border border-white/5 bg-white/5 p-4">
                <p className="text-sm text-mist/70">Unique companies</p>
                <p className="mt-2 text-2xl font-semibold text-cloud">{loading ? 'Loading…' : numberWithCommas(kpi?.unique_companies)}</p>
              </div>
              <div className="rounded-2xl border border-white/5 bg-white/5 p-4">
                <p className="text-sm text-mist/70">Kaggle share</p>
                <p className="mt-2 text-2xl font-semibold text-cloud">
                  {loading ? 'Loading…' : percent(kpi?.sources?.kaggle || 0, (kpi?.sources?.kaggle || 0) + (kpi?.sources?.remotive || 0))}
                </p>
              </div>
              <div className="rounded-2xl border border-white/5 bg-white/5 p-4">
                <p className="text-sm text-mist/70">Remotive share</p>
                <p className="mt-2 text-2xl font-semibold text-cloud">
                  {loading ? 'Loading…' : percent(kpi?.sources?.remotive || 0, (kpi?.sources?.kaggle || 0) + (kpi?.sources?.remotive || 0))}
                </p>
              </div>
            </div>
            <div className="mt-4">
              {error ? <p className="text-sm text-red-300">{error}</p> : <SoWhat kpi={kpi} />}
            </div>
          </Card>

          <Card>
            <SectionTitle eyebrow="Section B" title="Trends" subtitle="Top titles and skills pulled from CSV artifacts." />
            <div className="mt-4 grid gap-4 lg:grid-cols-2">
              <TrendChart title="Top titles" data={topTitles} />
              <TrendChart title="Top skills" data={topSkills} />
            </div>
          </Card>

          <Card>
            <SectionTitle eyebrow="Section C" title="Skill Graph" subtitle="Table fallback showing strongest skill pairs from skill_graph.json." />
            <SkillGraphTable graph={graph} />
          </Card>

          <Card>
            <SectionTitle eyebrow="Section D" title="Recommendation demo" subtitle="Dropdown selects profile; shows top 10 jobs with reasons." />
            <div className="flex flex-wrap items-center gap-3">
              <label className="text-sm text-mist/70">Profile</label>
              <select
                value={selectedProfile}
                onChange={(e) => setSelectedProfile(e.target.value)}
                className="rounded-lg border border-white/10 bg-ink/80 px-3 py-2 text-sm text-cloud"
              >
                {profiles.map((p) => (
                  <option key={p.name} value={p.name}>
                    {p.name}
                  </option>
                ))}
                {profiles.length === 0 &&
                  Object.keys(recs).map((name) => (
                    <option key={name} value={name}>
                      {name}
                    </option>
                  ))}
              </select>
              {profileBlurb ? <span className="text-sm text-mist/70">Profile: {profileBlurb}</span> : null}
            </div>
            <div className="mt-4 space-y-3">
              {selectedRecs.length === 0 && !loading && <p className="text-sm text-mist/70">No recommendations found.</p>}
              {selectedRecs.map((rec) => (
                <div key={rec.job_id} className="rounded-2xl border border-white/5 bg-ink/60 p-4">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <p className="text-cloud font-semibold">{rec.title}</p>
                      <p className="text-sm text-mist/70">
                        {rec.company} · {rec.source}
                      </p>
                    </div>
                    <div className="text-sm text-accent font-semibold">{rec.score.toFixed(3)}</div>
                  </div>
                  {rec.source_url ? (
                    <a href={rec.source_url} target="_blank" rel="noreferrer" className="text-xs text-accent underline">
                      Open listing
                    </a>
                  ) : null}
                  <p className="mt-2 text-xs text-mist/70">reasons = คำ/สกิลที่ match</p>
                  <Reasons reasons={rec.reasons} />
                </div>
              ))}
            </div>
          </Card>
        </div>
      </Container>
    </ArtifactsGate>
  );
}
