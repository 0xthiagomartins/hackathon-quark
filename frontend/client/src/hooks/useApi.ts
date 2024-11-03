import axios, { AxiosInstance, AxiosError } from "axios";
import { useAuth } from "../context/AuthContext";

const useApi = (): AxiosInstance => {
    const { token, refreshToken, logout } = useAuth();

    const api = axios.create({
        baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
    });

    console.log("API Base URL:", api.defaults.baseURL);

    const logError = (message: string, data: any) => {
        console.error(message, data);
    };

    api.interceptors.request.use(
        (config) => {
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        },
        (error: AxiosError) => Promise.reject(error)
    );

    api.interceptors.response.use(
        (response) => response,
        async (error: AxiosError) => {
            if (error.response) {
                logError("API Response Error:", error.response.data);

                if (error.response.status === 401) {
                    try {
                        await refreshToken();
                        if (error.config) {
                            return api.request(error.config);
                        }
                    } catch (refreshError) {
                        logError("Token refresh failed:", refreshError);
                        logout();
                        return Promise.reject(refreshError);
                    }
                }
            } else if (error.request) {
                logError("No response received:", error.request);
            } else {
                logError("Axios Error:", error.message);
            }
            return Promise.reject(error);
        }
    );

    return api;
};

export default useApi;