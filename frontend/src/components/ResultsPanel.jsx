import styles from "./ResultsPanel.module.css";

export default function ResultsPanel({ transcript, summary }) {
  return (
    <div className={styles.container}>
      <Section title="Summary">
        <p>{summary.summary}</p>
      </Section>

      <Section title="Participants">
        <ul>
          {summary.participants.map((p, i) => <li key={i}>{p}</li>)}
        </ul>
      </Section>

      <Section title="Decisions">
        <ul>
          {summary.decisions.map((d, i) => <li key={i}>{d}</li>)}
        </ul>
      </Section>

      <Section title="Action Items">
        <ul>
          {summary.action_items.map((item, i) => (
            <li key={i}>
              <span className={styles.task}>{item.task}</span>
              {item.owner && (
                <span className={styles.owner}> — {item.owner}</span>
              )}
            </li>
          ))}
        </ul>
      </Section>

      <Section title="Full Transcript">
        <p className={styles.transcript}>{transcript}</p>
      </Section>
    </div>
  );
}

function Section({ title, children }) {
  return (
    <div className={styles.section}>
      <h3 className={styles.sectionTitle}>{title}</h3>
      {children}
    </div>
  );
}