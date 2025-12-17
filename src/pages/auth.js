import React from 'react';
import Layout from '@theme/Layout';
import AuthBox from '../components/AuthBox/AuthBox';
import { useAuth } from '../contexts/AuthContext';
import { useHistory } from '@docusaurus/router';

function AuthPage() {
  const { handleLoginSuccess } = useAuth();
  const history = useHistory();

  const onLoginSuccess = (userName) => {
    handleLoginSuccess(userName);
    history.push('/'); // Redirect to home page after successful login
  };

  const onLogout = () => {
    // This will be handled by the Navbar's logout button, but included for completeness
    // If AuthBox itself needs to trigger a logout, it would call this.
    // However, the logout button in AuthBox is a placeholder and ideally
    // should only exist in the Navbar for a consistent UX.
    history.push('/auth'); // Redirect to auth page after logout (if triggered from AuthBox)
  };

  return (
    <Layout title="Authentication">
      <main>
        <AuthBox onLoginSuccess={onLoginSuccess} onLogout={onLogout} />
      </main>
    </Layout>
  );
}

export default AuthPage;
