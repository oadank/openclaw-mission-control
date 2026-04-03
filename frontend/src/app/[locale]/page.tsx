import { LandingHero } from '@/components/organisms/LandingHero';
import { LandingShell } from '@/components/templates/LandingShell';

export default function HomePage() {
  return (
    <LandingShell>
      <LandingHero />
    </LandingShell>
  );
}
