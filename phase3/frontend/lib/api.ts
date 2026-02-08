import axios from 'axios';

/* =========================
   Cookie Helpers
========================= */

const setCookie = (name: string, value: string, days: number = 1) => {
  if (typeof document === 'undefined') return;

  const expires = new Date();
  expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Strict`;
};

const getCookie = (name: string): string | null => {
  if (typeof document === 'undefined') return null;

  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop()!.split(';').shift() ?? null;
  }
  return null;
};

const deleteCookie = (name: string) => {
  if (typeof document === 'undefined') return;

  document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
};

/* =========================
   Axios Instance
========================= */

const apiClient = axios.create({
  baseURL:
    process.env.NEXT_PUBLIC_API_URL ||
    (typeof window !== 'undefined' && window.location.hostname === 'localhost'
      ? 'http://localhost:8000'
      : 'https://riaz110-todo.hf.space'),
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

/* =========================
   Request Interceptor
========================= */

apiClient.interceptors.request.use(
  (config) => {
    try {
      if (typeof window === 'undefined') return config;

      let token: string | null = localStorage.getItem('token');

      // If not in localStorage, try cookie
      if (!token) {
        const cookieValue = document.cookie
          .split('; ')
          .find(row => row.startsWith('auth_token='))
          ?.split('=')[1];
        if (cookieValue) {
          token = cookieValue;
          localStorage.setItem('token', cookieValue);
        }
      }

      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Error getting JWT token:', error);
    }

    return config;
  },
  (error) => Promise.reject(error)
);


/* =========================
   Response Interceptor
========================= */

apiClient.interceptors.response.use(
  (response) => {
    if (response.data?.access_token) {
      const token: string = response.data.access_token;
      localStorage.setItem('token', token);
      setCookie('auth_token', token);
    }
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        deleteCookie('auth_token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
