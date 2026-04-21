// frontend/src/store/useAuthStore.ts
import { create } from "zustand";
import * as SecureStore from "expo-secure-store";
import { User } from "../types/api";
import client from "../api/client";

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean | string;
  login: (
    email: string,
    password: string,
    deviceFingerprint: string,
  ) => Promise<void>;
  logout: () => Promise<void>;
  loadFromStorage: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()((set) => ({
  user: null,
  token: null,
  isLoading: false,
  login: async (email, password, deviceFingerprint) => {
    console.log('useAuthStore: login called with', { email, deviceFingerprint });
    set({ isLoading: true });
    try {
      console.log('useAuthStore: making POST request to /auth/login');
      const response = await client.post("/auth/login", {
        email,
        password,
        device_fingerprint: deviceFingerprint,
      });
      console.log('useAuthStore: response received', response.status);
      const { access_token, user } = response.data;
      console.log('useAuthStore: storing token and user data');
      await SecureStore.setItemAsync("userToken", access_token);
      await SecureStore.setItemAsync("userData", JSON.stringify(user));
      console.log('useAuthStore: setting user state');
      set({ user, token: access_token, isLoading: false });
    } catch (error: any) {
      console.error('useAuthStore: login error', error);
      if (error.response) {
        console.error('useAuthStore: error response data', error.response.data);
        console.error('useAuthStore: error response status', error.response.status);
      } else if (error.request) {
        console.error('useAuthStore: error request (no response)', error.request);
      } else {
        console.error('useAuthStore: error message', error.message);
      }
      set({ isLoading: false });
      throw error;
    }
  },
  logout: async () => {
    await SecureStore.deleteItemAsync("userToken");
    await SecureStore.deleteItemAsync("userData");
    set({ user: null, token: null });
  },
  loadFromStorage: async () => {
    const token = await SecureStore.getItemAsync("userToken");
    const userData = await SecureStore.getItemAsync("userData");
    if (token && userData) {
      set({ token, user: JSON.parse(userData) });
    }
  },
}));
