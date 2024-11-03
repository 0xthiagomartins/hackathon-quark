"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import useApi from "../../../hooks/useApi";

interface User {
    id: number;
    name: string;
    email: string;
    role_id: number;
}

export default function UserManagement() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const roleId = searchParams.get("role_id") || "1";
    const api = useApi();
    const [users, setUsers] = useState<User[]>([]);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await api.get(`/users/${roleId}`);
                setUsers(response.data);
            } catch (err: any) {
                setError("Failed to fetch users.");
                console.error(err);
            }
        };

        fetchUsers();
    }, [api, roleId]);

    return (
        <div className="p-8 bg-background text-foreground">
            <h1 className="text-3xl mb-4 text-primary">User Management</h1>
            {error && <p className="text-red-500 mb-4">{error}</p>}
            <table className="min-w-full bg-foreground">
                <thead>
                    <tr>
                        <th className="py-2 px-4 bg-secondary text-left">ID</th>
                        <th className="py-2 px-4 bg-secondary text-left">Name</th>
                        <th className="py-2 px-4 bg-secondary text-left">Email</th>
                        <th className="py-2 px-4 bg-secondary text-left">Role ID</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map((user) => (
                        <tr key={user.id} className="border-t border-secondary">
                            <td className="py-2 px-4">{user.id}</td>
                            <td className="py-2 px-4">{user.name}</td>
                            <td className="py-2 px-4">{user.email}</td>
                            <td className="py-2 px-4">{user.role_id}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
} 