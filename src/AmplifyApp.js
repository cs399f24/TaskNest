import React, { useEffect } from 'react';
import { Amplify } from 'aws-amplify';
import { fetchAuthSession } from 'aws-amplify/auth';
import { useNavigate } from 'react-router-dom';
import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import Navbar from './components/navbar/Navbar';
import './amplifyApp.css'
import { motion } from 'framer-motion';

import awsExports from './aws-exports';
Amplify.configure(awsExports);

const AuthenticatedContent = ({ user, signOut }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const getAuthTokens = async () => {
      try {
        if (user) {
          const session = await fetchAuthSession();
          console.log("id token", session.tokens.idToken);
          console.log("access token", session.tokens.accessToken);
          
          localStorage.setItem('user_id', user.username);
          navigate('/home');
        }
      } catch (error) {
        console.error('Error getting authentication tokens:', error);
      }
    };

    getAuthTokens();
  }, [user, navigate]);

  return null;
};

export const AmplifyApp = () => {
  return (
    <Authenticator>
      {(props) => <AuthenticatedContent {...props} />}
    </Authenticator>
  );
};

export default AmplifyApp;