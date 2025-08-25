export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role?: string;
  provider?: 'email' | 'google' | 'github' | 'facebook';
  createdAt: string;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  loading: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupCredentials {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}