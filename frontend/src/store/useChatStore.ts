import { create } from 'zustand';
import { get, post } from '../api/client';
import { ChatResponse, ChatMessage, WealthAction } from '../types/api';

interface ChatState {
  messages: ChatMessage[];
  suggestedQuestions: string[];
  isLoading: boolean;
  sendMessage: (text: string) => Promise<void>;
  fetchSuggestions: () => Promise<void>;
}

export const useChatStore = create<ChatState>()((set, getStore) => ({
  messages: [
    { role: 'assistant', content: 'Hello! I am your AI wealth twin. How can I assist you with your finances today?' }
  ],
  suggestedQuestions: [],
  isLoading: false,
  
  sendMessage: async (text: string) => {
    const userMessage: ChatMessage = { role: 'user', content: text };
    const currentMessages = getStore().messages;
    
    set({ 
      messages: [...currentMessages, userMessage],
      isLoading: true 
    });

    try {
      // Send the last 6 messages as history
      const history = currentMessages.slice(-6);
      
      const response = await post<ChatResponse>('/ai_chat/message', {
        user_message: text,
        conversation_history: history,
        user_id: 1 // Default to 1 as per instructions, but auth header is also sent
      });

      const assistantMessage: ChatMessage = { 
        role: 'assistant', 
        content: response.assistant_message 
      };

      set({ 
        messages: [...getStore().messages, assistantMessage],
        isLoading: false 
      });
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'I am sorry, I am having trouble connecting right now. Please try again later.'
      };
      set({ 
        messages: [...getStore().messages, errorMessage],
        isLoading: false 
      });
    }
  },

  fetchSuggestions: async () => {
    try {
      const data = await get<string[]>('/ai_chat/suggested-questions');
      set({ suggestedQuestions: data });
    } catch (error) {
      console.error('Failed to fetch suggested questions:', error);
    }
  }
}));