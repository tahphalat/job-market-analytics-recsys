import Link from 'next/link';
import { Container } from '../components/Container';
import { SectionTitle } from '../components/SectionTitle';
import { Card } from '../components/Card';
import { Badge } from '../components/Badge';
import { Button } from '../components/Button';

const highlights = [
  {
    title: 'Overview in 30s',
    copy: 'KPIs, Kaggle vs Remotive coverage, and where the volume sits.',
    href: '/projects/jobscope'
  },
  {
    title: 'Trends & Graphs',
    copy: 'Top titles, emerging skills, and a co-occurrence network from real postings.',
    href: '/projects/jobscope#trends'
  },
  {
    title: 'Recommendation Demo',
    copy: 'Data Engineer / Analyst / Scientist paths with reasons you can skim.',
    href: '/demo'
  }
];

export default function HomePage() {
  return (
    <Container className="pb-12 pt-10 lg:pt-14">
      <section className="mb-14 grid gap-8 rounded-3xl bg-gradient-to-br from-white/5 via-white/0 to-white/5 p-8 shadow-glow">
        <div className="max-w-3xl space-y-4">
          <Badge>JobScope MVP</Badge>
          <h1 className="font-display text-4xl leading-tight sm:text-5xl">JobScope: สรุปตลาดงาน + แนะนำงานที่เหมาะกับคุณ</h1>
          <p className="text-lg text-mist/80">
            ตลาดงานเหมือนซูเปอร์มาร์เก็ตของเยอะ: ไม่รู้เลือกงานไหน, ไม่รู้ช่วงนี้อะไรมาแรง, ไม่รู้ควรอัปสกิลอะไรเพิ่ม. JobScope รวบ KPIs, เทรนด์, skill graph, และ demo
            แนะนำงานให้ดูจบใน 30 วินาที.
          </p>
          <div className="flex flex-wrap items-center gap-3">
            <Button href="/projects/jobscope">View JobScope Dashboard</Button>
            <Button variant="ghost" href="/demo">
              Demo in 2 minutes
            </Button>
            <span className="text-sm text-mist/60">Kaggle + Remotive | Skill graph | Recs</span>
          </div>
        </div>
        <div className="grid gap-4 sm:grid-cols-3">
          {highlights.map((item) => (
            <Card key={item.title} className="flex h-full flex-col justify-between transition hover:-translate-y-1 hover:border-accent/50 hover:shadow-glow">
              <div className="space-y-2">
                <p className="text-sm uppercase tracking-wide text-mist/70">{item.title}</p>
                <p className="text-sm text-mist/90">{item.copy}</p>
              </div>
              <div className="mt-6 text-xs font-semibold text-accent">
                <Link href={item.href}>Open</Link>
              </div>
            </Card>
          ))}
        </div>
      </section>

      <section className="grid gap-6 rounded-3xl border border-white/5 bg-white/5 p-6 backdrop-blur lg:grid-cols-3">
        <div className="lg:col-span-2">
          <SectionTitle title="What this shows" subtitle="Minimal dashboard to answer where demand sits, what spikes, and how to respond." />
          <div className="mt-4 grid gap-3 text-mist/90 sm:grid-cols-2">
            <div className="rounded-xl border border-white/5 bg-white/5 px-4 py-3">
              <p className="text-xs uppercase tracking-wide text-mist/60">A</p>
              <p className="font-semibold">Overview</p>
              <p className="text-sm text-mist/80">KPIs + Kaggle vs Remotive source mix.</p>
            </div>
            <div className="rounded-xl border border-white/5 bg-white/5 px-4 py-3">
              <p className="text-xs uppercase tracking-wide text-mist/60">B</p>
              <p className="font-semibold">Trends</p>
              <p className="text-sm text-mist/80">Top titles & skills from artifacts.</p>
            </div>
            <div className="rounded-xl border border-white/5 bg-white/5 px-4 py-3">
              <p className="text-xs uppercase tracking-wide text-mist/60">C</p>
              <p className="font-semibold">Skill Graph</p>
              <p className="text-sm text-mist/80">Skill pairs / co-occurrence network.</p>
            </div>
            <div className="rounded-xl border border-white/5 bg-white/5 px-4 py-3">
              <p className="text-xs uppercase tracking-wide text-mist/60">D</p>
              <p className="font-semibold">Recommendation demo</p>
              <p className="text-sm text-mist/80">DE/DA/DS with reasons for every match.</p>
            </div>
          </div>
        </div>
        <Card className="h-full">
          <div className="flex h-full flex-col justify-between rounded-2xl bg-gradient-to-br from-accent/20 via-ink to-highlight/10 p-[1px]">
            <div className="h-full rounded-2xl bg-ink/80 p-5">
              <h3 className="font-display text-xl">Why recruiters care</h3>
              <ul className="mt-3 space-y-2 text-sm text-mist/90">
                <li>Data Engineering: canonical schema + dedupe + provenance.</li>
                <li>Data Analytics: KPI + dashboards + insights from artifacts.</li>
                <li>Data Science: TF-IDF recommender + explainability.</li>
                <li>Software: clean structure + docs + reproducibility.</li>
              </ul>
            </div>
          </div>
        </Card>
      </section>

      <section className="mt-8">
        <Card className="flex flex-wrap items-start gap-4 text-sm text-mist/80">
          <Badge>Data sources</Badge>
          <p>
            Kaggle job postings + Remotive API (attribution placeholder). All artifacts load client-side from <code className="text-accent">/public/artifacts</code>.
          </p>
        </Card>
      </section>
    </Container>
  );
}
