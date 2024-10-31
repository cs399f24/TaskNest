import React, { useState } from 'react';
import UserPool from './Userpool'; 
import './SignUp.css'
import Button from '../../components/button/button';
import {motion} from 'framer-motion'

export const SignUp = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const onSubmit = (event) => {
    event.preventDefault();
    UserPool.signUp(email, password, [], null, (err, data) => {
      if (err) {
        setErrorMessage(err.message);
        return;
      }
      setErrorMessage(""); // Clear error message on success
      console.log("Signup successful:", data);
    });
  };

  return (
    <div className='sign-up-page'>
      <motion.form  
        onSubmit={onSubmit}
        initial={{ opacity: 0, y:50 }}
        animate={{ opacity: 1, y:0 }}
        transition={{ duration: 0.9 }}
      >
        <h1>Create An Account!</h1>
        <input 
          type="email" 
          value={email} 
          onChange={(event) => setEmail(event.target.value)} 
          placeholder="Email"
          required
        />
        <input 
          type="password" 
          value={password} 
          onChange={(event) => setPassword(event.target.value)} 
          placeholder="Password"
          required
        />
          {errorMessage && <p className="error-message">{errorMessage}</p>}

        <Button submit="submit" text='Sign Up' />
      </motion.form>
    </div>
  );
}

export default SignUp