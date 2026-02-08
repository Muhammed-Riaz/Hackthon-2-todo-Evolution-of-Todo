'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import apiClient from '@/lib/api';

// Helper functions to manage cookies
const setCookie = (name: string, value: string, days: number = 1) => {
  const expires = new Date();
  expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
  document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Strict`;
};

const deleteCookie = (name: string) => {
  document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
};

interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  created_at?: string;
  updated_at?: string;
}

interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, firstName?: string, lastName?: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    // Check if user is already authenticated on initial load
    const checkStoredAuth = async () => {
      try {
        setIsLoading(true);
        let storedUser = localStorage.getItem('user');
        let storedToken = localStorage.getItem('token');

        // If not in localStorage, try to get from cookie
        if (!storedToken) {
          const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('auth_token='));
          storedToken = cookieValue ? cookieValue.split('=')[1] : null;
        }

        if (!storedUser && storedToken) {
          // If we have a token but no user info, we should validate the token with the backend
          try {
            const response = await apiClient.get('/api/auth/me');
            if (response.data) {
              storedUser = JSON.stringify(response.data);
              localStorage.setItem('user', storedUser);
            }
          } catch (validationError) {
            // Token might be invalid/expired, clear everything
            localStorage.removeItem('user');
            localStorage.removeItem('token');
            deleteCookie('auth_token');
            return;
          }
        }

        if (storedUser && storedToken) {
          setUser(JSON.parse(storedUser));
          setToken(storedToken);
        }
      } catch (error) {
        console.error('Auth check failed:', error);
      } finally {
        setIsLoading(false);
      }
    };

    checkStoredAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await apiClient.post<TokenResponse>('/api/auth/login', {
        username: email, // Backend expects 'username' field for email
        password: password
      });

      if (response.data) {
        const userData = response.data.user;
        const accessToken = response.data.access_token;

        setUser(userData);
        setToken(accessToken);

        // Store in localStorage for persistence
        localStorage.setItem('user', JSON.stringify(userData));
        localStorage.setItem('token', accessToken);

        // Also store in cookie for server-side access
        setCookie('auth_token', accessToken);

        router.push('/dashboard');
      }
    } catch (error: any) {
      console.error('Login failed:', error);
      let errorMessage = 'Login failed. Please try again.';
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      }
      throw new Error(errorMessage);
    }
  };

  const register = async (email: string, password: string, firstName?: string, lastName?: string) => {
    try {
      const response = await apiClient.post<TokenResponse>('/api/auth/signup', {
        email,
        password,
        first_name: firstName,
        last_name: lastName
      });

      if (response.data) {
        const userData = response.data.user;
        const accessToken = response.data.access_token;

        setUser(userData);
        setToken(accessToken);

        // Store in localStorage for persistence
        localStorage.setItem('user', JSON.stringify(userData));
        localStorage.setItem('token', accessToken);

        // Also store in cookie for server-side access
        setCookie('auth_token', accessToken);

        router.push('/dashboard');
      }
    } catch (error: any) {
      console.error('Registration failed:', error);
      let errorMessage = 'Registration failed. Please try again.';
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      }
      throw new Error(errorMessage);
    }
  };

  const logout = async () => {
    try {
      // Call the logout endpoint
      await apiClient.post('/api/auth/logout');
    } catch (error) {
      console.error('Logout API call failed:', error);
      // Continue with local cleanup anyway
    } finally {
      // Clear local state and storage
      setUser(null);
      setToken(null);
      localStorage.removeItem('user');
      localStorage.removeItem('token');
      deleteCookie('auth_token'); // Also clear the cookie

      // Redirect to login
      router.push('/login');
    }
  };

  const isAuthenticated = !!(user && token);

  // Protect certain routes
  useEffect(() => {
    if (!isLoading && !isAuthenticated && pathname?.startsWith('/dashboard')) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, pathname, router]);

  const value = {
    user,
    token,
    isLoading,
    login,
    register,
    logout,
    isAuthenticated,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}