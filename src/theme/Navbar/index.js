import React from 'react';
import Navbar from '@theme-original/Navbar';
import { useAuth } from '../../contexts/AuthContext';
import { useHistory } from '@docusaurus/router'; // To redirect to login page

function CustomNavbar(props) {
  console.log('CustomNavbar loaded!'); // Added console log
  const { userName, handleLogout } = useAuth();
  // useHistory hook is only available in a Router context, which Docusaurus provides.
  const history = useHistory();

  const handleLoginClick = () => {
    history.push('/auth'); // Redirect to the auth page
  };

  return (
    <>
      <Navbar {...props} />
      <div style={{
        position: 'absolute',
        right: 0,
        top: 0,
        height: '60px',
        display: 'flex',
        alignItems: 'center',
        paddingRight: '20px',
        zIndex: 100 // Ensure it's above other elements
      }}>
        {userName ? (
          <>
            <span style={{ marginRight: '10px', color: 'var(--ifm-navbar-link-color)' }}>Hello, {userName}!</span>
            <button onClick={handleLogout} style={{
                background: '#dc3545',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                padding: '8px 12px',
                cursor: 'pointer'
            }}>Logout</button>
          </>
        ) : (
          <button onClick={handleLoginClick} style={{
            background: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            padding: '8px 12px',
            cursor: 'pointer'
        }}>Login / Sign Up</button>
        )}
      </div>
    </>
  );
}

export default CustomNavbar;

