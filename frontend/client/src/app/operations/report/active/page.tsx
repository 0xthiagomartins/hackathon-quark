"use client";

import { useState } from "react";
import useApi from "../../../../hooks/useApi";

export default function ActiveOperationsReport() {
  const api = useApi();
  const [report, setReport] = useState<string>("");
  const [error, setError] = useState("");

  const generateReport = async () => {
    try {
      const response = await api.get("/operations/report/active");
      setReport(response.data);
    } catch (err: any) {
      setError("Failed to generate report.");
      console.error(err);
    }
  };

  return (
    <div className="p-8 bg-background text-foreground">
      <h1 className="text-3xl mb-4 text-primary">Active Operations Report</h1>
      <button
        onClick={generateReport}
        className="mb-4 bg-primary text-white px-4 py-2 rounded hover:bg-accent"
      >
        Generate Report
      </button>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      {report && (
        <div className="whitespace-pre-wrap bg-foreground p-4 rounded">
          {report}
        </div>
      )}
    </div>
  );
} 