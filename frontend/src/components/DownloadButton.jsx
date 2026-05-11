import styles from "./DownloadButton.module.css";

export default function DownloadButton({ onClick, isLoading }) {
  return (
    <button
      className={styles.button}
      onClick={onClick}
      disabled={isLoading}
    >
      {isLoading ? "Generating..." : "⬇ Download as Word"}
    </button>
  );
}