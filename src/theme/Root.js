import React from 'react';
import OriginalRoot from '@docusaurus/theme-classic/theme/Root';
import { AuthProvider } from '../contexts/AuthContext';

function Root(props) {
  return (
    <AuthProvider>
      <OriginalRoot {...props} />
    </AuthProvider>
  );
}

export default Root;
