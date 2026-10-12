import './dashboard.css';

/** Skeleton placeholder used while a dashboard section loads. */
export function Load({ label }: { label: string }) {
  return (
    <div role="status" aria-label={`${label} loading`}>
      <div className="sf-skel" />
      <span style={{ position: 'absolute', width: 1, height: 1, overflow: 'hidden', clip: 'rect(0 0 0 0)' }}>
        Loading {label}…
      </span>
    </div>
  );
}

/** Error box with a retry action, used by every dashboard section. */
export function ErrBox({ message, onRetry }: { message: string; onRetry: () => void }) {
  return (
    <div className="sf-error" role="alert">
      <div>{message}</div>
      <div className="sf-err-sub">The backend did not answer this request.</div>
      <button className="sf-btn-ghost sf-retry" onClick={onRetry}>
        Try again
      </button>
    </div>
  );
}

/** Small colored dot. */
export function Dot({ color }: { color: string }) {
  return <span className="sf-dot" style={{ background: color }} />;
}
