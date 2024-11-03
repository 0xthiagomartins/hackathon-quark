"use client";

import { useState } from "react";
import useApi from "../../hooks/useApi";
import Loader from "../../components/Loader";
import Button from "../../components/Button";
import { importClients, approveClients, generateClientsReport } from "../../helpers/operations";

export default function Clients() {
    const api = useApi();

    // States for Import Clients
    const [importFile, setImportFile] = useState<File | null>(null);
    const [importMessage, setImportMessage] = useState<string>("");

    // States for Approve Clients
    const [approveMessage, setApproveMessage] = useState<string>("");

    // States for Generate Clients Report
    const [report, setReport] = useState<string>("");
    const [reportError, setReportError] = useState<string>("");

    // Import Clients Handler
    const handleImport = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!importFile) {
            setImportMessage("Please select a file to import.");
            return;
        }

        try {
            await importClients(api, importFile);
            setImportMessage("Clients imported successfully!");
            setImportFile(null);
        } catch (err: any) {
            if (err.response) {
                // Server responded with a status other than 2xx
                setImportMessage(`Import failed: ${err.response.data.message || "Server Error"}`);
            } else if (err.request) {
                // Request was made but no response received
                setImportMessage("Import failed: No response from server.");
            } else {
                // Something else happened
                setImportMessage(`Import failed: ${err.message}`);
            }
            console.error(err);
        }
    };

    // Approve Clients Handler
    const handleApprove = async () => {
        try {
            await approveClients(api);
            setApproveMessage("Clients approved successfully!");
        } catch (err: any) {
            setApproveMessage("Failed to approve clients.");
            console.error(err);
        }
    };

    // Generate Clients Report Handler
    const handleGenerateReport = async () => {
        try {
            const data = await generateClientsReport(api);
            setReport(data);
            setReportError("");
        } catch (err: any) {
            setReportError("Failed to generate report.");
            console.error(err);
        }
    };

    return (
        <div className="p-8 bg-background text-foreground">
            <h1 className="text-3xl mb-6 text-primary">Clients Management</h1>

            {/* Import Clients Section */}
            <section className="mb-8">
                <h2 className="text-2xl mb-4 text-secondary">Import Clients</h2>
                <form onSubmit={handleImport} className="bg-foreground p-4 rounded shadow-md">
                    <input
                        type="file"
                        accept=".csv, .xlsx"
                        onChange={(e) => setImportFile(e.target.files ? e.target.files[0] : null)}
                        className="mb-4 w-full"
                        required
                    />
                    <Button type="submit" label="Import Clients" className="w-full" />
                </form>
                {importMessage && (
                    <p className={`mt-2 ${importMessage.includes("Failed") ? "text-red-500" : "text-green-500"}`}>
                        {importMessage}
                    </p>
                )}
            </section>

            {/* Approve Clients Section */}
            <section className="mb-8">
                <h2 className="text-2xl mb-4 text-secondary">Approve Clients</h2>
                <Button onClick={handleApprove} label="Approve Clients" className="bg-accent text-white px-4 py-2 rounded hover:bg-primary" />
                {approveMessage && (
                    <p className={`mt-2 ${approveMessage.includes("Failed") ? "text-red-500" : "text-green-500"}`}>
                        {approveMessage}
                    </p>
                )}
            </section>

            {/* Generate Clients Report Section */}
            <section>
                <h2 className="text-2xl mb-4 text-secondary">Generate Clients Report</h2>
                <Button onClick={handleGenerateReport} label="Generate Report" className="bg-primary text-white px-4 py-2 rounded hover:bg-accent mb-4" />
                {reportError && <p className="text-red-500 mb-4">{reportError}</p>}
                {report && (
                    <pre className="whitespace-pre-wrap bg-foreground p-4 rounded">{report}</pre>
                )}
            </section>
        </div>
    );
} 