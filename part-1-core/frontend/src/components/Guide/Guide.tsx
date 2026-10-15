import { useCallback, useState } from 'react';
import GuideButton from './GuideButton';
import GuidePanel from './GuidePanel';
import GuideTour from './GuideTour';
import './Guide.css';

/* Guide root: floating button + chat panel + product tour.
   Mount once near the app root (e.g. inside AppShell) — parent wires nothing. */
export default function Guide() {
  const [open, setOpen] = useState(false);
  const [touring, setTouring] = useState(false);

  const toggle = useCallback(() => setOpen((o) => !o), []);
  const close = useCallback(() => setOpen(false), []);
  const startTour = useCallback(() => {
    setOpen(false);
    setTouring(true);
  }, []);
  const endTour = useCallback(() => setTouring(false), []);

  return (
    <>
      <GuideButton open={open} onToggle={toggle} />
      {open && !touring && <GuidePanel onStartTour={startTour} onClose={close} />}
      {touring && <GuideTour onDone={endTour} />}
    </>
  );
}
