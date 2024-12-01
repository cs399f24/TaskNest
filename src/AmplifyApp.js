import React from 'react';
import { Amplify } from 'aws-amplify';
import { useNavigate } from 'react-router-dom';
import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import Navbar from './components/navbar/Navbar';  // Adjust the path as needed

import awsExports from './aws-exports';
Amplify.configure(awsExports);

export const AmplifyApp = () => {
  const navigate = useNavigate();

  return (
    <Authenticator>
      {({ signOut, user }) => {
        console.log('Current user:', user);
        localStorage.setItem('user_id', user.username);
        navigate('/home');
        
        return (
          <main>
            <Navbar signOut={signOut} />
            <h1>Hello {user.username}</h1>
          </main>
        );
      }}
    </Authenticator>
  );
}

export default AmplifyApp;