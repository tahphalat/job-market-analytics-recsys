
'use client';

import { useEffect, useState } from 'react';
import { Container } from '../../../components/Container';
import { Badge } from '../../../components/Badge';
import { ArtifactsGate } from '../../../src/components/ArtifactsGate';
import {
  ArtifactMissingError,
  loadKpiSummary,
  loadTopSkills,
  loadTopTitles,
  loadJobsLite
} from '../../../src/lib/artifacts/fetchers';
import { 
    KpiSummary, 
    CountRow,
    JobLite
} from '../../../src/lib/artifacts/types';

// Components
import { SystemOverview } from './components/SystemOverview';
import { MarketInsights } from './components/MarketInsights';
import { JobBrowser } from './components/JobBrowser';
import { RealTimeMonitor } from './components/RealTimeMonitor';

type NavItem = 'System Overview' | 'Market Insights' | 'Job Browser' | 'Real-time Monitor';

export default function JobScopePage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeNav, setActiveNav] = useState<NavItem>('System Overview');

  // Data State
  const [kpi, setKpi] = useState<KpiSummary | null>(null);
  const [topTitles, setTopTitles] = useState<CountRow[]>([]);
  const [topSkills, setTopSkills] = useState<CountRow[]>([]);
  const [jobs, setJobs] = useState<JobLite[]>([]);

  useEffect(() => {
    let mounted = true;
    async function loadAll() {
      try {
        const results = await Promise.allSettled([
          loadKpiSummary(),
          loadTopTitles(),
          loadTopSkills(),
          loadJobsLite()
        ]);
        if (!mounted) return;

        const [kpiRes, titlesRes, skillsRes, jobsRes] = results;

        if (kpiRes.status === 'fulfilled') setKpi(kpiRes.value);
        if (titlesRes.status === 'fulfilled') setTopTitles(titlesRes.value);
        if (skillsRes.status === 'fulfilled') setTopSkills(skillsRes.value);
        if (jobsRes.status === 'fulfilled') setJobs(jobsRes.value);
        else console.warn("Could not load jobs_lite.csv");

        setError(null);
      } catch (err) {
        const message = err instanceof ArtifactMissingError ? 'Artifacts missing. Run make export_web' : 'Failed to load artifacts.';
        if (mounted) setError(message);
      } finally {
        if (mounted) setLoading(false);
      }
    }
    loadAll();
    return () => { mounted = false; };
  }, []);

  const navItems: NavItem[] = [
    'System Overview',
    'Market Insights',
    'Job Browser', 
    'Real-time Monitor'
  ];

  return (
    <ArtifactsGate>
      <Container className="pb-16 pt-10 lg:pt-14 font-sans">
         {/* Header */}
        <div className="mb-12">
            <div className="flex flex-wrap items-center gap-4 mb-4">
                <Badge>Internal Tool</Badge>
                <div className="h-px bg-white/10 flex-grow"></div>
                <div className="text-xs font-mono text-mist/50">v2.0.0-beta</div>
            </div>
            <h1 className="font-display text-5xl sm:text-6xl font-bold tracking-tight text-white mb-6">
                JobScope <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent to-highlight">Analytics</span>
            </h1>
            <p className="max-w-2xl text-lg text-mist/80 leading-relaxed">
                Comprehensive market intelligence platform for Data Engineering careers. 
                Analyzing <span className="text-white font-semibold">{loading ? '...' : kpi?.total_jobs.toLocaleString()}</span> listings to decode skills, salaries, and trends.
            </p>
        </div>

        {/* Navigation */}
        <div className="sticky top-4 z-40 mb-8 overflow-x-auto pb-2 scrollbar-hide -mx-4 px-4 sm:mx-0 sm:px-0">
            <div className="flex sm:flex-wrap gap-2 p-1 bg-surface/80 backdrop-blur-md border border-white/5 rounded-xl w-max sm:w-auto">
                {navItems.map(item => (
                    <button
                        key={item}
                        onClick={() => setActiveNav(item)}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${
                            activeNav === item 
                            ? 'bg-primary text-black shadow-lg shadow-white/10' 
                            : 'text-mist/60 hover:text-white hover:bg-white/5'
                        }`}
                    >
                        {item}
                    </button>
                ))}
            </div>
        </div>

        {/* Main Content Area */}
        <div className="min-h-[500px] animate-fade-in-up">
            {activeNav === 'System Overview' && (
                <SystemOverview kpi={kpi} />
            )}
            
            {activeNav === 'Market Insights' && (
                <MarketInsights 
                    topTitles={topTitles.map(t => ({ name: t.value, count: t.count }))} 
                    topSkills={topSkills.map(s => ({ name: s.value, count: s.count }))} 
                />
            )}

            {activeNav === 'Job Browser' && (
                <JobBrowser jobs={jobs} />
            )}

             {activeNav === 'Real-time Monitor' && (
                <RealTimeMonitor />
            )}
        </div>

        {/* Footer info */}
        <div className="mt-16 pt-8 border-t border-white/5 text-center text-xs text-mist/40 font-mono">
            JobScope Analytics Platform • Built with Next.js, Tailwind, & Python
        </div>

      </Container>
    </ArtifactsGate>
  );
}
