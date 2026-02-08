'use client';

import { useState, useRef, useEffect, memo } from 'react';
import { ChatProvider, useChat } from './ChatProvider';

interface MessageProps {
  message: {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
    status?: 'sent' | 'sending' | 'error';
  };
}

function MessageBubble({ message }: MessageProps) {
  const isUser = message.role === 'user';

  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
      role="listitem"
      aria-label={`${message.role} message: ${message.content}`}
    >
      <div
        className={`max-w-xs lg:max-w-md px-5 py-3 rounded-2xl shadow-sm ${
          isUser
            ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-br-none'
            : 'bg-white text-gray-800 rounded-bl-none border border-gray-200'
        }`}
        role="article"
        aria-roledescription={isUser ? "user message" : "assistant message"}
      >
        <div className="whitespace-pre-wrap" aria-label="Message content">{message.content}</div>
        <div className={`text-xs mt-2 flex items-center ${isUser ? 'text-indigo-200' : 'text-gray-500'}`} aria-label="Message timestamp">
          <span>{message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
          {message.status === 'sending' && (
            <span className="ml-2 flex items-center">
              <div className="w-2 h-2 bg-current rounded-full animate-pulse mr-1"></div>
              Sending...
            </span>
          )}
          {message.status === 'error' && (
            <span className="ml-2 text-red-400 flex items-center">
              <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd"></path>
              </svg>
              Failed
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

function ChatInput({ onSend, disabled, errorMessage }: { onSend: (content: string) => void; disabled: boolean; errorMessage: string | null }) {
  const [inputValue, setInputValue] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !disabled) {
      onSend(inputValue.trim());
      setInputValue('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 150) + 'px';
    }
  }, [inputValue]);

  return (
    <div className="border-t border-gray-200/50 pt-4">
      {errorMessage && (
        <div
          className="mb-3 p-3 bg-red-50 border border-red-200 text-red-700 rounded-xl text-sm"
          role="alert"
          aria-live="assertive"
        >
          <div className="flex items-center">
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd"></path>
            </svg>
            {errorMessage}
          </div>
        </div>
      )}
      <form onSubmit={handleSubmit} className="flex gap-3" role="form" aria-label="Chat input form">
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask me to manage your tasks... (e.g. 'Add a task to buy groceries')"
            disabled={disabled}
            className="w-full px-4 py-3 pr-12 border border-gray-300/50 rounded-2xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white shadow-sm resize-none transition-all duration-200"
            aria-label="Type your message"
            aria-disabled={disabled}
            aria-describedby={errorMessage ? "chat-error-message" : undefined}
            rows={1}
          />
          <div className="absolute right-3 bottom-3 flex items-center">
            <button
              type="submit"
              disabled={disabled || !inputValue.trim()}
              className="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white flex items-center justify-center hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-md hover:shadow-lg"
              aria-label="Send message"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </form>
      {errorMessage && (
        <div id="chat-error-message" className="sr-only" aria-live="assertive">
          {errorMessage}
        </div>
      )}
    </div>
  );
}

function InnerChatView() {
  const { conversation, sendMessage, startNewConversation, isLoading, error, clearError } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Scroll to bottom when new messages arrive
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversation.messages]);

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto px-4" role="main" aria-label="Chat interface">
      <div className="flex-1 overflow-y-auto py-6 space-y-6" role="region" aria-label="Chat messages">
        {conversation.messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center py-12" role="status" aria-live="polite">
            <div className="w-20 h-20 rounded-full bg-gradient-to-r from-indigo-100 to-purple-100 flex items-center justify-center mb-6">
              <svg className="w-10 h-10 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Start a Conversation</h3>
            <p className="text-gray-600 max-w-md">
              Your AI assistant is ready to help you manage tasks. Send a message to get started!
            </p>
          </div>
        ) : (
          <>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-lg font-semibold text-gray-800" id="chat-session-heading">Chat Session</h2>
              <button
                onClick={startNewConversation}
                className="text-sm bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-4 py-2 rounded-full hover:from-indigo-700 hover:to-purple-700 transition-all duration-200 shadow-sm hover:shadow-md flex items-center"
                aria-label="Start new chat session"
              >
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                New Chat
              </button>
            </div>
            <ul role="list" aria-labelledby="chat-session-heading">
              {conversation.messages.map((message) => (
                <MessageBubble key={message.id} message={message} />
              ))}
            </ul>
          </>
        )}
        <div ref={messagesEndRef} tabIndex={-1} />
      </div>

      <div className="pb-4">
        <ChatInput
          onSend={sendMessage}
          disabled={isLoading}
          errorMessage={error}
        />
      </div>
    </div>
  );
}

const MemoizedInnerChatView = memo(InnerChatView);

export default function ChatView() {
  return (
    <ChatProvider>
      <MemoizedInnerChatView />
    </ChatProvider>
  );
}