import React, { createContext, useState, useEffect, useContext } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [userName, setUserName] = useState(null);

  useEffect(() => {
    const storedUserName = localStorage.getItem('user_name');
    if (storedUserName) {
      setUserName(storedUserName);
    }
  }, []);

  const handleLoginSuccess = (name) => {
    setUserName(name);
  };

  const handleLogout = () => {
    localStorage.removeItem('jwt_token');
    localStorage.removeItem('user_name');
    setUserName(null);
  };

  return (
    <AuthContext.Provider value={{ userName, handleLoginSuccess, handleLogout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
