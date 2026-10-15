import { useState } from 'react';
import './visual.css';

export type DiagramType = 'osi-layers' | 'tcp-handshake' | 'data-pipeline' | 'network-topology' | 'git-branching' | 'pr-lifecycle' | 'subnetting' | 'tls-handshake';

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

/* ---------------- Git branching & merge ---------------- */
function GitBranching() {
  const W = 620;
  const H = 300;
  const mainY = 210;
  const featY = 80;
  // commit dots on main: A --- B ----------------- E(merge)
  //                        \                       /
  //                         C --- D (feature) ----
  const mainCommits = [70, 170, 550];
  const featCommits = [230, 340, 450];
  return (
    <figure className="visual-diagram">
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Git branching: feature branch diverges from main and merges back">
        <defs>
          <marker id="visual-arrow3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth={6} markerHeight={6} orient="auto-start-reverse">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#39D98A" />
          </marker>
        </defs>
        {/* main branch line */}
        <line x1={40} y1={mainY} x2={580} y2={mainY} stroke="#8B5CF6" strokeWidth={3} />
        {/* feature branch: diverges from B, curves up, runs, merges into E */}
        <path
          d={`M 170 ${mainY} C 200 ${mainY}, 200 ${featY}, 230 ${featY} L 450 ${featY} C 480 ${featY}, 510 ${mainY}, 550 ${mainY}`}
          fill="none"
          stroke="#39D98A"
          strokeWidth={3}
          markerEnd="url(#visual-arrow3)"
        />
        {/* main commits */}
        {mainCommits.map((x, i) => (
          <g key={`m${i}`}>
            <circle cx={x} cy={mainY} r={11} fill="#8B5CF6" stroke="#F5F7FB" strokeWidth={2} />
            <text x={x} y={mainY + 32} textAnchor="middle" className="visual-svg-note" fill="#9AA6BB">
              {['A', 'B', 'E ✓'][i]}
            </text>
          </g>
        ))}
        {/* feature commits */}
        {featCommits.map((x, i) => (
          <g key={`f${i}`}>
            <circle cx={x} cy={featY} r={11} fill="#39D98A" stroke="#F5F7FB" strokeWidth={2} />
            <text x={x} y={featY - 20} textAnchor="middle" className="visual-svg-note" fill="#9AA6BB">
              {['C', 'D', ''][i]}
            </text>
          </g>
        ))}
        {/* branch labels */}
        <text x={40} y={mainY - 14} className="visual-svg-label" fill="#8B5CF6" fontWeight={700}>main</text>
        <text x={470} y={featY - 14} className="visual-svg-label" fill="#39D98A" fontWeight={700}>feature/login</text>
        {/* travelling merge dot: rides the feature curve into main */}
        <circle
          cx={170}
          cy={mainY}
          r={6}
          fill="#E879F9"
          className="visual-git-dot"
        />
        <text x={W / 2} y={H - 12} textAnchor="middle" className="visual-svg-note" fill="#9AA6BB">
          git checkout -b feature/login → work → git merge feature/login
        </text>
      </svg>
      <figcaption className="visual-diagram-cap">
        Branches are cheap pointers — diverge, commit freely, merge back when done.
      </figcaption>
    </figure>
  );
}

/* ---------------- PR lifecycle ---------------- */
const PR_STAGES = [
  { emoji: '📝', name: 'PR Created', desc: 'Push branch, open PR' },
  { emoji: '👀', name: 'Review', desc: 'Teammates comment' },
  { emoji: '🔄', name: 'Changes', desc: 'Address feedback' },
  { emoji: '✅', name: 'Approved', desc: 'Checks pass, +1s in' },
  { emoji: '🎉', name: 'Merged', desc: 'Lands on main' },
];

function PrLifecycle() {
  const W = 620;
  const H = 170;
  const bw = 96;
  const bh = 96;
  const gapX = (W - 5 * bw) / 4;
  return (
    <figure className="visual-diagram">
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Pull request lifecycle: created, review, changes, approved, merged">
        <defs>
          <linearGradient id="visual-pr" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#39D98A" />
            <stop offset="100%" stopColor="#3ED6F2" />
          </linearGradient>
        </defs>
        {PR_STAGES.map((s, i) => {
          const x = i * (bw + gapX);
          const y = (H - bh) / 2 - 8;
          return (
            <g key={s.name}>
              <rect x={x} y={y} width={bw} height={bh} rx={14} fill="url(#visual-pr)" opacity={0.9} />
              <text x={x + bw / 2} y={y + 38} textAnchor="middle" fontSize={26}>
                {s.emoji}
              </text>
              <text x={x + bw / 2} y={y + 64} textAnchor="middle" className="visual-svg-label" fill="#060913" fontWeight={700}>
                {s.name}
              </text>
              <text x={x + bw / 2} y={y + bh + 20} textAnchor="middle" className="visual-svg-note" fill="#9AA6BB">
                {s.desc}
              </text>
              {i < PR_STAGES.length - 1 && (
                <line
                  x1={x + bw + 4}
                  y1={y + bh / 2}
                  x2={x + bw + gapX - 4}
                  y2={y + bh / 2}
                  className="visual-flow-line"
                  stroke="#39D98A"
                  strokeWidth={2.5}
                  markerEnd="url(#visual-arrow2)"
                />
              )}
            </g>
          );
        })}
      </svg>
      <figcaption className="visual-diagram-cap">
        Every pull request flows through review before it earns a place on main.
      </figcaption>
    </figure>
  );
}

/* ---------------- subnetting: /24 split into four /26s ---------------- */
const SUBNETS = [
  { cidr: '192.168.1.0/26', range: '.0 – .63', hosts: '62 hosts', color: '#8B5CF6' },
  { cidr: '192.168.1.64/26', range: '.64 – .127', hosts: '62 hosts', color: '#3ED6F2' },
  { cidr: '192.168.1.128/26', range: '.128 – .191', hosts: '62 hosts', color: '#39D98A' },
  { cidr: '192.168.1.192/26', range: '.192 – .255', hosts: '62 hosts', color: '#F5B84B' },
];

function Subnetting() {
  const [active, setActive] = useState<number | null>(null);
  const W = 460;
  const barY = 46;
  const barH = 54;
  const barX = 14;
  const barW = W - barX * 2;
  const segW = barW / 4;
  return (
    <figure className="visual-diagram">
      <svg viewBox={`0 0 ${W} 150`} role="img" aria-label="192.168.1.0/24 divided into four /26 subnets">
        <text x={barX} y={24} className="visual-svg-label" fill="#E7ECF5" fontWeight={700}>
          192.168.1.0/24 — borrow 2 bits → four /26 subnets
        </text>
        {SUBNETS.map((s, i) => {
          const isActive = active === i;
          return (
            <g
              key={s.cidr}
              onMouseEnter={() => setActive(i)}
              onMouseLeave={() => setActive(null)}
              onClick={() => setActive(isActive ? null : i)}
              style={{ cursor: 'pointer' }}
            >
              <rect
                x={barX + i * segW} y={barY} width={segW - 4} height={barH} rx={10}
                fill={s.color} opacity={isActive ? 1 : 0.82}
              />
              <text x={barX + i * segW + (segW - 4) / 2} y={barY + 24}
                className="visual-svg-note" fill="#060913" fontWeight={800} textAnchor="middle">
                /26
              </text>
              <text x={barX + i * segW + (segW - 4) / 2} y={barY + 42}
                className="visual-svg-note" fill="#060913" textAnchor="middle">
                {s.range}
              </text>
            </g>
          );
        })}
        <text x={barX} y={128} className="visual-svg-note" fill="#9AA6BB">
          block size = 256 − 192 = 64 → subnets at .0, .64, .128, .192
        </text>
      </svg>
      <figcaption className="visual-diagram-cap" aria-live="polite">
        {active !== null ? (
          <>
            <strong>{SUBNETS[active].cidr}:</strong> {SUBNETS[active].range},{' '}
            {SUBNETS[active].hosts} usable (64 addresses − network − broadcast).
          </>
        ) : (
          'Hover or tap a subnet to see its range.'
        )}
      </figcaption>
    </figure>
  );
}

/* ---------------- TLS 1.2 handshake flow ---------------- */
const TLS_STEPS = [
  { from: 'Client', to: 'Server', label: 'ClientHello', desc: 'Offers cipher suites + random Rc.', color: '#8B5CF6' },
  { from: 'Server', to: 'Client', label: 'ServerHello + Certificate', desc: 'Picks cipher, sends random Rs + CA-signed certificate.', color: '#3ED6F2' },
  { from: 'Client', to: 'Server', label: 'ClientKeyExchange', desc: 'Premaster secret encrypted with server public key.', color: '#39D98A' },
  { from: 'Client', to: 'Server', label: 'Finished', desc: 'Both derive session keys — encrypted chat begins.', color: '#F5B84B' },
];

function TlsHandshake() {
  const [active, setActive] = useState<number | null>(null);
  const W = 460;
  const cxC = 90;
  const cxS = W - 90;
  const topY = 30;
  const stepH = 34;
  return (
    <figure className="visual-diagram">
      <svg viewBox={`0 0 ${W} ${topY + TLS_STEPS.length * stepH + 44}`} role="img" aria-label="TLS 1.2 handshake message flow">
        {['Client', 'Server'].map((who, i) => {
          const cx = i === 0 ? cxC : cxS;
          return (
            <g key={who}>
              <circle cx={cx} cy={topY - 8} r={20} fill="#1B2340" stroke="#8B5CF6" strokeWidth={2} />
              <text x={cx} y={topY - 3} textAnchor="middle" className="visual-svg-note" fill="#E7ECF5" fontWeight={700}>
                {who === 'Client' ? '💻' : '🖥️'}
              </text>
              <text x={cx} y={topY + 22} textAnchor="middle" className="visual-svg-label" fill="#9AA6BB">
                {who}
              </text>
              <line x1={cx} y1={topY + 30} x2={cx} y2={topY + TLS_STEPS.length * stepH + 8}
                stroke="#3A4666" strokeDasharray="4 4" />
            </g>
          );
        })}
        {TLS_STEPS.map((s, i) => {
          const y = topY + 34 + i * stepH;
          const ltr = s.from === 'Client';
          const x1 = ltr ? cxC + 6 : cxS - 6;
          const x2 = ltr ? cxS - 6 : cxC + 6;
          const isActive = active === i;
          return (
            <g
              key={s.label}
              onMouseEnter={() => setActive(i)}
              onMouseLeave={() => setActive(null)}
              onClick={() => setActive(isActive ? null : i)}
              style={{ cursor: 'pointer' }}
            >
              <line x1={x1} y1={y} x2={x2} y2={y} stroke={s.color}
                strokeWidth={isActive ? 4 : 2.5} opacity={isActive ? 1 : 0.85} />
              <polygon
                points={ltr ? `${x2},${y} ${x2 - 9},${y - 5} ${x2 - 9},${y + 5}` : `${x2},${y} ${x2 + 9},${y - 5} ${x2 + 9},${y + 5}`}
                fill={s.color}
              />
              <text x={(x1 + x2) / 2} y={y - 7} textAnchor="middle"
                className="visual-svg-note" fill="#E7ECF5" fontWeight={700}>
                {i + 1}. {s.label}
              </text>
            </g>
          );
        })}
      </svg>
      <figcaption className="visual-diagram-cap" aria-live="polite">
        {active !== null ? (
          <>
            <strong>Step {active + 1} — {TLS_STEPS[active].label}:</strong> {TLS_STEPS[active].desc}
          </>
        ) : (
          'Hover or tap a step to see what happens.'
        )}
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
  'git-branching': 'Git Branching & Merge',
  'pr-lifecycle': 'Pull Request Lifecycle',
  'subnetting': 'Subnetting — /24 into four /26s',
  'tls-handshake': 'TLS 1.2 Handshake',
};

export default function ConceptDiagram({ type, title, className = '' }: Props) {
  return (
    <div className={`visual-concept${className ? ` ${className}` : ''}`}>
      <div className="visual-concept-title">{title ?? TITLES[type]}</div>
      {type === 'osi-layers' && <OsiLayers />}
      {type === 'tcp-handshake' && <TcpHandshake />}
      {type === 'data-pipeline' && <DataPipeline />}
      {type === 'network-topology' && <NetworkTopology />}
      {type === 'git-branching' && <GitBranching />}
      {type === 'pr-lifecycle' && <PrLifecycle />}
      {type === 'subnetting' && <Subnetting />}
      {type === 'tls-handshake' && <TlsHandshake />}
    </div>
  );
}
