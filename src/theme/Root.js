import React from 'react';
import OriginalRoot from '@theme-original/Root';
import { AuthProvider } from '../contexts/AuthContext';

function Root(props) {
  return (
    <AuthProvider>
      <OriginalRoot {...props} />
    </AuthProvider>
  );
}

export default Root;
