import Link from 'next/link';
import { Container } from '../../components/Container';
import { SectionTitle } from '../../components/SectionTitle';
import { Card } from '../../components/Card';
import { Badge } from '../../components/Badge';

export default function ContactPage() {
  return (
    <Container className="pb-12 pt-10 lg:pt-14">
      <div className="space-y-3">
        <Badge>Contact</Badge>
        <h1 className="font-display text-4xl">Let&apos;s talk hiring signals</h1>
        <p className="text-mist/80">
          Quick response for collaborations, product feedback, or roles that need a fast data-read of the market.
        </p>
      </div>

      <div className="mt-8 grid gap-4">
        <Card>
          <p className="text-sm text-mist/70">Email</p>
          <Link href="mailto:jobscope@demo.work" className="mt-2 inline-flex items-center text-lg font-semibold text-accent hover:underline">
            jobscope@demo.work
          </Link>
          <p className="mt-2 text-sm text-mist/70">Typical response: &lt;24h | Timezone: GMT+7</p>
        </Card>
        <Card>
          <SectionTitle title="Contact form" subtitle="No backend — feel free to email directly." />
          <form className="mt-3 grid gap-3">
            <div className="grid gap-1">
              <label className="text-sm text-mist/70">Name</label>
              <input className="rounded-lg border border-white/10 bg-ink/80 px-3 py-2 text-sm text-cloud" placeholder="Your name" />
            </div>
            <div className="grid gap-1">
              <label className="text-sm text-mist/70">Email</label>
              <input className="rounded-lg border border-white/10 bg-ink/80 px-3 py-2 text-sm text-cloud" placeholder="you@example.com" />
            </div>
            <div className="grid gap-1">
              <label className="text-sm text-mist/70">Message</label>
              <textarea className="rounded-lg border border-white/10 bg-ink/80 px-3 py-2 text-sm text-cloud" rows={4} placeholder="How can I help?" />
            </div>
            <button type="button" className="rounded-full bg-gradient-to-r from-accent to-highlight px-4 py-2 text-sm font-semibold text-ink shadow-glow">
              Send (opens email)
            </button>
          </form>
          <p className="mt-3 text-sm text-mist/70">
            Or email directly: <Link href="mailto:jobscope@demo.work" className="text-accent underline">jobscope@demo.work</Link>
          </p>
          <div className="mt-3 text-sm text-mist/60">
            Artifacts not found? Run <code className="text-accent">make run_all && make export_web</code> then refresh /projects/jobscope.
          </div>
        </Card>
      </div>
    </Container>
  );
}
