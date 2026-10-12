export default function Placeholder({ title, note }: { title: string; note: string }) {
  return (
    <div>
      <h1 className="page-title">{title}</h1>
      <p className="page-sub">{note}</p>
      <div className="card">
        <p className="coming" style={{ marginTop: 0 }}>
          This section is on the build roadmap — coming in a later slice.
        </p>
      </div>
    </div>
  );
}
