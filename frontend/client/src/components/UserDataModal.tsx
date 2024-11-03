"use client";

import * as Dialog from "@radix-ui/react-dialog";
import { useState, useEffect } from "react";
import useApi from "../hooks/useApi";
import Loader from "./Loader";
import Button from "./Button";

interface User {
    id: number;
    name: string;
    email: string;
    role_id: number;
}

export default function UserDataModal() {
    const api = useApi();
    const [open, setOpen] = useState(false);
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const fetchUserData = async () => {
        setLoading(true);
        setError("");
        try {
            const response = await api.get("/users/me");
            setUser(response.data);
        } catch (err: any) {
            setError("Failed to fetch user data.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (open) {
            fetchUserData();
        }
    }, [open]);

    return (
        <Dialog.Root open={open} onOpenChange={setOpen}>
            <Dialog.Trigger asChild>
                <Button label="User Data" className="text-secondary hover:text-primary" />
            </Dialog.Trigger>
            <Dialog.Portal>
                <Dialog.Overlay className="fixed inset-0 bg-black bg-opacity-30" />
                <Dialog.Content className="fixed bg-foreground text-foreground p-6 rounded shadow-lg top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 max-w-md w-full">
                    <Dialog.Title className="text-2xl text-primary">User Information</Dialog.Title>
                    <Dialog.Description className="mt-2 text-gray-500">Details about the current user.</Dialog.Description>
                    <div className="mt-4">
                        {loading ? (
                            <Loader />
                        ) : error ? (
                            <p className="text-red-500">{error}</p>
                        ) : user ? (
                            <div>
                                <p><strong>Name:</strong> {user.name}</p>
                                <p><strong>Email:</strong> {user.email}</p>
                                <p><strong>Role ID:</strong> {user.role_id}</p>
                            </div>
                        ) : (
                            <p>No user data available.</p>
                        )}
                    </div>
                    <Dialog.Close asChild>
                        <Button label="Close" className="mt-4 bg-secondary text-white px-4 py-2 rounded hover:bg-accent" />
                    </Dialog.Close>
                </Dialog.Content>
            </Dialog.Portal>
        </Dialog.Root>
    );
} 