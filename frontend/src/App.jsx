import { useState } from "react";
import { uploadAudio, summarize, downloadDocx } from "./api/client";
import UploadForm from "./components/UploadForm";
import ResultsPanel from "./components/ResultsPanel";
import DownloadButton from "./components/DownloadButton";
import styles from "./App.module.css";

export default function App() {
  const [transcript, setTranscript] = useState(null);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);

  async function handleUpload(file) {
    setError(null);
    setTranscript(null);
    setSummary(null);
    setIsProcessing(true);

    try {
      const { transcript } = await uploadAudio(file);
      setTranscript(transcript);

      const summary = await summarize(transcript);
      setSummary(summary);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsProcessing(false);
    }
  }

  async function handleDownload() {
    setIsDownloading(true);
    try {
      await downloadDocx(transcript, summary);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsDownloading(false);
    }
  }

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>Meeting Summarizer</h1>
        <p className={styles.subtitle}>Upload a recording and get an instant summary</p>
      </header>

      <main className={styles.main}>
        <UploadForm onUpload={handleUpload} isLoading={isProcessing} />

        {isProcessing && (
          <p className={styles.status}>Processing your recording, please wait...</p>
        )}

        {error && (
          <p className={styles.error}>{error}</p>
        )}

        {summary && transcript && (
          <>
            <DownloadButton onClick={handleDownload} isLoading={isDownloading} />
            <ResultsPanel transcript={transcript} summary={summary} />
          </>
        )}
      </main>
    </div>
  );
}