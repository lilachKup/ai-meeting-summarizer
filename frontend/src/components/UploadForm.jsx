import { useRef } from "react";
import styles from "./UploadForm.module.css";

export default function UploadForm({ onUpload, isLoading }) {
  const inputRef = useRef(null);

  function handleFileChange(e) {
    const file = e.target.files[0];
    if (file) onUpload(file);
  }

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Upload Meeting Recording</h2>
      <p className={styles.subtitle}>Supported formats: mp3, wav</p>
      <button
        className={styles.button}
        onClick={() => inputRef.current.click()}
        disabled={isLoading}
      >
        {isLoading ? "Processing..." : "Choose File"}
      </button>
      <input
        ref={inputRef}
        type="file"
        accept=".mp3,.wav"
        onChange={handleFileChange}
        className={styles.hiddenInput}
      />
    </div>
  );
}