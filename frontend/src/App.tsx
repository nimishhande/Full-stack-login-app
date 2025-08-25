import React, { useState, useEffect } from 'react';
import LoginForm from './components/LoginForm';
import SignupForm from './components/SignupForm';
import Dashboard from './components/Dashboard';
import { User, AuthState } from './types/auth';

function App() {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
    loading: true
  });
  const [currentView, setCurrentView] = useState<'login' | 'signup'>('login');

  useEffect(() => {
    // Check for existing auth token on app load
    const token = localStorage.getItem('authToken');
    if (token) {
      // In a real app, validate token with backend
      fetchUserProfile(token);
    } else {
      setAuthState(prev => ({ ...prev, loading: false }));
    }
  }, []);

  const fetchUserProfile = async (token: string) => {
    try {
      // Simulate API call - replace with actual backend endpoint
      const response = await fetch('/api/auth/profile', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const user = await response.json();
        setAuthState({
          isAuthenticated: true,
          user,
          loading: false
        });
      } else {
        localStorage.removeItem('authToken');
        setAuthState({
          isAuthenticated: false,
          user: null,
          loading: false
        });
      }
    } catch (error) {
      setAuthState({
        isAuthenticated: false,
        user: null,
        loading: false
      });
    }
  };

  const handleLogin = (user: User, token: string) => {
    localStorage.setItem('authToken', token);
    setAuthState({
      isAuthenticated: true,
      user,
      loading: false
    });
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setAuthState({
      isAuthenticated: false,
      user: null,
      loading: false
    });
  };

  if (authState.loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (authState.isAuthenticated && authState.user) {
    return <Dashboard user={authState.user} onLogout={handleLogout} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {currentView === 'login' ? (
          <LoginForm 
            onLogin={handleLogin} 
            onSwitchToSignup={() => setCurrentView('signup')}
          />
        ) : (
          <SignupForm 
            onSignup={handleLogin} 
            onSwitchToLogin={() => setCurrentView('login')}
          />
        )}
      </div>
    </div>
  );
}

export default App;