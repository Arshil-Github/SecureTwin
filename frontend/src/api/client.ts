// frontend/src/api/client.ts
import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const baseURL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';
console.log('API Client: Using baseURL', baseURL);

const client = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

client.interceptors.request.use(async (config) => {
  const token = await SecureStore.getItemAsync('userToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      await SecureStore.deleteItemAsync('userToken');
      // TODO: Redirect to login
    }
    return Promise.reject(error);
  }
);

export const get = <T>(url: string, params?: any) => client.get<T>(url, { params }).then((res) => res.data);
export const post = <T>(url: string, data?: any) => client.post<T>(url, data).then((res) => res.data);
export const put = <T>(url: string, data?: any) => client.put<T>(url, data).then((res) => res.data);
export const del = <T>(url: string) => client.delete<T>(url).then((res) => res.data);

export default client;
