"use client";

import { useState } from "react";
import useApi from "../../hooks/useApi";
import Loader from "../../components/Loader";
import Button from "../../components/Button";

export default function Operations() {
    const api = useApi();

    const [importFile, setImportFile] = useState<File | null>(null);
    const [importMessage, setImportMessage] = useState<string>("");

    const [approveMessage, setApproveMessage] = useState<string>("");

    const [activeReport, setActiveReport] = useState<string>("");
    const [activeReportError, setActiveReportError] = useState<string>("");
    const [currentReport, setCurrentReport] = useState<string>("");
    const [currentReportError, setCurrentReportError] = useState<string>("");

    // Import Operations Handler
    const handleImport = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!importFile) {
            setImportMessage("Please select a file to import.");
            return;
        }

        const formData = new FormData();
        formData.append("file", importFile);

        try {
            await api.post("/operations/import", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            setImportMessage("Operations imported successfully!");
            setImportFile(null);
        } catch (err: any) {
            setImportMessage("Failed to import operations.");
            console.error(err);
        }
    };

    const handleApprove = async () => {
        try {
            await api.patch("/operations/import");
            setApproveMessage("Operations approved successfully!");
        } catch (err: any) {
            setApproveMessage("Failed to approve operations.");
            console.error(err);
        }
    };

    const handleGenerateActiveReport = async () => {
        try {
            const response = await api.get("/operations/report/active");
            setActiveReport(response.data);
            setActiveReportError("");
        } catch (err: any) {
            setActiveReportError("Failed to generate active operations report.");
            console.error(err);
        }
    };

    const handleGenerateCurrentReport = async () => {
        try {
            const response = await api.get("/operations/report/current");
            setCurrentReport(response.data);
            setCurrentReportError("");
        } catch (err: any) {
            setCurrentReportError("Failed to generate current operations report.");
            console.error(err);
        }
    };

    return (
        <div className="p-8 bg-background text-foreground">
            <h1 className="text-3xl mb-6 text-primary">Operations Management</h1>

            <section className="mb-8">
                <h2 className="text-2xl mb-4 text-secondary">Import Operations</h2>
                <form onSubmit={handleImport} className="bg-foreground p-4 rounded shadow-md">
                    <input
                        type="file"
                        accept=".csv, .xlsx"
                        onChange={(e) => setImportFile(e.target.files ? e.target.files[0] : null)}
                        className="mb-4 w-full"
                        required
                    />
                    <Button type="submit" label="Import Operations" className="w-full" />
                </form>
                {importMessage && (
                    <p className={`mt-2 ${importMessage.includes("Failed") ? "text-red-500" : "text-green-500"}`}>
                        {importMessage}
                    </p>
                )}
            </section>

            <section className="mb-8">
                <h2 className="text-2xl mb-4 text-secondary">Approve Operations</h2>
                <Button onClick={handleApprove} label="Approve Operations" className="bg-accent text-white px-4 py-2 rounded hover:bg-primary" />
                {approveMessage && (
                    <p className={`mt-2 ${approveMessage.includes("Failed") ? "text-red-500" : "text-green-500"}`}>
                        {approveMessage}
                    </p>
                )}
            </section>

            <section className="mb-8">
                <h2 className="text-2xl mb-4 text-secondary">Active Operations Report</h2>
                <Button onClick={handleGenerateActiveReport} label="Generate Active Report" className="bg-primary text-white px-4 py-2 rounded hover:bg-accent mb-4" />
                {activeReportError && <p className="text-red-500 mb-4">{activeReportError}</p>}
                {activeReport && (
                    <pre className="whitespace-pre-wrap bg-foreground p-4 rounded">{activeReport}</pre>
                )}
            </section>

            <section>
                <h2 className="text-2xl mb-4 text-secondary">Current Operations Report</h2>
                <Button onClick={handleGenerateCurrentReport} label="Generate Current Report" className="bg-primary text-white px-4 py-2 rounded hover:bg-accent mb-4" />
                {currentReportError && <p className="text-red-500 mb-4">{currentReportError}</p>}
                {currentReport && (
                    <pre className="whitespace-pre-wrap bg-foreground p-4 rounded">{currentReport}</pre>
                )}
            </section>
        </div>
    );
} 