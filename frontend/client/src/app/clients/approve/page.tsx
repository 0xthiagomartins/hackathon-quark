"use client";

import { useState } from "react";
import useApi from "../../../hooks/useApi";

export default function ApproveClients() {
  const api = useApi();
  const [message, setMessage] = useState("");

  const handleApprove = async () => {
    try {
      await api.patch("/clients/import");
      setMessage("Clients approved successfully!");
    } catch (err: any) {
      setMessage("Failed to approve clients.");
      console.error(err);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-background">
      <div className="bg-foreground p-6 rounded shadow-md w-full max-w-md text-center">
        <h2 className="text-2xl mb-4 text-primary">Approve Clients</h2>
        {message && <p className="mb-4">{message}</p>}
        <button
          onClick={handleApprove}
          className="w-full bg-accent text-white py-2 rounded hover:bg-primary"
        >
          Approve Clients
        </button>
      </div>
    </div>
  );
} 