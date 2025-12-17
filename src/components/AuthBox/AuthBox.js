import React, { useState } from 'react';
import styles from './AuthBox.module.css';

function AuthBox({ onLoginSuccess, onLogout }) {
  const [isSignUp, setIsSignUp] = useState(true);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [softwareBackground, setSoftwareBackground] = useState('');
  const [hardwareBackground, setHardwareBackground] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const API_BASE_URL = 'http://localhost:8000'; // Assuming FastAPI is running on this port

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage('');

    const endpoint = isSignUp ? '/auth/signup' : '/auth/signin';
    const body = isSignUp
      ? { name, email, software_background: softwareBackground, hardware_background: hardwareBackground, experience_level: experienceLevel, password }
      : { email, password };

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('jwt_token', data.access_token);
        localStorage.setItem('user_name', data.user.name); // Assuming the API returns user name on login/signup
        setMessage(`Success: ${data.message || (isSignUp ? 'Sign up successful!' : 'Login successful!')}`);
        onLoginSuccess(data.user.name);
      } else {
        setMessage(`Error: ${data.detail || 'Something went wrong.'}`);
      }
    } catch (error) {
      setMessage(`Network error: ${error.message}`);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('jwt_token');
    localStorage.removeItem('user_name');
    onLogout(); // Notify parent component about logout
  };

  return (
    <div className={styles.authBox}>
      <h2>{isSignUp ? 'Sign Up' : 'Sign In'}</h2>
      <form onSubmit={handleSubmit}>
        {isSignUp && (
          <div className={styles.formGroup}>
            <label htmlFor="name">Name:</label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
        )}
        <div className={styles.formGroup}>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        {isSignUp && (
          <>
            <div className={styles.formGroup}>
              <label htmlFor="softwareBackground">Software Background:</label>
              <input
                type="text"
                id="softwareBackground"
                value={softwareBackground}
                onChange={(e) => setSoftwareBackground(e.target.value)}
              />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="hardwareBackground">Hardware Background:</label>
              <input
                type="text"
                id="hardwareBackground"
                value={hardwareBackground}
                onChange={(e) => setHardwareBackground(e.target.value)}
              />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="experienceLevel">Experience Level:</label>
              <select
                id="experienceLevel"
                value={experienceLevel}
                onChange={(e) => setExperienceLevel(e.target.value)}
              >
                <option value="">Select...</option>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="expert">Expert</option>
              </select>
            </div>
          </>
        )}
        <div className={styles.formGroup}>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">{isSignUp ? 'Sign Up' : 'Sign In'}</button>
      </form>
      <p className={styles.switchMode}>
        {isSignUp ? 'Already have an account?' : "Don't have an account?"}{' '}
        <span onClick={() => setIsSignUp(!isSignUp)}>
          {isSignUp ? 'Sign In' : 'Sign Up'}
        </span>
      </p>
      {localStorage.getItem('jwt_token') && (
        <button onClick={handleLogout} className={styles.logoutButton}>
          Logout
        </button>
      )}
      {message && <p className={styles.message}>{message}</p>}
    </div>
  );
}

export default AuthBox;
