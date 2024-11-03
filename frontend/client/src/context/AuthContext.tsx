"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import useApi from "../hooks/useApi";

interface AuthContextType {
    token: string | null;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
    refreshToken: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({
    token: null,
    login: async () => { },
    logout: () => { },
    refreshToken: async () => { },
});

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const api = useApi();
    const [token, setToken] = useState<string | null>(() => {
        return typeof window !== "undefined" ? localStorage.getItem("token") : null;
    });

    useEffect(() => {
        if (token) {
            localStorage.setItem("token", token);
        } else {
            localStorage.removeItem("token");
        }
    }, [token]);

    const login = async (email: string, password: string) => {
        try {
            const response = await api.post("/auth", { email, password });
            setToken(response.data.access_token);
        } catch (error) {
            throw error;
        }
    };

    const logout = () => {
        setToken(null);
    };

    const refreshToken = async () => {
        try {
            const response = await api.patch("/auth");
            setToken(response.data.access_token);
        } catch (error) {
            throw error;
        }
    };

    return (
        <AuthContext.Provider value={{ token, login, logout, refreshToken }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);