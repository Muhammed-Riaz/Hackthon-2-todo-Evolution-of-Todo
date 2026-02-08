'use client';

import { createContext, useContext, useState, ReactNode, useCallback } from 'react';
import { chatApi } from '@/lib/chat/api';
import { useAuth } from '@/contexts/AuthContext';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  status?: 'sent' | 'sending' | 'error';
}

interface Conversation {
  id?: number;
  messages: Message[];
}

interface ChatContextType {
  conversation: Conversation;
  sendMessage: (content: string) => Promise<void>;
  startNewConversation: () => void;
  isLoading: boolean;
  error: string | null;
  clearError: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export function ChatProvider({ children }: { children: ReactNode }) {
  const [conversation, setConversation] = useState<Conversation>({ messages: [] });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { user, isLoading: isAuthLoading } = useAuth();

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const startNewConversation = useCallback(() => {
    setConversation({ messages: [] });
  }, []);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    // Check if auth is still loading
    if (isAuthLoading) {
      setError('Please wait while we verify your authentication...');
      return;
    }

    // Check if user is authenticated
    if (!user || !user.id) {
      setError('You must be logged in to send messages. Please log in and try again.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Add user message to conversation
      const userMessage: Message = {
        id: `user-${Date.now()}`,
        role: 'user',
        content,
        timestamp: new Date(),
        status: 'sending'
      };

      setConversation(prev => ({
        ...prev,
        messages: [...prev.messages, userMessage]
      }));

      // Use user ID from auth context
      const userId = user.id;

      console.log('[ChatProvider] Sending message with user_id:', userId);

      // Make API call to backend using the chat API client
      const response = await chatApi.sendMessage(userId, {
        conversation_id: conversation.id,
        message: content
      });

      console.log('[ChatProvider] Received response:', response);

      // Update conversation with new ID if it was created
      if (response.conversation_id && !conversation.id) {
        setConversation(prev => ({
          ...prev,
          id: response.conversation_id
        }));
      }

      // Add assistant response to conversation
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.response,
        timestamp: new Date()
      };

      setConversation(prev => ({
        id: response.conversation_id || prev.id,
        messages: [...prev.messages, { ...userMessage, status: 'sent' }, assistantMessage]
      }));

      // Process tool calls if any
      if (response.tool_calls && Array.isArray(response.tool_calls) && response.tool_calls.length > 0) {
        const toolConfirmationMessage: Message = {
          id: `tool-${Date.now()}`,
          role: 'assistant',
          content: `I've executed the requested actions: ${response.tool_calls.map((call: any) => call.name).join(', ')}.`,
          timestamp: new Date()
        };
        setConversation(prev => ({
          id: response.conversation_id || prev.id,
          messages: [...prev.messages, toolConfirmationMessage]
        }));
      }
    } catch (err: any) {
      console.error('[ChatProvider] Error sending message:', err);
      setError(err.message || 'Failed to send message');

      // Update user message status to error
      setConversation(prev => ({
        ...prev,
        messages: prev.messages.map(msg =>
          msg.id.startsWith('user-') && msg.status === 'sending'
            ? { ...msg, status: 'error' }
            : msg
        )
      }));
    } finally {
      setIsLoading(false);
    }
  }, [conversation.id, user, isAuthLoading]);

  return (
    <ChatContext.Provider
      value={{
        conversation,
        sendMessage,
        startNewConversation,
        isLoading,
        error,
        clearError
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
}
