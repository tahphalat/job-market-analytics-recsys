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
          <p className="text-sm text-mist/70">More</p>
          <ul className="mt-2 space-y-2 text-mist/90">
            <li>
              <Link href="/projects/jobscope" className="text-accent underline-offset-4 hover:underline">
                Explore the JobScope dashboard
              </Link>
            </li>
            <li>
              <Link href="/demo" className="text-accent underline-offset-4 hover:underline">
                Watch the recommender demo
              </Link>
            </li>
          </ul>
        </Card>
      </div>
    </Container>
  );
}
