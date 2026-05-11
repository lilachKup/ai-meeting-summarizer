import styles from "./ResultsPanel.module.css";

// Detects if a string is mostly Hebrew/Arabic (RTL)
function detectDirection(text) {
  if (!text) return "ltr";
  const rtlChars = (text.match(/[\u0590-\u05FF\u0600-\u06FF]/g) || []).length;
  return rtlChars > text.length * 0.3 ? "rtl" : "ltr";
}

export default function ResultsPanel({ transcript, summary }) {
  const dir = detectDirection(summary.summary || transcript);

  return (
    <div className={styles.container} dir={dir}>
      <Section title="Summary" dir={dir}>
        <p>{summary.summary}</p>
      </Section>

      <Section title="Participants" dir={dir}>
        <ul>
          {summary.participants.map((p, i) => <li key={i}>{p}</li>)}
        </ul>
      </Section>

      <Section title="Decisions" dir={dir}>
        <ul>
          {summary.decisions.map((d, i) => <li key={i}>{d}</li>)}
        </ul>
      </Section>

      <Section title="Action Items" dir={dir}>
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

      <Section title="Full Transcript" dir={detectDirection(transcript)}>
        <p className={styles.transcript}>{transcript}</p>
      </Section>
    </div>
  );
}

function Section({ title, children, dir }) {
  return (
    <div className={styles.section} dir={dir}>
      <h3 className={styles.sectionTitle} dir={dir}>{title}</h3>
      {children}
    </div>
  );
}
