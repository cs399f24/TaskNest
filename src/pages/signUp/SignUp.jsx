import React, { useState } from 'react';
import UserPool from './Userpool'; 

export const SignUp = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  
  console.log(UserPool); // Check the output here

  const onSubmit = (event) => {
    event.preventDefault();
    UserPool.signUp(email, password, [], null, (err, data) => {
      if (err) {
        console.log("Error signing up:", err);
        return;
      }
      console.log("Signup successful:", data);
    });
  };
  

  return (
    <div>
      <form onSubmit={onSubmit}>
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
        <button type='submit'>Sign Up</button>
      </form>
    </div>
  );
}

export default SignUp