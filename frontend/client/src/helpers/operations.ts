import axios, { AxiosInstance } from "axios";
import { useAuth } from "../context/AuthContext";
import { Tokens } from "../types/api";

export const importOperations = async (api: AxiosInstance, file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await api.post("/operations/import", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const approveOperations = async (api: AxiosInstance) => {
    try {
        const response = await api.patch("/operations/import");
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const generateActiveOperationsReport = async (api: AxiosInstance) => {
    try {
        const response = await api.get("/operations/report/active");
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const generateCurrentOperationsReport = async (api: AxiosInstance) => {
    try {
        const response = await api.get("/operations/report/current");
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const importClients = async (api: AxiosInstance, file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await api.post("/clients/import", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const approveClients = async (api: AxiosInstance) => {
    try {
        const response = await api.patch("/clients/import");
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const generateClientsReport = async (api: AxiosInstance) => {
    try {
        const response = await api.get("/clients/report");
        return response.data;
    } catch (error) {
        throw error;
    }
};