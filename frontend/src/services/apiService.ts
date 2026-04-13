import axios, { AxiosError } from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const uploadFiles = async (files: File[]) => {
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));

    try {
        const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        const err = error as AxiosError<any>;

        throw new Error(
            `Upload failed: ${err.response?.data?.detail || err.message}`
        );
    }
};

export const fetchInsights = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/insights`);
        return response.data;
    } catch (error) {
        const err = error as AxiosError<any>;

        throw new Error(
            `Insights fetch failed: ${err.response?.data?.detail || err.message}`
        );
    }
};