import React, { useState } from 'react';
import './LogIn.css'
import Button from '../../components/button/button';
import {motion} from 'framer-motion'
import { CognitoUser, AuthenticationDetails } from 'amazon-cognito-identity-js';
import Userpool from '../signUp/Userpool';

export const LogIn = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessages, setErrorMessages] = useState("");
    const [successMessage, setSuccessMessage] = useState(""); // New state for success message

    const onSubmit = (event) => {
        event.preventDefault();

        const user = new CognitoUser({
            Username: email,
            Pool: Userpool
        });

        const authDetails = new AuthenticationDetails({
            Username: email,
            Password: password
        });

        user.authenticateUser(authDetails, {
            onSuccess: data => {
                console.log("onSuccess:", data);
                setErrorMessages(""); // Clear error messages on success
                setSuccessMessage("Login successful!"); // Set success message
            },
            onFailure: err => {
                console.error("onFailure:", err);
                setErrorMessages(err.message || "An error occurred during login."); // Set error message
                setSuccessMessage(""); // Clear success message on failure
            },
            newPasswordRequired: data => {
                console.log("newPasswordRequired:", data);
            }
        });
    };

    console.log(Userpool); // Check the output here

    return (
        <div className='log-in-page'>
            <motion.form  
                onSubmit={onSubmit}
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.9 }}
            >
                <h1>Log In To Your Account!</h1>
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
                {errorMessages && <p className="error-message">{errorMessages}</p>}
                {successMessage && <p className="success-message">{successMessage}</p>} {/* Display success message */}

                <Button submit="submit" text='Log In' />
            </motion.form>
        </div>
    );
}

export default LogIn;
