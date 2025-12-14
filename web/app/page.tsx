import Link from 'next/link';
import { Hero } from '../components/Hero';
import { BentoGrid, BentoItem } from '../components/BentoGrid';
import { Container } from '../components/Container';
import kpiSummary from '../public/artifacts/kpi_summary.json';

const formatNumber = (num: number) => new Intl.NumberFormat('en-US').format(num);

export default function HomePage() {
  const kpi = kpiSummary as any;
  const totalJobs = kpi?.total_jobs || 0;
  const companies = kpi?.unique_companies || 0;
  const kaggle = kpi?.sources?.kaggle || 0;
  
  return (
    <main>
      <Hero />
      
      <Container className="pb-24 space-y-12">
        <section className="animate-fade-in-up" style={{ animationDelay: '2.2s' }}>
          <h2 className="text-2xl font-display text-primary mb-6">Market Pulse</h2>
          <BentoGrid>
            <BentoItem title="Total Jobs Tracked" value={formatNumber(totalJobs)} subtitle="Across Kaggle & Secondary Sources" />
            <BentoItem title="Unique Companies" value={formatNumber(companies)} subtitle="Hiring for Data roles" />
            <BentoItem title="Sources" className="bg-surface/60">
               <div className="flex flex-col gap-2 mt-2">
                 <div className="flex justify-between text-sm">
                   <span className="text-secondary">Kaggle (Primary)</span>
                   <span className="text-primary font-mono">{formatNumber(kaggle)}</span>
                 </div>
                 <div className="flex justify-between text-sm">
                   <span className="text-secondary">Kaggle (Secondary)</span>
                   <span className="text-primary font-mono">{formatNumber(totalJobs - kaggle)}</span>
                 </div>
               </div>
            </BentoItem>
          </BentoGrid>
        </section>

        <section className="animate-fade-in-up" style={{ animationDelay: '2.4s' }}>
           <h2 className="text-2xl font-display text-primary mb-6">Features</h2>
           <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
             <div className="p-6 rounded-xl border border-border bg-surface/20 group hover:border-accent/40 transition-colors">
               <h3 className="text-xl font-display text-primary mb-2 group-hover:text-accent transition-colors">Skill Graph Analysis</h3>
               <p className="text-secondary leading-relaxed">
                 We build a co-occurrence graph to understand which skills are frequently hired together. 
                 This helps you plan your learning path (e.g. Python -> Spark -> Airflow).
               </p>
             </div>
             <div className="p-6 rounded-xl border border-border bg-surface/20 group hover:border-highlight/40 transition-colors">
               <h3 className="text-xl font-display text-primary mb-2 group-hover:text-highlight transition-colors">Explainable Recommendations</h3>
               <p className="text-secondary leading-relaxed">
                 Our TF-IDF model doesn't just give you a list. It explains <i>why</i> a job is a good match based on your profile keywords.
               </p>
             </div>
           </div>
        </section>
      </Container>
    </main>
  );
}
