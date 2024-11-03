"use client";

import { useState } from "react";
import useApi from "../../../hooks/useApi";

export default function ImportOperations() {
  const api = useApi();
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a file to import.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      await api.post("/operations/import", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setMessage("Operations imported successfully!");
      setFile(null);
    } catch (err: any) {
      setMessage("Failed to import operations.");
      console.error(err);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-background">
      <form
        onSubmit={handleSubmit}
        className="bg-foreground p-6 rounded shadow-md w-full max-w-md"
      >
        <h2 className="text-2xl mb-4 text-center text-primary">Import Operations</h2>
        {message && <p className="mb-4 text-center">{message}</p>}
        <div className="mb-4">
          <label className="block mb-1">Select File</label>
          <input
            type="file"
            accept=".csv, .xlsx"
            onChange={handleFileChange}
            className="w-full border border-secondary px-3 py-2 rounded"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-primary text-white py-2 rounded hover:bg-accent"
        >
          Import
        </button>
      </form>
    </div>
  );
} 