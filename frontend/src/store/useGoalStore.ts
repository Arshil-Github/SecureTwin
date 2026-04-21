// frontend/src/store/useGoalStore.ts
import { create } from 'zustand';
import { GoalStatus, GoalConflict } from '../types/api';
import { get, post } from '../api/client';

interface GoalState {
  goals: GoalStatus[];
  conflicts: GoalConflict[];
  isLoading: boolean;
  fetchGoals: () => Promise<void>;
  fetchConflicts: () => Promise<void>;
  createGoal: (data: any) => Promise<void>;
}

export const useGoalStore = create<GoalState>()((set) => ({
  goals: [],
  conflicts: [],
  isLoading: false,
  fetchGoals: async () => {
    set({ isLoading: true });
    try {
      const data = await get<GoalStatus[]>('/goals/');
      set({ goals: data, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
    }
  },
  fetchConflicts: async () => {
    try {
      const data = await get<GoalConflict[]>('/goals/conflicts');
      set({ conflicts: data });
    } catch (error) {
      console.error("Failed to fetch conflicts", error);
    }
  },
  createGoal: async (data) => {
    await post('/goals/', data);
    const goals = await get<GoalStatus[]>('/goals/');
    set({ goals });
  },
}));
