// frontend/src/store/useWealthStore.ts
import { create } from 'zustand';
import { WealthSnapshot, WealthAction } from '../types/api';
import { get } from '../api/client';

interface WealthState {
  snapshot: WealthSnapshot | null;
  actions: WealthAction[];
  isLoading: boolean;
  fetchSnapshot: () => Promise<void>;
  fetchActions: () => Promise<void>;
}

export const useWealthStore = create<WealthState>()((set) => ({
  snapshot: null,
  actions: [],
  isLoading: false,
  fetchSnapshot: async () => {
    set({ isLoading: true });
    try {
      const data = await get<WealthSnapshot>('/wealth/snapshot');
      set({ snapshot: data, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
    }
  },
  fetchActions: async () => {
    try {
      const data = await get<WealthAction[]>('/insights/actions');
      set({ actions: data });
    } catch (error) {}
  },
}));
