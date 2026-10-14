import { useState } from 'react';
import './visual.css';

export type DiagramType = 'osi-layers' | 'tcp-handshake' | 'data-pipeline' | 'network-topology';

interface Props {
  type: DiagramType;
  /** Optional caption shown above the diagram. */
  title?: string;
  className?: string;
}

/* ---------------- OSI 7 layers ---------------- */
const OSI = [
  { n: 7, name: 'Application', desc: 'What you use every day: HTTP, DNS, email, APIs.', color: '#8B5CF6' },
  { n: 6, name: 'Presentation', desc: 'Data formats, encryption (TLS) and compression.', color: '#A78BFA' },
  { n: 5, name: 'Session', desc: 'Opens, manages and closes connections between apps.', color: '#E879F9' },
  { n: 4, name: 'Transport', desc: 'TCP/UDP: reliable delivery, ports and flow control.', color: '#3ED6F2' },
  { n: 3, name: 'Network', desc: 'Packets, IP addresses and routing across networks.', color: '#39D98A' },
  { n: 2, name: 'Data Link', desc: 'Frames, MAC addresses; switches on the local network.', color: '#F5B84B' },
  { n: 1, name: 'Physical', desc: 'Raw bits as electrical, light or radio signals.', color: '#7C8DB0' },
];

function OsiLayers() {
  const [active, setActive] = useState<number | null>(null);
  const W = 400;
  const rowH = 46;
  const gap = 8;
  const top = 10;
  const x = 60;
  const w = W - x - 70;
  return (
    <figure className="visual-diagram">
      <svg viewBox={`0 0 ${W} ${top * 2 + 7 * rowH + 6 * gap}`} role="img" aria-label="OSI model: seven stacked layers">
        {OSI.map((l, i) => {
          const y = top + i * (rowH + gap);
          const isActive = active === l.n;
          return (
            <g
              key={l.n}
              className={`visual-osi-layer${isActive ? ' is-active' : ''}`}
              onMouseEnter={() => setActive(l.n)}
              onMouseLeave={() => setActive(null)}
              onClick={() => setActive(isActive ? null : l.n)}
              style={{ cursor: 'pointer' }}
            >
              <rect x={x} y={y} width={w} height={rowH} rx={10} fill={l.color} opacity={isActive ? 1 : 0.82} />
              <text x={x + 14} y={y + rowH / 2 + 5} className="visual-svg-num" fill="#060913" fontWeight={800}>
                {l.n}
              </text>
              <text x={x + 44} y={y + rowH / 2 + 5} className="visual-svg-label" fill="#060913" fontWeight={700}>
                {l.name}
              </text>
              {i < 4 ? (
                <text x={x + w + 10} y={y + rowH / 2 + 4} className="visual-svg-note" fill="#9AA6BB">
                  host
                </text>
              ) : (
                <text x={x + w + 10} y={y + rowH / 2 + 4} className="visual-svg-note" fill="#9AA6BB">
                  media
                </text>
              )}
            </g>
          );
        })}
      </svg>
      <figcaption className="visual-diagram-cap" aria-live="polite">
        {active ? (
          <>
            <strong>Layer {active} — {OSI.find((l) => l.n === active)?.name}:</strong>{' '}
            {OSI.find((l) => l.n === active)?.desc}
          </>
        ) : (
          'Hover or tap a layer to see what it does.'
        )}
      </figcaption>
    </figure>
  );
}

/* ---------------- TCP 3-way handshake ---------------- */
function TcpHandshake() {
  const W = 480;
  const H = 250;
  const cx = 78;
  const sx = W - 78;
  const rows = [
    { y: 66, from: cx, to: sx, label: 'SYN', sub: 'Can we talk?', delay: '0s' },
    { y: 128, from: sx, to: cx, label: 'SYN + ACK', sub: 'Yes, can you?', delay: '1.1s' },
    { y: 190, from: cx, to: sx, label: 'ACK', sub: "Let's talk!", delay: '2.2s' },
  ];
  return (
    <figure className="visual-diagram">
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label="TCP three-way handshake: SYN, SYN-ACK, ACK">
        <defs>
          <marker id="visual-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#3ED6F2" />
          </marker>
        </defs>
        {/* nodes */}
        {[
          { x: cx, label: 'Client', emoji: '💻' },
          { x: sx, label: 'Server', emoji: '🖥️' },
        ].map((n) => (
          <g key={n.label}>
            <circle cx={n.x} cy={H / 2} r={34} className="visual-node" />
            <text x={n.x} y={H / 2 + 2} textAnchor="middle" fontSize={22}>
              {n.emoji}
            </text>
            <text x={n.x} y={H / 2 + 54} textAnchor="middle" className="visual-svg-label" fill="#F5F7FB">
              {n.label}
            </text>
          </g>
        ))}
        {/* arrows + travelling dots */}
        {rows.map((r) => {
          const leftToRight = r.from < r.to;
          const x1 = r.from + (leftToRight ? 40 : -40);
          const x2 = r.to + (leftToRight ? -40 : 40);
          const dist = Math.abs(x2 - x1);
          return (
            <g key={r.label}>
              <line x1={x1} y1={r.y} x2={x2} y2={r.y} stroke="#3ED6F2" strokeWidth={2} opacity={0.45} markerEnd="url(#visual-arrow)" />
              <text x={(x1 + x2) / 2} y={r.y - 10} textAnchor="middle" className="visual-svg-label" fill="#3ED6F2" fontWeight={700}>
                {r.label}
              </text>
              <text x={(x1 + x2) / 2} y={r.y + 18} textAnchor="middle" className="visual-svg-note" fill="#9AA6BB">
                {r.sub}
              </text>
              <circle
                cx={x1}
                cy={r.y}
                r={5}
                fill="#E879F9"
                className="visual-tcp-dot"
                style={{ ['--travel' as string]: `${leftToRight ? dist : -dist}px`, animationDelay: r.delay }}
              />
            </g>
          );
        })}
      </svg>
      <figcaption className="visual-diagram-cap">
        Three packets open every TCP connection — the dots replay the handshake forever.
      </figcaption>
    </figure>
  );
}

/* ---------------- Data pipeline ---------------- */
const STAGES = [
  { emoji: '📥', name: 'Collect', desc: 'Gather raw data' },
  { emoji: '🧹', name: 'Clean', desc: 'Fix missing values' },
  { emoji: '📊', name: 'Analyze', desc: 'Find patterns' },
  { emoji: '📈', name: 'Visualize', desc: 'Charts & dashboards' },
  { emoji: '✅', name: 'Decide', desc: 'Act on insights' },
];

function DataPipeline() {
  const W = 620;
  const H = 170;
  const bw = 96;
  const bh = 96;
  const gapX = (W - 5 * bw) / 4;
  return (
    <figure className="visual-diagram">
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Data pipeline: collect, clean, analyze, visualize, decide">
        <defs>
          <marker id="visual-arrow2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#8B5CF6" />
          </marker>
          <linearGradient id="visual-stage" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#8B5CF6" />
            <stop offset="100%" stopColor="#3ED6F2" />
          </linearGradient>
        </defs>
        {STAGES.map((s, i) => {
          const x = i * (bw + gapX);
          const y = (H - bh) / 2 - 8;
          return (
            <g key={s.name}>
              <rect x={x} y={y} width={bw} height={bh} rx={14} fill="url(#visual-stage)" opacity={0.9} />
              <text x={x + bw / 2} y={y + 38} textAnchor="middle" fontSize={26}>
                {s.emoji}
              </text>
              <text x={x + bw / 2} y={y + 64} textAnchor="middle" className="visual-svg-label" fill="#060913" fontWeight={700}>
                {s.name}
              </text>
              <text x={x + bw / 2} y={y + bh + 20} textAnchor="middle" className="visual-svg-note" fill="#9AA6BB">
                {s.desc}
              </text>
              {i < STAGES.length - 1 && (
                <line
                  x1={x + bw + 4}
                  y1={y + bh / 2}
                  x2={x + bw + gapX - 4}
                  y2={y + bh / 2}
                  className="visual-flow-line"
                  stroke="#8B5CF6"
                  strokeWidth={2.5}
                  markerEnd="url(#visual-arrow2)"
                />
              )}
            </g>
          );
        })}
      </svg>
      <figcaption className="visual-diagram-cap">
        Raw data becomes decisions in five flowing steps.
      </figcaption>
    </figure>
  );
}

/* ---------------- Star network topology ---------------- */
const NODES = [
  { label: 'Laptop', emoji: '💻' },
  { label: 'Phone', emoji: '📱' },
  { label: 'Server', emoji: '🖥️' },
  { label: 'Printer', emoji: '🖨️' },
  { label: 'TV', emoji: '📺' },
  { label: 'IoT', emoji: '💡' },
];

function NetworkTopology() {
  const W = 420;
  const H = 360;
  const hx = W / 2;
  const hy = H / 2;
  const R = 125;
  return (
    <figure className="visual-diagram">
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Star network topology: devices connected to a central router">
        {NODES.map((n, i) => {
          const a = (i / NODES.length) * Math.PI * 2 - Math.PI / 2;
          const x = hx + R * Math.cos(a);
          const y = hy + R * Math.sin(a);
          return (
            <g key={n.label}>
              <line x1={hx} y1={hy} x2={x} y2={y} stroke="#3ED6F2" strokeWidth={1.5} opacity={0.35} />
              <circle cx={x} cy={y} r={22} className="visual-node" style={{ animationDelay: `${i * 0.25}s` }} />
              <text x={x} y={y + 1} textAnchor="middle" fontSize={18}>
                {n.emoji}
              </text>
              <text
                x={x}
                y={y + 38}
                textAnchor="middle"
                className="visual-svg-note"
                fill="#9AA6BB"
              >
                {n.label}
              </text>
            </g>
          );
        })}
        {/* hub pulse rings */}
        <circle cx={hx} cy={hy} r={30} fill="none" stroke="#8B5CF6" strokeWidth={2} className="visual-pulse" />
        <circle cx={hx} cy={hy} r={30} fill="none" stroke="#8B5CF6" strokeWidth={2} className="visual-pulse visual-pulse-2" />
        {/* hub */}
        <circle cx={hx} cy={hy} r={30} className="visual-hub" />
        <text x={hx} y={hy + 2} textAnchor="middle" fontSize={24}>
          📡
        </text>
        <text x={hx} y={hy + 50} textAnchor="middle" className="visual-svg-label" fill="#F5F7FB" fontWeight={700}>
          Router
        </text>
      </svg>
      <figcaption className="visual-diagram-cap">
        Every device talks through the central router — one cable fails, the rest keep working.
      </figcaption>
    </figure>
  );
}

/* ---------------- main component ---------------- */
const TITLES: Record<DiagramType, string> = {
  'osi-layers': 'OSI Model — 7 Layers',
  'tcp-handshake': 'TCP 3-Way Handshake',
  'data-pipeline': 'Data Pipeline',
  'network-topology': 'Star Network Topology',
};

export default function ConceptDiagram({ type, title, className = '' }: Props) {
  return (
    <div className={`visual-concept${className ? ` ${className}` : ''}`}>
      <div className="visual-concept-title">{title ?? TITLES[type]}</div>
      {type === 'osi-layers' && <OsiLayers />}
      {type === 'tcp-handshake' && <TcpHandshake />}
      {type === 'data-pipeline' && <DataPipeline />}
      {type === 'network-topology' && <NetworkTopology />}
    </div>
  );
}
