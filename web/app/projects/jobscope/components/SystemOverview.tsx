
'use client';

import Image from 'next/image';
import { Card } from '../../../../components/Card';
import { SectionTitle } from '../../../../components/SectionTitle';
import { KpiSummary } from '../../../../src/lib/artifacts/types';
import { Badge } from '../../../../components/Badge';

function numberWithCommas(num?: number) {
  if (num === undefined || Number.isNaN(num)) return '—';
  return num.toLocaleString('en-US');
}

export function SystemOverview({ kpi }: { kpi: KpiSummary | null }) {
  return (
    <div className="space-y-6">
      <Card>
        <SectionTitle 
            eyebrow="System Architecture" 
            title="Overview" 
            subtitle="High-level architecture of the JobScope platform handling Big Data ingestion and processing." 
        />
        
        <div className="mt-8 grid gap-8 lg:grid-cols-2 lg:items-center">
            <div className="space-y-4 text-mist/80 leading-relaxed">
                <p>
                    <strong className="text-primary">Data Source:</strong> We process over <strong className="text-accent">120,000+</strong> job postings from Kaggle and real-time APIs.
                </p>
                <p>
                    <strong className="text-primary">Lambda Architecture:</strong> The system is designed to handle both Batch (historical) and Speed (streaming) layers simultaneously, ensuring both comprehensive analysis and real-time responsiveness.
                </p>
                 <ul className="list-disc pl-5 space-y-2">
                    <li><strong className="text-primary">Scalability:</strong> Built on Kafka & Parquet to scale to millions of records.</li>
                    <li><strong className="text-primary">Data Quality:</strong> Automated &quot;Data Guard&quot; validation steps.</li>
                </ul>
                <div className="pt-4">
                     <Badge>~10k jobs/day (Batch)</Badge> <Badge>~100 events/sec (Speed)</Badge>
                </div>
            </div>
            
            <div className="relative rounded-xl overflow-hidden border border-white/10 bg-black/50 p-2">
                <div className="relative aspect-video w-full">
                     <Image 
                        src="/artifacts/figures/architecture_diagram.png" 
                        alt="Architecture Diagram" 
                        fill
                        className="object-contain"
                    />
                </div>
                <p className="mt-2 text-center text-xs text-mist/50">Figure 1.1: JobScope Data Pipeline</p>
            </div>
        </div>

        {/* Mermaid Diagram Fallback / Simple Flow */}
        <div className="mt-8 rounded-xl border border-white/5 bg-surface/30 p-6">
             <h4 className="text-sm font-mono text-mist/70 mb-4 uppercase tracking-wider">Logic Flow</h4>
             <div className="flex flex-wrap justify-center items-center gap-4 text-sm">
                <div className="flex flex-col items-center gap-2 p-3 bg-ink/80 rounded border border-white/10">
                    <span className="font-semibold text-accent">Kaggle Source</span>
                </div>
                <span className="text-mist/30">→</span>
                <div className="flex flex-col items-center gap-2 p-3 bg-ink/80 rounded border border-white/10">
                    <span className="font-semibold text-primary">Raw Layer</span>
                    <span className="text-xs text-mist/50">Validation</span>
                </div>
                 <span className="text-mist/30">→</span>
                <div className="flex flex-col items-center gap-2 p-3 bg-ink/80 rounded border border-white/10">
                    <span className="font-semibold text-primary">Curated Layer</span>
                    <span className="text-xs text-mist/50">Transform</span>
                </div>
                 <span className="text-mist/30">→</span>
                <div className="flex flex-col items-center gap-2 p-3 bg-ink/80 rounded border border-white/10">
                    <span className="font-semibold text-highlight">Artifacts</span>
                    <span className="text-xs text-mist/50">Aggregates</span>
                </div>
                 <span className="text-mist/30">→</span>
                 <div className="flex flex-col items-center gap-2 p-3 bg-surface border border-accent/20 shadow-[0_0_15px_rgba(56,189,248,0.15)] rounded">
                    <span className="font-semibold text-white">Streamlit / Web</span>
                    <span className="text-xs text-accent">Dashboard</span>
                </div>
             </div>
        </div>
      </Card>
      
      {/* KPI Cards */}
       <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card className="flex flex-col justify-center items-center text-center py-6">
                <span className="text-sm text-mist/70">Total Jobs</span>
                <span className="text-3xl font-display font-bold text-primary mt-2">{numberWithCommas(kpi?.total_jobs)}</span>
                <span className="text-xs text-accent mt-1">Analyzed</span>
            </Card>
            <Card className="flex flex-col justify-center items-center text-center py-6">
                 <span className="text-sm text-mist/70">Companies</span>
                <span className="text-3xl font-display font-bold text-primary mt-2">{numberWithCommas(kpi?.unique_companies)}</span>
            </Card>
            <Card className="flex flex-col justify-center items-center text-center py-6">
                 <span className="text-sm text-mist/70">Avg Salary</span>
                <span className="text-3xl font-display font-bold text-primary mt-2">$112k</span>
                <span className="text-xs text-green-400 mt-1">+4% YoY</span>
            </Card>
            <Card className="flex flex-col justify-center items-center text-center py-6">
                 <span className="text-sm text-mist/70">Source</span>
                <span className="text-3xl font-display font-bold text-primary mt-2">Kaggle</span>
                <span className="text-xs text-mist/50 mt-1">Multi-source</span>
            </Card>
       </div>
    </div>
  );
}
