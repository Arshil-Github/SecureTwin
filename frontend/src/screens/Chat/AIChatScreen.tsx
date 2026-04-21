// frontend/src/screens/Chat/AIChatScreen.tsx
import React, { useState, useRef, useEffect } from 'react';
import { View, Text, ScrollView, TextInput, TouchableOpacity, KeyboardAvoidingView, Platform, ActivityIndicator } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons, MaterialIcons } from '@expo/vector-icons';
import { useChatStore } from '../../store/useChatStore';

export default function AIChatScreen() {
  const insets = useSafeAreaInsets();
  const [input, setInput] = useState('');
  const { messages, suggestedQuestions, isLoading, sendMessage, fetchSuggestions } = useChatStore();
  const scrollViewRef = useRef<ScrollView>(null);

  useEffect(() => {
    fetchSuggestions();
  }, []);

  const handleSend = () => {
    if (!input.trim() || isLoading) return;
    sendMessage(input.trim());
    setInput('');
  };

  return (
    <View className="flex-1 bg-primary">
      {/* Header */}
      <View 
        className="px-6 py-4 flex-row justify-between items-center border-b border-borderWhite bg-primary/80"
        style={{ paddingTop: insets.top }}
      >
        <TouchableOpacity>
          <MaterialIcons name="account-balance-wallet" size={24} color="#00E5C0" />
        </TouchableOpacity>
        <View className="flex-row items-center gap-2">
          <Text className="font-bold text-sm tracking-[2] text-accent uppercase">ASK YOUR TWIN</Text>
          <View className="w-2 h-2 rounded-full bg-accent" />
        </View>
        <TouchableOpacity>
          <Ionicons name="notifications-outline" size={24} color="#00E5C0" />
        </TouchableOpacity>
      </View>

      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'} 
        className="flex-1"
        keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 20}
      >
        <ScrollView 
          ref={scrollViewRef}
          className="flex-1"
          contentContainerClassName="px-6 pt-8 pb-32"
          onContentSizeChange={() => scrollViewRef.current?.scrollToEnd({ animated: true })}
        >
          {messages.map((msg, index) => (
            <View key={index.toString()} className={`flex-row mb-6 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              {msg.role === 'assistant' && (
                <View className="w-10 h-10 rounded-full bg-surface border border-borderWhite items-center justify-center mr-3">
                  <MaterialIcons name="auto-awesome" size={20} color="#00E5C0" />
                </View>
              )}
              <View 
                className={`max-w-[80%] p-4 rounded-2xl border border-borderWhite ${
                  msg.role === 'user' ? 'bg-white/5 rounded-tr-sm' : 'bg-surface rounded-tl-sm'
                }`}
              >
                <Text className="text-textPrimary text-sm leading-relaxed">{msg.content}</Text>
              </View>
            </View>
          ))}

          {isLoading && (
            <View className="flex-row mb-6 justify-start items-center">
              <View className="w-10 h-10 rounded-full bg-surface border border-borderWhite items-center justify-center mr-3">
                <MaterialIcons name="auto-awesome" size={20} color="#00E5C0" />
              </View>
              <View className="p-4 rounded-2xl border border-borderWhite bg-surface rounded-tl-sm">
                <ActivityIndicator size="small" color="#00E5C0" />
              </View>
            </View>
          )}

          {/* Suggested Chips */}
          <View className="flex-row flex-wrap gap-2 mt-4">
             {suggestedQuestions.map((chip, i) => (
               <TouchableOpacity 
                  key={i} 
                  className="border border-borderWhite bg-white/5 px-4 py-2 rounded-full"
                  onPress={() => setInput(chip)}
                >
                 <Text className="text-textPrimary/70 text-[10px] uppercase font-bold tracking-[2]">{chip}</Text>
               </TouchableOpacity>
             ))}
          </View>
        </ScrollView>

        {/* Input Bar */}
        <View 
          className="px-6 py-4 bg-primary/40 border-t border-borderWhite"
          style={{ paddingBottom: insets.bottom + 10 }}
        >
          <View className="flex-row items-center bg-white/5 border border-borderWhite rounded-full px-5 py-3">
            <TextInput 
              className="flex-1 text-textPrimary text-sm h-6"
              placeholder="Ask anything about your finances..."
              placeholderTextColor="rgba(242, 237, 228, 0.3)"
              value={input}
              onChangeText={setInput}
              onSubmitEditing={handleSend}
            />
            <TouchableOpacity onPress={handleSend} disabled={isLoading || !input.trim()}>
              <Ionicons name="send" size={20} color={input.trim() && !isLoading ? "#00E5C0" : "rgba(0, 229, 192, 0.4)"} />
            </TouchableOpacity>
          </View>
        </View>
      </KeyboardAvoidingView>
    </View>
  );
}
