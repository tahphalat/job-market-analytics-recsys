import Link from 'next/link';
import { Container } from '../../components/Container';
import { SectionTitle } from '../../components/SectionTitle';
import { Card } from '../../components/Card';
import { Badge } from '../../components/Badge';
import { Button } from '../../components/Button';

export default function ContactPage() {
  return (
    <Container className="pb-12 pt-10 lg:pt-14 space-y-6">
      <div className="space-y-3">
        <Badge>Contact</Badge>
        <h1 className="font-display text-4xl">Let&apos;s talk</h1>
        <p className="text-mist/80">
          Data engineering, analytics, and full-stack. Open to internships or collabs — quick replies.
        </p>
      </div>

      <Card className="space-y-4">
        <SectionTitle title="Find me" subtitle="Reach me through the links below." />
        <div className="flex flex-wrap items-center gap-3">
          <Button href="https://github.com/phalat.tah" target="_blank" rel="noreferrer">
            GitHub
          </Button>
          <Button href="https://www.linkedin.com/in/phalat-lorratthanan-b1a669323/" variant="ghost" target="_blank" rel="noreferrer">
            LinkedIn
          </Button>
          <Link href="mailto:phalat.tah@gmail.com" className="text-accent underline-offset-4 hover:underline">
            phalat.tah@gmail.com
          </Link>
        </div>
      </Card>
    </Container>
  );
}
