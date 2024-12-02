import React, { useEffect } from 'react';
import { Amplify } from 'aws-amplify';
import { useNavigate } from 'react-router-dom';
import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import Navbar from './components/navbar/Navbar';
import './amplifyApp.css'
import {motion} from 'framer-motion';

import awsExports from './aws-exports';
Amplify.configure(awsExports);

// Separate component for authenticated state
const AuthenticatedContent = ({ user, signOut }) => {
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      console.log('Current user:', user);
      localStorage.setItem('user_id', user.username);
      navigate('/home');
    }
  }, [user, navigate]);

  return null; // or return a loading spinner if needed
};

export const AmplifyApp = () => {
  return (
    <Authenticator>
      {(props) => <AuthenticatedContent {...props} />}
    </Authenticator>
  );
};

export default AmplifyApp;